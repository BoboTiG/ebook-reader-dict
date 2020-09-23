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

# A warning will be printed when a template contains superfuous spaces,
# except for those listed bellow:
templates_warning_skip: Tuple[str, ...] = tuple()


def last_template_handler(parts: Tuple[str, ...], locale: str) -> str:
    """Will be call in utils.py::transform() when all template handlers were not used."""
    from ..user_functions import capitalize, lookup_italic, term

    # Handle the {{lang}} template when it comes with unknown locale
    if parts[0] == "lang":
        return parts[-1]

    # {{tpl|item}} -> <i>(Template)</i>
    if len(parts) == 2:
        return term(capitalize(lookup_italic(parts[0], locale)))

    # {{tpl|item1|item2|...}} -> ''
    if len(parts) > 2:
        return ""

    # <i>(Template)</i>
    return term(capitalize(lookup_italic(parts[0], locale))) if parts[0] else ""


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/$LOCALE
release_description = """\
Words count: {words_count}
Wiktionary dump: {dump_date}

:arrow_right: Download: [dicthtml-{locale}.zip]({url})

---

Installation:

1. Copy the `dicthtml-{locale}.zip` file into the `.kobo/dict/` folder of the reader.
2. Restart the reader.

---

Caracteristics:

- Only definitions are included: there are no quote nor ethymology.
- Proper nouns are not included.
- Conjuged verbs are not included.

<sub>Updated on {creation_date}</sub>
"""
