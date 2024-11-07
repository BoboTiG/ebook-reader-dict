"""Danish language."""

import re

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
section_patterns = ("#", r"\*")
section_sublevels = (3, 4)
head_sections = ("{{da}}", "dansk", "{{=da=}}", "{{-da-}}", "{{mul}}", "{{=mul=}}", "{{-mul-}}")
etyl_section = ("{{etym}}", "{{etym2}}", "etymologi", "etymologi 1", "etymologi 2", "etymologi 3", "etymologi 4")
sections = (
    *etyl_section,
    "-adj-",
    "adjektiv",
    "adverbium",
    "formelt subjekt",
    "interfiks",
    "interjektion",
    "konjugation",
    "lydord",
    "noun",
    "personligt prononmen",
    "possessivt prononmen",
    "possessivt pronomen" "possessivt pronomen (ejestedord)" "præfiks",
    "prefix",
    "pronomen",
    "prœposition",
    "proposition",
    "proprium",
    "substantiv",
    "ubestemt prononmen",
    "ubestemt pronomen",
    "ubestemt talord",
    "udtryk",
    "verbum",
    "{{abbr}}",
    "{{abr}}",
    "{{adj}}",
    "{{adv}}",
    "{{afl}}",
    "{{art}}",
    "{{car-num}}",
    "{{conj}}",
    "{{dem-pronom}}",
    "{{end}}",
    "{{expr}}",
    "{{frase}}",
    "{{interj}}",
    "{{lyd}}",
    "{{noun}}",
    "{{noun2}}",
    "{{part}}",
    "{{pers-pronom}}",
    "{{phr}}",
    "{{pp}}",
    "{{pref}}",
    "{{prep}}",
    "{{pron}}",
    "{{prop}}",
    "{{prov}}",
    "{{seq-num}}",
    "{{suf}}",
    "{{symb}}",
    "{{symb|mul}}",
    "{{ubest-pronon}}",
    "{{verb}}",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "da-car-numbers",
    "da-v-pres",
    "da-verb",
    "de",
    "definition mangler",
    "dm",
    "infl",
    "IPA",
    "Personlige pronominer på dansk",
    "Possessive pronominer på dansk",
    "pn",
    "rfe",
    "-syn-",
    "wikipedia",
    "Wikipedia",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "botanik": "botanik",
    "geologi": "geologi",
    "grøntsag": "grøntsag",
    "internet": "internet",
    "patologi": "patologi",
    "plante": "plante",
    "skeleton": "anatomi",
}

templates_multi = {
    # {{alternativ stavemåde af|botanizer}}
    "alternativ stavemåde af": "italic(parts[0]) + ' ' + strong(parts[1])",
    # {{archaic form of|}}
    "archaic form of": "italic('forældet form af')",
    # {{c}}
    "c": "italic('fælleskøn')",
    # {{confix|cysto|itis|lang=da}}
    "confix": "parts[1] + '- + -' + parts[2]",
    # {{data}}
    "data": "'(' + italic('data') + ')'",
    # {{da-adj-N}}
    "da-adj-1": "italic('intetkønsform af')",
    "da-adj-2": "italic('bestemt og flertal af')",
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
    # {{flertal af}}
    "flertal af": "italic('flertalsform af')",
    # {{forældet stavemåde af}}
    "forældet stavemåde af": "italic('forældet stavemåde af')",
    # {{form of|imperative form|bjerge|lang=da}}
    "form of": "italic(capitalize(parts[1]) + ' af') + ' ' + strong(parts[2])",
    # {{fysik}}
    "fysik": "'(' + italic('fysik') + ')'",
    # {{genitivsform af}}
    "genitivform af": "italic('genitivform af')",
    # {{genitivsform af}}
    "genitivsform af": "italic('genitivform af')",
    # {{genitiv ental ubestemt af}}
    "genitiv ental ubestemt af": "italic('genitiv ental ubestemt af')",
    # {{genitiv ubestemt entalsform af}}
    "genitiv ubestemt entalsform af": "italic('genitiv ubestemt entalsform af')",
    # {{imperativ af|være}}
    "imperativ af": "f\"{italic('imperativ af')} {strong(parts[1])}\"",
    # {{l|da|USA}}
    "l": "parts[-1]",
    # {{label|militær|våben}}
    "label": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{m}}
    "m": "italic('hankøn')",
    # {{n}}
    "n": "italic('intetkøn')",
    # {{only in}}
    "only in": "italic('bruges kun i frasen')",
    # {{p}}
    "p": "italic('flertal')",
    # {{præteritum participium af}}
    "præteritum participium af": "italic('præteritum participium af')",
    # {{stavefejl for}}
    "stavefejl for": "italic('stavefejl for')",
    # {{trad|en|limnology}}
    "trad": "parts[-1] + superscript('(' + parts[1] + ')')",
    # {{URchar|الكحل}}
    "URchar": "parts[-1]",
    # {{w|Pierre Curie|Pierre}}
    "w": "parts[1]",
    # {{ZHchar|北京}}
    "ZHchar": "parts[-1]",
}
templates_multi["imperativ form af"] = templates_multi["imperativ af"]

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/da
release_description = """\
Ordtælling: {words_count}
Dump Wiktionary: {dump_date}

Full version:
{download_links_full}

Etymology-free version:
{download_links_noetym}

<sub>Opdateret den {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_pronunciations(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"\{\{IPA(?:\|(.*?))?\|lang=da\}\}"),
) -> list[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{IPA|/bɛ̜ːˀ/|lang=da}}")
    ['/bɛ̜ːˀ/']
    """
    return [item for sublist in (re.findall(pattern, code) or []) for item in sublist.split("|") if item]


def last_template_handler(template: tuple[str, ...], locale: str, word: str = "") -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["en"], "da")
        'Engelsk'
        >>> last_template_handler(["unknown"], "da")
        '##opendoublecurly##unknown##closedoublecurly##'

        >>> last_template_handler(["skeleton"], "da")
        '<i>(anatomi)</i>'

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

        >>> last_template_handler(["prefix", "hoved", "gade", "lang=da"], "da")
        'hoved- + gade'

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
    from ...user_functions import capitalize, concat, extract_keywords_from, italic, lookup_italic, strong, term
    from .. import defaults
    from .langs import langs

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl in {"abbreviation of", "abbr of"}:
        return f"{italic('Forkortelse af')} {strong(parts[-1])}"

    if tpl in {"compound", "com"}:
        return concat(parts, sep=" + ")

    if tpl == "etyl":
        return langs[parts[0]]

    if tpl in {"initialism of", "init of"}:
        return f"{italic('Initialforkortelse af')} {strong(parts[-1])}"

    if tpl == "prefix":
        return f"{parts[0]}- + {parts[1]}"

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

    if label := lookup_italic(tpl, locale, empty_default=True):
        return term(label)

    if not parts and (lang := langs.get(tpl)):
        return capitalize(lang)

    return defaults.last_template_handler(template, locale, word=word)
