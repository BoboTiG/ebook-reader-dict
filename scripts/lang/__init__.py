"""Internationalization stuff."""

from . import fr

# Markers for sections of the current locale
language = {
    "fr": fr.patterns,
}

# Minimum dictionary size
size_min = {
    "fr": fr.size_min,
}

# Templates replacements: wikicode -> text conversion
templates = {
    "fr": fr.templates,
}
templates_multi = {
    "fr": fr.templates_multi,
}

# Templates to ignore
templates_ignored = {
    "fr": fr.templates_ignored,
}

# Translations
translations = {
    "fr": fr.translations,
}
