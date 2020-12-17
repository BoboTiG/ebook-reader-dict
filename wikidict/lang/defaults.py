"""Defaults values for locales without specific needs."""
from typing import Dict, Tuple

# Regex to find the genre
genre = r""

# Markers for sections that contain interesting text to analyse.
section_patterns = (r"\#",)
sublist_patterns = (r"\#",)
section_level = 2
section_sublevels = (3,)

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore: Tuple[str, ...] = tuple()

# But some words need to be kept even if they would have been skipped by definitions_to_ignore
words_to_keep: Tuple[str, ...] = tuple()

# Templates to ignore: the text will be deleted.
templates_ignored: Tuple[str, ...] = tuple()

# Templates that will be completed/replaced using italic style.
templates_italic: Dict[str, str] = {}

# Templates that will be completed/replaced using custom style.
templates_other: Dict[str, str] = {}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["transliterator", "ar", "سم"], "fr")
        'sm'
        >>> last_template_handler(["transliterator", "ar"], "fr", word="زب")
        'zb'
    """
    from ..user_functions import capitalize, lookup_italic, term
    from ..transliterator import transliterate

    # Handle the {{lang}} template when it comes with unknown locale
    if template[0].lower() == "lang":
        return template[-1]

    # Handle the specific {{transliterator}} template (which is a Wiktionary module)
    if template[0] == "transliterator":
        lang = template[1]
        text = template[2] if len(template) == 3 else word
        return transliterate(lang, text)

    # {{tpl|item}} -> <i>(Template)</i>
    if len(template) == 2:
        return term(capitalize(lookup_italic(template[0], locale)))

    italic = lookup_italic(template[0], locale, True)
    if italic:
        return term(capitalize(italic))

    # {{tpl|item1|item2|...}} -> ''
    if len(template) > 2:
        return ""

    # <i>(Template)</i>
    return term(capitalize(lookup_italic(template[0], locale))) if template[0] else ""
