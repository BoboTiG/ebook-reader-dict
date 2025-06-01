"""Danish language."""

import re

from .langs import langs

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
section_patterns = ("#", r"\*")
section_sublevels = (3, 4)
head_sections = ("{{da}}", "{{=da=}}", "{{-da-}}", "dansk", "{{mul}}", "{{=mul=}}", "{{-mul-}}")
etyl_section = ("{{etym}}", "{{etym2}}", "etymologi", "etymologi 1", "etymologi 2", "etymologi 3", "etymologi 4")
sections = (
    *etyl_section,
    "-adj-",
    "adjektiv",
    "adverbium",
    "bogstav",
    "fast udtryk",
    "formelt subjekt",
    "interfiks",
    "interjektion",
    "konjugation",
    "lydord",
    "noun",
    "pronomen",
    "personligt prononmen",
    "possessivt prononmen",
    "possessivt pronomen",
    "possessivt pronomen (ejestedord)",
    "possessivt pronomenpossessivt pronomen (ejestedord)præfiks",
    "prefix",
    "pronomen",
    "prœposition",
    "proposition",
    "proprium",
    "sætning",
    "substantiv",
    "symbol",
    "ubestemt prononmen",
    "ubestemt pronomen",
    "ubestemt talord",
    "udtryk",
    "verbum",
    "{{abbr}",
    "{{abr}",
    "{{abr|mul}",
    "{{adj}",
    "{{adv}",
    "{{afl}",
    "{{art}",
    "{{car-num}",
    "{{car-num|mul}",
    "{{conj}",
    "{{dem-pronom}",
    "{{end}",
    "{{expr}",
    "{{frase}",
    "{{interj}",
    "{{lyd}",
    "{{noun}",
    "{{noun2}",
    "{{num}",
    "{{part}",
    "{{pers-pronom}",
    "{{phr}",
    "{{pp}",
    "{{pref}",
    "{{prep}",
    "{{pron}",
    "{{prop}",
    "{{prov}",
    "{{seq-num}",
    "{{sætning}",
    "{{suf}",
    "{{symb}",
    "{{symb|mul}",
    "{{ubest-pronon}",
    "{{verb}",
)

# Variantes
variant_titles = sections
variant_templates = ("{{alternativ stavemåde af", "{{form of", "{{flexion", "{{imperativ af", "{{imperativ form af")

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
    # {{forældet stavemåde af}}
    "forældet stavemåde af": "italic('forældet stavemåde af')",
    # {{fysik}}
    "fysik": "'(' + italic('fysik') + ')'",
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

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/da
release_description = """\
### 🌟 For at kunne blive opdateret regelmæssigt har dette projekt brug for støtte; [klik her](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) for at donere. 🌟

<br/>


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


def find_pronunciations(code: str, locale: str) -> list[str]:
    """
    >>> find_pronunciations("", "da")
    []
    >>> find_pronunciations("{{IPA|/bɛ̜ːˀ/|lang=da}}", "da")
    ['/bɛ̜ːˀ/']
    """
    pattern = re.compile(rf"\{{\{{IPA(?:\|(.*?))?\|lang={locale}\}}\}}")
    return [item for sublist in (re.findall(pattern, code) or []) for item in sublist.split("|") if item]


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    all_templates: list[tuple[str, str, str]] | None = None,
    variant_only: bool = False,
) -> str:
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

        >>> last_template_handler(["da-adj", "påståeligt", "påståelige"], "da", word="påståelig")
        'påståelig (<i>intetkøn</i> påståeligt, <i>flertal og bestemt ental attributiv</i> påståelige)'

        >>> last_template_handler(["compound", "hjemme", "værn", "langa=da"], "da")
        'hjemme + værn'
        >>> last_template_handler(["com", "hjemme", "værn", "langa=da"], "da")
        'hjemme + værn'

        >>> last_template_handler(["etyl", "fr", "da"], "da")
        'fransk'
        >>> last_template_handler(["etyl", "non", "da"], "da")
        'oldnordisk'
        >>> last_template_handler(["etyl", "cmn", "pt"], "da")
        'kinesisk'

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
    from .template_handlers import lookup_template, render_template

    tpl, *parts = template

    tpl_variant = f"__variant__{tpl}"
    if variant_only:
        tpl = tpl_variant
        template = tuple([tpl_variant, *parts])
    elif lookup_template(tpl_variant):
        # We are fetching the output of a variant template, we do not want to keep it
        return ""

    if lookup_template(template[0]):
        return render_template(word, template)

    data = extract_keywords_from(parts)

    if tpl in {"abbreviation of", "abbr of"}:
        return f"{italic('Forkortelse af')} {strong(parts[-1])}"

    if tpl == "da-adj":
        return f"{word} (<i>intetkøn</i> {parts[0]}, <i>flertal og bestemt ental attributiv</i> {parts[1]})"

    if tpl in {"compound", "com"}:
        return concat(parts, " + ")

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

    return defaults.last_template_handler(template, locale, word=word, all_templates=all_templates)


random_word_url = "https://da.wiktionary.org/wiki/Speciel:RandomRootpage"


def adjust_wikicode(code: str, locale: str, *, all_langs: str = "|".join(langs)) -> str:
    # sourcery skip: inline-immediately-returned-variable
    r"""
    >>> adjust_wikicode("{{(}}\n* {{en}}: {{trad|en|limnology}}\n{{)}}", "da")
    ''

    >>> adjust_wikicode("{{=da=}}", "da")
    '=={{da}}=='

    >>> adjust_wikicode("===dansk===", "da")
    '=={{da}}=='
    >>> adjust_wikicode("===Foo===", "fo")
    '=={{fo}}=='

    >>> adjust_wikicode("{{-avv-|da}}", "da")
    '=== {{avv}} ==='

    >>> adjust_wikicode("{{-avv-|ANY}}", "da")
    '=== {{avv|ANY}} ==='

    >>> adjust_wikicode("{{-avv-}}", "da")
    '=== {{avv}} ==='

    >>> adjust_wikicode("#Pluralis af [[tale|tale]]", "da")
    '# {{flexion|tale}}'
    >>> adjust_wikicode("#Pluralis af [[tale#Substantiv|tale]]", "da")
    '# {{flexion|tale}}'
    >>> adjust_wikicode("# Nutid af [[tale#Verbum|tale]]", "da")
    '# {{flexion|tale}}'
    >>> adjust_wikicode("# Flertal af [[grand-maman]]: [[bedstemor]].", "da")
    '# {{flexion|grand-maman}}'
    """
    code = code.replace("----", "")

    # {{(}} .* {{)}}
    code = re.sub(r"\{\{\(\}\}(.+)\{\{\)\}\}", "", code, flags=re.DOTALL | re.MULTILINE)

    # {{=da=}} → =={{da}}==
    code = re.sub(r"\{\{=(\w+)=\}\}", r"=={{\1}}==", code, flags=re.MULTILINE)

    # ===dansk=== → =={{da}}==
    code = re.sub(rf"=+\s*{locale}\w+\s*=+", rf"=={{{{{locale}}}}}==", code, flags=re.IGNORECASE | re.MULTILINE)

    # Transform sub-locales into their own section to prevent mixing stuff
    # {{-da-}} → =={{da}}==
    # {{-mul-}} → =={{mul}}==
    code = re.sub(rf"\{{\{{-({all_langs})-\}}\}}", r"=={{\1}}==", code, flags=re.MULTILINE)

    # {{-avv-|da}} → === {{avv}} ===
    code = re.sub(rf"^\{{\{{-(.+)-\|{locale}\}}\}}", r"=== {{\1}} ===", code, flags=re.MULTILINE)

    # {{-avv-|ANY}} → === {{avv|ANY}} ===
    code = re.sub(r"^\{\{-(.+)-\|(\w+)\}\}", r"=== {{\1|\2}} ===", code, flags=re.MULTILINE)

    # {{-avv-}} → === {{avv}} ===
    code = re.sub(r"^\{\{-(\w+)-\}\}", r"=== {{\1}} ===", code, flags=re.MULTILINE)

    #
    # Variants
    #

    # `#Pluralis af [[tale#Substantiv|tale]]` → `# {{flexion|tale}}`
    forms = "|".join(
        [
            "flertal",
            "genitivsform af",
            "genitiv ental ubestemt af",
            "genitiv ubestemt entalsform af",
            "nutid",
            "pluralis",
        ]
    )
    code = re.sub(
        rf"^#\s*((?:{forms})\s+af\s+\[\[([^\]#|]+)(?:[#|].+)?]].*)",
        r"# {{flexion|\2}}",
        code,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    return code
