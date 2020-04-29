"""Internationalization stuff."""

from . import fr

# Markers for sections of the current locale
language = {
    "fr": fr.patterns,
}

# Templates to skip in the wikicode -> text conversion
ignored_templates = {
    "fr": fr.ignored_templates,
}

# Release description sentences
release_tr = {
    "fr": fr.release_tr,
}

# Minimum dictionary size
size_min = {
    "fr": fr.size_min,
}
