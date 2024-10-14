"""Internationalization stuff."""

from importlib import import_module
from pathlib import Path
from typing import Any, TypeVar

from . import defaults

ALL_LOCALES = {
    locale.name: import_module(f"wikidict.lang.{locale.name}")
    for locale in sorted(Path(__file__).parent.glob("*"))
    if locale.is_dir() and locale.name != "__pycache__"
}

Arg = TypeVar("Arg")
PopulatedDict = dict[str, Any]


def _populate(attr: str) -> PopulatedDict:
    """
    Create a dict for all locales pointing to the appropriate attribute.
    Fallback to `defaults`.
    """
    return {
        locale.__name__.split(".")[-1]: getattr(locale, attr) if hasattr(locale, attr) else getattr(defaults, attr)
        for locale in ALL_LOCALES.values()
    }


# Float number separator
float_separator: dict[str, str] = _populate("float_separator")

# Thousads separator
thousands_separator: dict[str, str] = _populate("thousands_separator")

# Markers for sections that contain interesting text to analyse.
section_patterns: dict[str, tuple[str, ...]] = _populate("section_patterns")
sublist_patterns: dict[str, tuple[str, ...]] = _populate("sublist_patterns")
section_level: dict[str, int] = _populate("section_level")
section_sublevels: dict[str, tuple[int, ...]] = _populate("section_sublevels")
head_sections: dict[str, tuple[str, ...]] = _populate("head_sections")
etyl_section: dict[str, tuple[str]] = _populate("etyl_section")
sections: dict[str, tuple[str, ...]] = _populate("sections")

# Variants
# Section titles considered interesting to look variants into
variant_titles: dict[str, tuple[str, ...]] = _populate("variant_titles")
# Template names considered interesting to look variants into
variant_templates: dict[str, tuple[str, ...]] = _populate("variant_templates")

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore: dict[str, tuple[str, ...]] = _populate("definitions_to_ignore")

# Templates replacements: wikicode -> text conversion

# Templates to ignore: the text will be deleted.
templates_ignored: dict[str, tuple[str, ...]] = _populate("templates_ignored")

# Templates that will be completed/replaced using italic style.
# Ex: {{absol}} -> <i>(Absolument)</i>
# Ex: {{absol|fr}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123|...}} -> <i>(Absolument)</i>
templates_italic: dict[str, dict[str, str]] = _populate("templates_italic")

# Templates more complex to manage. More work is needed.
# The code on the right will be passed to a function that will execute it.
# It is possible to use any Python function and ones defined in user_functions.py.
#
# Available arguments:
#   - *tpl* (string) containing the template name.
#   - *parts* (list of strings) containing the all parts of the template.
#
# Example with the complete template "{{comparatif de|bien|fr|adv}}":
#   - *tpl* will contain the string "comparatif de".
#   - *parts* will contain the list ["comparatif de", "bien", "fr", "adv"].
#
# You can access to *tpl* and *parts* to apply changes and get the result wanted.
templates_multi: dict[str, dict[str, str]] = _populate("templates_multi")

# Templates that will be completed/replaced using custom style.
templates_other: dict[str, dict[str, str]] = _populate("templates_other")

# The full release description on GitHub:
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/$LOCALE
release_description: dict[str, str] = _populate("release_description")

# Dictionary name that will be printed below each definition
wiktionary: dict[str, str] = _populate("wiktionary")

# Function to find gender(s)
find_genders = _populate("find_genders")

# Function to find pronunciation(s)
find_pronunciations = _populate("find_pronunciations")

# When a template is not handled by any previous template handlers,
# this function will be called with *parts* as argument.
last_template_handler = _populate("last_template_handler")
