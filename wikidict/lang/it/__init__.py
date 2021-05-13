"""Italian language."""
from typing import Dict, Tuple

# Regex to find the pronunciation
pronunciation = r"{IPA\|/([^/]+)/"

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{-it-}}",)
etyl_section = ["{{etim}}"]
sections = (
    *head_sections,
    *etyl_section,
    "{{acron}",
    "{{agg}",
    "{{avv}",
    "{{avv}",
    "{{art}",
    "{{cong}",
    "{{inter}",
    "{{pref}",
    "{{Pn}",
    "{{prep}",
    "{{pron poss}",
    "{{suff}",
    "{{sost}",
    "{{verb}",
)

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = (
    "{{verb form",
    "{{nome",
    "{{agg form",
    "{{sost form",
    "{{It-conj",
)

# Templates to ignore: the text will be deleted.
templates_ignored: Tuple[str, ...] = tuple()

# Templates that will be completed/replaced using italic style.
templates_italic: Dict[str, str] = {}

# Templates more complex to manage.
templates_multi: Dict[str, str] = {}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/it
release_description = """\
Numero di parole: {words_count}
Export Wiktionary: {dump_date}

Files disponibili:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Aggiornato il {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wikizionario (ɔ) {year}"
