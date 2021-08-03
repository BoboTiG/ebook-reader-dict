"""Greek language."""
from typing import Dict, Tuple

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
    # {{resize|Βικιλεξικό|140}}
    "resize": "f'<span style=\"font-size:{parts[2]}%;\">{parts[1]}</span>'",
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["γραπτηεμφ", "1889"], "el")
        '<i>(η λέξη μαρτυρείται από το 1889)</i>'
        >>> last_template_handler(["γραπτηεμφ", "1889", "0=-"], "el")
        'η λέξη μαρτυρείται από το 1889'
    """
    from ...user_functions import extract_keywords_from, term
    from ..defaults import last_template_handler as default

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "γραπτηεμφ":
        phrase = f"η λέξη μαρτυρείται από το {parts[0]}"
        if not data["0"]:
            phrase = term(phrase)
        return phrase

    return default(template, locale, word)


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
