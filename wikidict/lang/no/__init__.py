"""Norwegian language."""

import re

from ...user_functions import flatten, uniq

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("norsk",)
section_sublevels = (3, 4)
etyl_section = ("Etymologi",)
sections = (
    *etyl_section,
    "Substantiv",
    "Verb",
)

# Variants
variant_titles = tuple(section for section in sections if section not in etyl_section)
variant_templates = (
    "{{no-sub-bøyningsform",
    "{{no-verb-bøyningsform",
)

# Templates to ignore: the text will be deleted.
definitions_to_ignore = (
    "no-sub-bunn",
    "no-sub-m1",
    "no-sub-rad",
    "no-sub-slutt",
    "no-sub-start",
    "no-sub-topp",
    #
    # For variants
    #
    "no-sub-bøyningsform",
    "no-verb-bøyningsform",
)

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/no
release_description = """\
Ord räknas: {words_count}
Dumpa Wiktionary: {dump_date}

Tillgängliga filer:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Uppdaterad på {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"

# Templates more complex to manage.
templates_multi = {
    # {{feilstaving av|førstvoterende|språk=no}}
    "feilstaving av": 'f"Feilstaving av {parts[1]}."',
    # {{prefiks|a|biotisk|språk=no}}
    "prefiks": 'f"{italic(parts[1])}- + {italic(parts[2])}"',
    # {{suffiks|konsentrere|sjon|språk=no}}
    "suffiks": 'f"{italic(parts[1])} + -{italic(parts[2])}"',
    #
    # For variants
    #
    # {{no-sub-bøyningsform|be|funn|nb=ja|nrm=ja|nn=ja}}
    "no-sub-bøyningsform": "parts[2]",
    # {{no-verb-bøyningsform|pret|finne|nb=ja|nrm=ja}}
    "no-verb-bøyningsform": "parts[2]",
}


def find_genders(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"{{no-sub\|(\w+)}}"),
) -> list[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("{{no-sub|m}}")
    ['m']
    >>> find_genders("{{no-sub|mf}}")
    ['mf']
    """
    return uniq(flatten(pattern.findall(code)))
