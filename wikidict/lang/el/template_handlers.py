from collections import defaultdict

from ...user_functions import concat, extract_keywords_from, italic, parenthesis, strong
from .langs import langs


def render_π(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_π("π", ["λέξη"], defaultdict(str))
    'λέξη'
    >>> render_π("π", ["επί-"], defaultdict(str, {".1": "επ"}))
    'επ'
    >>> render_π("π", ["-ism", "en", "imsss"], defaultdict(str))
    'imsss'
    """
    return data[".1"] or parts[2 if len(parts) == 3 else 0]


def render_βλ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_βλ("βλ", [], defaultdict(str))
    '<i>→ δείτε τη λέξη</i>'
    >>> render_βλ("βλ", [], defaultdict(str, {"0": "-"}))
    '<i>→ δείτε</i>'
    >>> render_βλ("βλ", [], defaultdict(str, {"και": "1"}))
    '<i>→ και δείτε τη λέξη</i>'
    >>> render_βλ("βλ", [], defaultdict(str, {"και": "2"}))
    '<i>→ δείτε και τη λέξη</i>'
    >>> render_βλ("βλ", [], defaultdict(str, {"πθ": "1"}))
    '<i>→ δείτε παράθεμα στο</i>'
    >>> render_βλ("βλ", [], defaultdict(str, {"πθ": "1", "και": "2"}))
    '<i>→ δείτε και παράθεμα στο</i>'
    >>> render_βλ("βλ", [], defaultdict(str, {"όρος": "1"}))
    '<i>→ δείτε τους όρους</i>'
    >>> render_βλ("βλ", [], defaultdict(str, {"όρος": "..."}))
    '<i>→ δείτε ...</i>'
    >>> render_βλ("βλ", ["a", "b", "c"], defaultdict(str, {"όρος": "1", "γλ": "en"}))
    '<i>→ δείτε τους όρους</i> a, b<i> και </i>c'
    """
    text = "→"
    no_prefix = "πθ" not in data and "όρος" not in data and "0"

    if data["και"] == "1":
        text += " και"
    if data["0"] == "-":
        no_prefix = False
    text += " δείτε"
    if data["και"] == "2":
        text += " και"
    if no_prefix:
        text += " τις λέξεις" if len(parts) > 1 else " τη λέξη"

    if data["πθ"]:
        text += " παράθεμα στο"
    elif όρος := data["όρος"]:
        text += f" {'τους όρους' if όρος == '1' else όρος}"

    following = (" " + concat(parts, ", ", last_sep=italic(" και "))) if parts else ""
    return f"{italic(text)}{following}"


def render_μεγ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_μεγ("μεγ", [], defaultdict(str))
    '<i>μεγεθυντικό του</i>'
    >>> render_μεγ("μεγ", ["γυναίκα"], defaultdict(str))
    '<i>μεγεθυντικό του</i> γυναίκα'
    >>> render_μεγ("μεγ", ["casa", "ona", "es"], defaultdict(str))
    'casa + <i>μεγεθυντικό επίθημα</i> -ona'
    >>> render_μεγ("μεγ", ["casa", "ona", "es", "cas(a)"], defaultdict(str))
    'cas(a) + <i>μεγεθυντικό επίθημα</i> -ona'
    >>> render_μεγ("μεγ", ["casa", "ona", "es"], defaultdict(str, {"4": "cas(a)"}))
    'cas(a) + <i>μεγεθυντικό επίθημα</i> -ona'
    """
    if data["4"]:
        parts[0] = data["4"]
    elif len(parts) == 4:
        parts[0] = parts[3]

    prefix = suffix = ""
    try:
        prefix, suffix = parts[:2]
    except ValueError:
        if parts:
            prefix = parts[0]

    if suffix:
        return f"{prefix} + {italic('μεγεθυντικό επίθημα')} -{suffix}"

    return f"{italic('μεγεθυντικό του')} {prefix}".rstrip()


def render_υπο(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_υπο("μεγ", ["βουνό", "αλάκι"], defaultdict(str))
    'βουνό + <i>υποκοριστικό επίθημα</i> -αλάκι'
    >>> render_υπο("μεγ", ["βουνό", "αλάκι", "grc"], defaultdict(str))
    'βουνό + <i>υποκοριστικό επίθημα</i> -αλάκι'
    >>> render_υπο("μεγ", ["βουνό", "αλάκι", "", "βουν(ό)"], defaultdict(str))
    'βουν(ό) + <i>υποκοριστικό επίθημα</i> -αλάκι'
    >>> render_υπο("μεγ", ["βουνό", "αλάκι"], defaultdict(str, {"4": "βουν(ό)"}))
    'βουν(ό) + <i>υποκοριστικό επίθημα</i> -αλάκι'
    """
    if data["4"]:
        parts[0] = data["4"]
    elif len(parts) == 4:
        parts[0] = parts[3]

    prefix = suffix = ""
    try:
        prefix, suffix = parts[:2]
    except ValueError:
        if parts:
            prefix = parts[0]

    return f"{prefix} + {italic('υποκοριστικό επίθημα')} -{suffix}"


def render_ελνστ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ελνστ("ελνστ", [], defaultdict(str))
    '(<i>ελληνιστική κοινή</i>)'
    >>> render_ελνστ("ελνστ", [], defaultdict(str, {"0": "-"}))
    '<i>ελληνιστική κοινή</i>'
    >>> render_ελνστ("ελνστ", [""], defaultdict(str), word="-ης")
    '(<i>ελληνιστική κοινή</i>) -ης'
    >>> render_ελνστ("ελνστ", ["πολυχρονία"], defaultdict(str))
    '(<i>ελληνιστική κοινή</i>) πολυχρονία'
    """
    text = italic("ελληνιστική κοινή")
    if not data["0"]:
        text = parenthesis(text)
    if parts:
        if not parts[0]:
            parts[0] = word
        text += f" {parts[0]}"
    return text


def render_etym(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_etym("etym", ["grc", "el", "ἄλαστος"], defaultdict(str))
    '<i>αρχαία ελληνική</i> ἄλαστος'
    >>> render_etym("etym", ["enm", "en", "dene"], defaultdict(str, {"tnl": "κυριολεκτικά: κοιλάδα, τοπωνυμικό για αυτόν που έμενε στις περιοχές Dean, Deen ή Dean της Αγγλίας"}))
    '<i>μέση αγγλική</i> dene (κυριολεκτικά: κοιλάδα, τοπωνυμικό για αυτόν που έμενε στις περιοχές Dean, Deen ή Dean της Αγγλίας)'

    >>> render_etym("μτφδ", [], defaultdict(str))
    '(μεταφραστικό δάνειο)'
    >>> render_etym("μτφδ", ["en"], defaultdict(str))
    '(μεταφραστικό δάνειο) <i>αγγλική</i>'
    >>> render_etym("μτφδ", ["en", "el"], defaultdict(str))
    '(μεταφραστικό δάνειο) <i>αγγλική</i>'
    >>> render_etym("μτφδ", ["en", "el"], defaultdict(str, {"nodisplay": "1"}))
    ''
    >>> render_etym("μτφδ", ["en", "el"], defaultdict(str, {"000": "-"}))
    ''
    >>> render_etym("μτφδ", ["en", "el", "skyscraper"], defaultdict(str, {"00": "-"}))
    '(μεταφραστικό δάνειο) <i>αγγλική</i> skyscraper'
    >>> render_etym("μτφδ", ["fr", "el", "-culture"], defaultdict(str, {"text": "1"}))
    'μεταφραστικό δάνειο από <i>τη</i> <i>γαλλική</i> -culture'
    >>> render_etym("μτφδ", ["fr", "el", "-culture"], defaultdict(str, {"κειμ": "1"}))
    'μεταφραστικό δάνειο από <i>τη</i> <i>γαλλική</i> -culture'

    >>> render_etym("δαν", ["en", "el", "skyscraper"], defaultdict(str, {"00": "-"}))
    '(άμεσο δάνειο) <i>αγγλική</i> skyscraper'
    >>> render_etym("δαν", ["it", "el", "-are", "-ar(e)"], defaultdict(str))
    '(άμεσο δάνειο) <i>ιταλική</i> -ar(e)'
    >>> render_etym("δαν", ["ota", "el", "آجر"], defaultdict(str, {"tr": "âcürr"}))
    '(άμεσο δάνειο) <i>οθωμανική τουρκική</i> آجر (âcürr)'

    >>> render_etym("λδαν", ["en", "el", "skyscraper"], defaultdict(str))
    '(λόγιο δάνειο) <i>αγγλική</i> skyscraper'
    >>> render_etym("λδαν", ["en", "el", "skyscraper"], defaultdict(str, {"0": "-"}))
    '<i>αγγλική</i> skyscraper'

    >>> render_etym("κλη", ["en", "el", "skyscraper"], defaultdict(str))
    '(κληρονομημένο) <i>αγγλική</i> skyscraper'

    >>> render_etym("σμσδ", ["fr", "el", "-gène"], defaultdict(str))
    '(σημασιολογικό δάνειο) <i>γαλλική</i> -gène'
    >>> render_etym("σμσδ", ["fr", "el", "-gène"], defaultdict(str, {"text": "1"}))
    'σημασιολογικό δάνειο από <i>τη γαλλική</i> -gène'
    >>> render_etym("σμσδ", ["en", "el", "-genous"], defaultdict(str, {"text": "1"}))
    'σημασιολογικό δάνειο από <i>την αγγλική</i> -genous'
    """
    if data["000"] == "-" or data["nodisplay"] == "1":
        return ""

    phrase = (
        "μεταφραστικό δάνειο"
        if tpl == "μτφδ"
        else "άμεσο δάνειο"
        if tpl == "δαν"
        else "λόγιο δάνειο"
        if tpl == "λδαν"
        else "κληρονομημένο"
        if tpl == "κλη"
        else "σημασιολογικό δάνειο"
        if tpl == "σμσδ"
        else ""
    )
    key = "frm"
    if tpl != "etym":
        if data["0"] == "-":
            phrase = ""
        elif data["text"] != "1" and data["κειμ"] != "1":
            phrase = f"({phrase})"
        else:
            phrase += " από"
            if tpl == "σμσδ":
                key = "apo"
            else:
                phrase += f" {italic('τη')}"

    if parts:
        phrase = f"{phrase} {italic(str(langs[parts.pop(0)][key]))}"
    if parts:
        parts.pop(0)  # Remove the lang
    if parts:
        phrase += f" {parts[-1]}"

    if tnl := (data["tnl"] or data["tr"]):
        phrase += f" ({tnl})"

    return phrase.strip()


def render_παθ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_παθ("παθ", [], defaultdict(str))
    '<i>παθητική φωνή</i>'
    >>> render_παθ("παθ", [], defaultdict(str, {"μπ": "1"}))
    '<i>μεσοπαθητική φωνή</i>'
    >>> render_παθ("παθ", [], defaultdict(str, {"μ": "1"}))
    '<i>μέση φωνή</i>'
    >>> render_παθ("παθ", ["λύνω"], defaultdict(str))
    '<i>παθητική φωνή του ρήματος</i> <b>λύνω</b>'
    >>> render_παθ("παθ", ["λύω"], defaultdict(str, {"μπ": "1"}))
    '<i>μεσοπαθητική φωνή του ρήματος</i> <b>λύω</b>'
    >>> render_παθ("παθ", ["αἱρῶ", "grc"], defaultdict(str, {"μπ": "1", "τύπος": "σνρ"}))
    '<i>μεσοπαθητική φωνή του συνηρημένου ρήματος</i> <b>αἱρῶ</b>'
    """
    phrase = "παθητική φωνή"
    if data["μπ"] == "1":
        phrase = "μεσοπαθητική φωνή"
    elif data["μ"] == "1":
        phrase = "μέση φωνή"

    if parts:
        verb = parts[0]
        if verb:
            if data["τύπος"] in ("σνρ", "συνηρημένο", "contr", "contracted"):
                phrase += " του συνηρημένου ρήματος"
            else:
                phrase += " του ρήματος"
            phrase = italic(phrase)
            phrase += f" {strong(verb)}"
    else:
        phrase = italic(phrase)

    return phrase


def render_ουσεπ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ουσεπ("ουσεπ α", [], defaultdict(str))
    '<i>ουσιαστικοποιημένο αρσενικό</i>'
    >>> render_ουσεπ("ουσεπ α", ["καλός"], defaultdict(str))
    '<i>ουσιαστικοποιημένο αρσενικό του επιθέτου</i> καλός'
    >>> render_ουσεπ("ουσεπ α", ["καλός", "grc"], defaultdict(str))
    '<i>ουσιαστικοποιημένο αρσενικό του επιθέτου</i> καλός'
    >>> render_ουσεπ("ουσεπ α", ["καλός", "grc", "καλός (καλόν)"], defaultdict(str))
    '<i>ουσιαστικοποιημένο αρσενικό του επιθέτου</i> καλός (καλόν)'
    >>> render_ουσεπ("ουσεπ α", ["δεδομένος"], defaultdict(str, {"μτχ": "1"}))
    '<i>ουσιαστικοποιημένο αρσενικό της μετοχής</i> δεδομένος'

    >>> render_ουσεπ("ουσεπ ο", [], defaultdict(str))
    '<i>ουσιαστικοποιημένο ουδέτερο</i>'

    >>> render_ουσεπ("ουσεπ θ", [], defaultdict(str))
    '<i>ουσιαστικοποιημένο θηλυκό</i>'
    """
    text = "ουσιαστικοποιημένο "
    match tpl.split(" ", 1)[1]:
        case "θ":
            text += "θηλυκό"
        case "α":
            text += "αρσενικό"
        case "ο":
            text += "ουδέτερο"

    if parts:
        text += f" {'της μετοχής' if data['μτχ'] == '1' else 'του επιθέτου'}"
        return f"{italic(text)} {parts[2 if len(parts) > 2 else 0]}"

    return italic(text)


def render_γραπτήεμφ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_γραπτήεμφ("γραπτήεμφ", [], defaultdict(str))
    '(<i>μαρτυρείται από το</i>)'
    >>> render_γραπτήεμφ("γραπτήεμφ", [], defaultdict(str, {"0": "-"}))
    'μαρτυρείται από το'
    >>> render_γραπτήεμφ("γραπτήεμφ", [], defaultdict(str, {"nostyle": "1"}))
    'μαρτυρείται από το'
    >>> render_γραπτήεμφ("γραπτήεμφ", [], defaultdict(str, {"ήδη": "1"}))
    '(<i>ήδη από το</i>)'
    >>> render_γραπτήεμφ("γραπτήεμφ", ["2025"], defaultdict(str))
    '(<i>μαρτυρείται από το 2025</i>)'
    >>> render_γραπτήεμφ("γραπτήεμφ", ["2025"], defaultdict(str, {"+": "η έκφραση"}))
    '(<i>η έκφραση μαρτυρείται από το 2025</i>)'
    >>> render_γραπτήεμφ("γραπτήεμφ", [], defaultdict(str, {"αι": "17"}))
    '(<i>μαρτυρείται από τον 17ο αιώνα</i>)'
    >>> render_γραπτήεμφ("γραπτήεμφ", [], defaultdict(str, {"αι": "5", ".": "πκε"}))
    '(<i>μαρτυρείται από τον 5ο αιώνα πκε</i>)'
    >>> render_γραπτήεμφ("γραπτήεμφ", [], defaultdict(str, {"δεκ": "2025"}))
    '(<i>μαρτυρείται από τη δεκαετία του 2025</i>)'
    >>> render_γραπτήεμφ("γραπτήεμφ", [], defaultdict(str, {"δεκ": "2025"}))
    '(<i>μαρτυρείται από τη δεκαετία του 2025</i>)'
    """
    text = f"{plus} " if (plus := data["+"]) else ""
    text += "ήδη" if data["ήδη"] else "μαρτυρείται"
    text += " από"
    if αι := data["αι"]:
        text += f" τον {αι}ο αιώνα"
    elif δεκ := data["δεκ"]:
        text += f" τη δεκαετία του {δεκ}"
    else:
        text += " το"
        if parts:
            text += f" {parts[0]}"
    if dot := data["."]:
        text += f" {dot}"

    return text if data["0"] or data["nostyle"] else f"({italic(text)})"


def render_πλ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_πλ("πλ", [], defaultdict(str))
    '<i>πληθυντικός</i>'
    >>> render_πλ("πλ", ["-αίικο"], defaultdict(str))
    '<i>πληθυντικός αριθμός του</i> <b>-αίικο</b>'
    """
    if not parts:
        return italic("πληθυντικός")
    return f"{italic('πληθυντικός αριθμός του')} {strong(parts[0])}"


template_mapping = {
    "π": render_π,
    "p": render_π,
    "βλ": render_βλ,
    "etym": render_etym,
    "σμσδ": render_etym,
    "κλη": render_etym,
    "δαν": render_etym,
    "λδαν": render_etym,
    "μτφδ": render_etym,
    "μεγ": render_μεγ,
    "υπο": render_υπο,
    "ελνστ": render_ελνστ,
    "παθ": render_παθ,
    "ουσεπ θ": render_ουσεπ,
    "ουσεπ α": render_ουσεπ,
    "ουσεπ ο": render_ουσεπ,
    "γραπτήεμφ": render_γραπτήεμφ,
    "πλ": render_πλ,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
