"""Greek language."""
from typing import Dict

# Regex to find the pronunciation
# {{ΔΦΑ|tɾeˈlos|γλ=el}}
# {{ΔΦΑ|γλ=el|ˈni.xta}}
pronunciation = r"{ΔΦΑ(?:\|γλ=el)?\|([^}\|]+)"
# Regex to find the gender
# '''{{PAGENAME}}''' {{θ}}
# '''{{PAGENAME}}''' {{ο}}
# '''{{PAGENAME}}''' {{α}}
# '''{{PAGENAME}}''' {{αθ}}
gender = r"'''{{PAGENAME}}''' \{\{([θαο]+)\}\}"

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{-el-}}",)
etyl_section = ["{{ετυμολογία}}"]
sections = (
    *head_sections,
    *etyl_section,
    "{{ουσιαστικό}",
    "{{ουσιαστικό|el}",
    "{{ρήμα}",
    "{{ρήμα|el}",
    "{{επίθετο}",
    "{{επίθετο|el}",
    "{{επίρρημα}",
    "{{επίρρημα|el}",
    "{{σύνδεσμος}",
    "{{σύνδεσμος|el}",
    "{{συντομομορφή}",
    "{{συντομομορφή|el}",
    "{{κύριο όνομα}",
    "{{κύριο όνομα|el}",
    "{{αριθμητικό}",
    "{{αριθμητικό|el}",
    "{{άρθρο}",
    "{{άρθρο|el}",
    "{{μετοχή}",
    "{{μετοχή|el}",
    "{{μόριο}",
    "{{μόριο|el}",
    "{{αντωνυμία}",
    "{{αντωνυμία|el}",
    "{{επιφώνημα}",
    "{{επιφώνημα|el}",
    "{{ρηματική έκφραση}",
    "{{επιρρηματική έκφραση}",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    "{{μορφή ουσιαστικού}",
    "{{μορφή ουσιαστικού|el}",
    "{{μορφή ρήματος}",
    "{{μορφή ρήματος|el}",
    "{{μορφή επιθέτου}",
    "{{μορφή επιθέτου|el}",
    "{{εκφράσεις}",
    "{{εκφράσεις|el}",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "el-κλίσ",
    "!",
    "R:TELETERM",
    "κλείδα-ελλ",
)

# Templates that will be completed/replaced using italic style.
templates_italic: Dict[str, str] = {}

# Templates more complex to manage.
templates_multi: Dict[str, str] = {
    # {{Term|statistica|it}}
    # "term": "small(term(parts[1]))",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/el
release_description = """\
Αριθμός λέξεων: {words_count}
Εξαγωγή Βικιλεξικού: {dump_date}

Διαθέσιμα αρχεία:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Ημερομηνία δημιουργίας: {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Βικιλεξικό (ɔ) {year}"
