"""Italian language."""
from typing import Dict, Tuple

# Regex to find the pronunciation
pronunciation = r"{IPA\|/([^/]+)/"

# Regex to find the gender
gender = r"{{Pn\|?w?}} ''([fm])[singvol ]*''"

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

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    "{{verb form",
    "{{nome",
    #  "{{agg form",
    "{{sost form",
    "{{-sost form-",
    "{{It-conj",
)

# Templates to ignore: the text will be deleted.
templates_ignored: Tuple[str, ...] = tuple()

# Templates that will be completed/replaced using italic style.
templates_italic: Dict[str, str] = {}

# Templates more complex to manage.
templates_multi: Dict[str, str] = {
    # {{context|ecology|lang=it}}
    "context": "small(term(parts[1]))",
    # {{Est|raro|it}}
    "Est": "small(term('per estensione'))",
    # {{Etim-link|aggrondare}}
    # {{Etim-link||cervice}}
    "Etim-link": "'Vedi: ' + parts[2] if len(parts) == 3 else 'Vedi: ' + parts[1]",
    # {{Glossa|raro|it}}
    "Glossa": "small(term(parts[1]))",
    # {{la}}
    "la": "'latino'",
    # {{Lett|non comune|it}}
    "Lett": "small(term('letteralmente'))",
    # {{Nodef|it}}
    "Nodef": "'-definizione mancante-'",
    # {{Noetim||it}}
    "Noetim": "'-etimologia mancante-'",
    # {{Quote|...}}
    "Quote": "'«' + parts[1] + '» ' + term(parts[2])",
    # {{Tabs|aggrondato|aggrondati|aggrondata|aggrondate}}
    "Tabs": "'Masc. sing. ' + parts[1] + ', masc. plur. ' + parts[2] + ', fem. sing. ' + parts[3] + ', fem. plur. ' + parts[4]",  # noqa
    # {{Taxon|Chromis chromis|Chromis chromis}}
    "Taxon": "'la sua classificazione scientifica è ' + strong(italic(parts[1]))",
    # {{Term|statistica|it}}
    "Term": "small(term(parts[1]))",
    "term": "small(term(parts[1]))",
    # {{Vd|acre#Italiano|acre}}
    "Vd": "'Vedi: ' + parts[2]",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/it
release_description = """\
Numero di parole: {words_count}
Export Wiktionary: {dump_date}

File disponibili:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Aggiornato il {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wikizionario (ɔ) {year}"
