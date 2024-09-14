"""Danish language."""

import re

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{da}}", "dansk", "{{=da=}}")
etyl_section = ("{{etym}}", "Etymologi")
sections = (
    *etyl_section,
    "Adjektiv",
    "Adverbium",
    "Konjugation",
    "Lydord",
    "Personligt prononmen",
    "Possessivt prononmen",
    "Pronomen",
    "Prœposition",
    "Proposition",
    "Substantiv",
    "Ubestemt prononmen",
    "Verbum",
    "{{abbr}}",
    "{{abr}}",
    "{{adj}}",
    "{{adv}}",
    "{{afl}}",
    "{{conj}}",
    "{{interj}}",
    "{{noun}}",
    "{{prep}}",
    "{{pron}}",
    "{{prop}}",
    "{{verb}}",
    "{{car-num}}",
    "-adj-",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "definition mangler",
    "da-v-pres",
    "de",
    "dm",
    "-syn-",
    "wikipedia",
    "Wikipedia",
    "infl",
)

templates_multi = {
    # {{c}}
    "c": "italic('fælleskøn')",
    # {{confix|cysto|itis|lang=da}}
    "confix": "parts[1] + '- + -' + parts[2]",
    # {{data}}
    "data": "'(' + italic('data') + ')'",
    # {{da-noun-N}}
    "da-noun-1": "italic('bestemt entalsform af')",
    "da-noun-2": "italic('ubestemt flertalsform af')",
    "da-noun-3": "italic('bestemt flertalsform af')",
    "da-noun-4": "italic('genitiv ubestemt entalsform af')",
    "da-noun-5": "italic('genitiv bestemt entalsform af')",
    "da-noun-6": "italic('genitiv ubestemt flertalsform af')",
    "da-noun-7": "italic('genitiv bestemt flertalsform af')",
    # {{dublet af|da|boulevard}}
    "dublet af": "'dublet af ' + strong(parts[-1])",
    # {{form of|imperative form|bjerge|lang=da}}
    "form of": "italic(parts[1] + ' of') + ' ' + strong(parts[2])",
    # {{fysik}}
    "fysik": "'(' + italic('fysik') + ')'",
    # {{genitivsform af}}
    "genitivform af": "italic('genitivform af')",
    # {{genitivsform af}}
    "genitivsform af": "italic('genitivform af')",
    # {{imperativ af}}
    "imperativ af": "italic('imperativ af')",
    # {{l|da|USA}}
    "l": "parts[-1]",
    # {{label|militær|våben}}
    "label": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{n}}
    "n": "italic('intetkøn')",
    # {{prefix|hoved|gade|lang=da}}
    "prefix": "parts[1] + '- + ' + parts[2]",
    # {{suffix|Norden|isk|lang=da}}
    "suffix": "parts[1] + ' + -' + parts[2]",
    # {{trad|en|limnology}}
    "trad": "parts[-1] + superscript('(' + parts[1] + ')')",
    # {{ZHchar|北京}}
    "ZHchar": "parts[-1]",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/da
release_description = """\
Ordtælling: {words_count}
Dump Wiktionary: {dump_date}

Tilgængelige filer:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Opdateret den {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_pronunciations(code: str) -> list[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{IPA|/bɛ̜ːˀ/|lang=da}}")
    ['/bɛ̜ːˀ/']
    """
    pattern = re.compile(r"\{\{IPA(?:\|(.*?))?\|lang=da\}\}", flags=re.MULTILINE)
    matches = re.findall(pattern, code) or []

    return [item for sublist in matches for item in sublist.split("|") if item]


def last_template_handler(template: tuple[str, ...], locale: str, word: str = "") -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["en"], "da")
        'Engelsk'
        >>> last_template_handler(["unknown"], "da")
        '##opendoublecurly##unknown##closedoublecurly##'

        >>> last_template_handler(["abbreviation of", "lang=da", "pansret mandskabsvogn"], "da")
        '<i>Forkortelse af</i> <b>pansret mandskabsvogn</b>'
        >>> last_template_handler(["abbr of", "pansret mandskabsvogn", "lang=da"], "da")
        '<i>Forkortelse af</i> <b>pansret mandskabsvogn</b>'

        >>> last_template_handler(["compound", "hjemme", "værn", "langa=da"], "da")
        'hjemme + værn'
        >>> last_template_handler(["com", "hjemme", "værn", "langa=da"], "da")
        'hjemme + værn'

        >>> last_template_handler(["etyl", "fr", "da"], "da")
        'fransk'
        >>> last_template_handler(["etyl", "non", "da"], "da")
        'oldnordisk'

        >>> last_template_handler(["initialism of", "lang=da", "København"], "da")
        '<i>Initialforkortelse af</i> <b>København</b>'
        >>> last_template_handler(["init of", "København", "lang=da"], "da")
        '<i>Initialforkortelse af</i> <b>København</b>'

        >>> last_template_handler(["term", "mouse", "lang=en"], "da")
        'mouse'
        >>> last_template_handler(["term", "cabotage", "", "kysttransport", "lang=fr"], "da")
        'cabotage (“‘kysttransport’”)'
        >>> last_template_handler(["term", "αὐτός", "autós", "selv", "lang=grc"], "da")
        'autós (“‘selv’”)'
        >>> last_template_handler(["term", "μέτρον", "", "tr=metron", "mål", "lang=grc}}"], "da")
        'μέτρον (metron), (“‘mål’”)'
        >>> last_template_handler(["term", "الجزائر", "Al Jazaïr", "tr=Øerne", "lang=ar}}"], "da")
        'Al Jazaïr (Øerne)'

        >>> last_template_handler(["suffix", "Norden", "isk", "lang=da"], "da")
        'Norden + -isk'
        >>> last_template_handler(["suf", "Norden", "isk", "lang=da"], "da")
        'Norden + -isk'

        >>> last_template_handler(["u", "de", "Reis"], "da")
        'Reis'
        >>> last_template_handler(["u", "gml", "-maker", "", "person der frembringer eller tilvirker noget"], "da")
        '<i>-maker</i> (“‘person der frembringer eller tilvirker noget’”)'
        >>> last_template_handler(["u", "en", "-ing", ""], "da")
        '<i>-ing</i>'
    """
    from ...lang import defaults
    from ...user_functions import capitalize, extract_keywords_from, italic, strong, term
    from .langs import langs

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl in {"abbreviation of", "abbr of"}:
        return f"{italic('Forkortelse af')} {strong(parts[-1])}"

    if tpl in {"compound", "com"}:
        return " + ".join(parts)

    if tpl == "etyl":
        return langs[parts[0]]

    if tpl in {"initialism of", "init of"}:
        return f"{italic('Initialforkortelse af')} {strong(parts[-1])}"

    if tpl == "term":
        match len(parts):
            case 1:
                return parts[0]
            case 2:
                return f"{parts[1] or parts[0]}{' (' + data['tr'] + ')' if data['tr'] else ''}"
            case 3:
                return f"{parts[1] or parts[0]}{' (' + data['tr'] + '),' if data['tr'] else ''} (“‘{parts[2]}’”)"
        return parts[0]

    if tpl in {"suffix", "suf"}:
        return f"{parts[0]} + -{parts[1]}"

    if tpl == "u":
        match len(parts):
            case 2:
                return parts[1]
            case 3:
                return italic(parts[1])
            case 4:
                return f"{italic(parts[1])} (“‘{parts[3]}’”)"

    if len(parts) == 1:
        return term(tpl)

    if not parts and (lang := langs.get(tpl)):
        return capitalize(lang)

    return defaults.last_template_handler(template, locale, word=word)
