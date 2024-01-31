"""Danish language."""
import re
from typing import List, Tuple

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{da}}", "dansk", "{{=da=}}")
etyl_section = ("{{etym}}",)
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

# Variants
variant_titles = (
    "Adjektiv",
    "Adverbium",
    "Pronomen",
    "Substantiv",
    "{{adj}}",
    "{{adv}}",
    "{{noun}}",
    "{{pron}}",
    "{{prop}}",
    "{{verb}}",
    "-adj-",
    "Alternativ form",
    "Alternative former",
    "Alternative stavemåder",
)
variant_templates = (
    "Bøjning",
    "Staves også",
    "flertal af",
    "genitivform af",
    "imperitiv af",
    "infl",
    "prœsens av",
    "da-noun-infl",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    "Bøjning",
    "Eksempler",
    "da-noun-4",
    "da-noun-5",
    "da-noun-6",
    "da-noun-7",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "definition mangler",
    "da-v-pres",
    "de",
    "dm",
    "-syn-",
    "etyl",
)

templates_multi = {
    # {{l|da|USA}}
    "l": "parts[-1]",
    # {{form of|imperative form|bjerge|lang=da}}
    "form of": "parts[1] + ' av ' + strong(parts[2])",
    # {{term|mouse|lang=en}}
    "term": "italic(parts[1]) + superscript('(' + parts[-1].lstrip('=lang') + ')')",
    # {{fysik}}
    "fysik": "'(fysik)'",
    # {{u|de|Reis}}
    "u": "italic(parts[-1]) + ' (' + parts[1] + ')'",
    # {{compound|hjemme|værn}}
    "compound": "' + '.join(parts[1:])",
    # {{trad|en|limnology}}
    "trad": "italic(parts[-1]) + superscript('(' + parts[1] + ')')",
    # {{en}}
    "en": "'Engelsk'",
    # {{suffix|Norden|isk|lang=da}}
    "suffix": "parts[1] + ' + -' + parts[2]",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/sv
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


def find_pronunciations(code: str) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{IPA|/bɛ̜ːˀ/|lang=da}}")
    ['/bɛ̜ːˀ/']
    """
    pattern = re.compile(r"\{\{IPA(?:\|(.*?))?\|lang=da\}\}", flags=re.MULTILINE)
    matches = re.findall(pattern, code)

    if len(matches) > 0:
        matches = [item for sublist in matches for item in sublist.split("|") if item]
        return matches

    return []


def last_template_handler(template: Tuple[str, ...], locale: str, word: str = "") -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["foo"], "da")

    """  # noqa
    from ...user_functions import extract_keywords_from
    from ..defaults import last_template_handler as default

    # tpl, *parts = template
    # data = extract_keywords_from(parts)

    return default(template, locale, word=word)
