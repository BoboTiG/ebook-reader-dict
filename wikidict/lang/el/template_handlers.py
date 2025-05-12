from collections import defaultdict

from ...user_functions import concat, extract_keywords_from, italic, parenthesis, strong
from .langs import langs


def get_lang(lang: str) -> str:
    return italic(str(langs[lang]["frm"]))


def render_bor(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_bor("bor", ["fr", "en"], defaultdict(str))
    '(άμεσο δάνειο) <i>γαλλική</i>'
    >>> render_bor("bor", ["fr", "en", "Européen"], defaultdict(str))
    '(άμεσο δάνειο) <i>γαλλική</i> Européen'
    >>> render_bor("bor", ["pt", "en", "China"], defaultdict(str, {"τύπος": "τόπος"}))
    '(άμεσο δάνειο) <i>πορτογαλική</i> China'
    """
    text = f"(άμεσο δάνειο) {get_lang(parts.pop(0))}"
    if len(parts) > 1:
        text += f" {parts[1]}"
    return text


def render_inh(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_inh("inh", ["ang", "en"], defaultdict(str))
    '<i>αγγλοσαξονική</i>'
    """
    return get_lang(parts[0])


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
    >>> render_etym("κλη", ["", "σκαμνί"], defaultdict(str, {"π": "οακ", "α": "εν"}))
    '(κληρονομημένο)'

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
        if ln := parts.pop(0):
            phrase = f"{phrase} {italic(str(langs[ln][key]))}"
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


def render_ρημ_τύπος(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ρημ_τύπος("ρημ τύπος", ["α' ενικό υποτακτικής παρακειμένου", "στραβώνω"], defaultdict(str))
    "<i>α' ενικό υποτακτικής παρακειμένου του ρήματος</i> <b>στραβώνω</b>"
    >>> render_ρημ_τύπος("ρημ τύπος", ["μπλαμπλα", "τιμάω", "el"], defaultdict(str))
    '<i>μπλαμπλα του ρήματος</i> <b>τιμάω</b>'
    >>> render_ρημ_τύπος("ρημ τύπος", ["μπλαμπλα", "τιμάω", "grc", "τιμάω / τιμῶ"], defaultdict(str))
    '<i>μπλαμπλα του ρήματος</i> <b>τιμάω / τιμῶ</b>'
    >>> render_ρημ_τύπος("ρημ τύπος", ["α' ενικό πρόσωπο αορίστου", "αγαπώ", "", "αγαπάω"], defaultdict(str))
    "<i>α' ενικό πρόσωπο αορίστου του ρήματος</i> <b>αγαπάω</b>"
    """
    text = f"{parts[0]} του ρήματος"
    return f"{italic(text)} {strong(parts[3 if len(parts) > 3 else 1])}"


def render_ουδ_του(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ουδ_του("ουδ του", ["επίπεδος"], defaultdict(str))
    '<i>ουδέτερο</i> του <b>επίπεδος</b>'
    >>> render_ουδ_του("ουδ του-πτώσειςΟΑΚεν", ["επίπεδος"], defaultdict(str))
    '<i>ονομαστική, αιτιατική και κλητική ενικού, ουδέτερου γένους</i> του <b>επίπεδος</b>'
    >>> render_ουδ_του("ουδ του-πτώσειςΟΑΚπλ", ["-άδικος"], defaultdict(str))
    '<i>ονομαστική, αιτιατική και κλητική πληθυντικού, ουδέτερου γένους</i> του <b>-άδικος</b>'
    >>> render_ουδ_του("ουδ του-πτώσηΓεν", ["έβδομου"], defaultdict(str))
    '<i>γενική ενικού, ουδέτερου γένους</i> του <b>έβδομου</b>'
    >>> render_ουδ_του("ουδ του-πτώσηΓπλ", ["έβδομος"], defaultdict(str))
    '<i>γενική πληθυντικού, ουδέτερου γένους</i> του <b>έβδομος</b>'

    >>> render_ουδ_του("αρσ του", ["απολωλός"], defaultdict(str))
    '<i>αρσενικό</i> του <b>απολωλός</b>'
    >>> render_ουδ_του("αρσ του-πτώσηΓεν", ["έβδομος"], defaultdict(str))
    '<i>γενική ενικού, αρσενικού γένους</i> του <b>έβδομος</b>'
    >>> render_ουδ_του("αρσ του-πτώσηΓπλ", ["έβδομος"], defaultdict(str))
    '<i>γενική πληθυντικού, αρσενικού γένους</i> του <b>έβδομος</b>'
    >>> render_ουδ_του("αρσ του-πτώσηΑεν", ["έκνομος"], defaultdict(str))
    '<i>αιτιατική ενικού, αρσενικού γένους</i> του <b>έκνομος</b>'
    """
    match tpl.replace(" ", "_"):
        case "ουδ_του":
            text = "ουδέτερο"
        case "ουδ_του-πτώσειςΟΑΚεν":
            text = "ονομαστική, αιτιατική και κλητική ενικού, ουδέτερου γένους"
        case "ουδ_του-πτώσειςΟΑΚπλ":
            text = "ονομαστική, αιτιατική και κλητική πληθυντικού, ουδέτερου γένους"
        case "ουδ_του-πτώσηΓεν":
            text = "γενική ενικού, ουδέτερου γένους"
        case "ουδ_του-πτώσηΓπλ":
            text = "γενική πληθυντικού, ουδέτερου γένους"

        case "αρσ_του":
            text = "αρσενικό"
        case "αρσ_του-πτώσηΓεν":
            text = "γενική ενικού, αρσενικού γένους"
        case "αρσ_του-πτώσηΓπλ":
            text = "γενική πληθυντικού, αρσενικού γένους"
        case "αρσ_του-πτώσηΑεν":
            text = "αιτιατική ενικού, αρσενικού γένους"
        case _:
            raise ValueError(f"Unhandled 'ουδ του' {tpl =}")
    return f"{italic(text)} του {strong(parts[0])}"


def render_πτώσειςΟΑΚπλ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_πτώσειςΟΑΚπλ("πτώσειςΟΑΚπλ", ["Ελληνούπολη"], defaultdict(str))
    '<i>ονομαστική, αιτιατική και κλητική πληθυντικού</i> του <b>Ελληνούπολη</b>'
    """
    return f"{italic('ονομαστική, αιτιατική και κλητική πληθυντικού')} του {strong(parts[0])}"


def render_πτώσηΓπλ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_πτώσηΓπλ("πτώσηΓπλ", ["Γαία"], defaultdict(str))
    '<i>γενική πληθυντικού</i> του <b>Γαία</b>'
    """
    return f"{italic('γενική πληθυντικού')} του {strong(parts[0])}"


def render_πτώσηΑπλ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_πτώσηΑπλ("πτώσηΑπλ", ["Δημητρός"], defaultdict(str))
    '<i>αιτιατική πληθυντικού</i> του <b>Δημητρός</b>'
    """
    return f"{italic('αιτιατική πληθυντικού')} του {strong(parts[0])}"


def render_πτώσηΚεν(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_πτώσηΚεν("πτώσηΚεν", ["Ίκαρος"], defaultdict(str))
    '<i>ονομαστική και κλητική πληθυντικού</i> του <b>Ίκαρος</b>'
    """
    return f"{italic('ονομαστική και κλητική πληθυντικού')} του {strong(parts[0])}"


def render_πτώσειςΟΚπλ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_πτώσειςΟΚπλ("πτώσειςΟΚπλ", ["Ίκαρος"], defaultdict(str))
    '<i>γενική πληθυντικού</i> του <b>Ίκαρος</b>'
    """
    return f"{italic('γενική πληθυντικού')} του {strong(parts[0])}"


def render_πτώσηΑεν(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_πτώσηΑεν("πτώσηΑεν", ["επίπεδος"], defaultdict(str))
    '<i>αιτιατική ενικού</i> του <b>επίπεδος</b>'
    """
    return f"{italic('αιτιατική ενικού')} του {strong(parts[0])}"


def render_θηλ_του(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_θηλ_του("θηλ του", ["τσιγγάνος"], defaultdict(str))
    '<i>θηλυκό</i> του <b>τσιγγάνος</b>'
    >>> render_θηλ_του("θηλ_του-πτώσειςΟΑΚεν", ["Αθηναϊκός"], defaultdict(str))
    '<i>ονομαστική, αιτιατική και κλητική ενικού, θηλυκού γένους</i> του <b>Αθηναϊκός</b>'
    >>> render_θηλ_του("θηλ του-πτώσηΓπλ", ["έβδομος"], defaultdict(str))
    '<i>γενική πληθυντικού, θηλυκού γένους</i> του <b>έβδομος</b>'
    >>> render_θηλ_του("θηλ του-πτώσειςΟΑΚπλ", ["έγγαμος"], defaultdict(str))
    '<i>ονομαστική, αιτιατική και κλητική πληθυντικού, θηλυκού γένους</i> του <b>έγγαμος</b>'
    >>> render_θηλ_του("θηλ του-πτώσηΓεν", ["έγγαμος"], defaultdict(str))
    '<i>γενική ενικού, θηλυκού γένους</i> του <b>έγγαμος</b>'
    >>> render_θηλ_του("θηλ του-πτώσειςΟΚεν", ["ξένος"], defaultdict(str))
    '<i>ονομαστική και κλητική ενικού, θηλυκού γένους</i> του <b>ξένος</b>'
    """
    match tpl.replace(" ", "_"):
        case "θηλ_του":
            text = "θηλυκό"
        case "θηλ_του-πτώσειςΟΑΚεν":
            text = "ονομαστική, αιτιατική και κλητική ενικού, θηλυκού γένους"
        case "θηλ_του-πτώσηΓπλ":
            text = "γενική πληθυντικού, θηλυκού γένους"
        case "θηλ_του-πτώσειςΟΑΚπλ":
            text = "ονομαστική, αιτιατική και κλητική πληθυντικού, θηλυκού γένους"
        case "θηλ_του-πτώσηΓεν":
            text = "γενική ενικού, θηλυκού γένους"
        case "θηλ_του-πτώσειςΟΚεν":
            text = "ονομαστική και κλητική ενικού, θηλυκού γένους"
        case _:
            raise ValueError(f"Unhandled 'θηλ του' {tpl =}")
    return f"{italic(text)} του {strong(parts[0])}"


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_variant("ουδ του-πτώσειςΟΑΚεν", ["επίπεδος"], defaultdict(str), word="επίπεδο")
    'επίπεδος'
    >>> render_variant("ουδ του-πτώσειςΟΑΚπλ", ["-άδικος"], defaultdict(str), word="-άδικο")
    '-άδικος'
    >>> render_variant("ουδ του-πτώσηΓεν", ["έβδομος"], defaultdict(str), word="έβδομου")
    'έβδομος'
    >>> render_variant("ουδ του-πτώσηΓπλ", ["έβδομος"], defaultdict(str), word="έβδομου")
    'έβδομος'

    >>> render_variant("αρσ του-πτώσηΓεν", ["έβδομος"], defaultdict(str), word="έβδομου")
    'έβδομος'
    >>> render_variant("αρσ του-πτώσηΓπλ", ["έβδομος"], defaultdict(str), word="έβδομων")
    'έβδομος'

    >>> render_variant("πτώσειςΟΑΚπλ", ["Ελληνούπολη"], defaultdict(str), word="Ελληνουπόλεις")
    'Ελληνούπολη'

    >>> render_variant("πτώσηΑεν", ["επίπεδος"], defaultdict(str), word="επίπεδο")
    'επίπεδος'

    >>> render_variant("θηλ του", ["τσιγγάνος"], defaultdict(str), word="τσιγγάνα")
    'τσιγγάνος'
    >>> render_variant("θηλ του-πτώσειςΟΑΚπλ", ["έγγαμος"], defaultdict(str), word="έγγαμες")
    'έγγαμος'
    """
    return parts[-1]


template_mapping = {
    "bor": render_bor,
    "inh": render_inh,
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
    "ρημ τύπος": render_ρημ_τύπος,
    "ρημ_τύπος": render_ρημ_τύπος,
    # "θηλ του": render_θηλ_του,
    # "θηλ_του": render_θηλ_του,
    # "θηλ του-πτώσειςΟΑΚεν": render_θηλ_του,
    # "θηλ_του-πτώσειςΟΑΚεν": render_θηλ_του,
    # "θηλ του-πτώσηΓπλ": render_θηλ_του,
    # "θηλ_του-πτώσηΓπλ": render_θηλ_του,
    # "θηλ του-πτώσειςΟΑΚπλ": render_θηλ_του,
    # "θηλ_του-πτώσειςΟΑΚπλ": render_θηλ_του,
    # "θηλ του-πτώσηΓεν": render_θηλ_του,
    # "θηλ_του-πτώσηΓεν": render_θηλ_του,
    # "θηλ του-πτώσειςΟΚεν": render_θηλ_του,
    # "θηλ_του-πτώσειςΟΚεν": render_θηλ_του,
    # "ουδ του": render_ουδ_του,
    # "ουδ_του": render_ουδ_του,
    # "ουδ του-πτώσειςΟΑΚεν": render_ουδ_του,
    # "ουδ_του-πτώσειςΟΑΚεν": render_ουδ_του,
    # "ουδ του-πτώσειςΟΑΚπλ": render_ουδ_του,
    # "ουδ_του-πτώσειςΟΑΚπλ": render_ουδ_του,
    # "ουδ του-πτώσηΓεν": render_ουδ_του,
    # "ουδ_του-πτώσηΓεν": render_ουδ_του,
    # "ουδ του-πτώσηΓπλ": render_ουδ_του,
    # "ουδ_του-πτώσηΓπλ": render_ουδ_του,
    # "αρσ του": render_ουδ_του,
    # "αρσ_του": render_ουδ_του,
    # "αρσ του-πτώσηΓεν": render_ουδ_του,
    # "αρσ_του-πτώσηΓεν": render_ουδ_του,
    # "αρσ του-πτώσηΓπλ": render_ουδ_του,
    # "αρσ_του-πτώσηΓπλ": render_ουδ_του,
    # "αρσ του-πτώσηΑεν": render_ουδ_του,
    # "αρσ_του-πτώσηΑεν": render_ουδ_του,
    # "πτώσειςΟΑΚπλ": render_πτώσειςΟΑΚπλ,
    # "πτώσειςΟΚπλ": render_πτώσειςΟΚπλ,
    # "πτώσηΑπλ": render_πτώσηΑπλ,
    # "πτώσηΓπλ": render_πτώσηΓπλ,
    # "πτώσηΚεν": render_πτώσηΓπλ,
    # "πτώσηΑεν": render_πτώσηΑεν,
    #
    # Variants
    #
    # έκνομο
    "__variant__ρημ τύπος": render_variant,
    "__variant__ρημ_τύπος": render_variant,
    "__variant__θηλ του": render_variant,
    "__variant__θηλ_του": render_variant,
    "__variant__θηλ του-πτώσειςΟΑΚεν": render_variant,
    "__variant__θηλ_του-πτώσειςΟΑΚεν": render_variant,
    "__variant__θηλ του-πτώσηΓπλ": render_variant,
    "__variant__θηλ_του-πτώσηΓπλ": render_variant,
    "__variant__θηλ του-πτώσειςΟΑΚπλ": render_variant,
    "__variant__θηλ_του-πτώσειςΟΑΚπλ": render_variant,
    "__variant__θηλ του-πτώσηΓεν": render_variant,
    "__variant__θηλ_του-πτώσηΓεν": render_variant,
    "__variant__θηλ του-πτώσειςΟΚεν": render_variant,
    "__variant__θηλ_του-πτώσειςΟΚεν": render_variant,
    "__variant__ουδ του": render_variant,
    "__variant__ουδ_του": render_variant,
    "__variant__ουδ του-πτώσειςΟΑΚεν": render_variant,
    "__variant__ουδ_του-πτώσειςΟΑΚεν": render_variant,
    "__variant__ουδ του-πτώσειςΟΑΚπλ": render_variant,
    "__variant__ουδ_του-πτώσειςΟΑΚπλ": render_variant,
    "__variant__ουδ του-πτώσηΓπλ": render_variant,
    "__variant__ουδ_του-πτώσηΓπλ": render_variant,
    "__variant__ουδ του-πτώσηΓεν": render_variant,
    "__variant__ουδ_του-πτώσηΓεν": render_variant,
    "__variant__αρσ του": render_variant,
    "__variant__αρσ_του": render_variant,
    "__variant__αρσ του-πτώσηΓεν": render_variant,
    "__variant__αρσ_του-πτώσηΓεν": render_variant,
    "__variant__αρσ του-πτώσηΓπλ": render_variant,
    "__variant__αρσ_του-πτώσηΓπλ": render_variant,
    "__variant__αρσ του-πτώσηΑεν": render_variant,
    "__variant__αρσ_του-πτώσηΑεν": render_variant,
    "__variant__πτώσειςΟΑΚπλ": render_variant,
    "__variant__πτώσειςΟΚπλ": render_variant,
    "__variant__πτώσηΑπλ": render_variant,
    "__variant__πτώσηΓπλ": render_variant,
    "__variant__πτώσηΑεν": render_variant,
    "__variant__πτώσηΚεν": render_variant,
    "__variant__κλ": render_variant,
    "__variant__infl": render_variant,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
