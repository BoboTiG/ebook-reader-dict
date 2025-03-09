"""Greek language."""

import re
from collections import defaultdict

from ...user_functions import italic, uniq
from .aliases import aliases
from .langs import langs

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{-el-}}",)
etyl_section = ("{{ετυμολογία}}",)
section_sublevels = (3, 4)
section_patterns = ("#", r"\*")
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
    "{{επίθημα}",
    "{{επίθημα|el}",
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
    "{{πρόθημα}",
    "{{πρόθημα|el}",
)

# Variants
variant_titles = sections
variant_templates = (
    "{{infl",
    "{{θηλ του",
    "{{κλ|",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    *variant_templates,
    "{{μορφή ουσιαστικού",
    "{{μορφή ρήματος",
    "{{μορφή επιθέτου}",
    "{{εκφράσεις",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "audio",
    "cat",
    "cf",
    "el-κλίσ",
    "el-κλίση-'ναός'",
    "el-κλίσ-'μανάβης'",
    "el-κλίση-'γιατρός'",
    "el-κλίση-'σοφία'",
    "el-κλίση-'παιδί'",
    "el-κλίση-'όμορφος'",
    "el-κλίσ-'ναύτης'",
    "el-κλίσ-'ωραίος'",
    "!",
    "R:TELETERM",
    "κλείδα-ελλ",
    "λείπει η ετυμολογία",
    "περίοδος",
    "από",
    "ετυ+",
    "λείπει ο ορισμός",
    "Βικιπαίδεια",
    "λείπει η κλίση",
    "χρειάζεται παράθεμα",
    "χρειάζεται προσοχή",
    "χρειάζεται τεκμηρίωση",
    "λείπει η μετάφραση",
    "clear",
    "πολυτ γραφή",
    "wlogo",
)

# Templates more complex to manage.
templates_multi: dict[str, str] = {
    # {{IPAchar|/ˈsɛləteɪp/}}
    "IPAchar": "parts[1]",
    # {{IPAstyle|ˈɑɹ.kən.sɔ}}
    "IPAstyle": "parts[1]",
    # {{resize|Βικιλεξικό|140}}
    "resize": "f'<span style=\"font-size:{parts[2]}%;\">{parts[1]}</span>'",
    # {{uni-script|ΛVΛV}}
    "uni-script": "parts[1]",
    # {{κνε}}
    "κνε": "italic('κοινή νεοελληνική')",
    # {{ιε}}
    "ιε": "italic('πρωτοϊνδοευρωπαϊκή ρίζα')",
    # {{νε}}
    "νε": "italic('νέα ελληνική')",
    # {{ουδ του|λέξη}}
    "ουδ του": "italic('ουδέτερο του') + ' ' + strong(parts[1])",
    # {{αιτ}}
    "αιτ": "italic(strong('αιτιατική'))",
    # {{λ2||τοπωνύμιο|τοπωνύμια}}
    "λ2": "parts[-1]",
    # {{β|lang=fr|Motosacoche}}
    "β": "parts[-1]",
    # {{θηλ ισσα|Αβαριτσιώτης|Αβαριτσιώτ(ης)}}
    "θηλ ισσα": 'f"{parts[-1]} + κατάληξη θηλυκού -ισσα"',
    # {{θηλ τρια|διευθυντής|διευθυντ(ής)}}
    "θηλ τρια": 'f"{parts[-1]} + κατάληξη θηλυκού -τρια"',
    # {{θηλ τρα|ψεύτης|ψεύ(της)}}
    "θηλ τρα": 'f"{parts[-1]} + κατάληξη θηλυκού -τρα"',
    # {{θηλ α|Κερκυραίος|Κερκυραί(ος)}}
    "θηλ α": 'f"{parts[-1]} + κατάληξη θηλυκού -α"',
    # {{θηλ ιστρια|εγωιστής|εγω(ιστής)}}
    "θηλ ιστρια": 'f"{parts[-1]} + κατάληξη θηλυκού -ίστρια"',
    # {{θηλ ού|μερακλής|μερακλ(ής)}}
    "θηλ ού": 'f"{parts[-1]} + κατάληξη θηλυκού -ού"',
    # {{θηλ ίνα|μερακλής|μερακλ(ής)}}
    "θηλ ίνα": 'f"{parts[-1]} + κατάληξη θηλυκού -ίνα"',
    # {{θηλ ιδα|προστάτης|προστάτ(ης)}}
    "θηλ ιδα": 'f"{parts[-1]} + κατάληξη θηλυκού -ιδα"',
}
# Alias
templates_multi["ουδ_του"] = templates_multi["ουδ του"]

# Templates that will be completed/replaced using custom style.
templates_other = {
    "*": "*",
    "gag": "γκαγκαούζ",
    "odt": "παλαιά ολλανδικά",
    "orv": "αρχαία ανατολική σλαβική γλώσσα",
    "osp": "παλαιά ισπανική",
    "oty": "αρχαία ταμίλ",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/el
release_description = """\
Αριθμός λέξεων: {words_count}
Εξαγωγή Βικιλεξικού: {dump_date}

Πλήρης έκδοση:
{download_links_full}

Έκδοση χωρίς ετυμολογία:
{download_links_noetym}

<sub>Ημερομηνία δημιουργίας: {creation_date}</sub>
"""

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
    *,
    pattern: re.Pattern[str] = re.compile(r"{{([^{}]*)}}"),
    line_pattern: str = "'''{{PAGENAME}}''' ",
) -> list[str]:
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
    >>> find_genders("'''{{PAGENAME}}''' {{α}} ({{ετ|ιδιωματικό|0=-}}, Κάλυμνος)")
    ['αρσενικό']
    """
    return [
        g
        for line in code.splitlines()
        for gender in pattern.findall(line[len(line_pattern) :])
        if line.startswith(line_pattern) and (g := _genders.get(gender.split("|")[0]))
    ]


def find_pronunciations(
    code: str,
    *,
    pattern: re.Pattern[str] = re.compile(r"{ΔΦΑ(?:\|γλ=el)?(?:\|el)?\|([^}\|]+)"),
) -> list[str]:
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


def text_language(lang_iso: str, *, args: dict[str, str] = defaultdict(str)) -> str:
    """
    see https://el.wiktionary.org/w/index.php?title=Module:%CE%B5%CF%84%CF%85%CE%BC%CE%BF%CE%BB%CE%BF%CE%B3%CE%AF%CE%B1&oldid=6368956 link_language function
    """
    lang: dict[str, str | bool] = langs[lang_iso]
    lang_name = str(lang["name"])  # neuter plural γαλλικά (or fem.sing. μέση γερμανκή)
    lang_frm = str(lang["frm"])  # feminine accusative singular γαλλική
    text = ""
    if lang_name and lang_frm:
        # feminine article + accusative singular τη γαλλική
        lang_donor_apo = str(lang["apo"])
        # προέλευσης από +apota -- FOR FAMILIES: σημιτικής προέλευσης
        lang_donor_from = str(lang["from"])
        if args["root"] == "1" or args["ρίζα"] == "1":
            text = f"{italic(lang_frm)} <i>ρίζα</i>"
        elif lang["family"]:
            text = italic(lang_donor_from)
        elif args["text"] == "1" or args["κειμ"] == "1":
            text = italic(lang_donor_apo)
        else:
            text = italic(lang_frm)

    return text


def labels_output(text_in: str, *, args: dict[str, str] = defaultdict(str)) -> str:
    """
    from https://el.wiktionary.org/w/index.php?title=Module:labels&oldid=5634715
    """
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

    if not nodisplay:
        if term != "":
            mytext = term
        elif text != "":
            mytext = text
        elif all_labels := data.get(label):
            if isinstance(all_labels, list):
                all_labels = all_labels[0]
            if all_labels.get("link") not in {None, "πατρότητα"}:
                mytext = show or f"{italic(all_labels['linkshow'])}"
        mytext = mytext if noparenthesis else f"({mytext})"
    return mytext


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    missed_templates: list[tuple[str, str]] | None = None,
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

        >>> last_template_handler(["λδδ", "grc", "el", "νήδυμος"], "el")
        '(διαχρονικό δάνειο) <i>αρχαία ελληνική</i> νήδυμος'
        >>> last_template_handler(["λδδ", "grc-koi", "el"], "el")
        '(διαχρονικό δάνειο) <i>ελληνιστική κοινή</i>'
        >>> last_template_handler(["λδδ", "0=-", "grc-koi", "el", "τεχνικός"], "el")
        '<i>ελληνιστική κοινή</i> τεχνικός'

        >>> last_template_handler(["λ", "ἡδύς", "grc"], "el")
        'ἡδύς'
        >>> last_template_handler(["λ"], "el", word="Ινδία")
        'Ινδία'
        >>> last_template_handler(["l", "Иваново", "ru", "lang=4", "tnl=Ιβάνοβο -του Ιβάν-, πόλη της Ρωσίας"], "el")
        '<i>ρωσική</i> Иваново (Ιβάνοβο -του Ιβάν-, πόλη της Ρωσίας)'
        >>> last_template_handler(["l", "acur", "tr=", "lang=4"], "el")
        '<i>νέα ελληνική</i> acur'

        >>> last_template_handler(["ετ"], "el")
        ''
        >>> last_template_handler(["ετ", "ιατρική"], "el")
        '(<i>ιατρική</i>)'
        >>> last_template_handler(["ετ", "ιατρική", "0=-"], "el")
        '<i>ιατρική</i>'
        >>> last_template_handler(["ετ", "ιατρική", "en"], "el")
        '<i>ιατρική</i>'
        >>> last_template_handler(["ετ", "ιατρική", "", "ιατρικών όρων", "0=-"], "el")
        'ιατρικών όρων'

        >>> last_template_handler(["λόγιο"], "el")
        '(<i>λόγιο</i>)'

        >>> last_template_handler(["ουσ"], "el")
        '<i>(ουσιαστικοποιημένο)</i>'

        >>> last_template_handler(["ετυμ", "ine-pro"], "el")
        '<i>πρωτοϊνδοευρωπαϊκή</i>'
        >>> last_template_handler(["ετυμ", "gkm"], "el")
        '<i>μεσαιωνική ελληνική</i>'
        >>> last_template_handler(["ετυμ", "μσν"], "el")
        '<i>μεσαιωνική ελληνική</i>'
        >>> last_template_handler(["ετυμ", "grc", "el", "ἔλαιον"], "el")
        '<i>αρχαία ελληνική</i> ἔλαιον'
        >>> last_template_handler(["ετυμ", "sla"], "el")
        '<i>σλαβικής προέλευσης</i>'
        >>> last_template_handler(["ετυμ", "yua"], "el")
        ''
        >>> last_template_handler(["ετυμ", "ar", "el", "آجُرّ", "tr=ʾājurr"], "el")
        '<i>αραβική</i> آجُرّ (ʾājurr)'

        >>> last_template_handler(["γρ", "τραπεζομάντιλο"], "el")
        '<i>άλλη γραφή του</i> <b>τραπεζομάντιλο</b>'
        >>> last_template_handler(["γρ", "ελαιόδενδρο", "μορφή"], "el")
        '<i>άλλη μορφή του</i> <b>ελαιόδενδρο</b>'
        >>> last_template_handler(["γρ", "ελαιόδενδρο", "πολυ", "εμφ=ελαιόδενδρο(ν)"], "el")
        '<i>πολυτονική γραφή του</i> <b>ελαιόδενδρο(ν)</b>'
        >>> last_template_handler(["γρ", "ποιέω", "ασυν", "grc"], "el")
        '<i>ασυναίρετη μορφή του</i> <b>ποιέω</b>'
        >>> last_template_handler(["γρ", "ποιέω", "ασυν", "grc", "εμφ=ποι-έω"], "el")
        '<i>ασυναίρετη μορφή του</i> <b>ποι-έω</b>'
        >>> last_template_handler(["γρ", "colour", "", "en"], "el")
        '<i>άλλη γραφή του</i> <b>colour</b>'
        >>> last_template_handler(["γρ", "colour", "freestyle text", "en"], "el")
        '<i>freestyle text</i> <b>colour</b>'

        >>> last_template_handler(["πρόσφ", "μαλλί", "-ης"], "el")
        'μαλλί + -ης'
        >>> last_template_handler(["πρόσφ", "μαλλί", ".1=μαλλ(ί)", "-ης"], "el")
        'μαλλ(ί) + -ης'

        >>> last_template_handler(["αρχ"], "el")
        '<i>αρχαία ελληνική</i>'
        >>> last_template_handler(["αρχ", "ὅπου"], "el")
        '<i>αρχαία ελληνική</i> ὅπου'

        >>> last_template_handler(["μσν"], "el")
        '<i>μεσαιωνική ελληνική</i>'
        >>> last_template_handler(["μσν", "ὅπου"], "el")
        '<i>μεσαιωνική ελληνική</i> ὅπου'

        >>> last_template_handler(["fr"], "el")
        'γαλλικά'

        >>> last_template_handler(["γραφή του", "άσος"], "el")
        '<i>άλλη γραφή του</i> <b>άσος</b>'
        >>> last_template_handler(["γραφή του", "αγάρ", "μορφ"], "el")
        '<i>άλλη μορφή του</i> <b>αγάρ</b>'

        >>> last_template_handler(["ετικ", "γαστρονομία", "τρόφιμα", "γλυκά"], "el")
        '(<i>γαστρονομία</i>, <i>τρόφιμα</i>, <i>γλυκό</i>)'
        >>> last_template_handler(["ετικ", "βιολ", "ιατρ"], "el")
        '(<i>βιολογία</i>, <i>ιατρική</i>)'

        >>> last_template_handler(["desc", "el", "πάρτι", "δαν"], "el")
        '↷ <i>νέα ελληνικά:</i> πάρτι'
        >>> last_template_handler(["απόγ", "el", "πάρτι", "δαν"], "el")
        '↷ <i>νέα ελληνικά:</i> πάρτι'
        >>> last_template_handler(["απόγ", "σύμβολο=δαν"], "el")
        '↷'

        #
        # Variants
        #
        >>> last_template_handler(["infl", "grc", "ε=απρ", "χ=ενε", "γίγνομαι"], "el")
        'γίγνομαι'
        >>> last_template_handler(["θηλ του", "λέξη"], "el")
        'λέξη'
        >>> last_template_handler(["θηλ του-πτώσειςΟΑΚεν", "γκαντέμης"], "el")
        'γκαντέμης'
        >>> last_template_handler(["κλ", "", "σχολείο", "π=γ", "α=π"], "el")
        'σχολείο'
    """
    from ...user_functions import concat, extract_keywords_from, italic, strong, term
    from .. import defaults
    from .template_handlers import lookup_template, render_template

    if lookup_template(template[0]):
        return render_template(word, template)

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "γραφή του":
        if len(parts) == 1:
            parts.append("γραφ")
        return f"{italic('άλλη ' + parts[1] + 'ή του')} {strong(parts[0])}"

    if tpl in {"λδδ", "dlbor"}:
        phrase = "" if data["0"] else "(διαχρονικό δάνειο) "
        phrase += text_language(parts[0], args=data)
        if rest := data["1"] or parts[2] if len(parts) > 2 else "":
            phrase += f" {rest}"
        return phrase

    if tpl in {"λ", "l", "link"}:
        text = ""
        if data["lang"]:
            text += f"{text_language(parts[1]) if len(parts) > 1 else italic('νέα ελληνική')} "
        text += parts[0] if parts else word
        if tnl := data["tnl"]:
            text += f" ({tnl})"
        return text

    if tpl in {"απόγ", "desc"}:
        text = "↷"
        if data["σύμβολο"] == "δαν":
            return text
        text += f" {italic(str(langs[parts[0]]['name']) + ':')} {parts[1]}"
        return text

    if tpl in {"ετ", "ετικέτα"}:
        if not parts:
            return ""
        if len(parts) <= 2:
            data["label"] = parts[0]
        else:
            data["label"] = parts[2]
            data["text"] = parts[2]

        # No parenthesis when more than one part (non-Greek words)
        if len(parts) > 1 and "0" not in data:
            data["0"] = "-"

        return labels_output(data.get("text", ""), args=data)

    if tpl == "ετικ":
        return f"({', '.join(italic(aliases.get(part, part)) for part in parts)})"

    if tpl == "ετυμ":
        text = text_language(parts[0])
        if len(parts) > 2:
            text += f" {parts[2]}"
        if tr := data["tr"]:
            text += f" ({tr})"
        return text

    if tpl == "λόγιο":
        data["label"] = tpl
        return labels_output("", args=data)

    if text := {
        "λενδ": "λόγιο ενδογενές δάνειο",
        "βλφρ": "δείτε την έκφραση",
    }.get(tpl, ""):
        if not data["0"]:
            text += ":"
        return text

    if text := {
        "αρχ": "αρχαία ελληνική",
        "μσν": "μεσαιωνική ελληνική",
    }.get(tpl, ""):
        phrase = italic(text)
        if parts:
            phrase += f" {parts[0]}"
        return phrase

    if text := {
        "γραπτηεμφ": f"η λέξη μαρτυρείται από το {parts[0] if parts else ''}",
        "μτφρ": "μεταφορικά",
        "κτεπε": "κατʼ επέκταση",
        "μτβ": "μεταβατικό",
        "αμτβ": "αμετάβατο",
        "ουσ": "ουσιαστικοποιημένο",
        "νεολ": "νεολογισμός",
        "μπφ": "μέση-παθητική φωνή του ρήματος",
        "μτβ+αμτβ": "μεταβατικό και αμετάβατο",
        "μτγν": "ελληνιστική",
        "μτγρ": "μεταγραφή",
        "μτχα": "μετοχή παθητικού αορίστου",
        "μτχπα": "μετοχή παθητικού αορίστου",
        "μτχε": "μετοχή παθητικού ενεστώτα",
        "μτχπε": "μετοχή παθητικού ενεστώτα",
        "μτχεα": "μετοχή ενεργητικού αορίστου",
        "μτχεε": "μετοχή ενεργητικού ενεστώτα",
        "μτχεμ": "μετοχή ενεργητικού μέλλοντα",
        "μτχεπ": "μετοχή ενεργητικού παρακειμένου",
        "μτχμα": "μετοχή μέσου αορίστου",
        "μτχπ": "μετοχή παρακειμένου",
        "μτχπμ": "μετοχή παθητικού μέλλοντα",
        "μτχπp": "μετοχή παθητικού παρακειμένου",
        "μτχππ": "μετοχή παθητικού παρακειμένου",
        "μτχππαναδ": "μετοχή παθητικού παρακειμένου",
        "μτχχρ": "μετοχή παθητικού παρακειμένου",
        "μυθολ": "μυθολογία",
        "παρετυμολογία": "παρετυμολογία",
        "συνηθ": "πιο συνηθισμένο",
        "σπαν": "σπάνιο",
        "σπάν": "σπάνιο",
        "καταχρ": "καταχρηστικά",
        "σνκδ": "συνεκδοχικά",
        "μειωτ": "μειωτικό",
        "ορθοδ": "ορθοδοξία",
        "θρησκεία": "θρησκεία",
        "χυδαίο": "χυδαίο",
        "λαϊκότροπο": "λαϊκότροπο",
        "οεν": "ουδέτερο",
        "οικ": "οικείο",
        "απρόσωπο": "απρόσωπο",
        "αργκ": "αργκό",
        "αργκό": "αργκό",
        "παρωχ": "παρωχημένο",
        "ειδικ": "ειδικότερα",
        "ειδικότερα": "ειδικότερα",
        "ειρων": "ειρωνικό",
        "ειρωνικά": "ειρωνικό",
        "ειρωνικό": "ειρωνικό",
        "κυριολ": "κυριολεκτικά",
        "κυριολ+μτφρ": "κυριολεκτικά και μεταφορικά",
        "ετυμ en": "αγγλική",
        "ετυμ fr": "γαλλική",
        "ετυμ_en": "αγγλική",
        "ετυμ_fr": "γαλλική",
        "κυριολεκτικά": "κυριολεκτικά",
        "καθ κοινή": "καθαρεύουσα",
        "καθ μεσ": "καθαρεύουσα",
        "καθαρεύουσα": "καθαρεύουσα",
        "κατ' επέκταση": "κατ' επέκταση",
        "γενικότερα": "γενικότερα",
        "αρχαιοπρεπές": "αρχαιοπρεπές",
        "δημοτική": "δημοτική",
        "δοτική": "δοτική",
        "επτανησιακά": "επτανησιακά",
        "επώνυμο": "επώνυμο",
        "καταχρηστικά": "καταχρηστικά",
        "κεφαλονίτικα": "κεφαλονίτικα",
        "ετυμολογία": "ετυμολογία",
        "σπάνιο": "σπάνιο",
        "συγγενή": "συγγενή",
        "σημειώσεις συντακτών": "σημειώσεις συντακτών",
        "σημειώσεις": "σημειώσεις",
        "σημείωση": "σημείωση",
        "προσφώνηση": "προσφώνηση",
        "προσχέδιο": "προσχέδιο",
        "προφορικό": "προφορικό",
        "μεταβατικό": "μεταβατικό",
        "μεταφορικά": "μεταφορικά",
        "μορφολογικά": "μορφολογικά",
        "νεολογισμός": "νεολογισμός",
        "οικείο": "οικείο",
        "όνομα": "όνομα",
        "παιδιά": "παιδιά",
        "παράθεμα": "παράθεμα",
        "παρωχημένο": "παρωχημένο",
        "αρχαιοπρ": "αρχαιοπρεπές",
        "αττ": "αττικός τύπος",
        "συνεκδοχικά": "συνεκδοχικά",
        "ταυτόσημα": "ταυτόσημα",
        "δημ la": "δημώδης λατινική",
        "δημοτ": "δημοτική",
        "δωρ": "δωρικός τύπος",
        "χυδ": "χυδαίο",
        "US": "ΗΠΑ",
        "ΗΠΑ": "ΗΠΑ",
        "UK": "ΗΒ",
        "USA": "ΗΠΑ",
        "λογοτ": "λογοτεχνικό",
        "λοκ": "λοκρικός τύπος",
        "ανθρωπολ": "ανθρωπολογία",
    }.get(tpl, ""):
        return text if data["0"] else term(text)

    if text := {
        "αθ": "αρσενικό ή θηλυκό",
        "ταυτ": "ταυτόσημα",
        "αναδρομικός": "αναδρομικός σχηματισμός",
        "κρητ αρχ": "κρητικός τύπος",
        "λατ": "λατινικά",
        "υστερο la": "υστερολατινική",
        "αντιδάνειο": "αντιδάνειο",
        "χρειάζεται": "χρειάζεται",
        "συνων": "συνώνυμα",
        "συνών": "συνώνυμα",
        "ποιητ": "ποιητικός τύπος",
    }.get(tpl, ""):
        return text if data["0"] else italic(text)

    if tpl == "γρ":
        desc = parts[1] if len(parts) > 1 else ""
        desc = {
            "": "άλλη γραφή του",
            "απλοπ": "απλοποιημένη γραφή του",
            "μη απλοπ": "απλοποιημένη γραφή του",
            "ασυν": "ασυναίρετη μορφή του",
            "ετυμ": "ετυμολογική γραφή του",
            "μονο": "μονοτονική γραφή του",
            "μορφή": "άλλη μορφή του",
            "πολυ": "πολυτονική γραφή του",
            "πολ": "πολυτονική γραφή του",
            "παρωχ": "παρωχημένη γραφή του",
            "σνρ": "συνηρημένη μορφή του",
            "συνων": "συνώνυμο του",
        }.get(desc, desc)
        return f"{italic(desc)} {strong(data['εμφ'] or parts[0])}"

    if tpl in {"πρόσφ", "προσφ"}:
        words = []
        for idx, part in enumerate(parts, 1):
            words.append(data[f".{idx}"] or part)
        return concat(words, " + ")

    # This is a country in the current locale
    if lang := langs.get(tpl):
        return str(lang["name"])

    #
    # Variants
    #
    if tpl.startswith(("infl", "κλ", "θηλ του", "θηλ_του")):
        return parts[-1]

    return defaults.last_template_handler(template, locale, word=word, missed_templates=missed_templates)
