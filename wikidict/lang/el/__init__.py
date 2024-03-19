"""Greek language."""

import re
from collections import defaultdict
from typing import Dict, List, Pattern, Tuple, Union

from ...user_functions import extract_keywords_from, italic, term, uniq
from .langs import langs

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
    "{{φράση}",
    "{{φράση|el}",
    "{{έκφραση}",
    "{{έκφραση|el}",
    "{{παροιμία}",
    "{{παροιμία|el}",
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
    "θο": "θηλυκό ή ουδέτερο",
    "αο": "αρσενικό ή ουδέτερο",
    "ακρ": "ακρωνύμιο",
}


def find_genders(
    code: str,
    pattern: Pattern[str] = re.compile(r"{{([^{}]*)}}"),
    line_pattern: str = "'''{{PAGENAME}}''' ",
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
    >>> find_genders("'''{{PAGENAME}}''' {{θο}} {{ακλ}}")
    ['θηλυκό ή ουδέτερο', 'άκλιτο']
    >>> find_genders("'''{{PAGENAME}}''' {{αο}} {{ακλ}} {{ακρ}}")
    ['αρσενικό ή ουδέτερο', 'άκλιτο', 'ακρωνύμιο']
    """
    return [
        _genders[gender.split("|")[0]]
        for line in code.splitlines()
        for gender in pattern.findall(line[len(line_pattern) :])
        if line.startswith(line_pattern)
    ]


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(r"{ΔΦΑ(?:\|γλ=el)?(?:\|el)?\|([^}\|]+)"),
) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{ΔΦΑ|tɾeˈlos|γλ=el}}")
    ['/tɾeˈlos/']
    >>> find_pronunciations("{{ΔΦΑ|γλ=el|ˈni.xta}}")
    ['/ˈni.xta/']
    >>> find_pronunciations("{{ΔΦΑ|el|ˈni.ði.mos}}")
    ['/ˈni.ði.mos/']
    """
    return [f"/{p}/" for p in uniq(pattern.findall(code))]


def text_language(lang_donor_iso: str, myargs: Dict[str, str] = defaultdict(str)) -> str:
    """
    see https://el.wiktionary.org/w/index.php?title=Module:%CE%B5%CF%84%CF%85%CE%BC%CE%BF%CE%BB%CE%BF%CE%B3%CE%AF%CE%B1&oldid=6368956 link_language function
    """  # noqa
    lang: Dict[str, Union[str, bool]] = langs[lang_donor_iso]
    lang_donor = str(lang["name"])  # neuter plural γαλλικά (or fem.sing. μέση γερμανκή)
    lang_donor_frm = str(lang["frm"])  # feminine accusative singular γαλλική
    if lang_donor != "" and lang_donor_frm != "":
        # feminine article + accusative singular τη γαλλική
        lang_donor_apo = str(lang["apo"])
        # προέλευσης από +apota -- FOR FAMILIES: σημιτικής προέλευσης
        lang_donor_from = str(lang["from"])
        if myargs["root"] == "1" or myargs["ρίζα"] == "1":
            mytext = f"{italic(lang_donor_frm)} <i>ρίζα</i>"
        elif lang["family"]:
            mytext = italic(lang_donor_from)
        elif myargs["text"] == "1" or myargs["κειμ"] == "1":
            mytext = italic(lang_donor_apo)
        else:
            mytext = italic(lang_donor_frm)

    return mytext


def labels_output(text_in: str, args: Dict[str, str] = defaultdict(str)) -> str:
    """
    from https://el.wiktionary.org/w/index.php?title=Module:labels&oldid=5634715
    """
    from .aliases import aliases
    from .labels import labels as data

    mytext = ""

    label = args.get("label") or args.get("topic") or args.get("ετικέτα") or ""

    alias = ""
    if label in aliases:
        alias = label
        label = aliases[alias]

    text = text_in or args["1"]
    term = args["όρος"] or args["term"] or ""
    show = args["εμφ"] or args["show"] or ""
    noparenthesis = args["0"]
    if not label or label is None:
        return ""
    nodisplay = args["nodisplay"] or args["000"]
    if nodisplay == "" and data.get(label, {}).get("link") != "πατρότητα":
        if term != "":
            mytext = term
        elif text != "":
            mytext = text
        else:
            mytext = f"{show}" if show != "" else f'{italic(data[label]["linkshow"])}'
        mytext = mytext if noparenthesis != "" else f"({mytext})"
    return mytext


def last_template_handler(template: Tuple[str, ...], locale: str, word: str = "") -> str:
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

        >>> last_template_handler(["λδδ", "grc", "el", "νήδυμος"], "el")
        '(διαχρονικό δάνειο) <i>αρχαία ελληνική</i> νήδυμος'

        >>> last_template_handler(["λ", "ἡδύς", "grc"], "el")
        'ἡδύς'

        >>> last_template_handler(["ετ", "ιατρική"], "el")
        '(<i>ιατρική</i>)'
        >>> last_template_handler(["ετ", "ιατρική", "0=-"], "el")
        '<i>ιατρική</i>'

        >>> last_template_handler(["λόγιο"], "el")
        '(<i>λόγιο</i>)'

        >>> last_template_handler(["ουσ"], "el")
        '(<i>ουσιαστικοποιημένο</i>)'

    """
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

    if tpl in ["λδδ", "dlbor"]:
        phrase = "(διαχρονικό δάνειο) "
        phrase += text_language(parts[0], data)
        phrase += f" {data['1'] or parts[2]}"
        return phrase

    if tpl in ["λ", "l", "link"]:
        return parts[0]

    if tpl in ["ετ", "ετικέτα"]:
        data["label"] = parts[0]
        return labels_output(data.get("text", ""), data)

    if tpl == "λόγιο":
        data["label"] = tpl
        return labels_output("", data)

    if tpl == "ουσ":
        text = italic("ουσιαστικοποιημένο")
        return text if data["0"] else f"({text})"

    return default(template, locale, word)
