"""Defaults values for locales without specific needs."""
from typing import Dict, Tuple


# Regex to find the genre
genre = r""

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


def last_template_handler(parts: Tuple[str, ...]) -> str:
    """
    Will be call in utils.py::transform() when all template handlers
    will not be used.
    """
    from ..user_functions import capitalize

    # {{grammaire|fr}} -> (Grammaire)
    if len(parts) == 2:
        return f"<i>({capitalize(parts[0])})</i>"

    # {{conj|grp=1|fr}} -> ''
    if len(parts) > 2:
        return ""

    return f"<i>({capitalize(parts[0])})</i>" if parts[0] else ""


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/$LOCALE
release_description = """\
:warning: Contributors needed for that locale.

Words count: {words_count}
Wiktionary dump: {dump_date}

:arrow_right: Download: [dicthtml-{locale}.zip]({url})

---

Installation:

1. Copy the `dicthtml-{locale}.zip` file into the `.kobo/dict/` folder of the reader.
2. Restart the reader.

---

Caracteristics :

- Only definitions are included: there is no quote nor ethymology.
- 1-character words are not included.
- Proper nouns are not included.
- Conjuged verbs are not included.

<sub>Updated on {creation_date}</sub>
"""
