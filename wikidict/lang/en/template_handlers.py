import contextlib
import math
import re
from collections import defaultdict
from typing import TypedDict

from num2words import num2words

from ...transliterator import transliterate
from ...user_functions import (
    capitalize,
    concat,
    extract_keywords_from,
    italic,
    lookup_italic,
    ruby,
    small,
    strong,
    superscript,
    term,
)
from .labels import labels, syntaxes
from .langs import langs
from .places import (
    placetypes_aliases,
    recognized_placenames,
    recognized_placetypes,
    recognized_qualifiers,
)
from .si_unit import prefix_to_exp, prefix_to_symbol, unit_to_symbol, unit_to_type


def gender_number_specs(parts: str) -> str:
    """
    Source: https://en.wiktionary.org/wiki/Module:gender_and_number

    >>> gender_number_specs("m")
    '<i>m</i>'
    >>> gender_number_specs("m-p")
    '<i>m pl</i>'
    >>> gender_number_specs("m-an-p")
    '<i>m anim pl</i>'
    >>> gender_number_specs("?-p")
    '<i>? pl</i>'
    >>> gender_number_specs("?!-an-s")
    '<i>gender unattested anim sg</i>'
    >>> gender_number_specs("mfbysense-p")
    '<i>m pl or f pl by sense</i>'
    >>> gender_number_specs("mfequiv-s")
    '<i>m sg or f sg same meaning</i>'
    >>> gender_number_specs("mfequiv")
    '<i>m or f same meaning</i>'
    >>> gender_number_specs("biasp-s")
    '<i>impf sg or pf sg</i>'
    >>> gender_number_specs("f,n")
    '<i>f or n</i>'
    """
    specs = {
        # Genders
        "m": "m",
        "n": "n",
        "f": "f",
        "gneut": "gender-neutral",
        "g!": "gender unattested",
        "c": "c",
        # Numbers
        "s": "sg",
        "d": "du",
        "num!": "number unattested",
        "p": "pl",
        # Animacy
        "an": "anim",
        "in": "inan",
        "an!": "animacy unattested",
        "pr": "pers",
        "anml": "animal",
        "np": "npers",
        # Virility
        "vr": "vir",
        "nv": "nvir",
        # Aspect
        "pf": "pf",
        "impf": "impf",
        "asp!": "aspect unattested",
        # Other
        "?": "?",
        "?!": "gender unattested",
    }
    specs_combined = {
        "biasp": [specs["impf"], specs["pf"]],
        "f,n": [specs["f"], specs["n"]],
        "mf": [specs["m"], specs["f"]],
        "mfbysense": [specs["m"], specs["f"]],
        "mfequiv": [specs["m"], specs["f"]],
    }
    result = []

    for part in parts.split("-"):
        if part in specs_combined:
            combinations = specs_combined[parts.split("-")[0]]
            spec = specs[parts.split("-")[1]] if "-" in parts else ""
            res = " or ".join(f"{a} {b}".strip() for a, b in zip(combinations, [spec] * len(combinations), strict=True))
            if "sense" in part:
                res += " by sense"
            elif "equiv" in part:
                res += " same meaning"
            result.append(res)
            return italic(" or ".join(result))
        else:
            result.append(specs[part])

    return italic(" ".join(result))


def join_names(
    data: defaultdict[str, str],
    key: str,
    last_sep: str,
    *,
    include_langname: bool = False,
    key_alias: str = "",
    prefix: str = "",
    suffix: str = "",
) -> str:
    var_a = []
    if data[key] or data[key_alias]:
        for i in range(1, 10):
            var_key = f"{key}{i}" if i != 1 else key
            var_text = data[var_key]
            var_alias_key = ""
            if key_alias:
                var_alias_key = f"{key_alias}{i}" if i != 1 else key_alias
            if not var_text and var_alias_key:
                var_text = data[var_alias_key]
            if var_text:
                for origins in var_text.split(","):
                    if include_langname and ":" in origins:
                        data_split = origins.split(":")
                        text = f"{langs[data_split[0]]} {data_split[1]}"
                        if trans := transliterate(data_split[0], data_split[1]):
                            text += f" ({trans})"
                        var_a.append(text)
                    else:
                        langnametext = "English " if include_langname else ""
                        var_a.append(langnametext + prefix + origins + suffix)
    return concat(var_a, ", ", last_sep=last_sep) if var_a else ""


def gloss_tr_poss(data: defaultdict[str, str], gloss: str, *, trans: str = "") -> str:
    local_phrase = []
    phrase = ""
    trts = ""
    if data["tr"]:
        trts += f"{italic(data['tr'])}"
    if data["ts"]:
        if trts:
            trts += " "
        trts += f"{'/' + data['ts'] + '/'}"
    if trts:
        local_phrase.append(trts)
    if trans:
        local_phrase.append(f"{italic(trans)}")
    if gloss:
        local_phrase.append(f"“{gloss}”")
    if data["pos"]:
        local_phrase.append(f"{data['pos']}")
    if data["lit"]:
        local_phrase.append(f"{'literally “' + data['lit'] + '”'}")
    if local_phrase:
        phrase += " ("
        phrase += concat(local_phrase, ", ")
        phrase += ")"
    return phrase


def misc_variant(start: str, tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    if parts:
        parts.pop(0)  # Remove the language
    p = data["alt"] or data["2"] or (parts.pop(0) if parts else "") or ""
    data["t"] = data["t"] or data["3"] or ""
    starter = "" if data["notext"] in ("1", "yes") else start
    if p and starter:
        starter += " of"
    phrase = starter if data["nocap"] else starter.capitalize()
    if p != "-":
        phrase += f" {italic(p)}" if phrase else f"{italic(p)}"
    phrase += gloss_tr_poss(data, data["t"] or data["gloss"] or "")
    return phrase


def misc_variant_no_term(title: str, tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    if data["notext"] in ("1", "yes"):
        return ""
    return data.get("title", title if data["nocap"] in ("1", "yes") else capitalize(title))


def render_accent(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_accent("a", ["en", "ethnology"], defaultdict(str))
    '<i>(ethnology)</i>'
    >>> render_accent("a", ["en", "(ethnology)"], defaultdict(str))
    '<i>(ethnology)</i>'
    >>> render_accent("a", ["en", "RP"], defaultdict(str))
    '<i>(Received Pronunciation)</i>'
    """
    text = labels.get(parts[-1], parts[-1])
    return italic(text) if text.startswith("(") else term(text)


def render_aka(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_aka("aka", [], defaultdict(str))
    'a.k.a.'
    >>> render_aka("aka", [], defaultdict(str, {"aka": "1"}))
    'aka'
    >>> render_aka("aka", [], defaultdict(str, {"AKA": "1"}))
    'AKA'
    >>> render_aka("aka", [], defaultdict(str, {"uc": "1"}))
    'AKA'
    """
    if not data:
        return "a.k.a."
    text = "aka"
    if data["AKA"] or data["uc"]:
        text = text.upper()
    return text


def render_ante2(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ante2("ante2", ["1702"], defaultdict(str))
    '<i>ante</i> <b>1702</b>'
    >>> render_ante2("ante2", ["1702"], defaultdict(str, {"short": "yes"}))
    '<i>a.</i> <b>1702</b>'
    """
    init = "a." if data["short"] else "ante"
    return f"{italic(init)} {strong(parts[0])}"


def render_bce(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_bce("B.C.E.", [], defaultdict(str))
    '<small>B.C.E.</small>'
    >>> render_bce("C.E.", [], defaultdict(str, {"nodot": "1"}))
    '<small>CE</small>'
    >>> render_bce("CE", [], defaultdict(str))
    '<small>CE</small>'
    """
    nodot = data["nodot"] in ("1", "yes") or tpl in {"CE", "BCE"}
    text = "C.E." if tpl in {"C.E.", "CE", "A.D.", "AD"} else "B.C.E."
    return small(text.replace(".", "")) if nodot else small(text)


def render_bond_credit_rating(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_bond_credit_rating("bond credit rating", ["a bond is upper-medium grade with low risk of default"], defaultdict(str, {"lt": "1", "s": "1", "f": "1"}))
    '{{lb|mul|finance}} <i>Long-term bond credit rating by S&P Global Ratings and Fitch Ratings, indicating that a bond is upper-medium grade with low risk of default.</i>'
    """
    text = "{{lb|mul|finance}} <i>"

    if data["lt"]:
        text += "Long-term"
    if data["st"]:
        text += "Short-term"

    text += " bond credit rating by"

    agencies: list[str] = []
    if data["m"]:
        agencies.append("Moody's Investors Service")
    if data["s"]:
        agencies.append("S&P Global Ratings")
    if data["f"]:
        agencies.append("Fitch Ratings")
    text += f" {concat(agencies, ', ', last_sep=' and ')},"

    return f"{text} indicating that {parts[0]}.</i>"


def render_cap(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_cap("cap", ["beef"], defaultdict(str))
    'Beef'
    >>> render_cap("cap", ["common cold"], defaultdict(str))
    'Common cold'
    >>> render_cap("cap", ["bracket", "s"], defaultdict(str))
    'Brackets'

    # We need to be able to transcript here
    # >>> render_cap("cap", ["σκύλαξ"], defaultdict(str, {"lang": "grc"}))
    # 'Σκύλαξ (Skúlax)'
    # >>> render_cap("cap", ["кот", "а́"], defaultdict(str, {"lang": "ru"}))
    # 'Кота́ (Kotá)'
    """
    return f"{capitalize(''.join(parts))}"


def render_century(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_century("century", ["17"], defaultdict(str))
    '<small>[from 17th c.]</small>'
    >>> render_century("century", ["1"], defaultdict(str))
    '<small>[from 1st c.]</small>'
    >>> render_century("century", ["2", "3"], defaultdict(str))
    '<small>[2nd–3rd c.]</small>'
    """

    def ordinal(n: str) -> str:
        suffix = "th"
        with contextlib.suppress(ValueError):
            x = int(n)
            mod10 = x % 10
            mod100 = x % 100
            if mod10 == 1 and mod100 != 11:
                suffix = "st"
            elif mod10 == 2 and mod100 != 12:
                suffix = "nd"
            elif mod10 == 3 and mod100 != 13:
                suffix = "rd"
        return f"{n}{suffix}"

    if len(parts) > 1:
        phrase = f"{ordinal(parts[0])}–{ordinal(parts[1])} c."
    else:
        phrase = f"from {ordinal(parts[0])} c."

    return small(f"[{phrase}]")


def render_chemical_symbol(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_chemical_symbol("chemical symbol", ["calcium"], defaultdict(str))
    '<i>(chemistry) Chemical symbol for</i> <b>calcium</b>.'
    >>> render_chemical_symbol("chemical symbol", ["unnilquadium"], defaultdict(str, {"sys": "1"}))
    '<i>(chemistry) Systematic chemical symbol for</i> <b>unnilquadium</b>.'
    >>> render_chemical_symbol("chemical symbol", ["unnilquadium", "rutherfordium"], defaultdict(str, {"sys": "1"}))
    '<i>(chemistry) Systematic chemical symbol for</i> <b>unnilquadium</b>, now named <b>rutherfordium</b>.'
    >>> render_chemical_symbol("chemical symbol", ["copernicium"], defaultdict(str, {"obs": "1"}))
    '<i>(chemistry, obsolete) Obsolete chemical symbol for</i> <b>copernicium</b>.'
    """
    if data["obs"] == "1":
        text = "(chemistry, obsolete) Obsolete chemical symbol for"
    elif data["sys"] == "1":
        text = "(chemistry) Systematic chemical symbol for"
    else:
        text = "(chemistry) Chemical symbol for"
    text = f"{italic(text)} {strong(parts.pop(0))}"
    if parts:
        text += f", now named {strong(parts.pop(0))}"
    return f"{text}."


def render_clipping(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_clipping("clipping", ["en", "automobile"], defaultdict(str))
    'Clipping of <i>automobile</i>'
    >>> render_clipping("clipping", ["en", "-"], defaultdict(str))
    'Clipping of'
    >>> render_clipping("clipping", ["fr", "métropolitain"], defaultdict(str, {"notext": "1"}))
    '<i>métropolitain</i>'
    >>> render_clipping("clipping", ["ru", "ку́бовый краси́тель"], defaultdict(str, {"t": "vat dye", "nocap": "1"}))
    'clipping of <i>ку́бовый краси́тель</i> (“vat dye”)'
    """
    return misc_variant("clipping", tpl, parts, data, word=word)


def render_coinage(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_coinage("coin", ["en", "Josiah Willard Gibbs"], defaultdict(str))
    'Coined by Josiah Willard Gibbs'
    >>> render_coinage("coin", ["en", "Josiah Willard Gibbs"], defaultdict(str, {"in":"1881", "nat":"American", "occ":"scientist"}))
    'Coined by American scientist Josiah Willard Gibbs in 1881'
    >>> render_coinage("coin", ["en", "Josiah Willard Gibbs"], defaultdict(str, {"alt":"Josiah W. Gibbs", "nationality":"American", "occupation":"scientist"}))
    'Coined by American scientist Josiah W. Gibbs'
    >>> render_coinage("coin", [], defaultdict(str, {"1":"en", "2":"Charles Rice", "in": "c. 1000"}))
    'Coined by Charles Rice c. 1000'
    >>> render_coinage("coin", ["mul", "Q1043"], defaultdict(str, {"exnihilo": "1", "in": "in the 1950s"}))
    'Coined <i>ex nihilo</i> by Swedish botanist, physician, and zoologist Carl Linnaeus in the 1950s'
    """
    if parts:
        parts.pop(0)  # Remove the language

    phrase = ""
    if data["notext"] != "1":
        starter = "coined"
        if data["exnihilo"]:
            starter += " <i>ex nihilo</i>"
        starter += " by"
        phrase = starter if data["nocap"] else starter.capitalize()
        if data["nationality"]:
            phrase += f" {data['nationality']}"
        elif data["nat"]:
            phrase += f" {data['nat']}"
        if occ := join_names(data, "occ", " and ", include_langname=False, key_alias="occupation"):
            phrase += f" {occ}"
        phrase += " "

    who = data["alt"] or data["2"] or (parts.pop(0) if parts else "unknown") or "unknown"
    if who.startswith("Q") and who[1:].isdigit():
        from . import wikidata

        who = wikidata.COINERS[who]

    phrase += who

    if date := data["in"]:
        if date.isdigit():
            phrase += " in"
        phrase += f" {date}"

    return phrase


def render_contraction(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    return misc_variant("contraction", tpl, parts, data, word=word)


def render_lang_def(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    lang_src = parts.pop(0)
    match what := parts.pop(0):
        case "letter":
            if parts:
                number = parts.pop(0)
                text = f"The {num2words(number, lang='en', to='ordinal')} letter of the {langs[lang_src]} alphabet,"
                if parts:
                    text += f" called {strong(parts.pop(0))} and"
                text += f" written in the {data['sc'].removesuffix('-')} script"
            elif lang_src == "en":
                text = f"The {what} of the English alphabet, written in the {data['sc'].removesuffix('-')} script"
            else:
                text = f"A {what} of the {data['sc']}script"
        case "name":
            text = f"The {what} of the {data['sc']}script letter"
        case "ordinal":
            number = num2words(parts.pop(0), lang="en", to="ordinal")
            text = f"The {what} number {strong(number)}, derived from this letter of the {langs[lang_src]} alphabet,"
            if parts:
                text += f" called {strong(parts.pop(0))} and"
            text += f" written in the {data['sc'].removesuffix('-')} script"
        case _:
            raise ValueError(f"Unhandled {tpl!r} {what=}")

    text = italic(text)
    if len(parts) > 1:
        text += f" {strong(parts[0])} / {strong(parts[1])}"

    return f"{text}{'' if data['nodot'] else '.'}"


def render_cyrl_def(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_cyrl_def("Cyrl-def", ["en", "name", "Ԫ", "ԫ"], defaultdict(str, {"sc": "Cyrl"}))
    '<i>The name of the Cyrillic script letter</i> <b>Ԫ</b> / <b>ԫ</b>.'
    >>> render_cyrl_def("Cyrl-def", ["mul", "letter"], defaultdict(str, {"sc": "Cyrl", "nodot": "1"}))
    '<i>A letter of the Cyrillic script</i>'
    """
    data["sc"] = "Cyrillic "
    return render_lang_def(tpl, parts, data, word=word)


def render_latn_def(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_latn_def("Latn-def", ["en", "name", "M", "m"], defaultdict(str))
    '<i>The name of the Latin-script letter</i> <b>M</b> / <b>m</b>.'
    >>> render_latn_def("Latn-def", ["en", "letter"], defaultdict(str))
    '<i>The letter of the English alphabet, written in the Latin script</i>.'
    >>> render_latn_def("Latn-def", ["en", "letter", "1"], defaultdict(str))
    '<i>The first letter of the English alphabet, written in the Latin script</i>.'
    >>> render_latn_def("Latn-def", ["en", "letter", "1", "a"], defaultdict(str))
    '<i>The first letter of the English alphabet, called <b>a</b> and written in the Latin script</i>.'
    >>> render_latn_def("Latn-def", ["en", "ordinal", "1"], defaultdict(str))
    '<i>The ordinal number <b>first</b>, derived from this letter of the English alphabet, written in the Latin script</i>.'
    >>> render_latn_def("Latn-def", ["en", "ordinal", "1", "a"], defaultdict(str))
    '<i>The ordinal number <b>first</b>, derived from this letter of the English alphabet, called <b>a</b> and written in the Latin script</i>.'
    """
    data["sc"] = "Latin-"
    return render_lang_def(tpl, parts, data, word=word)


def render_dating(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_dating("ante", ["1880"], defaultdict(str))
    '<i>a.</i> <b>1880</b>,'
    >>> render_dating("ante", ["1880", "1900"], defaultdict(str))
    '<i>a.</i> <b>1880</b> 1900,'
    >>> render_dating("circa", ["1880", "1900"], defaultdict(str))
    '<i>c.</i> <b>1880</b> 1900,'
    """
    init = f"{tpl[0]}."
    start = data["1"] or parts.pop(0) if parts else ""
    end = data["2"] or parts.pop(0) if parts else ""

    return f"{italic(init)} {strong(start)}" + (f" {end}" if end else "") + ","


def render_deverbal(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_deverbal("deverbal", [], defaultdict(str))
    'Deverbal'
    >>> render_deverbal("deverbal", ["fr", "accorder"], defaultdict(str))
    'Deverbal from <i>accorder</i>'
    >>> render_deverbal("deverbal", ["it", "sguardare", "", "to look at"], defaultdict(str, {"nocap": "1"}))
    'deverbal from <i>sguardare</i> (“to look at”)'
    """
    text = "deverbal" if data["nocap"] == "1" else "Deverbal"
    if len(parts) > 1:
        text += f" from {italic(parts[1])}"
        if len(parts) > 3:
            text += f" (“{parts[3]}”)"
    return text


def render_etydate(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_etydate("etydate", ["1880"], defaultdict(str))
    'First attested in 1880'
    >>> render_etydate("etydate", ["1880"], defaultdict(str, {"nocap": "1"}))
    'first attested in 1880'
    >>> render_etydate("etydate", ["first half of the 19th century"], defaultdict(str))
    'First attested in the first half of the 19th century'
    >>> render_etydate("etydate", ["c", "1900"], defaultdict(str))
    'First attested in <i>c.</i> 1900'
    >>> render_etydate("etydate", ["c", "1900", "2000"], defaultdict(str))
    'First attested in <i>c.</i> 1900, but in common usage only as of 2000'
    >>> render_etydate("etydate", ["c", "1900", "first half of the 21st century"], defaultdict(str))
    'First attested in <i>c.</i> 1900, but in common usage only as of the first half of the 21st century'
    >>> render_etydate("etydate", ["r", "1900", "1910"], defaultdict(str))
    'First attested in 1900–1910'
    >>> render_etydate("etydate", ["r", "1900", "1910", "1980"], defaultdict(str))
    'First attested in 1900–1910, but in common usage only as of 1980'
    >>> render_etydate("etydate", ["r", "1900", "1910", "first half of the 19st century"], defaultdict(str))
    'First attested in 1900–1910, but in common usage only as of the first half of the 19st century'
    """

    def render_etydate_l2(parts: list[str]) -> str:
        phrase = ", but in common usage only as of "
        if parts[0] == "c":
            phrase += f"{italic('c.')} "
            phrase += f"{parts[2]}–{parts[3]}" if parts[1] == "r" else parts[1]
        else:
            if parts[0] == "r":
                phrase += f"{parts[1]}–{parts[2]}"
            else:
                phrase += parts[0] if re.match(r"\d+$", parts[0]) else f"the {parts[0]}"
        return phrase

    nocap = data["nocap"] in ("1", "yes")
    phrase = ("f" if nocap else "F") + "irst attested in "
    if parts[0] == "c":
        phrase += f"{italic('c.')} "
        if parts[1] == "r":
            phrase += f"{parts[2]}–{parts[3]}"
            if len(parts) > 4:
                phrase += render_etydate_l2(parts[4:])
        else:
            phrase += parts[1]
            if len(parts) > 2:
                phrase += render_etydate_l2(parts[2:])
    else:
        if parts[0] == "r":
            phrase += f"{parts[1]}–{parts[2]}"
            if len(parts) > 3:
                phrase += render_etydate_l2(parts[3:])
        else:
            phrase += parts[0] if re.match(r"\d+$", parts[0]) else f"the {parts[0]}"
    return phrase


def alter_demonym_parts(parts: list[str]) -> list[str]:
    def rpl(match: re.Match[str]) -> str:
        kind, pos, place = match.groups()

        kind = placetypes_aliases.get(kind, kind)
        prep = recognized_placetypes[kind.lower()]["preposition"] or "of"
        if pos.istitle():
            kind = kind.title()
        as_prefix = pos.lower() == "pref"
        multiple_places = "," in place

        if multiple_places:
            kind += "s"
            place = concat(place.split(","), ", ", last_sep=" and ")

        return f"{kind} {prep} {place}" if as_prefix else f"{place} {kind}"

    for idx, part in enumerate(parts.copy()):
        has_changed = False
        if "<<" in part:
            part = re.sub(r"<<(\w+)(?::also)?:(\w+)(?::also)?/([^>]+)>>", rpl, part)
            has_changed = True

        if "<q:" in part:
            part = re.sub(r"(\w+)<q:([^>]+)>", r"(<i>\2</i>) \1", part)
            has_changed = True
        if "<qq:" in part:
            part = re.sub(r"(\w+)<qq:([^>]+)>", r"\1 (<i>\2</i>)", part)
            has_changed = True
        if "<t:" in part or "<gloss:" in part:
            part = re.sub(r"<(?:t|gloss):([^>]+)>", r" (\1)", part)
            has_changed = True

        if "w:" in part:
            part = part.replace("w:", "")
            has_changed = True

        if "<<" in part:
            part = re.sub(r"<<\w/([^>]+)>>", r"\1", part)
            has_changed = True

        if has_changed:
            parts[idx] = part

    return parts


def render_demonym_adj(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_demonym_adj("demonym-adj", ["en", "Tucson"], defaultdict(str))
    'Of, from or relating to Tucson.'
    >>> render_demonym_adj("demonym-adj", ["en", "Tucson"], defaultdict(str, {"nocap": "1", "nodot": "1"}))
    'of, from or relating to Tucson'
    >>> render_demonym_adj("demonym-adj", ["it", "w:Abatemarco"], defaultdict(str))
    'of, from or relating to Abatemarco'

    >>> render_demonym_adj("demonym-adj", ["en", "Alexandria<t:city in Egypt>", "Alexandria<t:city in Virginia, USA>"], defaultdict(str))
    'Of, from or relating to Alexandria (city in Egypt) or Alexandria (city in Virginia, USA).'
    >>> render_demonym_adj("demonym-adj", ["it", "Alexandria in Egypt"], defaultdict(str, {"t": "Alexandrian", "t2": "Alexandrine"}))
    'Alexandrian, Alexandrine (of, from or relating to Alexandria in Egypt)'
    >>> render_demonym_adj("demonym-adj", ["es", "Linares, Colombia", "w:Linares, Jaén", "w:Linares de la Sierra", "w:Linares de Mora", "w:Linares de Riofrío", "w:Linares, Nuevo León"], defaultdict(str))
    'of, from or relating to Linares, Colombia; Linares, Jaén; Linares de la Sierra; Linares de Mora; Linares de Riofrío; or Linares, Nuevo León'
    >>> render_demonym_adj("demonym-adj", ["en", "the <<r:pref/Karelia>>, politically split between the <<adr:pref/North Karelia,South Karelia,here>>, <<c/Finland>> and the <<rep:Pref:also/Karelia>>, <<c/Russia>>"], defaultdict(str))
    'Of, from or relating to the region of Karelia, politically split between the administrative regions of North Karelia, South Karelia and here, Finland and the Republic of Karelia, Russia.'
    >>> render_demonym_adj("demonym-adj", ["en", "the <<r:pref/Frisia>>: Either West Frisia (the Dutch <<p:also:pref/Friesland>>); North Frisia (in the German <<s:pref:also/Schleswig-Holstein>>, near the Danish border); or East Frisia (in the German <<s:pref:also/Lower Saxony>>, near the Dutch border)"], defaultdict(str))
    'Of, from or relating to the region of Frisia: Either West Frisia (the Dutch province of Friesland); North Frisia (in the German state of Schleswig-Holstein, near the Danish border); or East Frisia (in the German state of Lower Saxony, near the Dutch border).'
    >>> render_demonym_adj("demonym-adj", ["it", "Sanremo<gloss:town in Liguria>"], defaultdict(str))
    'of, from or relating to Sanremo (town in Liguria)'
    """
    is_english = parts[0] == "en"
    has_parenthesis = bool(data["t"])

    phrase = ""
    if t1 := data["t"]:
        phrase += t1
        for idx in range(2, 16):
            if t := data[f"t{idx}"]:
                phrase += f", {t}"
            else:
                break
        phrase += " ("
    phrase += "o" if data["nocap"] or not is_english else "O"
    phrase += "f, from or relating to "
    sep, last_sep = (
        (" or ", " or ")
        if len(parts[1:]) == 2
        else ("; ", "; or ")
        if any("t:" in part or "w:" in part for part in parts[1:])
        else (", ", " or ")
    )
    parts = alter_demonym_parts(parts)
    phrase += concat(parts[1:], sep, last_sep=last_sep)

    if re.search(r"<+\w+:", phrase):
        assert 0, f"Missing special place handling for demonym-adj: {parts}"

    if has_parenthesis:
        phrase += ")"

    if is_english and not data["nodot"]:
        phrase += "."

    return phrase


def render_demonym_noun(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_demonym_noun("demonym-noun", ["it", "w:Abatemarco"], defaultdict(str))
    'native or inhabitant of Abatemarco'
    >>> render_demonym_noun("demonym-noun", ["it", "w:Abatemarco"], defaultdict(str, {"g": "m"}))
    'native or inhabitant of Abatemarco (<i>usually male</i>)'
    >>> render_demonym_noun("demonym-noun", ["it", "Abdera"], defaultdict(str, {"t": "Abderite"}))
    'Abderite (native or inhabitant of Abdera)'
    >>> render_demonym_noun("demonym-noun", ["it", "Alexandria in Egypt"], defaultdict(str, {"t": "Alexandrian", "t2": "Alexandrine"}))
    'Alexandrian, Alexandrine (native or inhabitant of Alexandria in Egypt)'
    >>> render_demonym_noun("demonym-noun", ["it", "Alghero<qq:in Sardinia>"], defaultdict(str, {"t": "Algherese"}))
    'Algherese (native or inhabitant of Alghero (<i>in Sardinia</i>))'
    >>> render_demonym_noun("demonym-noun", ["it", "America", "the Americas", "the United States"], defaultdict(str, {"g": "f", "t": "American"}))
    'female American (female native or inhabitant of America, the Americas or the United States)'
    >>> render_demonym_noun("demonym-noun", ["it", "Latin America"], defaultdict(str, {"t": "Latina", "g": "f", "gloss_is_gendered": "true"}))
    'Latina (female native or inhabitant of Latin America)'
    >>> render_demonym_noun("demonym-noun", ["es", "San Juan<t:capital of Puerto Rico>", "San Juan<t:city in Cuba>", "w:San Juan de los Morros<t:capital of the state of Guárico, Venezuela>", "w:San Juan de la Maguana<t:city or province of the Dominican Republic>"], defaultdict(str, {"t": "Sanjuanero", "g": "m"}))
    'Sanjuanero (native or inhabitant of San Juan (capital of Puerto Rico); San Juan (city in Cuba); San Juan de los Morros (capital of the state of Guárico, Venezuela); or San Juan de la Maguana (city or province of the Dominican Republic)) (<i>usually male</i>)'

    >>> render_demonym_noun("demonym-noun", ["en", "the <<city:pref/Adelaide>>, <<s/South Australia>>", "<<c/Germany>>"], defaultdict(str))
    'A native or inhabitant of the city of Adelaide, South Australia, Germany.'
    >>> render_demonym_noun("demonym-noun", ["en", "the <<p:Pref/Quebec>>, <<c/Canada>>"], defaultdict(str))
    'A native or inhabitant of the Province of Quebec, Canada.'
    """
    is_english = parts[0] == "en"
    is_female = data["g"] == "f"
    skip_female_prefix = data["gloss_is_gendered"]
    has_parenthesis = bool(data["t"])

    if is_female:
        del data["g"]

    phrase = "A " if is_english else ""
    if is_female and not skip_female_prefix:
        phrase += "female "
    if t1 := data["t"]:
        phrase += t1
        for idx in range(2, 16):
            if t := data[f"t{idx}"]:
                phrase += f", {t}"
            else:
                break
        phrase += " ("
    if is_female:
        phrase += "female "
    phrase += "native or inhabitant of "
    sep, last_sep = (
        (", ", ", ")
        if is_english
        else ("; ", "; or ")
        if any("<t:" in part or "<w:" in part for part in parts[1:])
        else (", ", " or ")
    )
    parts = alter_demonym_parts(parts)
    phrase += concat(parts[1:], sep, last_sep=last_sep)

    if re.search(r"<+\w+:", phrase):
        assert 0, f"Missing special place handling for demonym-noun: {parts}"

    if has_parenthesis:
        phrase += ")"

    if data["g"] == "m":
        phrase += " (<i>usually male</i>)"

    if is_english and not data["nodot"]:
        phrase += "."

    return phrase


def render_foreign_derivation(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_foreign_derivation("bor", ["en", "ar", "الْعِرَاق", "", "Iraq"], defaultdict(str))
    'Arabic <i>الْعِرَاق</i> (<i>ālʿrāq</i>, “Iraq”)'
    >>> render_foreign_derivation("bor", [], defaultdict(str, {"1": "en", "2": "ja", "3": "マエバリ"}))
    'Japanese <i>マエバリ</i>'
    >>> render_foreign_derivation("bor+", [], defaultdict(str, {"1": "en", "2": "ja", "3": "マエバリ"}))
    'Borrowed from Japanese <i>マエバリ</i>'
    >>> render_foreign_derivation("der", ["en", "fro", "-"], defaultdict(str))
    'Old French'
    >>> render_foreign_derivation("der", ["en", "mul", "Jaborosa parviflora"], defaultdict(str))
    'translingual <i>Jaborosa parviflora</i>'
    >>> render_foreign_derivation("der+", ["en", "mul", "Jaborosa parviflora"], defaultdict(str))
    'Derived from translingual <i>Jaborosa parviflora</i>'
    >>> render_foreign_derivation("etyl", ["enm", "en"], defaultdict(str))
    'Middle English'
    >>> render_foreign_derivation("etyl", ["grc"], defaultdict(str))
    'Ancient Greek'
    >>> render_foreign_derivation("inh", ["en", "enm", "water"], defaultdict(str))
    'Middle English <i>water</i>'
    >>> render_foreign_derivation("inh", ["en", "ang", "wæter", "", "water"], defaultdict(str))
    'Old English <i>wæter</i> (“water”)'
    >>> render_foreign_derivation("inh", ["en", "ang", "etan"], defaultdict(str, {"t":"to eat"}))
    'Old English <i>etan</i> (“to eat”)'
    >>> render_foreign_derivation("inh", ["en", "ine-pro", "*werdʰh₁om", "*wr̥dʰh₁om"], defaultdict(str))
    'Proto-Indo-European <i>*wr̥dʰh₁om</i>'
    >>> render_foreign_derivation("inh+", ["en", "ine-pro", "*werdʰh₁om", "*wr̥dʰh₁om"], defaultdict(str))
    'Inherited from Proto-Indo-European <i>*wr̥dʰh₁om</i>'
    >>> render_foreign_derivation("noncog", ["fro", "livret"], defaultdict(str, {"t":"book, booklet"}))
    'Old French <i>livret</i> (“book, booklet”)'
    >>> render_foreign_derivation("noncog", ["xta", "I̱ta Ita"], defaultdict(str, {"lit":"flower river"})) #xochopa
    'Alcozauca Mixtec <i>I̱ta Ita</i> (literally “flower river”)'
    >>> render_foreign_derivation("noncog", ["egy", "ḫt n ꜥnḫ", "", "grain, food"], defaultdict(str, {"lit":"wood/stick of life"}))
    'Egyptian <i>ḫt n ꜥnḫ</i> (“grain, food”, literally “wood/stick of life”)'
    >>> render_foreign_derivation("cal", ["fr" , "en", "light year"], defaultdict(str, {"alt":"alt", "tr":"tr", "t":"t", "g":"m", "pos":"pos", "lit":"lit"}))
    'Calque of English <i>alt</i> <i>m</i> (<i>tr</i>, “t”, pos, literally “lit”)'
    >>> render_foreign_derivation("pcal", ["en" , "de", "Leberwurst"], defaultdict(str, {"nocap":"1"}))
    'partial calque of German <i>Leberwurst</i>'
    >>> render_foreign_derivation("sl", ["en", "ru", "пле́нум", "", "plenary session"], defaultdict(str, {"nocap":"1"}))
    'semantic loan of Russian <i>пле́нум</i> (<i>plenum</i>, “plenary session”)'
    >>> render_foreign_derivation("learned borrowing", ["en", "la", "consanguineus"], defaultdict(str))
    'Learned borrowing from Latin <i>consanguineus</i>'
    >>> render_foreign_derivation("learned borrowing", ["en", "LL.", "trapezium"], defaultdict(str, {"notext":"1"}))
    'Late Latin <i>trapezium</i>'
    >>> render_foreign_derivation("slbor", ["en", "fr", "mauvaise foi"], defaultdict(str, {"nocap":"1"}))
    'semi-learned borrowing from French <i>mauvaise foi</i>'
    >>> render_foreign_derivation("obor", ["en", "ru", "СССР"], defaultdict(str))
    'Orthographic borrowing from Russian <i>СССР</i> (<i>SSSR</i>)'
    >>> render_foreign_derivation("unadapted borrowing", ["en", "ar", "قِيَاس", "", "measurement, analogy"], defaultdict(str))
    'Unadapted borrowing from Arabic <i>قِيَاس</i> (<i>qīās</i>, “measurement, analogy”)'
    >>> render_foreign_derivation("psm", ["en", "yue", "-"], defaultdict(str))
    'Phono-semantic matching of Cantonese'
    >>> render_foreign_derivation("translit", ["en", "ar", "عَالِيَة"], defaultdict(str))
    'Transliteration of Arabic <i>عَالِيَة</i> (<i>ʿālī</i>)'
    >>> render_foreign_derivation("back-form", ["en", "zero derivation"], defaultdict(str, {"nocap":"1"}))
    'back-formation from <i>zero derivation</i>'
    >>> render_foreign_derivation("bf", ["en"], defaultdict(str))
    'Back-formation'

    >>> render_foreign_derivation("l", ["cs", "háček"], defaultdict(str))
    'háček'
    >>> render_foreign_derivation("l", ["en", "go", "went"], defaultdict(str))
    'went'
    >>> render_foreign_derivation("l", ["en", "God be with you"], defaultdict(str))
    'God be with you'
    >>> render_foreign_derivation("l", ["la", "similis"], defaultdict(str, {"t":"like"}))
    'similis (“like”)'
    >>> render_foreign_derivation("l", ["la", "similis", "", "like"], defaultdict(str))
    'similis (“like”)'
    >>> render_foreign_derivation("l", ["mul", "☧", ""], defaultdict(str))
    '☧'
    >>> render_foreign_derivation("l", ["ru", "ру́сский", "", "Russian"], defaultdict(str, {"g":"m"}))
    'ру́сский <i>m</i> (<i>russkij</i>, “Russian”)'
    >>> render_foreign_derivation("link", ["en", "water vapour"], defaultdict(str))
    'water vapour'
    >>> render_foreign_derivation("ll", ["en", "cod"], defaultdict(str))
    'cod'

    >>> render_foreign_derivation("m", ["en", "more"], defaultdict(str))
    '<i>more</i>'
    >>> render_foreign_derivation("m", ["en", "w:Group of Eight"], defaultdict(str))
    '<i>Group of Eight</i>'
    >>> render_foreign_derivation("m", ["enm", "us"], defaultdict(str))
    '<i>us</i>'
    >>> render_foreign_derivation("m", ["enm", "w:Group of Eight"], defaultdict(str))
    '<i>Group of Eight</i>'
    >>> render_foreign_derivation("m", ["ine-pro", "*h₁ed-"], defaultdict(str, {"t":"to eat"}))
    '<i>*h₁ed-</i> (“to eat”)'
    >>> render_foreign_derivation("m", ["ar", "عِرْق", "", "root"], defaultdict(str))
    '<i>عِرْق</i> (<i>ʿrq</i>, “root”)'
    >>> render_foreign_derivation("m", ["pal"], defaultdict(str, {"tr":"ˀl'k'", "ts":"erāg", "t":"lowlands"}))
    "(<i>ˀl'k'</i> /erāg/, “lowlands”)"
    >>> render_foreign_derivation("m", ["ar", "عَرِيق", "", "deep-rooted"], defaultdict(str))
    '<i>عَرِيق</i> (<i>ʿrīq</i>, “deep-rooted”)'

    >>> render_foreign_derivation("langname-mention", ["en", "-"], defaultdict(str))
    'English'
    >>> render_foreign_derivation("m+", ["en", "-"], defaultdict(str))
    'English'
    >>> render_foreign_derivation("m+", ["ja", "力車"], defaultdict(str, {"tr":"rikisha"}))
    'Japanese <i>力車</i> (<i>rikisha</i>)'
    """
    # Short path for the {{m|en|WORD}} template
    if tpl in {"m", "m-lite"} and len(parts) == 2 and parts[0] == "en" and not data:
        word = parts[1]
        if word.startswith("w:"):
            word = word[2:]
        return italic(word)

    mentions = (
        "back-formation",
        "backformation",
        "back-form",
        "backform",
        "bf",
        "l",
        "l-lite",
        "link",
        "ll",
        "mention",
        "m",
        "m-lite",
    )
    dest_lang_ignore = (
        "cog",
        "cog-lite",
        "cognate",
        "etyl",
        "langname-mention",
        "m+",
        "nc",
        "ncog",
        "noncog",
        "noncognate",
        *mentions,
    )
    if tpl not in dest_lang_ignore and parts:
        parts.pop(0)  # Remove the destination language

    dst_locale = parts.pop(0) if parts else data["2"]

    if tpl == "etyl" and parts:
        parts.pop(0)

    phrase = ""
    starter = ""
    if data["notext"] != "1":
        if tpl in {"bor+"}:
            starter = "borrowed from "
        elif tpl in {"calque", "cal", "clq"}:
            starter = "calque of "
        if tpl in {"der+"}:
            starter = "derived from "
        elif tpl in {"inh+"}:
            starter = "inherited from "
        elif tpl in {"partial calque", "pcal"}:
            starter = "partial calque of "
        elif tpl in {"semantic loan", "sl"}:
            starter = "semantic loan of "
        elif tpl in {"learned borrowing", "lbor"}:
            starter = "learned borrowing from "
        elif tpl in {"semi-learned borrowing", "slbor"}:
            starter = "semi-learned borrowing from "
        elif tpl in {"orthographic borrowing", "obor"}:
            starter = "orthographic borrowing from "
        elif tpl in {"unadapted borrowing", "ubor"}:
            starter = "unadapted borrowing from "
        elif tpl in {"phono-semantic matching", "psm"}:
            starter = "phono-semantic matching of "
        elif tpl in {"transliteration", "translit"}:
            starter = "transliteration of "
        elif tpl in {"back-formation", "backformation", "back-form", "backform", "bf"}:
            starter = "back-formation"
            if parts:
                starter += " from"
        phrase = starter if data["nocap"] == "1" else starter.capitalize()

    lang = "translingual" if dst_locale == "mul" else langs.get(dst_locale, "")
    phrase += lang if tpl not in mentions else ""

    if parts or data["3"]:
        word = parts.pop(0) if parts else data["3"]
        if word.startswith("w:"):
            word = word[2:]
        if word == "-":
            return phrase
    else:
        word = ""

    word = data["alt"] or word
    gloss = data["t"] or data["gloss"]

    if parts:
        word = parts.pop(0) or word  # 4, alt=

    if tpl in {"l", "l-lite", "link", "ll"}:
        phrase += f" {word}"
    elif word:
        phrase += f" {italic(word)}"
    if data["g"]:
        phrase += f" {gender_number_specs(data['g'])}"
    trans = "" if data["tr"] else transliterate(dst_locale, word)
    if parts:
        gloss = parts.pop(0)  # 5, t=, gloss=

    phrase += gloss_tr_poss(data, gloss, trans=trans)

    return phrase.lstrip()


def render_fa_sp(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_fa_sp("fa sp", ["en", "SH"], defaultdict(str, {"id": "self-harm", "t": "self-harm"}))
    '<i>Filter-avoidance spelling of</i> <b>SH</b> (“self-harm”).'
    """
    text = italic(("f" if data["nocap"] == "1" else "F") + "ilter-avoidance spelling of")
    text += f" {strong(parts[1])}"
    if t := data["t"]:
        text += f" (“{t}”)"
    dot = "" if data["nodot"] == "1" else (data["dot"] or ".")
    return f"{text}{dot}"


def render_frac(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_frac("frac", ["39", "47", "127"], defaultdict(str))
    '39<small><sup>47</sup><big>⁄</big><sub>127</sub></small>'
    >>> render_frac("frac", ["39", "47"], defaultdict(str))
    '<small><sup>39</sup><big>⁄</big><sub>47</sub></small>'
    >>> render_frac("frac", ["39"], defaultdict(str))
    '<small><sup>1</sup><big>⁄</big><sub>39</sub></small>'
    """
    phrase = ""
    if len(parts) == 3:
        phrase = f"{parts[0]}<small><sup>{parts[1]}</sup><big>⁄</big><sub>{parts[2]}</sub></small>"
    elif len(parts) == 2:
        phrase = f"<small><sup>{parts[0]}</sup><big>⁄</big><sub>{parts[1]}</sub></small>"
    elif len(parts) == 1:
        phrase = f"<small><sup>1</sup><big>⁄</big><sub>{parts[0]}</sub></small>"
    return phrase


def render_given_name(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_given_name("given name", ["en" , "male"], defaultdict(str))
    '<i>A male given name</i>'
    >>> render_given_name("given name", ["en" , "male"], defaultdict(str, {"or":"female", "A":"a Japanese"}))
    '<i>a Japanese male or female given name</i>'
    >>> render_given_name("given name", ["en" , "male"], defaultdict(str, {"from":"Spanish", "from2":"Portuguese", "from3":"French"}))
    '<i>A male given name from Spanish, Portuguese or French</i>'
    >>> render_given_name("given name", ["en" , "male"], defaultdict(str, {"from":"la:Patricius<t:patrician>"}))
    '<i>A male given name from Latin Patricius (“patrician”)</i>'
    >>> render_given_name("given name", ["en" , "female"], defaultdict(str, {"from":"place names", "usage":"modern", "var":"Savannah"}))
    '<i>A female given name transferred from the place name, of modern usage, variant of Savannah</i>'
    >>> render_given_name("given name", ["da" , "male"], defaultdict(str, {"eq":"Bertram,fr:Bertrand"}))
    '<i>A male given name, equivalent to English Bertram or French Bertrand</i>'
    >>> render_given_name("given name", ["en" , "female"], defaultdict(str, {"from":"Hebrew", "m":"Daniel", "f":"Daniela"}))
    '<i>A female given name from Hebrew, masculine equivalent Daniel, feminine equivalent Daniela</i>'
    >>> render_given_name("given name", ["lv" , "male"], defaultdict(str, {"from":"Slavic languages", "eq":"pl:Władysław,cs:Vladislav,ru:Владисла́в"}))
    '<i>A male given name from the Slavic languages, equivalent to Polish Władysław, Czech Vladislav or Russian Владисла́в (Vladislav)</i>'
    >>> render_given_name("given name", ["en" , "male"], defaultdict(str, {"from":"Germanic languages", "from2":"surnames"}))
    '<i>A male given name from the Germanic languages or transferred from the surname</i>'
    >>> render_given_name("given name", ["en", "female"], defaultdict(str, {"from":"coinages", "var":"Cheryl", "var2":"Shirley"}))
    '<i>A female given name originating as a coinage, variant of Cheryl or Shirley</i>'
    >>> render_given_name("given name", ["en", "male"], defaultdict(str, {"dim":"Mohammed", "dim2":"Moses", "dim3":"Maurice"}))
    '<i>A diminutive of the male given names Mohammed, Moses or Maurice</i>'
    >>> render_given_name("given name", ["en", "male", ], defaultdict(str, {"dim":"Mohammed"}))
    '<i>A diminutive of the male given name Mohammed</i>'
    >>> render_given_name("given name", ["en", "female"], defaultdict(str, {"diminutive":"Florence", "diminutive2":"Flora"}))
    '<i>A diminutive of the female given names Florence or Flora</i>'
    >>> render_given_name("given name", ["en", "male"], defaultdict(str, {"from":"Hindi", "meaning":"patience"}))
    '<i>A male given name from Hindi, meaning "patience"</i>'
    >>> render_given_name("given name", ["en", "female"], defaultdict(str, {"from":"Danish < grc:Αἰκατερῑ́νη", "var": "Karen"}))
    '<i>A female given name from Danish [in turn from Ancient Greek Αἰκατερῑ́νη], variant of Karen</i>'
    >>> render_given_name("given name", ["en", "male"], defaultdict(str, {"from":"la:Gabriēl < grc:Γαβρῑήλ < hbo:גַּבְרִיאֵל<tr:gaḇrīʾḗl><t:God is my strong man>"}))
    '<i>A male given name from Latin Gabriēl [in turn from Ancient Greek Γαβρῑήλ, in turn from Biblical Hebrew גַּבְרִיאֵל (<i>gaḇrīʾḗl</i>, “God is my strong man”)]</i>'
    >>> render_given_name("given name", ["da", "male"], defaultdict(str, {"usage":"traditionally popular", "eq": "Nicholas", "from":"la:Nīcolāī<pos:genitive>", "from2":"ru:Никола́й"}))
    '<i>A male given name from Latin Nīcolāī (genitive) or Russian Никола́й, of traditionally popular usage, equivalent to English Nicholas</i>'

    """
    parts.pop(0)  # language
    gender = data["gender"] or (parts.pop(0) if parts else "")
    gender += f" or {data['or']}" if data["or"] else ""
    phrase = f"{data['A'] or 'A'} "
    dimtext = join_names(data, "dim", " or ", include_langname=False, key_alias="diminutive")
    phrase += "diminutive of the " if dimtext else ""
    phrase += f"{gender} given name"
    phrase += "s" if ", " in dimtext or " or " in dimtext else ""
    phrase += f" {dimtext}" if dimtext else ""

    class Seg(TypedDict, total=False):
        prefix: str
        suffixes: list[str]

    fromsegs: list[Seg] = []
    lastfrom_seg: Seg = {}
    for i in range(1, 10):
        from_key = f"from{i}" if i != 1 else "from"
        if data[from_key]:
            from_text = data[from_key]
            suffix = ""
            if from_text == "surnames":
                prefix = "transferred from the "
                suffix = "surname"
            elif from_text == "place names":
                prefix = "transferred from the "
                suffix = "place name"
            elif from_text == "coinages":
                prefix = "originating as "
                suffix = "a coinage"
            else:
                prefix = "from "
                from_texts = [from_text]
                if " < " in from_text:
                    from_texts = from_text.split(" < ")
                prepend = False
                for from_text in from_texts:
                    if suffix:
                        suffix += ", in turn from " if prepend else " [in turn from "
                        prepend = True
                    if ":" in from_text:
                        # get t:
                        # remove <>
                        from_gloss = ""
                        from_data: defaultdict[str, str] = defaultdict(str)
                        matches = re.findall(r"<([^:]*):([^>]*)>", from_text)
                        for match in matches:
                            if match[0] == "t":
                                from_gloss = match[1]
                            else:
                                from_data[match[0]] = match[1]
                        from_text = re.sub(r"<([^>]*)>", "", from_text)
                        # todo fromalt
                        from_split = from_text.split(":")
                        lang = langs.get(from_split[0], from_split[0])
                        suffix += f"{lang} {from_split[1] if len(from_split) > 1 else ''}"
                        suffix += gloss_tr_poss(from_data, from_gloss)
                    elif from_text.endswith("languages"):
                        suffix = f"the {from_text}"
                    else:
                        suffix += from_text
                if prepend:
                    suffix += "]"
            if lastfrom_seg and lastfrom_seg.get("prefix", "") != prefix:
                fromsegs.append(lastfrom_seg)
                lastfrom_seg = {}
            if not lastfrom_seg:
                lastfrom_seg = {"prefix": prefix, "suffixes": []}
            lastfrom_seg["suffixes"].append(suffix)
    if lastfrom_seg:
        fromsegs.append(lastfrom_seg)
    if localphrase := [
        fromseg.get("prefix", "") + concat(fromseg.get("suffixes", []), ", ", last_sep=" or ") for fromseg in fromsegs
    ]:
        phrase += " " + concat(localphrase, ", ", last_sep=" or ")

    if meaningtext := join_names(data, "meaning", " or ", include_langname=False, prefix='"', suffix='"'):
        phrase += f", meaning {meaningtext}"

    if data["usage"]:
        phrase += ", of " + data["usage"] + " usage"

    if vartext := join_names(data, "var", " or "):
        phrase += f", variant of {vartext}"
    if mtext := join_names(data, "m", " and "):
        phrase += f", masculine equivalent {mtext}"
    if ftext := join_names(data, "f", " and "):
        phrase += f", feminine equivalent {ftext}"
    if eqext := join_names(data, "eq", " or ", include_langname=True):
        phrase += f", equivalent to {eqext}"

    return italic(phrase)


def render_han_simp(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_han_simp("Han simp", ["請"], defaultdict(str, {"f": "言", "t": "讠"}))
    'Simplified from 請 (言 → 讠)'
    >>> render_han_simp("Han simp", ["讀"], defaultdict(str, {"f": "言", "t": "讠", "f2": "賣", "t2": "卖"}))
    'Simplified from 讀 (言 → 讠 and 賣 → 卖)'
    """
    if data["a"]:
        assert 0
    text = ("s" if data["nocap"] else "S") + f"implified from {parts[0]} ("
    if f1 := data["f"]:
        text += f"{f1} → {data['t']}"
    if f2 := data["f2"]:
        text += f" and {f2} → {data['t2']}"
    return f"{text})"


def render_he_l(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_he_l("he-l", ["הר מגידו"], defaultdict(str, {"dwv": "הַר מְגִדּוֹ", "tr": "har megiddo"}))
    'הר מגידו / הַר מְגִדּוֹ (<i>har megiddo</i>)'
    """
    if dwv := data["dwv"]:
        parts[0] += f" / {dwv}"
    parts.insert(0, "he")
    return render_foreign_derivation("l", parts, data, word=word)


def render_he_m(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_he_m("he-m", ["צייר"], defaultdict(str, {"dwv": "צַיָּר", "tr": "tsayár"}))
    '<i>צייר / צַיָּר</i> (<i>tsayár</i>)'
    """
    if dwv := data["dwv"]:
        parts[0] += f" / {dwv}"
    parts.insert(0, "he")
    return render_foreign_derivation("m", parts, data, word=word)


def render_historical_given_name(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_historical_given_name("historical given name", ["en" , "male", "Saint Abundius, an early Christian bishop"], defaultdict(str))
    '<i>A male given name of historical usage, notably borne by Saint Abundius, an early Christian bishop</i>'
    >>> render_historical_given_name("historical given name", ["en" , "male"], defaultdict(str, {"eq": "John", "A":""}))
    '<i>male given name of historical usage, equivalent to English <b>John</b></i>'
    """
    data["1"] or (parts.pop(0) if parts else "")
    sex = data["2"] or (parts.pop(0) if parts else "")
    desc = data["3"] or (parts.pop(0) if parts else "")
    article = data.get("A", "A")
    phrase = f"{article} " if article else ""
    phrase += f"{sex} "
    phrase += "given name of historical usage"
    if data["eq"]:
        phrase += f", equivalent to English {strong(data['eq'])}"
    if desc:
        phrase += f", notably borne by {desc}"
    return italic(phrase)


def render_ipa_char(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ipa_char("historical given name", ["[tʃ]"], defaultdict(str))
    '[tʃ]'
    >>> render_ipa_char("historical given name", ["[tʃ]", "[ts]"], defaultdict(str))
    '[tʃ], [ts]'
    """
    return concat(parts, ", ")


def render_iso_216(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_iso_216("ISO 216", ["1189", "1682"], defaultdict(str))
    '(<i>international standards</i>) ISO 216 standard paper size of 1189 mm × 1682 mm (46.81 in × 66.22 in), with a surface area of 2 m² (21.53 sq ft).'
    >>> render_iso_216("ISO 216", ["1189", "1682"], defaultdict(str, {"env": "1"}))
    '(<i>international standards</i>) ISO 216 standard envelope size of 1189 mm × 1682 mm (46.81 in × 66.22 in), with a surface area of 2 m² (21.53 sq ft).'
    >>> render_iso_216("ISO 216", ["1189", "1682"], defaultdict(str, {"untrimmed": "1"}))
    '(<i>international standards</i>) ISO 216 standard untrimmed paper size of 1189 mm × 1682 mm (46.81 in × 66.22 in), with a surface area of 2 m² (21.53 sq ft).'
    """
    width_mm = float(parts[0])
    height_mm = float(parts[1])

    if data["env"]:
        paper_type = "envelope"
    elif data["untrimmed"]:
        paper_type = "untrimmed paper"
    else:
        paper_type = "paper"

    # Dimensions in inches
    width_in = round(width_mm / 25.4, 2)
    height_in = round(height_mm / 25.4, 2)

    # Surface area in m² or cm²
    area_m2 = width_mm * height_mm / 1_000_000
    area_cm2 = width_mm * height_mm / 100

    def no_trailing_zeros(v: float) -> str:
        return str(v).rstrip("0").rstrip(".")

    # Decide between m² and cm²
    if area_m2 > 0.1:
        # Number of significant digits, at least 2
        sig_digits = math.ceil(-math.log10(area_m2)) + 2 if area_m2 < 1 else 2
        area_value = round(area_m2, sig_digits)
        area_str = f"{no_trailing_zeros(area_value)} m²"
    else:
        sig_digits = math.ceil(-math.log10(area_cm2)) + 2 if area_cm2 < 1 else 2
        area_value = round(area_cm2, sig_digits)
        area_str = f"{no_trailing_zeros(area_value)} cm²"

    # Surface area in sq ft or sq in
    area_ft2 = width_mm * height_mm / 92903.04
    area_in2 = width_mm * height_mm / 645.16
    if area_ft2 > 1:
        sig_digits = math.ceil(-math.log10(area_ft2)) + 2 if area_ft2 < 10 else 2
        imperial_area_value = round(area_ft2, sig_digits)
        imperial_area_str = f"{no_trailing_zeros(imperial_area_value)} sq ft"
    else:
        sig_digits = math.ceil(-math.log10(area_in2)) + 2 if area_in2 < 10 else 2
        imperial_area_value = round(area_in2, sig_digits)
        imperial_area_str = f"{no_trailing_zeros(imperial_area_value)} sq in"

    return (
        f"(<i>international standards</i>) {tpl} standard {paper_type} size of "
        f"{no_trailing_zeros(width_mm)} mm × {no_trailing_zeros(height_mm)} mm "
        f"({width_in} in × {height_in} in), with a surface area of "
        f"{area_str} ({imperial_area_str})."
    )


def render_iso_217(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_iso_217("ISO 217", ["1189", "1682"], defaultdict(str, {"untrimmed": "1"}))
    '(<i>international standards</i>) ISO 217 standard untrimmed paper size of 1189 mm × 1682 mm (46.81 in × 66.22 in), with a surface area of 2 m² (21.53 sq ft).'
    """
    data["untrimmed"] = "1"
    return render_iso_216(tpl, parts, data, word=word)


def render_iso_639(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_iso_639("ISO 639", [], defaultdict(str), word="ysr")
    '<i>(international standards) language code for</i> <b>Sirenik</b>.'
    >>> render_iso_639("ISO 639", ["ja"], defaultdict(str))
    'ISO 639-1 code <b>ja</b>'
    >>> render_iso_639("ISO 639", ["", "crk"], defaultdict(str))
    'ISO 639-2 code <b>crk</b>'
    >>> render_iso_639("ISO 639", ["", "", "zho"], defaultdict(str))
    'ISO 639-3 code <b>zho</b>'
    >>> render_iso_639("ISO 639", ["zh", "", "zho"], defaultdict(str, {"ref": "1"}))
    'ISO 639-1 code <b>zh</b>, ISO 639-3 code <b>zho</b>'
    >>> render_iso_639("ISO 639", ["3", "Ambonese Malay"], defaultdict(str))
    '(<i>international standards</i>) <i>ISO 639-3 language code for</i> <b>Ambonese Malay</b>.'
    >>> render_iso_639("ISO 639", ["1"], defaultdict(str), word="ab")
    '(<i>international standards</i>) <i>ISO 639-1 language code for</i> <b>Abkhaz</b>.'
    >>> render_iso_639("ISO 639", ["3", "Asa language", "Asa"], defaultdict(str, {"obs": "1"}), word="aam")
    '(<i>international standards, obsolete</i>) <i>Former ISO 639-3 language code for</i> <b>Asa</b>.'
    >>> render_iso_639("ISO 639", ["3", "Ari language (New Guinea)", "Ari"], defaultdict(str, {"dab": "New Guinea"}), word="aac")
    '(<i>international standards</i>) <i>ISO 639-3 language code for</i> <b>Ari</b> (New Guinea).'
    """
    if not parts:
        return f"{italic('(international standards) language code for')} {strong(langs[word])}."

    if parts[0].isdigit():
        phrase = f"({italic('international standards' + (', obsolete' if data['obs'] else ''))}) "
        phrase += f"{italic(('Former ' if data['obs'] else '') + 'ISO 639-' + parts[0] + ' language code for')} "
        phrase += strong(parts[-1] if len(parts) > 1 else langs[word])
        if dab := data["dab"]:
            phrase += f" ({dab})"
        return f"{phrase}."

    return ", ".join([f"ISO 639-{idx} code {strong(part)}" for idx, part in enumerate(parts, 1) if part])


def render_iso_3166(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_iso_3166("ISO 3166", ["1", "3", "Aruba"], defaultdict(str, {"from": "1986"}), word="ABW")
    '(<i>international standards</i>) <i>ISO 3166-1 alpha-3 country code for</i> <b>Aruba</b> <i>since 1986</i>.'
    >>> render_iso_3166("ISO 3166", ["1", "2", "Ascension Island"], defaultdict(str, {"obs": "1"}), word="AC")
    '(<i>international standards, obsolete</i>) <i>Former ISO 3166-1 alpha-2 country code for</i> <b>Ascension Island</b>.'
    >>> render_iso_3166("ISO 3166", ["1", "2", "Ascension Island"], defaultdict(str, {"exr": "1"}), word="AC")
    '(<i>international standards</i>) <i>Exceptionally reserved ISO 3166-1 alpha-2 country code for</i> <b>Ascension Island</b>.'
    >>> render_iso_3166("ISO 3166", ["1", "2", "Ascension Island"], defaultdict(str, {"inr": "1"}), word="AC")
    '(<i>international standards</i>) <i>Indeterminately reserved ISO 3166-1 alpha-2 country code for</i> <b>Ascension Island</b>.'
    """
    phrase = "(<i>international standards"
    if data["obs"]:
        phrase += ", obsolete"
    phrase += "</i>) <i>"

    if data["exr"]:
        phrase += "Exceptionally reserved "
    elif data["inr"]:
        phrase += "Indeterminately reserved "
    elif data["obs"]:
        phrase += "Former "
    phrase += f"{tpl}-{parts[0]} alpha-{parts[1]} country code for</i> "

    phrase += strong(parts[-1] if len(parts) > 1 else langs[word])

    if since := data["from"]:
        phrase += f" <i>since {since}</i>"

    return f"{phrase}."


def render_iso_4217(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_iso_4217("ISO 4217", ["Cardano (blockchain platform)"], defaultdict(str))
    '(<i>international standards</i>) <i>ISO 4217 currency code for the</i> <b>Cardano (blockchain platform)</b>.'
    >>> render_iso_4217("ISO 4217", ["Cardano (blockchain platform)", "Cardano"], defaultdict(str))
    '(<i>international standards</i>) <i>ISO 4217 currency code for the</i> <b>Cardano</b>.'
    >>> render_iso_4217("ISO 4217", ["Cardano (blockchain platform)", "Cardano", "detail"], defaultdict(str))
    '(<i>international standards</i>) <i>ISO 4217 currency code for the</i> <b>Cardano</b><i>; detail</i>.'

    >>> render_iso_4217("ISO 4217", ["Cardano"], defaultdict(str, {"unoff": "1", "crypto": "1"}))
    '(<i>international standards</i>) <i>Unofficial non-ISO 4217 currency code for the cryptocurrency</i> <b>Cardano</b>.'
    >>> render_iso_4217("ISO 4217", ["Cardano"], defaultdict(str, {"fund": "1"}))
    '(<i>international standards</i>) <i>ISO 4217 currency code for the</i> <b>Cardano</b><i>; a unit of account</i>.'
    >>> render_iso_4217("ISO 4217", ["Cardano"], defaultdict(str, {"hist": "1"}))
    '(<i>international standards, historical</i>) <i>ISO 4217 currency code for the former</i> <b>Cardano</b>.'
    >>> render_iso_4217("ISO 4217", ["Cardano (blockchain platform)", "Cardano"], defaultdict(str, {"res": "1"}))
    '(<i>international standards</i>) <i>Reserved ISO 4217 currency code for the</i> <i>Cardano (blockchain platform)</i>.'
    >>> render_iso_4217("ISO 4217", ["Cardano"], defaultdict(str, {"obs": "1"}))
    '(<i>international standards, obsolete</i>) <i>Former ISO 4217 currency code for the</i> <b>Cardano</b>.'
    >>> render_iso_4217("ISO 4217", ["Cardano"], defaultdict(str, {"from": "1986"}))
    '(<i>international standards</i>) <i>ISO 4217 currency code for the</i> <b>Cardano</b><i>; a currency used since 1986</i>.'
    >>> render_iso_4217("ISO 4217", ["Cardano"], defaultdict(str, {"to": "1986"}))
    '(<i>international standards</i>) <i>ISO 4217 currency code for the</i> <b>Cardano</b><i>; a currency used until 1986</i>.'
    >>> render_iso_4217("ISO 4217", ["Cardano"], defaultdict(str, {"from": "1869", "to": "1986"}))
    '(<i>international standards</i>) <i>ISO 4217 currency code for the</i> <b>Cardano</b><i>; a currency used from 1869 to 1986</i>.'
    """
    phrase = "(<i>international standards"
    if data["hist"]:
        phrase += ", historical"
    if data["obs"]:
        phrase += ", obsolete"
    phrase += "</i>) <i>"

    if data["res"]:
        phrase += "Reserved "
    elif data["obs"]:
        phrase += "Former "
    elif data["unoff"]:
        phrase += "Unofficial non-"
    phrase += f"{tpl} currency code for the"
    if data["hist"]:
        phrase += " former"
    if data["crypto"]:
        phrase += " cryptocurrency"
    phrase += "</i> "

    if data["res"]:
        phrase += italic(parts[0])
    else:
        phrase += strong(parts[1 if len(parts) > 1 else 0])

    kind = "unit of account" if data["fund"] else "currency"
    if from_ := data["from"]:
        if to_ := data["to"]:
            phrase += f"<i>; a {kind} used from {from_} to {to_}</i>"
        else:
            phrase += f"<i>; a {kind} used since {from_}</i>"
    elif to_ := data["to"]:
        phrase += f"<i>; a {kind} used until {to_}</i>"
    elif data["fund"]:
        phrase += f"<i>; a {kind}</i>"

    if len(parts) > 2:
        phrase += f"<i>; {parts[2]}</i>"

    return f"{phrase}."


def render_ja_l(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ja_l("ja-l", ["縄抜け"], defaultdict(str))
    '縄抜け'
    >>> render_ja_l("ja-l", ["縄抜け", "なわぬけ"], defaultdict(str))
    '縄抜け (なわぬけ)'
    >>> render_ja_l("ja-l", ["縄抜け", "なわぬけ", "nawanuke"], defaultdict(str))
    '縄抜け (なわぬけ, <i>nawanuke</i>)'
    """
    text = parts.pop(0)
    if parts:
        if len(parts) == 1:
            text += f" ({parts[0]})"
        else:
            text += f" ({parts[0]}, {italic(parts[1])})"
    return text


def render_ja_r(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ja_r("ja-l", ["羨ましい"], defaultdict(str))
    '羨ましい'
    >>> render_ja_r("ja-l", ["羨ましい", "うらやましい"], defaultdict(str))
    '<ruby>羨ましい<rt>うらやましい</rt></ruby>'
    >>> render_ja_r("ja-l", ["羨ましい", "うらやましい", "a"], defaultdict(str, {"lit": "lit"}))
    '<ruby>羨ましい<rt>うらやましい</rt></ruby> (“a”, literally “lit”)'
    >>> render_ja_r("ja-l", ["羨ましい", "", "a"], defaultdict(str, {"lit": "lit"}))
    '羨ましい (“a”, literally “lit”)'

    >>> render_ja_r("ja-l", ["任天堂", "^ニンテンドー"], defaultdict(str))
    '<ruby>任天堂<rt>ニンテンドー</rt></ruby>'

    >>> render_ja_r("ja-l", ["物%の%哀れ", "もの %の% あわれ"], defaultdict(str))
    '<ruby>物<rt>もの</rt></ruby>の<ruby>哀れ<rt>あわれ</rt></ruby>'
    >>> render_ja_r("ja-l", ["物 の 哀れ", "もの の あわれ"], defaultdict(str))
    '<ruby>物<rt>もの</rt></ruby>の<ruby>哀れ<rt>あわれ</rt></ruby>'
    """
    if len(parts) == 1 or not parts[1]:
        text = parts[0]
    else:
        parts[1] = parts[1].removeprefix("^")

        if sep := "%" if "%" in parts[0] else " " if " " in parts[0] else "":
            texts = [part.strip() for part in parts[0].split(sep)]
            tops = [part.strip() for part in parts[1].split(sep)]
            text = "".join(t if t == p else ruby(t, p) for t, p in zip(texts, tops))
        else:
            text = ruby(parts[0], parts[1])

    more: list[str] = []
    if len(parts) > 2:
        more.append(f"“{parts[2]}”")
    if lit := data["lit"]:
        more.append(f"literally “{lit}”")
    if more:
        text += f" ({', '.join(more)})"

    return text


def render_ko_inline(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ko_inline("ko-l", ["한국어"], defaultdict(str))
    '한국어'
    >>> render_ko_inline("ko-l", ["한국어", "a"], defaultdict(str))
    '한국어 (<i>a</i>)'
    >>> render_ko_inline("ko-l", ["한국어", "a", "b"], defaultdict(str))
    '한국어 (<i>a</i>, “b”)'
    >>> render_ko_inline("ko-l", ["한국어", "a", "b", "c"], defaultdict(str))
    '한국어 (<i>a</i>, “b”)'
    >>> render_ko_inline("ko-l", ["한국어", "a", "b", "c", "d"], defaultdict(str))
    '한국어 (<i>a</i>, “b”) (<i>d</i>)'
    >>> render_ko_inline("ko-l", ["한국어", "a", "b", "c", "d", "e"], defaultdict(str))
    '한국어 (<i>a</i>, “b”) (<i>d</i>)'
    """
    # TODO: should be improved with transliteration
    text = f"{parts.pop(0)}"
    if parts:
        text += f" (<i>{parts.pop(0)}</i>"
        if parts:
            text += f", “{parts.pop(0)}”"
        text += f") (<i>{parts[1]}</i>)" if len(parts) > 1 else ")"
    return text


def render_ltc_l(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ltc_l("ltc-l", ["螺貝"], defaultdict(str))
    '螺貝'
    >>> render_ltc_l("ltc-l", ["螺貝", "shell; conch; conch trumpet"], defaultdict(str))
    '螺貝 (“shell; conch; conch trumpet”)'
    """
    text = parts.pop(0)
    if parts:
        text += f" (“{concat(parts, ', ')}”)"
    return text


def render_label(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_label("label", ["en" , "Australia", "slang"], defaultdict(str, {"nocat":"1"}))
    '<i>(Australia, slang)</i>'
    >>> render_label("lb", ["en" , "Australia"], defaultdict(str))
    '<i>(Australia)</i>'
    >>> render_label("lb", ["en" , "Australia", "or", "foobar"], defaultdict(str))
    '<i>(Australia or foobar)</i>'
    >>> render_label("lb", ["en" , "foobar", "and", "Australia", "or", "foobar"], defaultdict(str))
    '<i>(foobar and Australia or foobar)</i>'
    >>> render_label("lb", ["en" , "foobar", "_", "Australia", "foobar"], defaultdict(str))
    '<i>(foobar Australia, foobar)</i>'
    >>> # render_label("lb", ["en" , "roa-lor"], defaultdict(str))
    >>> # '<i>(Lorrain)</i>'
    >>> render_label("lbl", ["en" , "transitive"], defaultdict(str))
    '<i>(transitive)</i>'
    >>> render_label("lbl", ["en" , "ambitransitive"], defaultdict(str))
    '<i>(ambitransitive)</i>'
    >>> render_label("lbl", ["en" , "ambitransitive", "obsolete"], defaultdict(str))
    '<i>(ambitransitive, obsolete)</i>'
    >>> render_label("lbl", ["en" , "chiefly", "nautical"], defaultdict(str))
    '<i>(chiefly nautical)</i>'
    >>> render_label("lbl", ["en" , "", "nautical"], defaultdict(str))
    '<i>(nautical)</i>'
    """
    if len(parts) == 2:
        return term(lookup_italic(parts[1], "en"))

    res = ""
    omit_pre_comma = False
    omit_post_comma = True
    omit_pre_space = False
    omit_post_space = True

    for label in parts[1:]:
        omit_pre_comma = omit_post_comma
        omit_post_comma = False
        omit_pre_space = omit_post_space
        omit_post_space = False

        syntax = syntaxes.get(label)

        omit_comma = omit_pre_comma or (syntax["omit_pre_comma"] if syntax else False)
        omit_post_comma = syntax["omit_post_comma"] if syntax else False
        omit_space = omit_pre_space or (syntax["omit_pre_space"] if syntax else False)

        if label_display := lookup_italic(label, "en"):
            if res:
                res += "" if omit_comma else ","
                res += "" if omit_space else " "
            res += label_display

    return term(res)


def render_lit(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_lit("&lit", ["en", "foo", "bar"], defaultdict(str, {"nodot":"1"}))
    '<i>Used other than figuratively or idiomatically:</i> see <i>foo, bar</i>'
    >>> render_lit("&lit", ["en", "foo", "bar"], defaultdict(str, {"qualifier":"often", "dot":"!"}))
    '<i>often used other than figuratively or idiomatically:</i> see <i>foo, bar!</i>'
    >>> render_lit("&lit", ["en", "foo", "bar", "toto"], defaultdict(str))
    '<i>Used other than figuratively or idiomatically:</i> see <i>foo, bar, toto.</i>'
    >>> render_lit("&lit", ["en", "see <b>foo</b> or <b>bar</b>"], defaultdict(str))
    '<i>Used other than figuratively or idiomatically:</i> <i>see <b>foo</b> or <b>bar</b>.</i>'
    """
    starter = "Used other than figuratively or idiomatically"
    if data["qualifier"]:
        phrase = f"{data['qualifier']} {starter.lower()}"
    else:
        phrase = starter
    parts.pop(0)  # language
    endphrase = ""
    if parts:
        phrase += ":"
        phrase = italic(phrase)
        # first is wikified ?
        phrase += " " if "</" in parts[0] else " see "
        endphrase += concat(parts, ", ")

    if data["dot"]:
        endphrase += data["dot"]
    elif data["nodot"] != "1":
        endphrase += "."
    phrase += italic(endphrase)
    return phrase


def render_morphology(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_morphology("affix", ["en"], defaultdict(str, {"alt1":"tisa-","pos1":"unique name","alt2":"-gen-", "t2": "transfer of genetic material (transduced)", "alt3":"-lec-", "t3":"selection and enrichment manipulation", "alt4":"-leu-", "t4":"leukocytes", "alt5":"-cel", "t5":"cellular therapy"}))
    '<i>tisa-</i> (unique name)&nbsp;+&nbsp;<i>-gen-</i> (“transfer of genetic material (transduced)”)&nbsp;+&nbsp;<i>-lec-</i> (“selection and enrichment manipulation”)&nbsp;+&nbsp;<i>-leu-</i> (“leukocytes”)&nbsp;+&nbsp;<i>-cel</i> (“cellular therapy”)'
    >>> render_morphology("affix", ["mul", "dys-", "schēma"], defaultdict(str, {"lang1":"NL.","t1":"difficult, impaired, abnormal, bad","lang2":"la", "g2": "f,n", "t2":"shape, form"}))
    'New Latin <i>dys-</i> (“difficult, impaired, abnormal, bad”)&nbsp;+&nbsp;Latin <i>schēma</i> <i>f or n</i> (“shape, form”)'
    >>> render_morphology("aff", ["en", "'gram<t:Instagram>", "-er<id:occupation>"], defaultdict(str))
    "<i>'gram</i> and <i>-er</i>"

    >>> render_morphology("suffix", ["en", "do", "ing"], defaultdict(str))
    '<i>do</i>&nbsp;+&nbsp;<i>-ing</i>'

    >>> render_morphology("prefix", ["en", "un", "do"], defaultdict(str))
    '<i>un-</i>&nbsp;+&nbsp;<i>do</i>'
    >>> render_morphology("prefix", ["en", "e-", "bus"], defaultdict(str))
    '<i>e-</i>&nbsp;+&nbsp;<i>bus</i>'
    >>> render_morphology("prefix", ["en", "toto", "lala" ], defaultdict(str, {"t1":"t1", "tr1":"tr1", "alt1":"alt1", "pos1":"pos1"}))
    '<i>alt1-</i> (<i>tr1-</i>, “t1”, pos1)&nbsp;+&nbsp;<i>lala</i>'
    >>> render_morphology("prefix", ["en", "toto", "lala"], defaultdict(str, {"t2":"t2", "tr2":"tr2", "alt2":"alt2", "pos2":"pos2"}))
    '<i>toto-</i>&nbsp;+&nbsp;<i>alt2</i> (<i>tr2</i>, “t2”, pos2)'
    >>> render_morphology("pre", ["en", "in", "fare#Etymology_1"], defaultdict(str))
    '<i>in-</i>&nbsp;+&nbsp;<i>fare</i>'

    >>> render_morphology("suffix", ["en", "gabapentin", "-oid"], defaultdict(str))
    '<i>gabapentin</i>&nbsp;+&nbsp;<i>-oid</i>'
    >>> render_morphology("suffix", ["en", "toto", "lala"], defaultdict(str, { "t1":"t1", "tr1":"tr1", "alt1":"alt1", "pos1":"pos1"}))
    '<i>alt1</i> (<i>tr1</i>, “t1”, pos1)&nbsp;+&nbsp;<i>-lala</i>'
    >>> render_morphology("suffix", ["en", "toto", "lala"], defaultdict(str, {"t2":"t2", "tr2":"tr2", "alt2":"alt2", "pos2":"pos2"}))
    '<i>toto</i>&nbsp;+&nbsp;<i>-alt2</i> (<i>-tr2</i>, “t2”, pos2)'
    >>> render_morphology("suffix", ["en", "", "cide"], defaultdict(str))
    '&nbsp;+&nbsp;<i>-cide</i>'

    >>> render_morphology("confix", ["en", "neuro", "genic"], defaultdict(str))
    '<i>neuro-</i>&nbsp;+&nbsp;<i>-genic</i>'
    >>> render_morphology("confix", ["en", "neuro", "gene"], defaultdict(str,{"tr2":"genic"}))
    '<i>neuro-</i>&nbsp;+&nbsp;<i>-gene</i> (<i>-genic</i>)'
    >>> render_morphology("confix", ["en", "be", "dew", "ed"], defaultdict(str))
    '<i>be-</i>&nbsp;+&nbsp;<i>dew</i>&nbsp;+&nbsp;<i>-ed</i>'
    >>> render_morphology("confix", ["en", "i-", "-tard"], defaultdict(str))
    '<i>i-</i>&nbsp;+&nbsp;<i>-tard</i>'

    >>> render_morphology("compound", ["fy", "fier", "lj"], defaultdict(str, {"t1":"far", "t2":"leap", "pos1":"adj", "pos2":"v"}))
    '<i>fier</i> (“far”, adj)&nbsp;+&nbsp;<i>lj</i> (“leap”, v)'
    >>> render_morphology("compound", ["en", "en:where", "as"], defaultdict(str, {"gloss2":"that"}))
    'English <i>where</i>&nbsp;+&nbsp;<i>as</i> (“that”)'
    >>> render_morphology("com+", ["en", "where", "as"], defaultdict(str, {"gloss2":"that"}))
    'Compound of <i>where</i>&nbsp;+&nbsp;<i>as</i> (“that”)'

    >>> render_morphology("blend", ["he", "תַּשְׁבֵּץ", "חֵץ"], defaultdict(str, {"tr1":"tashbéts", "t1":"crossword", "t2":"arrow", "tr2":"chets"}))
    'Blend of <i>תַּשְׁבֵּץ</i> (<i>tashbéts</i>, “crossword”)&nbsp;+&nbsp;<i>חֵץ</i> (<i>chets</i>, “arrow”)'
    >>> render_morphology("blend", ["en"], defaultdict(str))
    'Blend'
    >>> render_morphology("blend", ["en", "scratch", "bill", ""], defaultdict(str, {"notext":"1", "t1":"money", "alt2":"bills"}))
    '<i>scratch</i> (“money”)&nbsp;+&nbsp;<i>bills</i>'
    >>> render_morphology("blend of", ["en", "extrasolar", "solar system"], defaultdict(str))
    'Blend of <i>extrasolar</i>&nbsp;+&nbsp;<i>solar system</i>'
    >>> render_morphology("blend", [], defaultdict(str, {"notext": "1", "1": "en", "2": "yarb", "3": "balls"}))
    '<i>yarb</i>&nbsp;+&nbsp;<i>balls</i>'

    >>> render_morphology("doublet", ["en" , "fire"], defaultdict(str))
    'Doublet of <i>fire</i>'
    >>> render_morphology("doublet", ["es" , "directo"], defaultdict(str, {"notext":"1"}))
    '<i>directo</i>'
    >>> render_morphology("doublet", ["en" , "advoke", "avouch", "avow"], defaultdict(str))
    'Doublet of <i>advoke</i>, <i>avouch</i> and <i>avow</i>'
    >>> render_morphology("doublet", ["ja", "モスコー"], defaultdict(str, {"tr1":"Mosukō", "nocap":"1"}))
    'doublet of <i>モスコー</i> (<i>Mosukō</i>)'
    >>> render_morphology("doublet", ["ja" , "ヴィエンヌ", "ウィーン"], defaultdict(str, {"tr1":"Viennu", "t1":"Vienne", "tr2":"Wīn"}))
    'Doublet of <i>ヴィエンヌ</i> (<i>Viennu</i>, “Vienne”) and <i>ウィーン</i> (<i>Wīn</i>)'
    >>> render_morphology("dbt", ["ru" , "ру́сский"], defaultdict(str, {"tr1":"rúkij", "t1":"R", "g1":"m", "pos1":"n", "lit1":"R"}))
    'Doublet of <i>ру́сский</i> <i>m</i> (<i>rúkij</i>, “R”, n, literally “R”)'
    """

    def add_dash(tpl: str, index: int, parts_count: int, chunk: str) -> str:
        if tpl in {"pre", "prefix", "con", "confix"} and i == 1:
            # remove trailing dashes
            chunk = re.sub(r"^([^-]*)-+$", r"\g<1>", chunk)
            chunk += "-"
        if tpl in {"suf", "suffix"} and i == 2:
            chunk = re.sub(r"^-+([^-]*)$", r"\g<1>", chunk)
            chunk = f"-{chunk}"
        if tpl in {"con", "confix"} and i == parts_count:
            chunk = re.sub(r"^-+([^-]*)$", r"\g<1>", chunk)
            chunk = f"-{chunk}"
        return chunk

    if not parts:
        return f"{italic(data['2'])}&nbsp;+&nbsp;{italic(data['3'])}"

    for idx in range(len(parts)):
        part = parts[idx]
        if "<" in part:
            parts[idx] = part.split("<", 1)[0]

    compound = [
        "af",
        "affix",
        "pre",
        "prefix",
        "suf",
        "suffix",
        "con",
        "confix",
        "com",
        "com+",
        "compound",
        "blend",
        "blend of",
    ]
    # Aliases
    if tpl == "dbt":
        tpl = "doublet"
    with_start_text = ["doublet", "piecewise doublet", "blend", "blend of"]
    parts.pop(0)  # language code
    phrase = "Compound of " if tpl == "com+" else ""
    if data["notext"] != "1" and tpl in with_start_text:
        starter = tpl
        if parts:
            starter += " " if tpl.endswith(" of") else " of "
        phrase = starter if data["nocap"] else starter.capitalize()
    a_phrase = []

    i = 1
    parsed_parts = []
    while True:
        p_dic = defaultdict(str)
        si = str(i)
        chunk = parts.pop(0) if parts else ""
        chunk = chunk.split("#")[0] if chunk else ""
        chunk = data[f"alt{si}"] or chunk
        p_dic["chunk"] = chunk
        p_dic["g"] = gender_number_specs(gender) if (gender := data[f"g{si}"]) else ""
        p_dic["tr"] = data[f"tr{si}"]
        p_dic["t"] = data[f"t{si}"] or data[f"gloss{si}"]
        p_dic["pos"] = data[f"pos{si}"]
        p_dic["lit"] = data[f"lit{si}"]
        p_dic["lang"] = data[f"lang{si}"]
        if ":" in chunk:
            lang, chunk = chunk.split(":", 1)
            p_dic["chunk"] = chunk
            p_dic["lang"] = lang
        if not chunk and not p_dic["tr"] and not p_dic["ts"] and not parts:
            break
        else:
            parsed_parts.append(p_dic)
        i += 1

    parts_count = len(parsed_parts)
    i = 1
    while parsed_parts:
        c = parsed_parts.pop(0)
        chunk = c["chunk"]
        chunk = add_dash(tpl, i, parts_count, chunk)
        if chunk:
            chunk = italic(chunk)
        if lang := c["lang"]:
            chunk = f"{langs.get(lang, lang)} {chunk}"
        if c["g"]:
            chunk += " " + c["g"]
        local_phrase = []
        if c["tr"]:
            result = c["tr"]
            result = add_dash(tpl, i, parts_count, result)
            local_phrase.append(italic(result))
        if c["t"]:
            local_phrase.append(f"{'“' + c['t'] + '”'}")
        if c["pos"]:
            local_phrase.append(c["pos"])
        if c["lit"]:
            local_phrase.append(f"{'literally “' + c['lit'] + '”'}")
        if local_phrase:
            chunk += " (" + concat(local_phrase, ", ") + ")"
        a_phrase.append(chunk)
        i += 1

    sep = ", "
    last_sep = " and "
    if tpl in compound:
        sep = "&nbsp;+&nbsp;"
        last_sep = sep

    phrase += concat(a_phrase, sep, last_sep=last_sep)

    # special case : {{suffix|en||cide}}
    if tpl in {"suf", "suffix"} and "&nbsp;+&nbsp;" not in phrase:
        phrase = f"&nbsp;+&nbsp;{phrase}"

    return phrase


def _render_morse_code(part: str, data: defaultdict[str, str], suffix: str) -> str:
    text = f"{italic(f'Visual rendering of Morse code {suffix}')} {strong(part)}"
    if gloss := data["gloss"]:
        text += f" (“{gloss}”)"
    return f"{text}."


def render_morse_code_abbreviation(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_morse_code_abbreviation("morse code abbreviation", ["AGN"], defaultdict(str))
    '<i>Visual rendering of Morse code abbreviation</i> <b>AGN</b>.'
    """
    return _render_morse_code(parts[0], data, "abbreviation")


def render_morse_code_for(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_morse_code_for("morse code for", ["M"], defaultdict(str))
    '<i>Visual rendering of Morse code for</i> <b>M</b>.'
    >>> render_morse_code_for("morse code for", ["="], defaultdict(str, {"gloss": "equal sign"}))
    '<i>Visual rendering of Morse code for</i> <b>=</b> (“equal sign”).'
    """
    return _render_morse_code(parts[0], data, "for")


def render_morse_code_prosign(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_morse_code_prosign("morse code prosign", ["SOS"], defaultdict(str))
    '<i>Visual rendering of Morse code prosign</i> <b>SOS</b>.'
    """
    return _render_morse_code(parts[0], data, "prosign")


def render_mul_cjk_stroke_def(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_mul_cjk_stroke_def("mul-cjk stroke-def", ["p"], defaultdict(str))
    '(<i>Chinese calligraphy</i>) The stroke {{m|mul|撇||left-falling}}.'
    >>> render_mul_cjk_stroke_def("mul-cjk stroke-def", ["h", "z", "t"], defaultdict(str))
    '(<i>Chinese calligraphy</i>) The stroke combination {{m|mul|橫||horizontal}} + {{m|mul|折||bent}} + {{m|mul|提||rising}}.'
    """
    # Source: https://en.wiktionary.org/w/index.php?title=Template:mul-cjk_stroke-def/char_def&oldid=40839292
    strokes = {
        "b": "{{m|mul|扁||flat}}",
        "d": "{{m|mul|點||dot}}",
        "g": "{{m|mul|鉤||hook}}",
        "h": "{{m|mul|橫||horizontal}}",
        "n": "{{m|mul|捺||right-falling}}",
        "p": "{{m|mul|撇||left-falling}}",
        "q": "{{m|mul|圈||circle}}",
        "s": "{{m|mul|豎||vertical}}",
        "t": "{{m|mul|提||rising}}",
        "w": "{{m|mul|彎||curved}}",
        "x": "{{m|mul|斜||slant}}",
        "z": "{{m|mul|折||bent}}",
    }

    text = "(<i>Chinese calligraphy</i>) The stroke "
    if len(parts) > 1:
        text += "combination "
    text += concat([strokes[part] for part in parts], " + ")
    return f"{text}."


def render_name_translit(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_name_translit("name translit", ["en", "ka", "შევარდნაძე"], defaultdict(str, {"type":"surname"}))
    '<i>A transliteration of the Georgian surname</i> <b>შევარდნაძე</b>'
    >>> render_name_translit("name translit", ["en", "fa", "فرید<tr:farid>"], defaultdict(str, {"type":"male given name"}))
    '<i>A transliteration of the Persian male given name</i> <b>فرید</b> (<i>farid</i>)'
    >>> render_name_translit("name translit", ["en", "ru", "Ива́нович<t:son of Ivan>"], defaultdict(str, {"type":"patronymic"}))
    '<i>A transliteration of the Russian patronymic</i> <b>Ива́нович</b> (<i>Ivanovič</i>, “<i>son of Ivan</i>”)'
    >>> render_name_translit("name translit", ["pt", "bg", "Ива́нов", "Ивано́в"], defaultdict(str, {"type":"surname"}))
    '<i>A transliteration of the Bulgarian surname</i> <b>Ива́нов</b> (<i>Ivanov</i>) <i>or</i> <b>Ивано́в</b> (<i>Ivanov</i>)'
    >>> render_name_translit("name translit", ["en", "el", "Γιάννης<eq:John>"], defaultdict(str, {"type":"male given name"}))
    '<i>A transliteration of the Greek male given name</i> <b>Γιάννης</b>, <i>equivalent to John</i>'
    >>> render_name_translit("name translit", ["fr", "ja"], defaultdict(str, {"type":"female given name"}))
    '<i>A transliteration of a Japanese female given name</i>'
    >>> render_name_translit("name translit", ["en", "bg,mk,sh", "Никола"], defaultdict(str, {"type":"male given name", "eq": "Nicholas"}))
    '<i>A transliteration of the Bulgarian, Macedonian or Serbo-Croatian male given name</i> <b>Никола</b> (<i>Nikola</i>), <i>equivalent to Nicholas</i>'
    >>> render_name_translit("name translit", ["en", "bg, mk,  sh ", "Никола"], defaultdict(str, {"type":"male given name", "eq": "Nicholas"}))
    '<i>A transliteration of the Bulgarian, Macedonian or Serbo-Croatian male given name</i> <b>Никола</b> (<i>Nikola</i>), <i>equivalent to Nicholas</i>'
    """
    parts.pop(0)  # Destination language
    src_langs = parts.pop(0)

    origins = concat([langs[src_lang.strip()] for src_lang in src_langs.split(",")], sep=", ", last_sep=" or ")
    text = italic(f"A transliteration of {'the' if parts else 'a'} {origins} {data['type']}")
    if not parts:
        return text

    what, rest = parts.pop(0), ""
    if "<" in what:
        what, rest = what.split("<", 1)

    transliterated = transliterate(src_langs.split(",", 1)[0], what)
    text += f" {strong(what)}"

    if rest:
        if transliterated:
            transliterated = f"{italic(transliterated)}, "

        kind, value = rest.split(":", 1)
        value = value.rstrip(">")
        match kind:
            case "eq":
                text += f", {italic(f'equivalent to {value}')}"
            case "t":
                text += f" ({transliterated}“{italic(value)}”)"
            case "tr":
                text += f" ({transliterated}{italic(value)})"
            case _:
                assert 0, f"Unhandled {kind=} in render_name_translit()"
    elif transliterated:
        text += f" ({italic(transliterated)})"

    if eq := data["eq"]:
        text += f", {italic(f'equivalent to {eq}')}"

    if parts:
        text += f" {italic('or')} {strong(parts[0])}"
        if transliterated:
            text += f" ({italic(transliterated)})"

    return text


def render_named_after(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_named_after("named-after", ["en", "Pierre Bézier"], defaultdict(str, {"nationality":"French", "occupation":"Renault engineer", "nocap":"1"}))
    'named after French Renault engineer Pierre Bézier'
    >>> render_named_after("named-after", ["en", "Bertrand Russell"], defaultdict(str, {"tr":"tr", "died":"1970", "born":"1872", "nat":"English", "occ":"mathematician", "occ2":"logician"}))
    'Named after English mathematician and logician Bertrand Russell (<i>tr</i>) (1872–1970)'
    >>> render_named_after("named-after", ["en", "Patrick Swayze"], defaultdict(str, {"alt":""}))
    'Patrick Swayze'
    >>> render_named_after("named-after", ["en"], defaultdict(str))
    'Named after an unknown person'
    """
    parts.pop(0)  # Remove the language
    p = parts.pop(0) if parts else ""
    p = p or "an unknown person"
    if "alt" in data:
        phrase = data["alt"]
    else:
        starter = "named after"
        phrase = starter if data["nocap"] else starter.capitalize()
        if data["nationality"]:
            phrase += f" {data['nationality']}"
        elif data["nat"]:
            phrase += f" {data['nat']}"
        if occ := join_names(data, "occ", " and ", include_langname=False, key_alias="occupation"):
            phrase += f" {occ}"
        phrase += " "
    phrase += f"{p}"
    if data["tr"]:
        phrase += f" ({italic(data['tr'])})"
    if data["died"] or data["born"]:
        phrase += f" ({data['born'] or '?'}–{data['died']})"
    return phrase


def render_nb(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_nb("...", [], defaultdict(str))
    ' […] '
    >>> render_nb("...", [], defaultdict(str, {"text":"etc."}))
    ' [etc.] '
    >>> render_nb("...", ["a"], defaultdict(str))
    ' [and the other form <i>a</i>] '
    >>> render_nb("...", ["a, b, c"], defaultdict(str))
    ' [and other forms <i>a, b, c</i>] '
    >>> render_nb("nb...", [], defaultdict(str))
    '&nbsp;[…]'
    >>> render_nb("nb...", [], defaultdict(str, {"text":"etc."}))
    '&nbsp;[etc.]'
    >>> render_nb("nb...", ["a"], defaultdict(str))
    '&nbsp;[and the other form <i>a</i>]'
    >>> render_nb("nb...", ["a, b, c"], defaultdict(str))
    '&nbsp;[and other forms <i>a, b, c</i>]'
    """
    sep = " " if tpl == "..." else "&nbsp;"
    phrase = f"{sep}["
    if not parts:
        phrase += data["text"] or "…"
    else:
        phrase += "and other forms " if "," in parts[0] else "and the other form "
        phrase += italic(parts[0])
    return f"{phrase}]{sep if tpl == '...' else ''}"


def render_nuclide(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_nuclide("nuclide", ["2", "1", "H"], defaultdict(str))
    '<sup>2</sup><sub style="margin-left:-1ex;">1</sub>H'
    >>> render_nuclide("nuclide", ["222", "86", "Rn"], defaultdict(str))
    '<sup>222</sup><sub style="margin-left:-2.3ex;">86</sub>Rn'
    >>> render_nuclide("nuclide", ["270", "108", "Hs"], defaultdict(str))
    '<sup>270</sup><sub style="margin-left:-3.5ex;">108</sub>Hs'
    """
    phrase = superscript(parts[0])
    sub_n = int(parts[1])
    if sub_n < 10:
        phrase += f'<sub style="margin-left:-1ex;">{sub_n}</sub>'
    elif sub_n < 100:
        phrase += f'<sub style="margin-left:-2.3ex;">{sub_n}</sub>'
    else:
        phrase += f'<sub style="margin-left:-3.5ex;">{sub_n}</sub>'
    phrase += parts[2]
    return phrase


def render_och_l(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_och_l("och-l", ["覺"], defaultdict(str))
    '覺 (OC)'
    >>> render_och_l("och-l", ["覺", "to awake, get insight"], defaultdict(str))
    '覺 (OC, “to awake, get insight”)'
    """
    # TODO: should be improved with transliteration
    text = f"{parts.pop(0)} (OC"
    if parts:
        text += f", “{parts[0]}”"
    return f"{text})"


def render_only_used_in(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_only_used_in("only used in", ["en", "Alexandrian limp"], defaultdict(str))
    '<i>Only used in</i> <b>Alexandrian limp</b>'
    >>> render_only_used_in("only used in", ["en", "Alexandrian limp"], defaultdict(str, {"t": "foo"}))
    '<i>Only used in</i> <b>Alexandrian limp</b> (“foo”)'
    """
    text = f"<i>Only used in</i> <b>{parts[-1]}</b>"
    if t := data["t"]:
        text += f" (“{t}”)"
    return text


def render_onomatopoeic(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_onomatopoeic("onom", ["en"], defaultdict(str))
    'Onomatopoeic'
    >>> render_onomatopoeic("onom", ["en"], defaultdict(str, {"nocap": "1"}))
    'onomatopoeic'
    >>> render_onomatopoeic("onom", ["en"], defaultdict(str, {"title": "imitative"}))
    'imitative'
    >>> render_onomatopoeic("onom", ["en"], defaultdict(str, {"notext": "1"}))
    ''
    """
    return misc_variant_no_term("onomatopoeic", tpl, parts, data, word=word)


def render_pedlink(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_pedlink("pedlink", ["foo"], defaultdict(str))
    'foo'
    >>> render_pedlink("pedlink", ["foo"], defaultdict(str, {"disp": "bar"}))
    'bar'
    """
    return data["disp"] or parts[0]


def render_phonetic_alphabet(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_phonetic_alphabet("phonetic-alphabet", ["A"], defaultdict(str, {"NATO/ICAO": "1", "ITU/IMO": "1"}))
    '{{lb|mul|international standards}} <i>NATO, ICAO, ITU & IMO radiotelephony clear code (spelling-alphabet name) for the letter</i> <b>A</b>.'
    """
    standards: list[str] = []
    if data["NATO/ICAO"]:
        standards.extend(("NATO", "ICAO"))
    if data["ITU/IMO"]:
        standards.extend(("ITU", "IMO"))
    standards_str = concat(standards, ", ", last_sep=" & ")

    label = "{{lb|mul|international standards}}"
    ng = f"{standards_str} radiotelephony clear code (spelling-alphabet name)"

    if data["word"]:
        for_what = ""
    elif data["num"]:
        for_what = "the digit"
    else:
        for_what = "the letter"

    return f"{label} <i>{ng} for {for_what}</i> <b>{parts[0]}</b>."


def render_place(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_place("place", ["en", "A country in the Middle East"], defaultdict(str))
    'A country in the Middle East'
    >>> render_place("place", ["en", "A country"], defaultdict(str, {"modern":"Iraq"}))
    'A country; modern Iraq'
    >>> render_place("place", ["en", "island", "regency/Pandeglang", "province/Banten", "c/Indonesia"], defaultdict(str))
    'An island of Pandeglang, Banten, Indonesia'
    >>> render_place("place", ["en", "village", "co/Fulton County", "s/Illinois"], defaultdict(str))
    'A village in Fulton County, Illinois'
    >>> render_place("place", ["en", "village", "co/Fulton County", "s/Illinois"], defaultdict(str, {"a": "a"}))
    'a village in Fulton County, Illinois'
    >>> render_place("place", ["en", "city/county seat", "co/Lamar County", "s/Texas"], defaultdict(str))
    'A city, the county seat of Lamar County, Texas'
    >>> render_place("place", ["en", "small town/and/unincorporated community"], defaultdict(str))
    'A small town and unincorporated community'
    >>> render_place("place", ["en", "town", "s/New York", ";", "named after Paris"], defaultdict(str))
    'A town in New York; named after Paris'
    >>> render_place("place", ["en", "s"], defaultdict(str))
    'A state'
    >>> render_place("place", ["en", "state", "overseas territory/United States Virgin Islands"], defaultdict(str))
    'A state of the United States Virgin Islands'
    >>> render_place("place", ["en", "state", "administrative region/Réunion"], defaultdict(str))
    'A state of the Réunion region'
    >>> render_place("place", ["en", "state", "c/USA"], defaultdict(str))
    'A state of the United States'
    >>> render_place("place", ["en", "city", "c/Republic of Ireland"], defaultdict(str))
    'A city in Republic of Ireland'
    >>> render_place("place", ["en", "city", "s/Georgia", "c/United States"], defaultdict(str))
    'A city in Georgia, United States'
    >>> render_place("place", ["en", "river", "in", "England", ", forming the boundary between", "co/Derbyshire", "and", "co/Staffordshire"], defaultdict(str))
    'A river in England, forming the boundary between Derbyshire and Staffordshire'
    >>> render_place("place", ["en", "barangay", "mun/Hilongos", "p/Leyte", "c/Philippines"], defaultdict(str))
    'A barangay of Hilongos, Leyte, Philippines'
    >>> render_place("place", ["en", "hamlet", "par/South Leigh and High Cogges", "dist/West Oxfordshire", "co/Oxfordshire", "cc/England"], defaultdict(str))
    'A hamlet in South Leigh and High Cogges parish, West Oxfordshire district, Oxfordshire, England'
    >>> render_place("place", ["en", "village/and/cpar", "in", "uauth/Central Bedfordshire", "co/Bedfordshire", "cc/England"], defaultdict(str))
    'A village and civil parish in  Central Bedfordshire district, Bedfordshire, England'
    >>> render_place("place", ["en", "prefecture", "c/Japan"], defaultdict(str, {"capital": "Mito"}))
    'A prefecture of Japan. Capital: Mito'
    >>> render_place("place", ["en", "suburban area", "in", "par/New Milton", "dist/New Forest", "co/Hampshire", "cc/England", "formerly a village named", "x/Milton"], defaultdict(str))
    'A suburban area in  New Milton parish, New Forest district, Hampshire, England, formerly a village named Milton'
    >>> render_place("place", ["en", "The capital city of <<s/South Carolina>>, and the county seat of <<co/Richland County>>"], defaultdict(str))
    'The capital city of South Carolina, and the county seat of Richland County'
    """
    parts.pop(0)  # Remove the language
    parts = [re.sub(r"<<(?:[^/>]+)/([^>]+)>>", r"\1", part) for part in parts]
    phrase = ""
    i = 1
    previous_rawpart = False
    last = next((part for part in parts[::-1] if "/" not in part), "")
    while parts:
        si = str(i)
        part = parts.pop(0)
        subparts = part.split("/")
        if part in ("in", "and"):
            phrase += f" {part}"
            phrase += " " if part == "in" else ""
            previous_rawpart = True
        elif i == 1:
            no_article = False
            for j, subpart in enumerate(subparts):
                if subpart == "and":
                    phrase = f"{phrase[:-2]} and"
                    no_article = True
                    continue
                subpart = placetypes_aliases.get(subpart, subpart)
                s = recognized_placetypes.get(subpart, {})
                qualifier = ""
                if not s:
                    q_array = subpart.split(" ")
                    qualifier = q_array[0]
                    if qualifier in recognized_qualifiers:
                        qualifier = recognized_qualifiers[qualifier]
                        subpart = " ".join(q_array[1:])
                    else:
                        qualifier = ""
                    subpart = placetypes_aliases.get(subpart, subpart)
                    s = recognized_placetypes.get(subpart, {})
                if s:
                    if not (preposition := s.get("preposition")):
                        s_fallback = recognized_placetypes.get(s["fallback"], {})
                        preposition = s_fallback.get("preposition")
                    if j == 0:
                        article = data["a"] or s["article"].title()
                    else:
                        article = "" if no_article else s["article"]
                    phrase += article
                    phrase += f" {qualifier}" if qualifier else ""
                    phrase += " " + s["display"]
                    no_article = False
                    if j == len(subparts) - 1:
                        phrase += f" {preposition or 'in'} " if parts and parts[0] != "in" else ""
                    else:
                        phrase += ", "
                else:
                    phrase += part
        elif len(subparts) > 1:
            phrase += ", " if i > 2 and not previous_rawpart else ""
            phrase += " " if previous_rawpart else ""
            kind, *places = subparts
            place = "/".join(places)
            kind = placetypes_aliases.get(kind, kind)
            placename_key = f"{kind}/{place}"
            is_administrative = "administrative" in kind
            if is_administrative:
                phrase += "the "
            if recognized_placename := recognized_placenames.get(placename_key):
                if i < 3 and (article := recognized_placename["article"]):
                    phrase += f"{article} "
                phrase += recognized_placename["display"]
            else:
                phrase += place
            if is_administrative:
                phrase += f" {kind.split(' ')[-1]}"
            elif kind in {"department", "district", "parish"}:
                phrase += f" {kind}"
            elif kind == "unitary authority":
                phrase += " district"
        elif part == ";":
            phrase += "; "
        else:
            if part == last and not phrase.endswith(("; ", ", ")):
                phrase += ", "
            phrase += part

        modern_key = "modern" + "" if i == 1 else si
        if data[modern_key]:
            phrase += f"; modern {data[modern_key]}"
        previous_rawpart = len(subparts) == 1 and i > 1
        i += 1

    if capital := data["capital"]:
        phrase += f". Capital: {capital}"

    return phrase


def render_si_unit(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_si_unit("SI-unit", ["en", "peta", "second", "time"], defaultdict(str))
    '(<i>metrology</i>) An SI unit of time equal to 10<sup>15</sup> seconds. Symbol: Ps'
    >>> render_si_unit("SI-unit-np", ["en", "nano", "gauss", "magnetism"], defaultdict(str))
    '(<i>metrology</i>) An SI unit of magnetism equal to 10<sup>-9</sup> gauss.'
    >>> render_si_unit("SI-unit", ["en", "peta", "second"], defaultdict(str))
    '(<i>metrology</i>) An SI unit of time equal to 10<sup>15</sup> seconds. Symbol: Ps'
    """
    parts.pop(0)  # language
    prefix = data["2"] or (parts.pop(0) if parts else "")
    unit = data["3"] or (parts.pop(0) if parts else "")
    category = data["4"] or (parts.pop(0) if parts else "") or unit_to_type.get(unit, "")
    exp = prefix_to_exp.get(prefix, "")
    s_end = "" if unit.endswith("z") or unit.endswith("s") else "s"
    phrase = f"({italic('metrology')}) An SI unit of {category} equal to 10{superscript(exp)} {unit}{s_end}."
    if unit in unit_to_symbol:
        symbol = prefix_to_symbol.get(prefix, "") + unit_to_symbol.get(unit, "")
        phrase += f" Symbol: {symbol}"
    return phrase


def render_si_unit_2(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_si_unit_2("SI-unit-2", ["peta", "meter", "length", "metre"], defaultdict(str))
    '(<i>metrology</i>) An SI unit of length equal to 10<sup>15</sup> meters; alternative spelling of <i>petametre</i>.'
    """
    prefix = data["1"] or (parts.pop(0) if parts else "")
    unit = data["2"] or (parts.pop(0) if parts else "")
    category = data["3"] or (parts.pop(0) if parts else "")
    alt = data["3"] or (parts.pop(0) if parts else "")
    exp = prefix_to_exp.get(prefix, "")
    return f"({italic('metrology')}) An SI unit of {category} equal to 10{superscript(exp)} {unit}s; alternative spelling of {italic(prefix + alt)}."


def render_si_unit_abb(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_si_unit_abb("SI-unit-abb", ["femto", "mole", "amount of substance"], defaultdict(str))
    '(<i>metrology</i>) <i>Symbol for</i> <b>femtomole</b>, an SI unit of amount of substance equal to 10<sup>-15</sup> moles'
    >>> render_si_unit_abb("SI-unit-abbnp", ["exa", "hertz", "frequency"], defaultdict(str))
    '(<i>metrology</i>) <i>Symbol for</i> <b>exahertz</b>, an SI unit of frequency equal to 10<sup>18</sup> hertz'
    """
    prefix = data["1"] or (parts.pop(0) if parts else "")
    unit = data["2"] or (parts.pop(0) if parts else "")
    category = data["3"] or (parts.pop(0) if parts else "")
    exp = prefix_to_exp.get(prefix, "")
    plural = "" if tpl.endswith("np") else "s"
    return f"({italic('metrology')}) {italic('Symbol for')} {strong(prefix + unit)}, an SI unit of {category} equal to 10{superscript(exp)} {unit}{plural}"


def render_si_unit_abb2(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_si_unit_abb2("SI-unit-abb2", ["exa", "liter", "litre", "fluid measure"], defaultdict(str))
    '(<i>metrology</i>) <i>Symbol for</i> <b>exaliter</b> (<i>exalitre</i>), an SI unit of fluid measure equal to 10<sup>18</sup> liters (<i>litres</i>).'
    """
    prefix = data["1"] or (parts.pop(0) if parts else "")
    unit = data["2"] or (parts.pop(0) if parts else "")
    kind = data["3"] or (parts.pop(0) if parts else "")
    category = data["4"] or (parts.pop(0) if parts else "")
    match prefix:
        case "quecto":
            exp = "&minus;30"
        case "ronto":
            exp = "&minus;27"
        case "yocto":
            exp = "&minus;24"
        case "zepto":
            exp = "&minus;21"
        case "atto":
            exp = "&minus;18"
        case "femto":
            exp = "&minus;15"
        case "pico":
            exp = "&minus;12"
        case "nano":
            exp = "&minus;9"
        case "micro":
            exp = "&minus;6"
        case "milli":
            exp = "&minus;3"
        case "centi":
            exp = "&minus;2"
        case "deci":
            exp = "&minus;1"
        case "deca":
            exp = "1"
        case "hecto":
            exp = "2"
        case "kilo":
            exp = "3"
        case "mega":
            exp = "6"
        case "giga":
            exp = "9"
        case "tera":
            exp = "12"
        case "peta":
            exp = "15"
        case "exa":
            exp = "18"
        case "zetta":
            exp = "21"
        case "yotta":
            exp = "24"
        case "ronna":
            exp = "27"
        case "quetta":
            exp = "30"
        case _:
            exp = "?"
    return f"({italic('metrology')}) {italic('Symbol for')} {strong(prefix + unit)} ({italic(prefix + kind)}), an SI unit of {category} equal to 10{superscript(exp)} {unit}s (<i>{kind}s</i>)."


def render_spelling_pronunciation(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_spelling_pronunciation("spelling pronunciation", ["en"], defaultdict(str))
    'Spelling pronunciation'
    >>> render_spelling_pronunciation("spelling pronunciation", ["en"], defaultdict(str, {"title": "Title"}))
    'Title'
    >>> render_spelling_pronunciation("spelling pronunciation", ["en"], defaultdict(str, {"nocap": "1"}))
    'spelling pronunciation'
    """
    if data["notext"]:
        return ""
    text = data["title"] or tpl
    return text if data["nocap"] else capitalize(text)


def render_surface_analysis(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_surface_analysis("surf", ["en", "ignore", "-ance"], defaultdict(str))
    'By surface analysis, <i>ignore</i>&nbsp;+&nbsp;<i>-ance</i>'
    """
    phrase = ("b" if data["nocap"] in ("1", "yes", "y") else "B") + "y surface analysis, "
    phrase += render_morphology("af", parts, data)
    return phrase


def render_surname(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_surname("surname", ["en"], defaultdict(str))
    '<i>A surname</i>'
    >>> render_surname("surname", [], defaultdict(str, {"lang": "en"}))
    '<i>A surname</i>'
    >>> render_surname("surname", ["en", ""], defaultdict(str))
    '<i>A surname</i>'
    >>> render_surname("surname", ["en", "rare"], defaultdict(str))
    '<i>A rare surname</i>'
    >>> render_surname("surname", ["en", "English"], defaultdict(str))
    '<i>An English surname</i>'
    >>> render_surname("surname", ["en", "occupational"], defaultdict(str, {"A":"An"}))
    '<i>An occupational surname</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"Latin"}))
    '<i>A surname from Latin</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"surnames"}))
    '<i>A surname transferred from the surname</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"given names"}))
    '<i>A surname transferred from the given name</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"nicknames"}))
    '<i>A surname transferred from the nickname</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"place names"}))
    '<i>A surname transferred from the place name</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"common nouns"}))
    '<i>A surname transferred from the common noun</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"coinages"}))
    '<i>A surname originating as a coinage</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"matronymics"}))
    '<i>A surname originating as a matronymic</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"patronymics"}))
    '<i>A surname originating as a patronymic</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"ethnonyms"}))
    '<i>A surname originating as an ethnonym</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"occupations"}))
    '<i>A surname originating as an occupation</i>'
    """
    if parts:
        parts.pop(0)  # Remove the lang

    art = data["A"] or ("An" if parts and parts[0].lower().startswith(("a", "e", "i", "o", "u")) else "A")

    from_value, from_text = data["from"], ""
    if from_value in {
        "common nouns",
        "given names",
        "nicknames",
        "place names",
        "surnames",
    }:
        from_text = f" transferred from the {from_value[:-1]}"
    elif from_value in {"coinages", "matronymics", "patronymics"}:
        from_text = f" originating as a {from_value[:-1]}"
    elif from_value in {"ethnonyms", "occupations"}:
        from_text = f" originating as an {from_value[:-1]}"
    elif from_value == "the Bible":
        from_text = " originating from the Bible"
    elif from_value:
        from_text = f" from {from_value}"

    return italic(f"{art} {parts[0]} {tpl}{from_text}") if parts and parts[0] else italic(f"{art} {tpl}{from_text}")


def render_taxon(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_taxon("taxon", ["genus", "family", "Elephantidae"], defaultdict(str))
    'A taxonomic genus within the family Elephantidae.'
    >>> render_taxon("taxon", ["genus", "family", "Elephantidae", "mammoth"], defaultdict(str))
    'A taxonomic genus within the family Elephantidae&nbsp;– mammoth.'
    """
    text = f"A taxonomic {parts[0]} within the {parts[1]} {parts[2]}"
    if len(parts) > 3:
        text += f"&nbsp;– {parts[3]}"
    return f"{text}."


def render_transclude(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    This template is special as it needs to look for another word's specific definition (targeted with the `{{senseid}} template`).

    Single senseid case: https://en.wiktionary.org/wiki/Afrika
    Multiple senseid case: https://en.wiktionary.org/wiki/Macao
    No senseid case: https://en.wiktionary.org/wiki/Ionian_Sea
    """
    import subprocess

    from ... import render, utils

    source_dir = render.get_source_dir("en", "en")
    file = render.get_latest_json_file(source_dir)

    source = parts[1]
    sense_id = data["id"]
    definitions: list[str] = []

    for sid in sense_id.split(","):
        output = subprocess.check_output(
            ["/bin/fgrep", f'"{source}": "', str(file)],
            env={"LC_ALL": "C"},
            text=True,
            encoding="unicode_escape",
        )
        pattern = re.compile(
            rf"#\s*\{{\{{(?:senseid|sid)\|\w+\|{sid}\}}\}}\s*(.+)"
            if "{{senseid|" in output or "{{sid|" in output
            else r"#\s*(\{\{place\|.+)"
        )
        definition = next(line.strip() for line in output.splitlines() if pattern.search(line))
        definition = pattern.sub(r"\1", definition)

        # At this point, the definition is something like `{{place|...}}`, and if the `tcl=` arg is used, we need to alter template arguments
        if "tcl=" in definition:
            place_arg = re.search(r"\{\{place\|(\w+)", definition)[1]  # type: ignore[index]
            tcl_args = re.search(r"tcl=([^}]+)\}\}", definition)[1].split(";;")  # type: ignore[index]
            definition = f"{{{{place|{place_arg}|{'|'.join(tcl_args)}}}}}"

        definition = re.sub(r"<<\w+/([^>]+)>>", r"\1", definition)
        definition = utils.process_templates(word, definition, "en")
        definition = definition.split(".", 1)[0]
        definitions.append(definition)

    if parts[0] == "en":
        return "\n".join(definitions)

    return f"{source} ({'\n'.join(definitions)})"


def render_uncertain(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_uncertain("unc", ["en"], defaultdict(str))
    'Uncertain'
    >>> render_uncertain("uncertain", ["en"], defaultdict(str, {"nocap": "1"}))
    'uncertain'
    >>> render_uncertain("uncertain", ["en"], defaultdict(str, {"title": "Not certain"}))
    'Not certain'
    """
    return misc_variant_no_term("uncertain", tpl, parts, data, word=word)


def render_univerbation(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_univerbation("univerbation", ["en"], defaultdict(str, {"nocap": "1"}))
    'univerbation'
    >>> render_univerbation("univerbation", ["en", "be", "gone"], defaultdict(str))
    'Univerbation of <i>be</i> + <i>gone</i>'
    """
    text = ("u" if data["nocap"] == "1" else "U") + "niverbation"
    if words := [italic(p) for p in parts[1:]]:
        text += " of "
    return f"{text}{concat(words, sep=' + ')}"


def render_unknown(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_unknown("unk", ["en"], defaultdict(str, { "notext":"1", "nocap":"1"}))
    ''
    >>> render_unknown("unk", ["en"], defaultdict(str))
    'Unknown'
    >>> render_unknown("unk", ["en"], defaultdict(str, {"nocap":"1"}))
    'unknown'
    >>> render_unknown("unk", ["en"], defaultdict(str, {"title":"Uncertain"}))
    'Uncertain'
    """
    if data["notext"] == "1":
        return ""
    elif data["title"]:
        return data["title"]
    elif data["nocap"] == "1":
        return "unknown"
    else:
        return "Unknown"


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_variant("__variant__en-archaic third-person singular of", ["verb"], defaultdict(str))
    'verb'

    >>> render_variant("__variant__infl of", ["en", "human", "", "s-verb-form"], defaultdict(str), word="humans")
    'human'
    >>> render_variant("__variant__infl of", ["en", "human", "", "s-verb-form"], defaultdict(str, {"1": "en", "2": "human", "3": "", "4": "s-verb-form"}), word="humans")
    'human'

    >>> render_variant("__variant__plural of", ["en", "woman"], defaultdict(str), word="women")
    'woman'

    >>> render_variant("__variant__form of", ["en", "Alternative (anglicized) spelling", "Wrocław"], defaultdict(str), word="Wroclaw")
    'Wrocław'
    >>> render_variant("__variant__adj form of", ["en", "Alternative (anglicized) spelling", "Wrocław"], defaultdict(str), word="Wroclaw")
    'Alternative (anglicized) spelling'
    """
    if "en-archaic" in tpl:
        return parts[0]

    if "_form of" in tpl:
        return parts[-1]

    return data["2"] or parts[1]


def render_vern(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_vern("vern", ["Pacific cod"], defaultdict(str))
    'Pacific cod'
    >>> render_vern("vern", ["freshwater sculpin"], defaultdict(str, {"pl": "s"}))
    'freshwater sculpins'
    >>> render_vern("vern", ["freshwater sculpin", "freshwater sculpins"], defaultdict(str))
    'freshwater sculpins'
    """
    return parts[-1] + data["pl"]


def render_vi_l(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_vi_l("vi-l", ["bánh"], defaultdict(str))
    'bánh'
    >>> render_vi_l("vi-l", ["bánh", "𨋣"], defaultdict(str))
    'bánh (𨋣)'
    """
    text = parts.pop(0)
    if parts:
        text += f" ({parts[0]})"
    return text


template_mapping = {
    "&lit": render_lit,
    "...": render_nb,
    "a": render_accent,
    "accent": render_accent,
    "A.D.": render_bce,
    "AD": render_bce,
    "af": render_morphology,
    "affix": render_morphology,
    "aka": render_aka,
    "ante": render_dating,
    "ante2": render_ante2,
    "a.": render_dating,
    "backform": render_foreign_derivation,
    "backformation": render_foreign_derivation,
    "back-form": render_foreign_derivation,
    "back-formation": render_foreign_derivation,
    "B.C.E.": render_bce,
    "BCE": render_bce,
    "B.C.": render_bce,
    "BC": render_bce,
    "bf": render_foreign_derivation,
    "blend of": render_morphology,
    "blend": render_morphology,
    "bond credit rating": render_bond_credit_rating,
    "bor": render_foreign_derivation,
    "bor-lite": render_foreign_derivation,
    "bor+": render_foreign_derivation,
    "borrowed": render_foreign_derivation,
    "cal": render_foreign_derivation,
    "cap": render_cap,
    "calque": render_foreign_derivation,
    "century": render_century,
    "C.E.": render_bce,
    "CE": render_bce,
    "circa": render_dating,
    "c.": render_dating,
    "chemical symbol": render_chemical_symbol,
    "clip": render_clipping,
    "clipping": render_clipping,
    "clq": render_foreign_derivation,
    "cog": render_foreign_derivation,
    "cog-lite": render_foreign_derivation,
    "cognate": render_foreign_derivation,
    "coin": render_coinage,
    "coined": render_coinage,
    "coinage": render_coinage,
    "contr": render_contraction,
    "contraction": render_contraction,
    "com": render_morphology,
    "com+": render_morphology,
    "compound": render_morphology,
    "con": render_morphology,
    "confix": render_morphology,
    "Cyrl-def": render_cyrl_def,
    "dbt": render_morphology,
    "demonym-adj": render_demonym_adj,
    "demonym-noun": render_demonym_noun,
    "der": render_foreign_derivation,
    "der+": render_foreign_derivation,
    "der-lite": render_foreign_derivation,
    "derived": render_foreign_derivation,
    "deverbal": render_deverbal,
    "doublet": render_morphology,
    "etydate": render_etydate,
    "etyl": render_foreign_derivation,
    "fa sp": render_fa_sp,
    "filter-avoidance spelling of": render_fa_sp,
    "frac": render_frac,
    "given name": render_given_name,
    "Han simp": render_han_simp,
    "he-l": render_he_l,
    "he-m": render_he_m,
    "historical given name": render_historical_given_name,
    "ic": render_ipa_char,
    "IPAchar": render_ipa_char,
    "ipachar": render_ipa_char,
    "ISO 216": render_iso_216,
    "ISO 217": render_iso_217,
    "ISO 269": render_iso_216,
    "ISO 639": render_iso_639,
    "ISO 3166": render_iso_3166,
    "ISO 4217": render_iso_4217,
    "inh": render_foreign_derivation,
    "inh-lite": render_foreign_derivation,
    "inh+": render_foreign_derivation,
    "inherited": render_foreign_derivation,
    "ja-l": render_ja_l,
    "ja-r": render_ja_r,
    "ko-inline": render_ko_inline,
    "ko-l": render_ko_inline,
    "l": render_foreign_derivation,
    "l-lite": render_foreign_derivation,
    "label": render_label,
    "langname-mention": render_foreign_derivation,
    "Latn-def": render_latn_def,
    "Latn-def-lite": render_latn_def,
    "lb": render_label,
    "lbl": render_label,
    "lbor": render_foreign_derivation,
    "learned borrowing": render_foreign_derivation,
    "link": render_foreign_derivation,
    "ll": render_foreign_derivation,
    "ltc-l": render_ltc_l,
    "m": render_foreign_derivation,
    "m+": render_foreign_derivation,
    "m-lite": render_foreign_derivation,
    "mention": render_foreign_derivation,
    "morse code abbreviation": render_morse_code_abbreviation,
    "morse code for": render_morse_code_for,
    "morse code prosign": render_morse_code_prosign,
    "mul-cjk stroke-def": render_mul_cjk_stroke_def,
    "name translit": render_name_translit,
    "named-after": render_named_after,
    "nb...": render_nb,
    "nc": render_foreign_derivation,
    "ncog": render_foreign_derivation,
    "noncog": render_foreign_derivation,
    "noncognate": render_foreign_derivation,
    "nuclide": render_nuclide,
    "obor": render_foreign_derivation,
    "och-l": render_och_l,
    "only in": render_only_used_in,
    "only used in": render_only_used_in,
    "onom": render_onomatopoeic,
    "onomatopeic": render_onomatopoeic,
    "onomatopoeia": render_onomatopoeic,
    "onomatopoeic": render_onomatopoeic,
    "orthographic borrowing": render_foreign_derivation,
    "partial calque": render_foreign_derivation,
    "pcal": render_foreign_derivation,
    "pedlink": render_pedlink,
    "phonetic alphabet": render_phonetic_alphabet,
    "phono-semantic matching": render_foreign_derivation,
    "piecewise doublet": render_morphology,
    "piecewise_doublet": render_morphology,
    "place": render_place,
    "post": render_dating,
    "p.": render_dating,
    "pre": render_morphology,
    "prefix": render_morphology,
    "psm": render_foreign_derivation,
    "semantic loan": render_foreign_derivation,
    "semi-learned borrowing": render_foreign_derivation,
    "SI-unit": render_si_unit,
    "SI-unit-2": render_si_unit_2,
    "SI-unit-abb": render_si_unit_abb,
    "SI-unit-abb2": render_si_unit_abb2,
    "SI-unit-abbnp": render_si_unit_abb,
    "SI-unit-np": render_si_unit,
    "sl": render_foreign_derivation,
    "slbor": render_foreign_derivation,
    "spelling pronunciation": render_spelling_pronunciation,
    "suf": render_morphology,
    "suffix": render_morphology,
    "surf": render_surface_analysis,
    "surface analysis": render_surface_analysis,
    "surface etymology": render_surface_analysis,
    "surname": render_surname,
    "taxon": render_taxon,
    "tcl": render_transclude,
    "term-label": render_label,
    "tlb": render_label,
    "transclude": render_transclude,
    "translit": render_foreign_derivation,
    "transliteration": render_foreign_derivation,
    "U": render_cap,
    "ubor": render_foreign_derivation,
    "uder": render_foreign_derivation,
    "unadapted borrowing": render_foreign_derivation,
    "unc": render_uncertain,
    "uncertain": render_uncertain,
    "univ": render_univerbation,
    "univerbation": render_univerbation,
    "unk": render_unknown,
    "unknown": render_unknown,
    "vern": render_vern,
    "vernacular": render_vern,
    "vi-l": render_vi_l,
    #
    # Variants
    #
    "__variant__active participle of": render_variant,
    "__variant__adj form of": render_variant,
    "__variant__agent noun of": render_variant,
    "__variant__an of": render_variant,
    "__variant__alternative plural of": render_variant,
    "__variant__female equivalent of": render_variant,
    "__variant__feminine equivalent of": render_variant,
    "__variant__femeq": render_variant,
    "__variant__feminine of": render_variant,
    "__variant__feminine plural of": render_variant,
    "__variant__feminine plural past participle of": render_variant,
    "__variant__feminine singular of": render_variant,
    "__variant__feminine singular past participle of": render_variant,
    "__variant__form of": render_variant,
    "__variant__gerund of": render_variant,
    "__variant__imperfective form of": render_variant,
    "__variant__inflection of": render_variant,
    "__variant__infl of": render_variant,
    "__variant__masculine plural of": render_variant,
    "__variant__masculine plural past participle of": render_variant,
    "__variant__neuter plural of": render_variant,
    "__variant__neuter singular past participle of": render_variant,
    "__variant__noun form of": render_variant,
    "__variant__participle of": render_variant,
    "__variant__passive of": render_variant,
    "__variant__passive participle of": render_variant,
    "__variant__past participle form of": render_variant,
    "__variant__past participle of": render_variant,
    "__variant__perfective form of": render_variant,
    "__variant__plural of": render_variant,
    "__variant__plural": render_variant,
    "__variant__present participle of": render_variant,
    "__variant__reflexive of": render_variant,
    "__variant__verbal noun of": render_variant,
    "__variant__verb form of": render_variant,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
