"""Romanian language."""
import re
from typing import List, Pattern

from ...user_functions import flatten, uniq

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{limba|ron}}",)
section_sublevels = (3,)
etyl_section = ("{{etimologie}}",)
sections = (
    "{{abreviere}",
    "{{adjectiv}",
    "{{adverb}",
    "{{articol}",
    "{{conjuncție}",
    "{{cuvânt compus}",
    *etyl_section,
    "{{expresie}",
    "{{interjecție}",
    "{{locuțiune adjectivală}",
    "{{locuțiune adverbială}",
    "{{locuțiune}",
    "{{numeral colectiv}",
    "{{numeral}",
    "{{nume propriu}",
    "{{participiu}",
    "{{prefix}",
    "{{prepoziție}",
    "{{pronume}",
    "{{substantiv}",
    "{{sufix}",
    "{{verb}",
)

# Templates more complex to manage.
templates_multi = {
    # {{n}}
    "n": "italic('n.')",
    # {{p}}
    "p": "italic('pl.')",
    # {{trad|el|παρα}}
    "trad": "parts[-1]",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ro
release_description = """\
Număr de cuvinte: {words_count}
Extragerea datelor din Wikționar: {dump_date}

Fișiere disponibile:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Ultima actualizare în {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wikționar (ɔ) {year}"


def find_genders(
    code: str,
    pattern: Pattern[str] = re.compile(r"gen={{([fmsingp]+)(?: \?\|)*}"),
) -> List[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("{{substantiv-ron|gen={{m}}|nom-sg=câine|nom-pl=câini")
    ['m']
    >>> find_genders("{{substantiv-ron|gen={{n}}}}")
    ['n']
    """
    return uniq(flatten(pattern.findall(code)))


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(r"{AFI\|(/[^/]+/)(?:\|(/[^/]+/))*"),
) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{AFI|/ka.priˈmulg/}}")
    ['/ka.priˈmulg/']
    """
    return uniq(flatten(pattern.findall(code)))
