from collections import defaultdict

from ...user_functions import concat, extract_keywords_from, italic, strong, term
from . import general
from .labels import label_syntaxes, labels
from .langs import langs
from .transliterator import transliterate


def parse_index_parameters(word: str, data: defaultdict[str, str], i: int) -> str:
    toadd = []

    if tr := data.get(f"tr{i}", ""):
        toadd.append(italic(tr))
    elif word and (tr := transliterate(data["lang1"], word)):
        toadd.append(italic(tr))

    if t := data.get(f"t{i}", ""):
        toadd.append(f"«{t}»")
    if pos := data.get(f"pos{i}", ""):
        toadd.append(pos)
    if lit := data.get(f"lit{i}", ""):
        toadd.append(f"literalment «{lit}»")

    return f" ({concat(toadd, ', ')})" if toadd else ""


def render_cognom(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_cognom("cognom", [], defaultdict(str))
    '<i>Cognom</i>'
    >>> render_cognom("cognom", ["en", "patronímic"], defaultdict(str))
    '<i>Cognom d’origen patronímic</i>'
    >>> render_cognom("cognom", ["es"], defaultdict(str, {"eq": "Llopis"}))
    '<i>Cognom, equivalent al català Llopis.</i>'
    >>> render_cognom("cognom", ["es"], defaultdict(str, {"eq": "Llopis", "punt": ","}))
    '<i>Cognom, equivalent al català Llopis,</i>'
    """
    phrase = tpl.title()
    if len(parts) > 1:
        phrase += f" d’origen {parts[-1]}"
    if eq := data["eq"]:
        phrase += f", equivalent al català {eq}"
        phrase += data["punt"] or "."
    return italic(phrase)


def render_comp(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_comp("comp", ["ca", "cap", "vespre"], defaultdict(str))
    '<i>cap</i> i <i>vespre</i>'
    >>> render_comp("comp", ["ca", "auto-", "retrat"], defaultdict(str))
    'prefix <i>auto-</i> i <i>retrat</i>'
    >>> render_comp("comp", ["ca", "a-", "-lèxia"], defaultdict(str))
    'prefix <i>a-</i> i el sufix <i>-lèxia</i>'
    >>> render_comp("comp", ["ca", "fred", "-ol-", "-ic"], defaultdict(str))
    "<i>fred</i>, l'infix <i>-ol-</i> i el sufix <i>-ic</i>"
    >>> render_comp("comp", ["ca", "argila", "+ar"], defaultdict(str))
    '<i>argila</i> i la desinència <i>-ar</i>'
    >>> render_comp("comp", ["ca", "xocar", "+Ø"], defaultdict(str))
    '<i>xocar</i> i la desinència <i>Ø</i>'
    >>> render_comp("comp", ["ca", "metro-", "-nom"], defaultdict(str, {"t1": "mesura"}))
    'prefix <i>metro-</i> («mesura») i el sufix <i>-nom</i>'
    >>> render_comp("comp", ["ca", "mini-", "pequenas"], defaultdict(str, {"lang2": "es", "t2": "PIMER"}))
    'prefix <i>mini-</i> i el castellà <i>pequenas</i> («PIMER»)'
    >>> render_comp("comp", ["ca", "Birma", "-ia"], defaultdict(str, {"lang1": "en"}))
    'anglès <i>Birma</i> i el sufix <i>-ia</i>'
    >>> render_comp("comp", ["ca", "a-", "casa", "-at"], defaultdict(str, {"lang1": "en"}))
    'prefix <i>a-</i>, <i>casa</i> i el sufix <i>-at</i>'
    >>> render_comp("comp", ["ca", "germen", "-al"], defaultdict(str, {"alt1": "germen, -inis", "lang1": "la"}))
    'llatí <i>germen, -inis</i> i el sufix <i>-al</i>'
    >>> render_comp("comp", ["ca", "germen", "-al"], defaultdict(str, {"alt2": "-al, -inis", "lang1": "la"}))
    'llatí <i>germen</i> i el sufix <i>-al, -inis</i>'
    >>> render_comp("comp", ["ca", "κώδεια", "-ina"], defaultdict(str, {"lang1": "grc", "t1": "calze de la rosella"}))
    'grec antic <i>κώδεια</i> (<i>kṓdeia</i>, «calze de la rosella») i el sufix <i>-ina</i>'
    >>> render_comp("comp", ["ca", "glico-", "raqui-", "-ia"], defaultdict(str))
    'prefix <i>glico-</i>, el prefix <i>raqui-</i> i el sufix <i>-ia</i>'
    """

    prefix_count = 0

    def value(word: str, *, standalone: bool = False) -> str:
        nonlocal prefix_count
        prefix_count += 1

        prefix = ""
        if word.startswith("-"):
            if standalone:
                prefix = "infix " if word.endswith("-") else "sufix "
            else:
                prefix = "l'infix " if word.endswith("-") else "el sufix "
        elif word.endswith("-"):
            prefix = "prefix " if prefix_count == 1 else "el prefix "
        elif word.startswith("+"):
            prefix = "desinència " if standalone else "la desinència "
            if any(x in word for x in ["Ø", "0", "∅", "⌀", "ø"]):
                word = "Ø"
            word = word.replace("+", "-")

        return f"{prefix}{italic(word)}"

    parts.pop(0)  # Remove the lang

    word1 = data["alt1"] or parts[0]
    parts.pop(0)
    if not parts:
        phrase = value(word1, standalone=True)
        if others := parse_index_parameters(word1, data, 1):
            phrase += others
        return phrase

    word2 = data["alt2"] or parts[0]
    parts.pop(0)
    if not parts:
        phrase = ""
        if lang1 := data["lang1"]:
            phrase = f"{langs[lang1]} "
        phrase += value(word1)
        if others := parse_index_parameters(word1, data, 1):
            phrase += others
        if lang2 := data["lang2"]:
            lang = langs[lang2]
            phrase += " i l'" if general.cal_apostrofar(lang) else " i el "
            phrase += f"{lang} {value(word2)}"
        else:
            phrase += f" i {value(word2)}"
        if others2 := parse_index_parameters("", data, 2):
            phrase += others2
        return phrase

    word3 = parts.pop(0) if parts else ""
    phrase = value(word1)
    if others := parse_index_parameters(word1, data, 1):
        phrase += others
    phrase += f", {value(word2)}"
    if others2 := parse_index_parameters("", data, 2):
        phrase += others2
    phrase += f" i {value(word3)}"
    if others3 := parse_index_parameters("", data, 3):
        phrase += others3

    return phrase


def render_g(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_g("g", ["m"], defaultdict(str))
    'm.'
    >>> render_g("g", ["f-p"], defaultdict(str))
    'f. pl.'
    >>> render_g("g", ["m", "f"], defaultdict(str))
    'm., f.'
    >>> render_g("g", ["m", "f", "p"], defaultdict(str))
    'm., f., pl.'
    >>> render_g("g", ["m-p", "f-p"], defaultdict(str))
    'm. pl., f. pl.'
    """
    specs = {
        "?": "?",
        # Genders
        "m": "m.",
        "f": "f.",
        "c": "c.",
        "n": "n.",
        "i": "inv.",
        # Combined codes
        "mof": "m. o f.",
        "fom": "f. o m.",
        # Additional qualifiers
        "an": "anim.",
        "in": "inan.",
        "anml": "animal",  # ucraïnès, belarús, polonès
        "per": "pers.",  # ucraïnès, belarús, polonès
        "vir": "vir.",  # polonès
        "nv": "nvir.",  # polonès
        "loc": "loc.",
        # Numbers
        "s": "sing.",
        "d": "dual",
        "p": "pl.",
        "indef": "indef.",  # basc
        # Verbs
        "vt": "trans.",
        "vi": "intr.",
        "vp": "pron.",
        "va": "aux.",
        "vm": "impers.",
    }
    return concat(
        [f"{specs[part.split('-')[0]]} {specs[part.split('-')[1]]}" if "-" in part else specs[part] for part in parts],
        ", ",
    )


def render_grafia(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_grafia("grafia", ["ca", "obsoleta des del 2016", "adeu"], defaultdict(str))
    '<i>Grafia obsoleta des del 2016 de</i> adeu.'
    >>> render_grafia("grafia", ["ca", "obsoleta des del 2016", "adeu"], defaultdict(str, {"alt": "ade"}))
    '<i>Grafia obsoleta des del 2016 de</i> ade.'
    """
    result = "Grafia"
    parts.pop(0)
    text = parts.pop(0) if parts else ""
    w = parts.pop(0) if parts else ""
    result += f" {text}" if text else ""
    result += " de"
    result = italic(result)
    result += f" {data['alt']}." if data["alt"] else f" {w}."
    return result


def render_label(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_label("marca", ["ca", "castells"], defaultdict(str))
    '<i>(argot casteller)</i>'
    >>> render_label("marca", ["ca", "castells", ""], defaultdict(str))
    '<i>(argot casteller)</i>'
    >>> render_label("marca", ["ca", "medicina"], defaultdict(str))
    '<i>(medicina)</i>'
    >>> render_label("marca", ["ca", "neologisme", "humorístic", "i", "a vegades", "despectiu"], defaultdict(str))
    '<i>(neologisme, humorístic i a vegades, despectiu)</i>'
    >>> render_label("marca", ["ca", "pronominal", "valencià", "_", "col·loquial"], defaultdict(str))
    '<i>(pronominal, valencià col·loquial)</i>'
    """
    res = ""
    omit_preComma = False
    omit_postComma = True

    for label in parts[1:]:
        if not label:
            continue

        omit_preComma = omit_postComma
        omit_postComma = False

        syntax = label_syntaxes.get(label)
        omit_comma = omit_preComma or (syntax["omit_preComma"] if syntax else False)
        omit_postComma = syntax["omit_postComma"] if syntax else False

        if label_display := labels.get(label):
            if res:
                res += " " if omit_comma else ", "
            res += label_display
        elif label != "_":
            res += " " if omit_comma else ", "
            res += label

    return term(res.strip())


def render_sigles_de(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_sigles_de("sigles de", ["ca", "Organització del Tractat de l'Atlàntic Nord"], defaultdict(str))
    "<i>Sigles de</i> <b>Organització del Tractat de l'Atlàntic Nord</b>"
    >>> render_sigles_de("sigles de", ["ca", "North Atlantic Treaty Organization"], defaultdict(str, {"t": "OTAN"}))
    '<i>Sigles de</i> <b>North Atlantic Treaty Organization</b> («OTAN»)'
    """
    phrase = f"{italic('Sigles de')} {strong(parts[-1])}"
    if data["t"]:
        phrase += f" («{data['t']}»)"
    return phrase


template_mapping = {
    "cognom": render_cognom,
    "comp": render_comp,
    "g": render_g,
    "grafia": render_grafia,
    "marca": render_label,
    "marca-nocat": render_label,
    "sigles de": render_sigles_de,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
