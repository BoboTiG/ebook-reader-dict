"""Catalan language."""
import re
from typing import List, Pattern, Tuple

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{-ca-}}", "{{-mul-}}")
etyl_section = ("{{-etimologia-", "{{-etim-", "{{etim-lang")
sections = (
    "Abreviatura",
    "Acrònim",
    "Adjectiu",
    "Adverbi",
    "Article",
    "Contracció",
    "Infix",
    "Interjecció",
    "Lletra",
    "Nom",
    "Numeral",
    "Prefix",
    "Preposició",
    "Pronom",
    "Sigles",
    "Sufix",
    "Símbol",
    "Verb",
    *etyl_section,
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    # Ignore conjuged verbs
    "ca-forma-conj",
    "forma-conj",
    # Proper nouns
    "cognom",
    "prenom",
    # Ignore genders
    "forma-f",
    # Ignore plurals
    "forma-p",
    # Quotes
    "ex-cit",
    "ex-us",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "categoritza",
    "catllengua",
    "manquen accepcions",
    "sense accepcions",
    "-etimologia-",
    "-etim-",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "alguerès-verb": "alguerès",
    "arcaic": "arcaisme",
    "fruits": "botànica",
    "plantes": "botànica",
    "valencià-verb": "valencià",
}

# Templates more complex to manage.
templates_multi = {
    # {{color|#E01010}}
    "color": "color(parts[1])",
    # {{def-meta|Utilitzat en l'expressió tros de quòniam.}}
    "def-meta": "italic(parts[-1])",
    # {{doblet|ca|Castellar}}
    "doblet": "italic(parts[-1])",
    # {{e|la|lupus}}
    "e": "parts[2]",
    # {{forma-|abreujada|ca|bicicleta}}
    "forma-": "f\"{italic('forma ' + parts[1] + ' de')} {strong(parts[-1])}\"",
    # {{forma-a|ca|Beget}}
    "forma-a": "f\"{italic('forma alternativa de')} {strong(parts[2])}\"",
    # {{forma-augm|ca|anticonstitucionalment}}
    "forma-augm": "f\"{italic('forma augmentativa de')} {strong(parts[2])}\"",
    # {{forma-dim|ca|amic}}
    "forma-dim": "f\"{italic('forma diminutiva de')} {strong(parts[2])}\"",
    # {{forma-inc|ca|garantir}}
    "forma-inc": "f\"{italic('forma incorrecta de')} {strong(parts[2])}\"",
    # {{forma-pron|ca|estimar}}
    "forma-pron": "f\"{italic('forma pronominal de')} {strong(parts[2])}\"",
    # {{forma-super|ca|alt}}
    "forma-super": "f\"{italic('forma superlativa de')} {strong(parts[2])}\"",
    # {{IPAchar|[θ]}}
    "IPAchar": "parts[-1]",
    # {{marca|ca|fruits}}
    # {{marca|ca|interrogatiu|condicional}}
    "marca": "term(lookup_italic(concat(parts, sep=', ', indexes=[2, 3, 4, 5], skip='_'), 'ca'))",
    # {{marca-nocat|ca|balear}}
    # {{marca-nocat|ca|occidental|balear}}
    "marca-nocat": "term(lookup_italic(concat(parts, sep=', ', indexes=[2, 3, 4, 5]), 'ca'))",
    # {{pron|hi|/baːzaːr/}}
    "pron": "', '.join(parts[2:])",
    # {{q|tenir bona planta}}
    "q": "term(parts[-1])",
    # {{sinònim|ca|aixecador}}
    "sinònim": "f\"{italic('Sinònim de')} {strong(parts[-1])}\"",
    # {{etim-s|ca|XIV}}
    "etim-s": "'segle ' + parts[2]",
}


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ca
release_description = """\
Les paraules compten: {words_count}
Abocador Viccionari: {dump_date}

Fitxers disponibles:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Actualitzat el {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Viccionari (ɔ) {year}"


def find_genders(
    code: str,
    pattern: Pattern[str] = re.compile(r"{ca-\w+\|([fm]+)"),
) -> List[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("{{ca-nom|m}}")
    ['m']
    >>> find_genders("{{ca-nom|m}} {{ca-nom|m}}")
    ['m']
    """
    matches: List[str] = []
    for match in pattern.findall(code):
        if match not in matches:
            matches.append(match)
    return matches


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(
        r"{\s*ca-pron\s*\|(?:q=\S*\|)?(?:\s*or\s*=\s*)?(/[^/]+/)"
    ),
) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{ca-pron|/as/}}")
    ['/as/']
    >>> find_pronunciations("{{ca-pron|or=/əɫ/}}")
    ['/əɫ/']
    >>> find_pronunciations("{{ca-pron|or=/əɫ/|occ=/eɫ/}}")
    ['/əɫ/']
    >>> find_pronunciations("{{ca-pron|q=àton|or=/əɫ/|occ=/eɫ/|rima=}}")
    ['/əɫ/']
    """
    return pattern.findall(code)


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["default-test-xyz"], "ca")
        '<i>(Default-test-xyz)</i>'

        >>> last_template_handler(["calc semàntic", "es", "ca", "pueblo"], "ca")
        'calc semàntic del castellà <i>pueblo</i>'

        >>> last_template_handler(["comp", "ca", "cap", "vespre"], "ca")
        '<i>cap</i> i <i>vespre</i>'
        >>> last_template_handler(["comp", "ca", "auto-", "retrat"], "ca")
        'prefix <i>auto-</i> i <i>retrat</i>'
        >>> last_template_handler(["comp", "ca", "a-", "-lèxia"], "ca")
        'prefix <i>a-</i> i el sufix <i>-lèxia</i>'
        >>> last_template_handler(["comp", "ca", "fred", "-ol-", "-ic"], "ca")
        "<i>fred</i>, l'infix <i>-ol-</i> i el sufix <i>-ic</i>"

        >>> last_template_handler(["epònim", "ca", "w=Niels Henrik Abel"], "ca")
        'Niels Henrik Abel'
        >>> last_template_handler(["epònim", "ca", "André-Marie Ampère", "w=Niels Henrik Abel"], "ca")
        'André-Marie Ampère'

        >>> last_template_handler(["etim-lang", "oc", "ca", "cabèco"], "ca")
        "De l'occità <i>cabèco</i>"
        >>> last_template_handler(["etim-lang", "la", "ca", "verba"], "ca")
        'Del llatí <i>verba</i>'
        >>> last_template_handler(["etim-lang", "en", "ca"], "ca")
        "De l'anglès"

        >>> last_template_handler(["del-lang", "la", "ca", "verba"], "ca")
        'del llatí <i>verba</i>'
        >>> last_template_handler(["Del-lang", "xib", "ca", "baitolo"], "ca")
        "De l'ibèric <i>baitolo</i>"

        >>> last_template_handler(["lleng", "la", "√ⵎⵣⵖ"], "ca")
        '√ⵎⵣⵖ'
        >>> last_template_handler(["lleng", "la", "tipus=terme", "Agnus Dei qui tollis peccata mundi..."], "ca")
        '<i>Agnus Dei qui tollis peccata mundi...</i>'
        >>> last_template_handler(["lleng", "la", "tipus=lema", "Agnus Dei qui tollis peccata mundi..."], "ca")
        '<b>Agnus Dei qui tollis peccata mundi...</b>'
        >>> last_template_handler(["lleng", "la", "tipus=negreta", "Agnus Dei qui tollis peccata mundi..."], "ca")
        '<b>Agnus Dei qui tollis peccata mundi...</b>'

        >>> last_template_handler(["terme", "it", "come"], "ca")
        '<i>come</i>'
        >>> last_template_handler(["terme", "ca", "seu", "el seu"], "ca")
        '<i>el seu</i>'
        >>> last_template_handler(["terme", "la", "diēs Iovis", "trad=dia de Júpiter"], "ca")
        '<i>diēs Iovis</i> («dia de Júpiter»)'
        >>> last_template_handler(["terme", "grc", "λόγος", "trans=lógos"], "ca")
        '<i>λόγος</i> (<i>lógos</i>)'
        >>> last_template_handler(["terme", "grc", "λόγος", "trans=lógos", "trad=paraula"], "ca")
        '<i>λόγος</i> (<i>lógos</i>, «paraula»)'
        >>> last_template_handler(["terme", "grc", "λόγος", "trans=lógos", "trad=paraula", "pos=gentilici"], "ca")
        '<i>λόγος</i> (<i>lógos</i>, «paraula», gentilici)'
        >>> last_template_handler(["term", "en", "[[cheap]] as [[chips]]", "lit=tant [[barat]] com les [[patates]]"], "ca") # noqa
        '<i>[[cheap]] as [[chips]]</i> (literalment «tant [[barat]] com les [[patates]]»)'

        >>> last_template_handler(["trad", "es", "manzana"], "ca")
        'manzana <sup>(es)</sup>'
        >>> last_template_handler(["trad", "es", "tr=manzana"], "ca")
        'manzana <sup>(es)</sup>'
        >>> last_template_handler(["trad", "sc=es", "manzana"], "ca")
        'manzana <sup>(es)</sup>'
    """
    from ...user_functions import (
        concat,
        extract_keywords_from,
        italic,
        strong,
        superscript,
    )
    from .. import defaults
    from .langs import langs

    tpl, *parts = template
    data = extract_keywords_from(parts)
    phrase = ""

    def parse_other_parameters() -> str:
        toadd = []
        if data["trans"]:
            toadd.append(italic(data["trans"]))
        if data["trad"]:
            toadd.append(f"«{data['trad']}»")
        if data["pos"]:
            toadd.append(data["pos"])
        if data["lit"]:
            toadd.append(f"literalment «{data['lit']}»")
        return f" ({concat(toadd, ', ')})" if toadd else ""

    if tpl == "calc semàntic":
        phrase = "calc semàntic "
        lang = langs[parts[0]]
        phrase += "de l'" if lang.startswith(("a", "i", "o", "u", "h")) else "del "
        phrase += f"{lang} "
        phrase += f"{italic(parts[-1])}{parse_other_parameters()}"
        return phrase

    if tpl == "comp":

        def value(word: str) -> str:
            prefix = ""
            if word.startswith("-"):
                prefix = "l'infix " if word.endswith("-") else "el sufix "
            elif word.endswith("-"):
                prefix = "prefix "
            return f"{prefix}{italic(word)}"

        parts.pop(0)  # Remove the lang
        word1 = parts.pop(0)
        word2 = parts.pop(0)
        word3 = parts.pop(0) if parts else ""
        if word3:
            return f"{italic(word1)}, {value(word2)} i {value(word3)}"
        return f"{value(word1)} i {value(word2)}"

    if tpl == "epònim":
        return parts[1] if len(parts) > 1 else (data["w"] if "w" in data else "")

    if tpl in ("etim-lang", "del-lang", "Del-lang"):
        if parts[0] in langs:
            lang = langs[parts[0]]
            phrase += "De l'" if lang.startswith(("a", "i", "o", "u", "h")) else "Del "
            if tpl == "del-lang" and phrase:
                phrase = phrase.lower()
            phrase += f"{lang}"
            if len(parts) > 2:
                phrase += f" {italic(parts[2])}"
        phrase += parse_other_parameters()
        return phrase

    if tpl == "lleng":
        phrase = parts[-1]
        if data["tipus"] == "terme":
            phrase = italic(phrase)
        elif data["tipus"] in ("lema", "negreta"):
            phrase = strong(phrase)
        return phrase

    if tpl in ("m", "terme", "term", "calc"):
        return f"{italic(parts[-1])}{parse_other_parameters()}"

    if tpl == "trad":
        src = data["sc"] or parts.pop(0)
        trans = data["tr"] or parts.pop(0)
        return f"{trans} {superscript(f'({src})')}"

    return defaults.last_template_handler(template, locale, word=word)
