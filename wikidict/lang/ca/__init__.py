"""Catalan language."""

import re

from ...user_functions import uniq
from .grc_trans import transliterate as transliterate_grc
from .ru_trans import transliterate as transliterate_ru

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

# Variants
variant_titles = (
    "Adjectiu",
    "Nom",
    "Verb",
)
variant_templates = (
    "{{ca-forma-conj",
    "{{forma-a",
    "{{forma-p",
    "{{forma-f",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    "forma-conj",
    "cognom",
    "prenom",
    "ex-cit",
    "ex-us",
    #
    # For variants
    #
    "ca-forma-conj",
    "forma-a",
    "forma-f",
    "forma-p",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "categoritza",
    "catllengua",
    "CN",
    "manquen accepcions",
    "sense accepcions",
    "-etimologia-",
    "-etim-",
)

# Templates more complex to manage.
templates_multi = {
    # {{AFI|/ˈwujt/}}
    "AFI": "parts[-1]",
    # {{ca-forma-conj|domdar|part|f|p}}
    "ca-forma-conj": "parts[1]",
    # {{claudàtors|[[milliarum]]}}
    "claudàtors": 'f"[{parts[1]}]"',
    # {{color|#E01010}}
    "color": "color(parts[1])",
    # {{def-meta|Utilitzat en l'expressió tros de quòniam.}}
    "def-meta": "italic(parts[-1])",
    # {{doblet|ca|Castellar}}
    "doblet": "italic(parts[-1])",
    # {{e-propi|ca|grèvol}}
    "e-propi": "strong(parts[-1])",
    # {{forma-a|ca|Bielorússia}}
    "forma-a": "parts[-1]",
    # {{forma-f|ca|halloweenià}}
    "forma-f": "parts[-1]",
    # {{forma-p|ca|experta}}
    "forma-p": "parts[-1]",
    # {{IPAchar|[θ]}}
    "IPAchar": "parts[-1]",
    # {{pron|hi|/baːzaːr/}}
    "pron": "', '.join(parts[2:])",
    # {{q|tenir bona planta}}
    "q": "term(concat(parts[1:], sep=', '))",
    # {{romanes|XIX}}
    "romanes": "small_caps(parts[-1].lower())",
    # {{etim-s|ca|XIV}}
    # {{etim-s|ca|XVII|1617}}
    "etim-s": "('segle ' + parts[2]) if len(parts) == 3 else parts[-1]",
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
"""

# Dictionary name that will be printed below each definition
wiktionary = "Viccionari (ɔ) {year}"


def find_genders(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"{ca-\w+\|([fm]+)"),
) -> list[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("{{ca-nom|m}}")
    ['m']
    >>> find_genders("{{ca-nom|m}} {{ca-nom|m}}")
    ['m']
    """
    return uniq(pattern.findall(code))


def find_pronunciations(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"{\s*ca-pron\s*\|(?:q=\S*\|)?(?:\s*or\s*=\s*)?(/[^/]+/)"),
) -> list[str]:
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
    return uniq(pattern.findall(code))


def last_template_handler(template: tuple[str, ...], locale: str, word: str = "") -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["default-test-xyz"], "ca")
        '##opendoublecurly##default-test-xyz##closedoublecurly##'

        >>> last_template_handler(["calc semàntic", "es", "ca", "pueblo"], "ca")
        'calc semàntic del castellà <i>pueblo</i>'

        >>> last_template_handler(["e", "grc", "υ", "tr=-"], "ca")
        'υ'

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
        >>> last_template_handler(["etim-lang", "grc", "ca", "φαιός", "trad=gris"], "ca")
        'Del grec antic <i>φαιός</i> (<i>phaiós</i>, «gris»)'
        >>> last_template_handler(["etim-lang", "ar", "ca", "برج", "alt=البرج", "trans=al-burj", "trad=la torre"], "ca")
        "De l'àrab <i>البرج</i> (<i>al-burj</i>, «la torre»)"

        >>> last_template_handler(["del-lang", "la", "ca", "verba"], "ca")
        'del llatí <i>verba</i>'
        >>> last_template_handler(["Del-lang", "xib", "ca", "baitolo"], "ca")
        "De l'ibèric <i>baitolo</i>"
        >>> last_template_handler(["Del-lang", "grc", "ca", "ῡ̔οειδής", "trad=en forma d’ípsilon"], "ca")
        'Del grec antic <i>ῡ̔οειδής</i> (<i>hȳoeidḗs</i>, «en forma d’ípsilon»)'
        >>> last_template_handler(["del-lang", "la", "ca"], "ca")
        ''
        >>> last_template_handler(["del-lang", "la", "ca", "-"], "ca")
        ''
        >>> last_template_handler(["Del-lang", "gem", "ca", "Adroar"], "ca")
        "D'un germànic <i>Adroar</i>"

        >>> last_template_handler(["Fals tall", "ca", "Far", "el Far"], "ca")
        'Fals tall sil·làbic de <i>el Far</i>'
        >>> last_template_handler(["fals tall", "ca", "s'endemà", "trad=l’endemà"], "ca")
        "fals tall sil·làbic de <i>s'endemà</i> («l’endemà»)"

        >>> last_template_handler(["la"], "ca")
        'Llatí'

        >>> last_template_handler(["m", "ca", "tardanies", "t=fruits tardans"], "ca")
        '<i>tardanies</i> («fruits tardans»)'
        >>> last_template_handler(["m", "grc", "ὖ"], "ca")
        '<i>ὖ</i> (<i>ŷ</i>)'
        >>> last_template_handler(["m", "grc", "ἄνῑσον", "ánison"], "ca")
        '<i>ánison</i> (<i>ánīson</i>)'

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
        >>> last_template_handler(["term", "en", "[[cheap]] as [[chips]]", "lit=tant [[barat]] com les [[patates]]"], "ca")
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
    from .langs import grups, langs
    from .template_handlers import lookup_template, render_template

    if lookup_template(template[0]):
        return render_template(word, template)

    from .general import cal_apostrofar

    tpl, *parts = template
    data = extract_keywords_from(parts)
    phrase = ""

    def parse_other_parameters(lang: str = "", word: str = "") -> str:
        toadd = []
        if data["trans"]:
            toadd.append(italic(data["trans"]))
        elif data["tr"] and data["tr"] != "-":
            toadd.append(italic(data["tr"]))
        elif lang == "grc" and word and data["tr"] != "-":
            toadd.append(italic(transliterate_grc(word)))
        elif lang == "ru" and word and data["tr"] != "-":
            toadd.append(italic(transliterate_ru(word)))
        if data["t"]:
            toadd.append(f"«{data['t']}»")
        if data["glossa"]:
            toadd.append(f"«{data['glossa']}»")
        if data["trad"]:
            toadd.append(f"«{data['trad']}»")
        if data["pos"]:
            toadd.append(data["pos"])
        if data["lit"]:
            toadd.append(f"literalment «{data['lit']}»")
        return f" ({concat(toadd, ', ')})" if toadd else ""

    def format_source(lang: str, lang_name: str, nocap: bool) -> str:
        if lang in grups:
            return "d'un " if nocap else "D'un "
        else:
            phrase = "d" if nocap else "D"
            phrase += "e l'" if cal_apostrofar(lang_name) else "el "
            return phrase

    if tpl == "calc semàntic":
        phrase = "calc semàntic "
        lang = langs[parts[0]]
        phrase += format_source(parts[0], lang, True)
        phrase += f"{lang} "
        phrase += f"{italic(parts[-1])}{parse_other_parameters()}"
        return phrase

    if tpl == "epònim":
        return parts[1] if len(parts) > 1 else (data["w"] if "w" in data else "")

    if tpl == "e":
        return f"{parts[-1]}{parse_other_parameters()}"

    if tpl in ("del-lang", "Del-lang") and (len(parts) <= 2 or parts[2] == "-"):
        return ""
    if tpl in ("etim-lang", "del-lang", "Del-lang"):
        if parts[0] in langs:
            lang = langs[parts[0]]
            phrase += format_source(parts[0], lang, tpl == "del-lang")
            phrase += f"{lang}"
            word = ""
            if len(parts) > 2:
                word = data["alt"] or parts[2]
                if len(parts) > 3:
                    phrase += f" {italic(parts[3])}"
                else:
                    phrase += f" {italic(word)}"
        phrase += parse_other_parameters(parts[0], word)
        return phrase

    if tpl in ("fals tall", "Fals tall"):
        return f"{tpl} sil·làbic de {italic(parts[-1])}{parse_other_parameters()}"

    if tpl == "lleng":
        phrase = parts[-1]
        if data["tipus"] == "terme":
            phrase = italic(phrase)
        elif data["tipus"] in ("lema", "negreta"):
            phrase = strong(phrase)
        return phrase

    if tpl in ("m", "terme", "term"):
        word = parts[2] if len(parts) > 2 else parts[1]
        return f"{italic(word)}{parse_other_parameters(parts[0], parts[1])}"
    if tpl == "calc":
        return f"{italic(parts[-1])}{parse_other_parameters(parts[0], parts[-1])}"

    if tpl == "trad":
        src = data["sc"] or parts.pop(0)
        trans = data["tr"] or parts.pop(0)
        return f"{trans} {superscript(f'({src})')}"

    # This is a country in the current locale
    if lang := langs.get(tpl, ""):
        return lang.capitalize()

    return defaults.last_template_handler(template, locale, word=word)
