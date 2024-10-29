from collections import defaultdict

from ...user_functions import concat, extract_keywords_from, italic
from .langs import langs


def render_βλ(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_βλ("βλ", [], defaultdict(str))
    '<i>→ δείτε τη λέξη</i>'
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
    no_prefix = "πθ" not in data and "όρος" not in data

    if data["και"] == "1":
        text += " και"
    if data["0"] != "-":
        text += " δείτε"
    if data["και"] == "2":
        text += " και"
    if no_prefix:
        text += " τις λέξεις" if len(parts) > 1 else " τη λέξη"

    if data["πθ"]:
        text += " παράθεμα στο"
    elif όρος := data["όρος"]:
        text += f" {'τους όρους' if όρος == '1' else όρος}"

    following = (" " + concat(parts, sep=", ", last_sep=italic(" και "))) if parts else ""
    return f"{italic(text)}{following}"


def render_etym(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
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

    >>> render_etym("λδαν", ["en", "el", "skyscraper"], defaultdict(str))
    '(λόγιο δάνειο) <i>αγγλική</i> skyscraper'

    >>> render_etym("κλη", ["en", "el", "skyscraper"], defaultdict(str))
    '(κληρονομημένο) <i>αγγλική</i> skyscraper'
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
        else ""
    )
    if tpl != "etym":
        if data["text"] != "1" and data["κειμ"] != "1":
            phrase = f"({phrase})"
        else:
            phrase += f" από {italic('τη')}"

    if parts:
        phrase = f"{phrase} {italic(str(langs[parts.pop(0)]['frm']))}"
    if parts:
        parts.pop(0)  # Remove the lang
    if parts:
        phrase += f" {parts[-1]}"

    if tnl := data["tnl"]:
        phrase += f" ({tnl})"

    return phrase.strip()


template_mapping = {
    "βλ": render_βλ,
    "etym": render_etym,
    "κλη": render_etym,
    "δαν": render_etym,
    "λδαν": render_etym,
    "μτφδ": render_etym,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
