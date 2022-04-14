"""Internationalization stuff."""
import re
from typing import Any, Callable, Dict, Pattern, Tuple, TypeVar

from . import ca, de, defaults, el, en, es, fr, it, no, pt, sv, ru
from .ca.langs import langs as CA
from .el.langs import langs as EL
from .en.langs import langs as EN
from .es.langs import langs as ES
from .fr.langs import langs as FR
from .pt.langs import langs as PT
from .ru.langs import langs as RU


#
# Start of manual edition allowed.
#

_ALL_LOCALES = (ca, de, el, en, es, fr, it, no, pt, sv, ru)


# A list of all languages translated into different locales
all_langs = {
    "ca": CA,
    "el": EL,
    "en": EN,
    "es": ES,
    "fr": FR,
    "pt": PT,
    "ru": RU,
}

# The template name dealing with files in the Wikicode (multi locales).
# [[PATTERN:...|...]]
pattern_file = (
    "Archivo",
    "Categoría",
    "categoría",
    "Catégorie",
    "Fichier",
    "File",
    "Fitxer",
    "Image",
    "image",
    "Imagen",
    "Αρχείο",
    "Εικόνα",
    "Файл",
)

#
# End of manual edition allowed.
#

Arg = TypeVar("Arg")
PopulatedDict = Dict[str, Any]


def _noop_callback(arg: Arg) -> Arg:
    """Simply returns the argument."""
    return arg


def _populate(
    attr: str, callback: Callable[[Any], Any] = _noop_callback
) -> PopulatedDict:
    """
    Create a dict for all locales pointing to the appropriate attribute.
    Fallback to `defaults`.
    """
    return {
        locale.__name__.split(".")[-1]: callback(getattr(locale, attr))
        if hasattr(locale, attr)
        else callback(getattr(defaults, attr))
        for locale in _ALL_LOCALES
    }


# Regex to find the pronunciation
pronunciation: Dict[str, Pattern[str]] = _populate("pronunciation", callback=re.compile)

# Regex to find the gender
gender: Dict[str, Pattern[str]] = _populate("gender", callback=re.compile)

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

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore: Dict[str, Tuple[str, ...]] = _populate("definitions_to_ignore")

# But some words need to be kept even if they would have been skipped by definitions_to_ignore
words_to_keep: Dict[str, Tuple[str, ...]] = _populate("words_to_keep")

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
#
# Available functions are documented into that HTML file:
#   html/wikidict/user_functions.html
templates_multi: Dict[str, Dict[str, str]] = _populate("templates_multi")

# Templates that will be completed/replaced using custom style.
templates_other: Dict[str, Dict[str, str]] = _populate("templates_other")

# When a template is not handled by any previous template handlers,
# this method will be called with *parts* as argument.
last_template_handler = _populate("last_template_handler")

# The full release description on GitHub:
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/$LOCALE
release_description: Dict[str, str] = _populate("release_description")

# Dictionary name that will be printed below each definition
wiktionary: Dict[str, str] = _populate("wiktionary")
