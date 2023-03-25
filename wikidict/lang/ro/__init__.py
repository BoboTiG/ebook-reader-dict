"""Romanian language."""
import re
from typing import List, Pattern, Tuple

from ...user_functions import flatten, uniq

# Float number separator
float_separator = "."

# Thousads separator
thousands_separator = ","

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{limba|ron}}",)
section_level = None
section_sublevels = (3,)
etyl_section = ("{{etimologie}}",)
sections = (
    "{{abreviere}",
    "{{adverb}",
    "{{adjectiv}",
    "{{articol}",
    *etyl_section,
    "{{pronume}",
    "{{substantiv}",
    "{{verb-}",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = ()

# Templates to ignore: the text will be deleted.
templates_ignored = ()

# Templates that will be completed/replaced using italic style.
templates_italic = {}

# Templates more complex to manage.
templates_multi = {}

# Templates that will be completed/replaced using custom text.
templates_other = {}


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
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wikționar (ɔ) {year}"


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


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.



    """  # noqa
    from ..defaults import last_template_handler as default

    return default(template, locale, word=word)
