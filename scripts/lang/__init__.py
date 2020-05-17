"""Internationalization stuff."""

from . import fr

# Markers for sections that contain interesting text to analyse.
patterns = {
    "fr": fr.patterns,
}

# The template name dealing with files in the Wikicode.
# Ex: (fr) [[Fichier:...|...|...|...]]
pattern_file = ("Fichier",)

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
# It is possible to use any Python fonction and ones defined in utils.py.
#
# Available arguments:
#   - *tpl* (string) containg the template name.
#   - *parts* (list of strings) containing the other parts of the template.
#
# Example with the complete template "{{comparatif de|bien|fr|adv}}":
#   - *tpl* will contain the string "comparatif de".
#   - *parts* will contain the list ["bien", "fr", "adv"].
#
# You can access to *tpl* and *parts* to apply changes and get the result wanted.
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

# Translations
translations = {
    "fr": fr.translations,
}

# Dictionary name that will be printed below each definition
wiktionary = {
    "fr": fr.wiktionary,
}
