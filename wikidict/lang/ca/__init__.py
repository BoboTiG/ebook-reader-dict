"""Catalan language."""
from typing import Tuple

# Regex to find the pronunciation
pronunciation = r"{\s*ca-pron\s*\|(?:\s*or\s*=\s*)?/([^/\|]+)"

# Regex to find the genre
genre = r"{ca-\w+\|([fm]+)"

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{-ca-}}", "{{-mul-}}")
etyl_section = ["{{-etimologia-", "{{-etim-", "{{etim-lang"]
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

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = (
    # Ignore conjuged verbs
    "ca-forma-conj",
    "forma-conj",
    # Proper nouns
    "cognom",
    "prenom",
    # Ignore genres
    "forma-f",
    # Ignore plurals
    "forma-p",
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
    # {{doblet|ca|Castellar}}
    "doblet": "italic(parts[-1])",
    # {{e|la|lupus}}
    "e": "parts[2]",
    # {{forma-|abreujada|ca|bicicleta}}
    "forma-": "f\"{italic('forma ' + parts[1] + ' de')} {strong(parts[-1])}\"",
    # {{forma-a|ca|Beget}}
    "forma-a": "f\"{italic('forma alternativa de')} {strong(parts[2])}\"",
    # {{forma-pron|ca|estimar}}
    "forma-pron": "f\"{italic('forma pronominal de')} {strong(parts[2])}\"",
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
    # {{etim-s|ca|XIV}}
    "etim-s": "'segle ' + parts[2]",
}

# Templates that will be completed/replaced using custom style.
templates_other = {
    "m": "m.",
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["default-test-xyz"], "ca")
        '<i>(Default-test-xyz)</i>'

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
        >>> last_template_handler(["terme", "en", "[[cheap]] as [[chips]]", "lit=tant [[barat]] com les [[patates]]"], "ca") # noqa
        '<i>[[cheap]] as [[chips]]</i> (literalment «tant [[barat]] com les [[patates]]»)'

        >>> last_template_handler(["trad", "es", "manzana"], "ca")
        'manzana <sup>(es)</sup>'
        >>> last_template_handler(["trad", "es", "tr=manzana"], "ca")
        'manzana <sup>(es)</sup>'
        >>> last_template_handler(["trad", "sc=es", "manzana"], "ca")
        'manzana <sup>(es)</sup>'
    """
    from .langs import langs
    from .. import defaults
    from ...user_functions import (
        concat,
        extract_keywords_from,
        italic,
        strong,
        superscript,
    )

    tpl = template[0]
    parts = list(template[1:])
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
        if not toadd:
            return ""
        return f" ({concat(toadd, ', ')})"

    if tpl in ("etim-lang", "del-lang", "Del-lang"):
        if parts[0] in langs:
            if langs[parts[0]].startswith(("a", "i", "o", "u", "h")):
                phrase += "De l'"
            else:
                phrase += "Del "
            if tpl == "del-lang" and phrase:
                phrase = phrase.lower()
            phrase += f"{langs[parts[0]]}"
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

    if tpl == "terme":
        return f"{italic(parts[-1])}{parse_other_parameters()}"

    if tpl == "trad":
        src = data["sc"] or parts.pop(0)
        trans = data["tr"] or parts.pop(0)
        return f"{trans} {superscript('(' + src + ')')}"

    return defaults.last_template_handler(template, locale, word=word)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ca
release_description = """\
Les paraules compten: {words_count}
Abocador Viccionari: {dump_date}

Fitxers disponibles:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Actualitzat el {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Viccionari (ɔ) {year}"
