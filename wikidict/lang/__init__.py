"""Internationalization stuff."""
from typing import Any, Dict, Tuple, TypeVar

from . import ca, de, defaults, el, en, es, fr, it, no, pt, ro, ru, sv

ALL_LOCALES = {
    "ca": ca,
    "de": de,
    "el": el,
    "en": en,
    "es": es,
    "fr": fr,
    "it": it,
    "no": no,
    "pt": pt,
    "ro": ro,
    "ru": ru,
    "sv": sv,
}


#
# Start of manual edition allowed.
#


#
# End of manual edition allowed.
#

Arg = TypeVar("Arg")
PopulatedDict = Dict[str, Any]


def _populate(attr: str) -> PopulatedDict:
    """
    Create a dict for all locales pointing to the appropriate attribute.
    Fallback to `defaults`.
    """
    return {
        locale.__name__.split(".")[-1]: getattr(locale, attr)
        if hasattr(locale, attr)
        else getattr(defaults, attr)
        for locale in ALL_LOCALES.values()
    }


# Float number separator
float_separator: Dict[str, str] = _populate("float_separator")

# Thousads separator
thousands_separator: Dict[str, str] = _populate("thousands_separator")

# Markers for sections that contain interesting text to analyse.
section_patterns: Dict[str, Tuple[str, ...]] = _populate("section_patterns")
sublist_patterns: Dict[str, Tuple[str, ...]] = _populate("sublist_patterns")
section_level: Dict[str, int] = _populate("section_level")
section_sublevels: Dict[str, Tuple[int, ...]] = _populate("section_sublevels")
head_sections: Dict[str, Tuple[str, ...]] = _populate("head_sections")
etyl_section: Dict[str, Tuple[str]] = _populate("etyl_section")
sections: Dict[str, Tuple[str, ...]] = _populate("sections")

# Variants
# Section titles considered interesting to look variants into
variant_titles: Dict[str, Tuple[str, ...]] = _populate("variant_titles")
# Template names considered interesting to look variants into
variant_templates: Dict[str, Tuple[str, ...]] = _populate("variant_templates")

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore: Dict[str, Tuple[str, ...]] = _populate("definitions_to_ignore")

# Templates replacements: wikicode -> text conversion

# Templates to ignore: the text will be deleted.
templates_ignored: Dict[str, Tuple[str, ...]] = _populate("templates_ignored")

# Templates that will be completed/replaced using italic style.
# Ex: {{absol}} -> <i>(Absolument)</i>
# Ex: {{absol|fr}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123|...}} -> <i>(Absolument)</i>
templates_italic: Dict[str, Dict[str, str]] = _populate("templates_italic")

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
templates_multi: Dict[str, Dict[str, str]] = _populate("templates_multi")

# Templates that will be completed/replaced using custom style.
templates_other: Dict[str, Dict[str, str]] = _populate("templates_other")

# The full release description on GitHub:
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/$LOCALE
release_description: Dict[str, str] = _populate("release_description")

# Dictionary name that will be printed below each definition
wiktionary: Dict[str, str] = _populate("wiktionary")

# Function to find gender(s)
find_genders = _populate("find_genders")

# Function to find pronunciation(s)
find_pronunciations = _populate("find_pronunciations")

# When a template is not handled by any previous template handlers,
# this function will be called with *parts* as argument.
last_template_handler = _populate("last_template_handler")
