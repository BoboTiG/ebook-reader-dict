"""German language (Deutsch)."""
from typing import Tuple

# Regex to find the pronunciation
pronunciation = r"{{Lautschrift\|([^}]+)}}"

# Regex to find the gender
gender = r",\s+{{([fmn]+)}}"

# Float number separator
float_separator = "."

# Thousads separator
thousands_separator = ","

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{Sprache|Deutsch}}", "{{sprache|deutsch}}")
etyl_section = ("{{Herkunft}}",)
sections = (
    *etyl_section,
    "{{Bedeutungen}",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = ()

# Templates to ignore: the text will be deleted.
templates_ignored = ("QS_Herkunft",)

# Templates that will be completed/replaced using italic style.
# templates_italic = {}

# Templates more complex to manage.
templates_multi = {
    # {{L|at||en}}
    "L": "parts[1]",
    # {{Ü|pl|dzień}}
    "Ü": "italic(parts[-1])",
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

    >>> last_template_handler(["default"], "de")
    '<i>(Default)</i>'
    """  # noqa
    from ..defaults import last_template_handler as default

    from .template_handlers import render_template, lookup_template

    if lookup_template(template[0]):
        return render_template(template)

    return default(template, locale, word=word)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/de
release_description = """\
Anzahl Worte: {words_count}
Wiktionary-Dump vom: {dump_date}

Verfügbare Wörterbuch-Formate:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df)

<sub>Aktualisiert am {creation_date}.</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"
