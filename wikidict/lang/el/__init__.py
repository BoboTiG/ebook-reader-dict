"""Greek language."""
import re
from typing import Dict, List, Pattern, Tuple

from ...user_functions import flatten, uniq

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{-el-}}",)
etyl_section = ("{{ετυμολογία}}",)
section_patterns = (r"\#", r"\*")
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

# Templates more complex to manage.
templates_multi: Dict[str, str] = {
    # {{resize|Βικιλεξικό|140}}
    "resize": "f'<span style=\"font-size:{parts[2]}%;\">{parts[1]}</span>'",
}


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/el
release_description = """\
Αριθμός λέξεων: {words_count}
Εξαγωγή Βικιλεξικού: {dump_date}

Διαθέσιμα αρχεία:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Ημερομηνία δημιουργίας: {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Βικιλεξικό (ɔ) {year}"


_genders = {
    "θ": "θηλυκό",
    "α": "αρσενικό",
    "αθ": "αρσενικό ή θηλυκό",
    "αθο": "αρσενικό, θηλυκό, ουδέτερο",
    "ακλ": "άκλιτο",
    "καθ": "(καθαρεύουσα)",
    "ο": "ουδέτερο",
}


def find_genders(
    code: str,
    pattern: Pattern[str] = re.compile(
        r"'''{{PAGENAME}}'''\s*(?:{{([θαοκλ]+)(?:\|([θαοκλ]+))*}})[,|\s]*(?:{{([θαοκλ]+)(?:\|([θαοκλ]+))*}})*"
    ),
) -> List[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("'''{{PAGENAME}}''' {{αθ}}")
    ['αρσενικό ή θηλυκό']
    >>> find_genders("'''{{PAGENAME}}''' {{αθ}}, {{ακλ|αθ}}")
    ['αρσενικό ή θηλυκό', 'άκλιτο']
    >>> find_genders("'''{{PAGENAME}}''' {{ακλ|αθ}}, {{αθ}}")
    ['άκλιτο', 'αρσενικό ή θηλυκό']
    """
    return [_genders[g] for g in uniq(flatten(pattern.findall(code)))]


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(r"{ΔΦΑ(?:\|γλ=el)?\|([^}\|]+)"),
) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{ΔΦΑ|tɾeˈlos|γλ=el}}")
    ['tɾeˈlos']
    >>> find_pronunciations("{{ΔΦΑ|γλ=el|ˈni.xta}}")
    ['ˈni.xta']
    """
    return uniq(pattern.findall(code))


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["γραπτηεμφ", "1889"], "el")
        '<i>(η λέξη μαρτυρείται από το 1889)</i>'
        >>> last_template_handler(["γραπτηεμφ", "1889", "0=-"], "el")
        'η λέξη μαρτυρείται από το 1889'

        >>> last_template_handler(["λενδ", "el", "fr"], "el")
        'λόγιο ενδογενές δάνειο:'
        >>> last_template_handler(["λενδ", "el", "fr", "0=-"], "el")
        'λόγιο ενδογενές δάνειο'
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

    if tpl == "λενδ":
        phrase = "λόγιο ενδογενές δάνειο"
        if not data["0"]:
            phrase += ":"
        return phrase

    if tpl == "κτεπε":
        phrase = "κατʼ επέκταση"
        if not data["0"]:
            phrase = term(phrase)
        return phrase

    return default(template, locale, word)
