from collections import defaultdict

from ...user_functions import extract_keywords_from, italic
from .langs import langs


def render_μτφδ(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_μτφδ("μτφδ", ["en", "el"], defaultdict(str))
    '(μεταφραστικό δάνειο) <i>αγγλική</i>'
    >>> render_μτφδ("μτφδ", ["en", "el"], defaultdict(str, {"nodisplay": "1"}))
    ''
    >>> render_μτφδ("μτφδ", ["en", "el"], defaultdict(str, {"000": "-"}))
    ''
    >>> render_μτφδ("μτφδ", ["en", "el", "skyscraper"], defaultdict(str, {"00": "-"}))
    '(μεταφραστικό δάνειο) <i>αγγλική</i> skyscraper'
    >>> render_μτφδ("μτφδ", ["fr", "el", "-culture"], defaultdict(str, {"text": "1"}))
    'μεταφραστικό δάνειο από <i>τη</i> <i>γαλλική</i> -culture'
    >>> render_μτφδ("μτφδ", ["fr", "el", "-culture"], defaultdict(str, {"κειμ": "1"}))
    'μεταφραστικό δάνειο από <i>τη</i> <i>γαλλική</i> -culture'
    """
    if data["000"] == "-" or data["nodisplay"] == "1":
        return ""

    phrase = "μεταφραστικό δάνειο"
    if data["text"] != "1" and data["κειμ"] != "1":
        phrase = f"({phrase})"
    else:
        phrase += f" από {italic('τη')}"
    phrase = f"{phrase} {italic(str(langs[parts.pop(0)]['frm']))}"
    parts.pop(0)  # Remove the lang
    if parts:
        phrase += f" {parts[0]}"
    return phrase


template_mapping = {
    "μτφδ": render_μτφδ,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
