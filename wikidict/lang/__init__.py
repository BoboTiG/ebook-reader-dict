"""Internationalization stuff."""
import re

from . import ca, defaults, en, es, fr, pt, sv
from .ca.langs import langs as CA
from .en.langs import langs as EN
from .es.langs import langs as ES
from .fr.langs import langs as FR
from .pt.langs import langs as PT

# A list of all languages translated into different locales
all_langs = {
    "ca": CA,
    "en": EN,
    "es": ES,
    "fr": FR,
    "pt": PT,
}

# Regex to find the pronunciation
pronunciation = {
    "ca": re.compile(ca.pronunciation),
    "en": re.compile(en.pronunciation),
    "es": re.compile(es.pronunciation),
    "fr": re.compile(fr.pronunciation),
    "pt": re.compile(pt.pronunciation),
    "sv": re.compile(sv.pronunciation),
}

# Regex to find the genre
genre = {
    "ca": re.compile(ca.genre),
    "en": re.compile(defaults.genre),
    "es": re.compile(defaults.genre),
    "fr": re.compile(fr.genre),
    "pt": re.compile(pt.genre),
    "sv": re.compile(defaults.genre),
}

# Float number separator
float_separator = {
    "ca": ca.float_separator,
    "en": en.float_separator,
    "es": es.float_separator,
    "fr": fr.float_separator,
    "pt": pt.float_separator,
    "sv": sv.float_separator,
}

# Thousads separator
thousands_separator = {
    "ca": ca.thousands_separator,
    "en": en.thousands_separator,
    "es": es.thousands_separator,
    "fr": fr.thousands_separator,
    "pt": pt.thousands_separator,
    "sv": sv.thousands_separator,
}

# Markers for sections that contain interesting text to analyse.
section_patterns = {
    "ca": defaults.section_patterns,
    "en": defaults.section_patterns,
    "es": es.section_patterns,
    "fr": defaults.section_patterns,
    "pt": pt.section_patterns,
    "sv": defaults.section_patterns,
}
sublist_patterns = {
    "ca": defaults.sublist_patterns,
    "en": defaults.sublist_patterns,
    "es": es.sublist_patterns,
    "fr": defaults.sublist_patterns,
    "pt": defaults.sublist_patterns,
    "sv": defaults.sublist_patterns,
}
section_level = {
    "ca": defaults.section_level,
    "en": defaults.section_level,
    "es": defaults.section_level,
    "fr": defaults.section_level,
    "pt": pt.section_level,
    "sv": defaults.section_level,
}
section_sublevels = {
    "ca": defaults.section_sublevels,
    "en": en.section_sublevels,
    "es": defaults.section_sublevels,
    "fr": defaults.section_sublevels,
    "pt": pt.section_sublevels,
    "sv": defaults.section_sublevels,
}
head_sections = {
    "ca": ca.head_sections,
    "en": en.head_sections,
    "es": es.head_sections,
    "fr": fr.head_sections,
    "pt": pt.head_sections,
    "sv": sv.head_sections,
}
etyl_section = {
    "ca": ca.etyl_section,
    "en": en.etyl_section,
    "es": es.etyl_section,
    "fr": fr.etyl_section,
    "pt": pt.etyl_section,
    "sv": "",
}
sections = {
    "ca": ca.sections,
    "en": en.sections,
    "es": es.sections,
    "fr": fr.sections,
    "pt": pt.sections,
    "sv": sv.sections,
}

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = {
    "ca": ca.definitions_to_ignore,
    "en": en.definitions_to_ignore,
    "es": es.definitions_to_ignore,
    "fr": fr.definitions_to_ignore,
    "pt": pt.definitions_to_ignore,
    "sv": defaults.definitions_to_ignore,
}

# But some words need to be kept even if they would have been skipped by definitions_to_ignore
words_to_keep = {
    "ca": defaults.words_to_keep,
    "en": defaults.words_to_keep,
    "es": defaults.words_to_keep,
    "fr": fr.words_to_keep,
    "pt": defaults.words_to_keep,
    "sv": defaults.words_to_keep,
}

# The template name dealing with files in the Wikicode.
# [[Fichier:...|...|...|...]] (fr)
# [[File:...|...|...|...]] (fr)
# [[Fitxer:...|...|...]] (ca)
# [[Image:...|...|...]] (fr)
pattern_file = ("Fichier", "File", "Fitxer", "Image")

# Templates replacements: wikicode -> text conversion

# Templates to ignore: the text will be deleted.
templates_ignored = {
    "ca": ca.templates_ignored,
    "en": en.templates_ignored,
    "es": es.templates_ignored,
    "fr": fr.templates_ignored,
    "pt": pt.templates_ignored,
    "sv": defaults.templates_ignored,
}

# Templates that will be completed/replaced using italic style.
# Ex: {{absol}} -> <i>(Absolument)</i>
# Ex: {{absol|fr}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123|...}} -> <i>(Absolument)</i>
templates_italic = {
    "ca": ca.templates_italic,
    "en": en.templates_italic,
    "es": es.templates_italic,
    "fr": fr.templates_italic,
    "pt": pt.templates_italic,
    "sv": defaults.templates_italic,
}

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
templates_multi = {
    "ca": ca.templates_multi,
    "en": en.templates_multi,
    "es": es.templates_multi,
    "fr": fr.templates_multi,
    "pt": pt.templates_multi,
    "sv": sv.templates_multi,
}

# Templates that will be completed/replaced using custom style.
templates_other = {
    "ca": ca.templates_other,
    "en": defaults.templates_other,
    "es": defaults.templates_other,
    "fr": fr.templates_other,
    "pt": defaults.templates_other,
    "sv": defaults.templates_other,
}

# When a template is not handled by any previous template handlers,
# this method will be called with *parts* as argument.
last_template_handler = {
    "ca": ca.last_template_handler,
    "en": en.last_template_handler,
    "es": es.last_template_handler,
    "fr": fr.last_template_handler,
    "pt": pt.last_template_handler,
    "sv": defaults.last_template_handler,
}

# The full release description on GitHub:
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/$LOCALE
release_description = {
    "ca": ca.release_description,
    "en": en.release_description,
    "es": es.release_description,
    "fr": fr.release_description,
    "pt": pt.release_description,
    "sv": sv.release_description,
}

# Dictionary name that will be printed below each definition
wiktionary = {
    "ca": ca.wiktionary,
    "en": en.wiktionary,
    "es": es.wiktionary,
    "fr": fr.wiktionary,
    "pt": pt.wiktionary,
    "sv": sv.wiktionary,
}
