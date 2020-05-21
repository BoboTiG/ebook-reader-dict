"""Internationalization stuff."""
import re

from . import fr
from .fr.langs import langs as FR

# A list of all languages translated into different locales
all_langs = {
    "fr": FR,
}

# Regex to find the pronunciation
pronunciation = {
    "fr": re.compile(fr.pronunciation),
}

# Regex to find the genre
genre = {
    "fr": re.compile(fr.genre),
}

# Markers for sections that contain interesting text to analyse.
patterns = {
    "fr": fr.patterns,
}

# The template name dealing with files in the Wikicode.
# [[Fichier:...|...|...|...]] (fr)
# [[File:...|...|...|...]] (fr)
# [[Image:...|...|...]] (fr)
pattern_file = ("Fichier", "File", "Image")

# Templates replacements: wikicode -> text conversion

# Templates to ignore: the text will be deleted.
templates_ignored = {
    "fr": fr.templates_ignored,
}

# Templates that will be completed/replaced using italic style.
# Ex: {{absol}} -> <i>(Absolument)</i>
# Ex: {{absol|fr}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123}} -> <i>(Absolument)</i>
# Ex: {{absol|fr|123|...}} -> <i>(Absolument)</i>
templates_italic = {
    "fr": fr.templates_italic,
}

# Templates more complex to manage. More work is needed.
# The code on the right will be passed to a function that will execute it.
# It is possible to use any Python fonction and ones defined in user_functions.py.
#
# Available arguments:
#   - *tpl* (string) containg the template name.
#   - *parts* (list of strings) containing the all parts of the template.
#
# Example with the complete template "{{comparatif de|bien|fr|adv}}":
#   - *tpl* will contain the string "comparatif de".
#   - *parts* will contain the list ["comparatif de", "bien", "fr", "adv"].
#
# You can access to *tpl* and *parts* to apply changes and get the result wanted.
#
# Available functions are documented into that HTML file:
#   html/scripts/user_functions.html
templates_multi = {
    "fr": fr.templates_multi,
}

# Templates that will be completed/replaced using custom style.
templates_other = {
    "fr": fr.templates_other,
}

# A warning will be printed when a template contains superfuous spaces,
# except for those listed bellow:
template_warning_skip = {
    "fr": fr.template_warning_skip,
}

# Float number separator
float_separator = {
    "fr": fr.float_separator,
}

# Thousads separator
thousands_separator = {
    "fr": fr.thousands_separator,
}

# Release content on gitHub
release_description = {
    "fr": fr.release_description,
}

# Dictionary name that will be printed below each definition
wiktionary = {
    "fr": fr.wiktionary,
}
