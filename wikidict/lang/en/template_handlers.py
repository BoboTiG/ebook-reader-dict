from collections import defaultdict  # noqa
from typing import Tuple, Dict, List, TypedDict

from .labels import label_syntaxes
from .langs import langs
from .places import (
    recognized_placetypes,
    recognized_placenames,
    recognized_qualifiers,
    placetypes_aliases,
)
from .si_unit import unit_to_symbol, prefix_to_exp, prefix_to_symbol, unit_to_type
from .. import defaults
from ...transliterator import transliterate
from ...user_functions import (
    capitalize,
    concat,
    extract_keywords_from,
    italic,
    lookup_italic,
    small,
    strong,
    superscript,
    term,
)


def join_names(
    data: Dict[str, str],
    key: str,
    last_sep: str,
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
                if include_langname and ":" in var_text:
                    data_split = var_text.split(":")
                    text = langs[data_split[0]] + " " + data_split[1]
                    trans = transliterate(data_split[0], data_split[1])
                    if trans:
                        text += f" ({trans})"
                    var_a.append(text)
                else:
                    langnametext = "English " if include_langname else ""
                    var_a.append(langnametext + prefix + var_text + suffix)
    if var_a:
        return concat(var_a, ", ", last_sep)
    return ""


def gloss_tr_poss(data: Dict[str, str], gloss: str, trans: str = "") -> str:
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


def render_coinage(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_coinage("coin", ["en", "Josiah Willard Gibbs"], defaultdict(str))
    'Coined by Josiah Willard Gibbs'
    >>> render_coinage("coin", ["en", "Josiah Willard Gibbs"], defaultdict(str, {"in":"1881", "nat":"American", "occ":"scientist"}))
    'Coined by American scientist Josiah Willard Gibbs in 1881'
    >>> render_coinage("coin", ["en", "Josiah Willard Gibbs"], defaultdict(str, {"alt":"Josiah W. Gibbs", "nationality":"American", "occupation":"scientist"}))
    'Coined by American scientist Josiah W. Gibbs'
    >>> render_coinage("coin", [], defaultdict(str, {"1":"en", "2":"Charles Rice"}))
    'Coined by Charles Rice'
    """  # noqa
    if parts:
        parts.pop(0)  # Remove the language
    p = data["alt"] or data["2"] or (parts.pop(0) if parts else "unknown") or "unknown"
    phrase = ""
    if data["notext"] != "1":
        starter = "coined by"
        phrase = starter if data["nocap"] else starter.capitalize()
        if data["nationality"]:
            phrase += f" {data['nationality']}"
        elif data["nat"]:
            phrase += f" {data['nat']}"
        occ = join_names(data, "occ", " and ", False, "occupation")
        if occ:
            phrase += f" {occ}"
        phrase += " "
    phrase += f"{p}"
    if data["in"]:
        phrase += f' in {data["in"]}'
    return phrase


def render_bce(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_bce("B.C.E.", [], defaultdict(str))
    '<small>B.C.E.</small>'
    >>> render_bce("C.E.", [], defaultdict(str, {"nodot": "1"}))
    '<small>CE</small>'
    """
    nodot = data["nodot"] in ("1", "yes")
    text = "C.E." if tpl in {"C.E.", "CE", "A.D.", "AD"} else "B.C.E."
    return small(text.replace(".", "")) if nodot else small(text)


def render_dating(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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

    return italic(init) + f" {strong(start)}" + (f" {end}" if end else "") + ","


def render_foreign_derivation(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_foreign_derivation("bor", ["en", "ar", "الْعِرَاق", "", "Iraq"], defaultdict(str))
    'Arabic <i>الْعِرَاق</i> (<i>ālʿrāq</i>, “Iraq”)'
    >>> render_foreign_derivation("bor", [], defaultdict(str, {"1": "en", "2": "ja", "3": "マエバリ"}))
    'Japanese <i>マエバリ</i>'
    >>> render_foreign_derivation("der", ["en", "fro", "-"], defaultdict(str))
    'Old French'
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
    '<b>more</b>'
    >>> render_foreign_derivation("m", ["enm", "us"], defaultdict(str))
    '<i>us</i>'
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
    """  # noqa
    # Short path for the {{m|en|WORD}} template
    if tpl == "m" and len(parts) == 2 and parts[0] == "en" and not data:
        return strong(parts[1])

    mentions = (
        "back-formation",
        "back-form",
        "bf",
        "l",
        "link",
        "ll",
        "mention",
        "m",
    )
    dest_lang_ignore = (
        "cog",
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
    word = ""
    if data["notext"] != "1":
        if tpl in {"calque", "cal", "clq"}:
            starter = "calque of "
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
        elif tpl in {"back-formation", "back-form", "bf"}:
            starter = "back-formation"
            if parts:
                starter += " from"
        phrase = starter if data["nocap"] == "1" else starter.capitalize()

    lang = langs.get(dst_locale, "")
    phrase += lang if tpl not in mentions else ""

    if parts or data["3"]:
        word = parts.pop(0) if parts else data["3"]

    if word == "-":
        return phrase

    word = data["alt"] or word
    gloss = data["t"] or data["gloss"]

    if parts:
        word = parts.pop(0) or word  # 4, alt=

    if tpl in {"l", "link", "ll"}:
        phrase += f" {word}"
    elif word:
        phrase += f" {italic(word)}"
    if data["g"]:
        phrase += f' {italic(data["g"])}'
    trans = transliterate(dst_locale, word) if not data["tr"] else ""
    if parts:
        gloss = parts.pop(0)  # 5, t=, gloss=

    phrase += gloss_tr_poss(data, gloss, trans)

    return phrase.lstrip()


def render_frac(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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
        phrase = (
            f"<small><sup>{parts[0]}</sup><big>⁄</big><sub>{parts[1]}</sub></small>"
        )
    elif len(parts) == 1:
        phrase = f"<small><sup>1</sup><big>⁄</big><sub>{parts[0]}</sub></small>"
    return phrase


def render_given_name(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_given_name("given name", ["en" , "male"], defaultdict(str))
    '<i>A male given name</i>'
    >>> render_given_name("given name", ["en" , "male"], defaultdict(str, {"or":"female", "A":"A Japanese"}))
    '<i>A Japanese male or female given name</i>'
    >>> render_given_name("given name", ["en" , "male"], defaultdict(str, {"from":"Spanish", "from2":"Portuguese", "from3":"French"}))
    '<i>A male given name from Spanish, Portuguese or French</i>'
    >>> render_given_name("given name", ["en" , "male"], defaultdict(str, {"from":"la:Patricius", "fromt":"patrician"}))
    '<i>A male given name from Latin Patricius (“patrician”)</i>'
    >>> render_given_name("given name", ["en" , "female"], defaultdict(str, {"from":"place names", "usage":"modern", "var":"Savannah"}))
    '<i>A female given name transferred from the place name, of modern usage, variant of Savannah</i>'
    >>> render_given_name("given name", ["da" , "male"], defaultdict(str, {"eq":"Bertram", "eq2":"fr:Bertrand"}))
    '<i>A male given name, equivalent to English Bertram and French Bertrand</i>'
    >>> render_given_name("given name", ["en" , "female"], defaultdict(str, {"from":"Hebrew", "m":"Daniel", "f":"Daniela"}))
    '<i>A female given name from Hebrew, masculine equivalent Daniel, feminine equivalent Daniela</i>'
    >>> render_given_name("given name", ["lv" , "male"], defaultdict(str, {"from":"Slavic languages", "eq":"pl:Władysław", "eq2":"cs:Vladislav", "eq3":"ru:Владисла́в"}))
    '<i>A male given name from the Slavic languages, equivalent to Polish Władysław, Czech Vladislav and Russian Владисла́в (Vladislav)</i>'
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
    """  # noqa
    parts.pop(0)  # language
    gender = data["gender"] or (parts.pop(0) if parts else "")
    gender += f' or {data["or"]}' if data["or"] else ""
    art = data["A"] or "A"
    phrase = f"{art} "
    dimtext = join_names(data, "dim", " or ", False, "diminutive")
    phrase += "diminutive of the " if dimtext else ""
    phrase += f"{gender} given name"
    phrase += "s" if ", " in dimtext or " or " in dimtext else ""
    phrase += f" {dimtext}" if dimtext else ""

    class Seg(TypedDict, total=False):
        prefix: str
        suffixes: List[str]

    fromsegs: List[Seg] = []
    lastfrom_seg: Seg = {}
    for i in range(1, 10):
        from_key = f"from{i}" if i != 1 else "from"
        if data[from_key]:
            from_text = data[from_key]
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
                if ":" in from_text:
                    # todo fromalt
                    from_split = from_text.split(":")
                    suffix = langs[from_split[0]] + " " + from_split[1]
                    fromt_key = f"fromt{i}" if i != 1 else "fromt"
                    if data[fromt_key]:
                        suffix += f" (“{data[fromt_key]}”)"
                elif from_text.endswith("languages"):
                    suffix = "the " + from_text
                else:
                    suffix = from_text
            if lastfrom_seg and lastfrom_seg.get("prefix", "") != prefix:
                fromsegs.append(lastfrom_seg)
                lastfrom_seg = {}
            if not lastfrom_seg:
                lastfrom_seg = {"prefix": prefix, "suffixes": []}
            lastfrom_seg["suffixes"].append(suffix)
    if lastfrom_seg:
        fromsegs.append(lastfrom_seg)
    localphrase = [
        fromseg.get("prefix", "") + concat(fromseg.get("suffixes", []), ", ", " or ")
        for fromseg in fromsegs
    ]
    if localphrase:
        phrase += " " + concat(localphrase, ", ", " or ")

    meaningtext = join_names(data, "meaning", " or ", False, prefix='"', suffix='"')
    if meaningtext:
        phrase += ", meaning " + meaningtext

    if data["usage"]:
        phrase += ", of " + data["usage"] + " usage"

    vartext = join_names(data, "var", " or ")
    if vartext:
        phrase += ", variant of " + vartext
    mtext = join_names(data, "m", " and ")
    if mtext:
        phrase += ", masculine equivalent " + mtext
    ftext = join_names(data, "f", " and ")
    if ftext:
        phrase += ", feminine equivalent " + ftext
    eqext = join_names(data, "eq", " and ", True)
    if eqext:
        phrase += ", equivalent to " + eqext

    return italic(phrase)


def render_historical_given_name(
    tpl: str, parts: List[str], data: Dict[str, str]
) -> str:
    """
    >>> render_historical_given_name("historical given name", ["en" , "male", "Saint Abundius, an early Christian bishop"], defaultdict(str, {}))   # noqa
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


def render_label(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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
    '<i>(transitive, intransitive)</i>'
    >>> render_label("lbl", ["en" , "ambitransitive", "obsolete"], defaultdict(str))
    '<i>(transitive, intransitive, obsolete)</i>'
    >>> render_label("lbl", ["en" , "chiefly", "nautical"], defaultdict(str))
    '<i>(chiefly nautical)</i>'
    >>> render_label("lbl", ["en" , "", "nautical"], defaultdict(str))
    '<i>(nautical)</i>'
    """
    if len(parts) == 2:
        return term(lookup_italic(parts[1], "en"))
    res = ""
    omit_preComma = False
    omit_postComma = True
    omit_preSpace = False
    omit_postSpace = True

    for label in parts[1:]:
        omit_preComma = omit_postComma
        omit_postComma = False
        omit_preSpace = omit_postSpace
        omit_postSpace = False

        syntax = label_syntaxes.get(label)

        omit_comma = omit_preComma or (syntax["omit_preComma"] if syntax else False)
        omit_postComma = syntax["omit_postComma"] if syntax else False
        omit_space = omit_preSpace or (syntax["omit_preSpace"] if syntax else False)

        label_display = lookup_italic(label, "en")
        if label_display:
            if res:
                res += "" if omit_comma else ","
                res += "" if omit_space else " "
            res += label_display

    return term(res)


def render_lit(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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
        phrase = f'{data["qualifier"]} {starter.lower()}'
    else:
        phrase = starter
    parts.pop(0)  # language
    endphrase = ""
    if parts:
        phrase += ":"
        phrase = italic(phrase)
        # first is wikified ?
        phrase += " " if "</" in parts[0] else " see "
        endphrase += concat([p for p in parts], ", ")

    if data["dot"]:
        endphrase += data["dot"]
    elif data["nodot"] != "1":
        endphrase += "."
    phrase += italic(endphrase)
    return phrase


def render_morphology(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_morphology("affix", ["en"], defaultdict(str, {"alt1":"tisa-","pos1":"unique name","alt2":"-gen-", "t2": "transfer of genetic material (transduced)", "alt3":"-lec-", "t3":"selection and enrichment manipulation", "alt4":"-leu-", "t4":"leukocytes", "alt5":"-cel", "t5":"cellular therapy"}))
    '<i>tisa-</i> (unique name)&nbsp;+&nbsp;<i>-gen-</i> (“transfer of genetic material (transduced)”)&nbsp;+&nbsp;<i>-lec-</i> (“selection and enrichment manipulation”)&nbsp;+&nbsp;<i>-leu-</i> (“leukocytes”)&nbsp;+&nbsp;<i>-cel</i> (“cellular therapy”)'
    >>> render_morphology("suffix", ["en", "do", "ing"], defaultdict(str))
    '<i>do</i>&nbsp;+&nbsp;<i>-ing</i>'
    >>> render_morphology("prefix", ["en", "un", "do"], defaultdict(str))
    '<i>un-</i>&nbsp;+&nbsp;<i>do</i>'
    >>> render_morphology("pre", ["en", "in", "fare#Etymology_1"], defaultdict(str))
    '<i>in-</i>&nbsp;+&nbsp;<i>fare</i>'
    >>> render_morphology("suffix", ["en", "toto", "lala"], defaultdict(str, { "t1":"t1", "tr1":"tr1", "alt1":"alt1", "pos1":"pos1"}))
    '<i>alt1</i> (<i>tr1</i>, “t1”, pos1)&nbsp;+&nbsp;<i>-lala</i>'
    >>> render_morphology("prefix", ["en", "toto", "lala" ], defaultdict(str, {"t1":"t1", "tr1":"tr1", "alt1":"alt1", "pos1":"pos1"}))
    '<i>alt1-</i> (<i>tr1-</i>, “t1”, pos1)&nbsp;+&nbsp;<i>lala</i>'
    >>> render_morphology("suffix", ["en", "toto", "lala"], defaultdict(str, {"t2":"t2", "tr2":"tr2", "alt2":"alt2", "pos2":"pos2"}))
    '<i>toto</i>&nbsp;+&nbsp;<i>-alt2</i> (<i>-tr2</i>, “t2”, pos2)'
    >>> render_morphology("prefix", ["en", "toto", "lala"], defaultdict(str, {"t2":"t2", "tr2":"tr2", "alt2":"alt2", "pos2":"pos2"}))
    '<i>toto-</i>&nbsp;+&nbsp;<i>alt2</i> (<i>tr2</i>, “t2”, pos2)'
    >>> render_morphology("suffix", ["en", "", "cide"], defaultdict(str))
    '&nbsp;+&nbsp;<i>-cide</i>'
    >>> render_morphology("confix", ["en", "neuro", "genic"], defaultdict(str))
    '<i>neuro-</i>&nbsp;+&nbsp;<i>-genic</i>'
    >>> render_morphology("confix", ["en", "neuro", "gene"], defaultdict(str,{"tr2":"genic"}))
    '<i>neuro-</i>&nbsp;+&nbsp;<i>-gene</i> (<i>-genic</i>)'
    >>> render_morphology("confix", ["en", "be", "dew", "ed"], defaultdict(str))
    '<i>be-</i>&nbsp;+&nbsp;<i>dew</i>&nbsp;+&nbsp;<i>-ed</i>'
    >>> render_morphology("compound", ["fy", "fier", "lj"], defaultdict(str, {"t1":"far", "t2":"leap", "pos1":"adj", "pos2":"v"}))
    '<i>fier</i> (“far”, adj)&nbsp;+&nbsp;<i>lj</i> (“leap”, v)'
    >>> render_morphology("blend", ["he", "תַּשְׁבֵּץ", "חֵץ"], defaultdict(str, {"tr1":"tashbéts", "t1":"crossword", "t2":"arrow", "tr2":"chets"}))  # noqa
    'Blend of <i>תַּשְׁבֵּץ</i> (<i>tashbéts</i>, “crossword”)&nbsp;+&nbsp;<i>חֵץ</i> (<i>chets</i>, “arrow”)'
    >>> render_morphology("blend", ["en"], defaultdict(str))
    'Blend'
    >>> render_morphology("blend", ["en", "scratch", "bill", ""], defaultdict(str, {"notext":"1", "t1":"money", "alt2":"bills"}))
    '<i>scratch</i> (“money”)&nbsp;+&nbsp;<i>bills</i>'
    >>> render_morphology("blend of", ["en", "extrasolar", "solar system"], defaultdict(str))
    'Blend of <i>extrasolar</i>&nbsp;+&nbsp;<i>solar system</i>'

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
    >>> render_morphology("doublet", ["ru" , "ру́сский"], defaultdict(str, {"tr1":"rúkij", "t1":"R", "g1":"m", "pos1":"n", "lit1":"R"}))
    'Doublet of <i>ру́сский</i> <i>m</i> (<i>rúkij</i>, “R”, n, literally “R”)'
    """  # noqa

    def add_dash(tpl: str, index: int, parts_count: int, chunk: str) -> str:
        if tpl in {"pre", "prefix", "con", "confix"} and i == 1:
            chunk += "-"
        if tpl in {"suf", "suffix"} and i == 2:
            chunk = "-" + chunk
        if tpl in {"con", "confix"} and i == parts_count:
            chunk = "-" + chunk
        return chunk

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
        "compound",
        "blend",
        "blend of",
    ]
    with_start_text = ["doublet", "piecewise doublet", "blend", "blend of"]
    parts.pop(0)  # language code
    phrase = ""
    if data["notext"] != "1" and tpl in with_start_text:
        starter = tpl
        if parts:
            if not tpl.endswith(" of"):
                starter += " of "
            else:
                starter += " "
        phrase = starter if data["nocap"] else starter.capitalize()
    a_phrase = []

    i = 1
    parsed_parts = []
    keep_parsing = True
    while keep_parsing:
        p_dic = defaultdict(str)
        si = str(i)
        chunk = parts.pop(0) if parts else ""
        chunk = chunk.split("#")[0] if chunk else ""
        chunk = data["alt" + si] or chunk
        p_dic["chunk"] = chunk
        p_dic["g"] = data["g" + si]
        p_dic["tr"] = data["tr" + si]
        p_dic["t"] = data["t" + si]
        p_dic["pos"] = data["pos" + si]
        p_dic["lit"] = data["lit" + si]
        if not chunk and not p_dic["tr"] and not p_dic["ts"] and not parts:
            keep_parsing = False
        else:
            parsed_parts.append(p_dic)
        i = i + 1

    parts_count = len(parsed_parts)
    i = 1
    while parsed_parts:
        c = parsed_parts.pop(0)
        chunk = c["chunk"]
        chunk = add_dash(tpl, i, parts_count, chunk)
        if chunk:
            chunk = italic(chunk)
        if c["g"]:
            chunk += " " + italic(c["g"])
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

    phrase += concat(a_phrase, sep, last_sep)

    # special case : {{suffix|en||cide}}
    if tpl == "suffix" and "&nbsp;+&nbsp;" not in phrase:
        phrase = "&nbsp;+&nbsp;" + phrase

    return phrase


def render_named_after(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_named_after("named-after", ["en", "Pierre Bézier"], defaultdict(str, {"nationality":"French", "occupation":"Renault engineer", "nocap":"1"}))
    'named after French Renault engineer Pierre Bézier'
    >>> render_named_after("named-after", ["en", "Bertrand Russell"], defaultdict(str, {"tr":"tr", "died":"1970", "born":"1872", "nat":"English", "occ":"mathematician", "occ2":"logician"}))
    'Named after English mathematician and logician Bertrand Russell (<i>tr</i>) (1872–1970)'
    >>> render_named_after("named-after", ["en", "Patrick Swayze"], defaultdict(str, {"alt":""}))
    'Patrick Swayze'
    >>> render_named_after("named-after", ["en"], defaultdict(str))
    'Named after an unknown person'
    """  # noqa
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
        occ = join_names(data, "occ", " and ", False, "occupation")
        if occ:
            phrase += f" {occ}"
        phrase += " "
    phrase += f"{p}"
    if data["tr"]:
        phrase += f" ({italic(data['tr'])})"
    if data["died"] or data["born"]:
        phrase += f" ({data['born'] or '?'}–{data['died']})"
    return phrase


def render_nb(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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


def render_nuclide(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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


def render_place(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_place("place", ["en", "A country in the Middle East"], defaultdict(str))
    'A country in the Middle East'
    >>> render_place("place", ["en", "A country"], defaultdict(str, {"modern":"Iraq"}))
    'A country; modern Iraq'
    >>> render_place("place", ["en", "village", "co/Fulton County", "s/Illinois"], defaultdict(str))
    'A village in Fulton County, Illinois'
    >>> render_place("place", ["en", "city/county seat", "co/Lamar County", "s/Texas"], defaultdict(str))
    'A city, the county seat of Lamar County, Texas'
    >>> render_place("place", ["en", "small town/and/unincorporated community"], defaultdict(str))
    'A small town and unincorporated community'
    >>> render_place("place", ["en", "town", "s/New York", ";", "named after Paris"], defaultdict(str))
    'A town in New York; named after Paris'
    >>> render_place("place", ["en", "s"], defaultdict(str))
    'A state'
    >>> render_place("place", ["en", "state", "c/USA"], defaultdict(str))
    'A state of the United States'
    >>> render_place("place", ["en", "city", "c/Republic of Ireland"], defaultdict(str))
    'A city in Ireland'
    >>> render_place("place", ["en", "city", "s/Georgia", "c/United States"], defaultdict(str))
    'A city in Georgia, United States'
    """
    parts.pop(0)  # Remove the language
    phrase = ""
    i = 1
    while parts:
        si = str(i)
        part = parts.pop(0)
        subparts = part.split("/")
        if i == 1:
            no_article = False
            for j, subpart in enumerate(subparts):
                if subpart == "and":
                    phrase = phrase[:-2] + " and"
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
                    phrase += "" if no_article else s["article"]
                    phrase += f" {qualifier}" if qualifier else ""
                    phrase += " " + s["display"]
                    no_article = False
                    if j == len(subparts) - 1:
                        phrase += f" {s['preposition']} " if parts else ""
                    else:
                        phrase += ", "
                else:
                    phrase += part
        elif len(subparts) > 1:
            phrase += ", " if i > 2 else ""
            subpart = subparts[0]
            subpart = placetypes_aliases.get(subpart, subpart)
            placename_key = subpart + "/" + subparts[1]
            placename = recognized_placenames.get(placename_key, {})
            if (
                placename
                and placename["display"]
                and placename["display"] in recognized_placenames
            ):
                placename_key = placename["display"]
                placename = recognized_placenames[placename_key]
            if placename:
                if placename["article"] and i < 3:
                    phrase += placename["article"] + " "
                if placename["display"]:
                    phrase += placename["display"].split("/")[1]
                else:
                    phrase += placename_key.split("/")[1]
            else:
                phrase += subparts[1]
        elif part == ";":
            phrase += "; "
        else:
            phrase += part

        modern_key = "modern" + "" if i == 1 else si
        if data[modern_key]:
            phrase += "; modern " + data[modern_key]
        i += 1
    return capitalize(phrase)


def render_si_unit(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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
    type = data["4"] or (parts.pop(0) if parts else "")
    if not type:
        type = unit_to_type.get(unit, "")
    exp = prefix_to_exp.get(prefix, "")
    s_end = "" if unit.endswith("z") or unit.endswith("s") else "s"
    phrase = f"({italic('metrology')}) An SI unit of {type} equal to 10{superscript(exp)} {unit}{s_end}."
    if unit in unit_to_symbol:
        symbol = prefix_to_symbol.get(prefix, "") + unit_to_symbol.get(unit, "")
        phrase += f" Symbol: {symbol}"
    return phrase


def render_si_unit_2(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_si_unit_2("SI-unit-2", ["peta", "meter", "length", "metre"], defaultdict(str))
    '(<i>metrology</i>) An SI unit of length equal to 10<sup>15</sup> meters; alternative spelling of <i>petametre</i>.'
    """
    prefix = data["1"] or (parts.pop(0) if parts else "")
    unit = data["2"] or (parts.pop(0) if parts else "")
    type = data["3"] or (parts.pop(0) if parts else "")
    alt = data["3"] or (parts.pop(0) if parts else "")
    exp = prefix_to_exp.get(prefix, "")
    return f"({italic('metrology')}) An SI unit of {type} equal to 10{superscript(exp)} {unit}s; alternative spelling of {italic(prefix+alt)}."  # noqa


def render_si_unit_abb(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_si_unit_abb("SI-unit-abb", ["femto", "mole", "amount of substance"], defaultdict(str))
    '(<i>metrology</i>) <i>Symbol for</i> <b>femtomole</b>, an SI unit of amount of substance equal to 10<sup>-15</sup> moles'
    """  # noqa
    prefix = data["1"] or (parts.pop(0) if parts else "")
    unit = data["2"] or (parts.pop(0) if parts else "")
    type = data["3"] or (parts.pop(0) if parts else "")
    exp = prefix_to_exp.get(prefix, "")
    return f"({italic('metrology')}) {italic('Symbol for')} {strong(prefix+unit)}, an SI unit of {type} equal to 10{superscript(exp)} {unit}s"  # noqa


def render_surname(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_surname("surname", ["en"], defaultdict(str))
    '<i>A surname.</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"nodot":"1"}))
    '<i>A surname</i>'
    >>> render_surname("surname", ["en", "rare"], defaultdict(str))
    '<i>A rare surname.</i>'
    >>> render_surname("surname", ["en", "occupational"], defaultdict(str, {"A":"An"}))
    '<i>An occupational surname.</i>'
    >>> render_surname("surname", ["en"], defaultdict(str, {"from":"Latin", "dot":","}))
    '<i>A surname, from Latin,</i>'
    """
    parts.pop(0)  # Remove the lang
    art = data["A"] or "A"
    dot = data["dot"] or ("" if data["nodot"] else ".")
    from_text = f", from {data['from']}" if data["from"] else ""
    if not parts:
        return italic(f"{art} {tpl}{from_text}{dot}")
    return italic(f"{art} {parts[0]} {tpl}{from_text}{dot}")


def render_unknown(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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


def render_vern(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_vern("vern", ["Pacific cod"], defaultdict(str))
    'Pacific cod'
    >>> render_vern("vern", ["freshwater sculpin"], defaultdict(str, {"pl": "s"}))
    'freshwater sculpins'
    >>> render_vern("vern", ["freshwater sculpin", "freshwater sculpins"], defaultdict(str))
    'freshwater sculpins'
    """
    return parts[-1] + data["pl"]


template_mapping = {
    "&lit": render_lit,
    "...": render_nb,
    "A.D.": render_bce,
    "AD": render_bce,
    "af": render_morphology,
    "affix": render_morphology,
    "ante": render_dating,
    "a.": render_dating,
    "back-form": render_foreign_derivation,
    "back-formation": render_foreign_derivation,
    "B.C.E.": render_bce,
    "BCE": render_bce,
    "B.C.": render_bce,
    "BC": render_bce,
    "bf": render_foreign_derivation,
    "blend of": render_morphology,
    "blend": render_morphology,
    "bor": render_foreign_derivation,
    "borrowed": render_foreign_derivation,
    "cal": render_foreign_derivation,
    "calque": render_foreign_derivation,
    "C.E.": render_bce,
    "CE": render_bce,
    "circa": render_dating,
    "c.": render_dating,
    "clq": render_foreign_derivation,
    "cog": render_foreign_derivation,
    "cognate": render_foreign_derivation,
    "coin": render_coinage,
    "coinage": render_coinage,
    "com": render_morphology,
    "compound": render_morphology,
    "con": render_morphology,
    "confix": render_morphology,
    "der": render_foreign_derivation,
    "derived": render_foreign_derivation,
    "doublet": render_morphology,
    "etyl": render_foreign_derivation,
    "frac": render_frac,
    "given name": render_given_name,
    "historical given name": render_historical_given_name,
    "inh": render_foreign_derivation,
    "inherited": render_foreign_derivation,
    "l": render_foreign_derivation,
    "label": render_label,
    "langname-mention": render_foreign_derivation,
    "lb": render_label,
    "lbl": render_label,
    "lbor": render_foreign_derivation,
    "learned borrowing": render_foreign_derivation,
    "link": render_foreign_derivation,
    "ll": render_foreign_derivation,
    "m": render_foreign_derivation,
    "m+": render_foreign_derivation,
    "mention": render_foreign_derivation,
    "named-after": render_named_after,
    "nb...": render_nb,
    "nc": render_foreign_derivation,
    "ncog": render_foreign_derivation,
    "noncog": render_foreign_derivation,
    "noncognate": render_foreign_derivation,
    "nuclide": render_nuclide,
    "obor": render_foreign_derivation,
    "orthographic borrowing": render_foreign_derivation,
    "partial calque": render_foreign_derivation,
    "pcal": render_foreign_derivation,
    "phono-semantic matching": render_foreign_derivation,
    "piecewise doublet": render_morphology,
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
    "SI-unit-np": render_si_unit,
    "sl": render_foreign_derivation,
    "slbor": render_foreign_derivation,
    "suf": render_morphology,
    "suffix": render_morphology,
    "surname": render_surname,
    "translit": render_foreign_derivation,
    "transliteration": render_foreign_derivation,
    "ubor": render_foreign_derivation,
    "unadapted borrowing": render_foreign_derivation,
    "unk": render_unknown,
    "unknown": render_unknown,
    "vern": render_vern,
    "vernacular": render_vern,
    "w": defaults.render_wikilink,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
