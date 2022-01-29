from typing import Dict, List, Tuple
from collections import defaultdict  # noqa

from .abk import abk

from ...user_functions import (
    extract_keywords_from,
    italic,
)


def render_K(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_K("K", ["Sport"], defaultdict(str))
    '<i>Sport:</i>'
    >>> render_K("K", ["trans."], defaultdict(str))
    '<i>transitiv:</i>'
    >>> render_K("K", ["trans.", "Linguistik", "Wortbildung"], defaultdict(str))
    '<i>transitiv, Linguistik, Wortbildung:</i>'
    >>> render_K("K", ["kPl.", "ugs."], defaultdict(str))
    '<i>kein Plural, umgangssprachlich:</i>'
    >>> render_K("K", ["Astronomie"], defaultdict(str, {"ft": "kurz für"}))
    '<i>Astronomie, kurz für:</i>'
    >>> render_K("K", ["intrans.", "Nautik"], defaultdict(str, {"t7": "_", "ft": "(von Schiffen)"}))
    '<i>intransitiv, Nautik (von Schiffen):</i>'
    >>> render_K("K", ["intrans.", "Nautik"], defaultdict(str, {"t7": "_", "ft": "(von Schiffen)"}))
    '<i>intransitiv, Nautik (von Schiffen):</i>'
    >>> render_K("K", ["test", "Nautik"], defaultdict(str, {"t1": "_"}))
    '<i>test Nautik:</i>'
    """  # noqa
    phrase = ""
    for i, p in enumerate(parts, start=1):
        s_index = str(i)
        t_index = f"t{s_index}"
        if p in abk:
            phrase += abk[p]
        else:
            phrase += p
        sep = ""
        if i != len(parts):
            sep = data[t_index] if t_index in data else ","
        if sep == "_":
            sep = " "
        elif sep:
            sep = f"{sep} "
        phrase += sep
    ft = f"{data['ft']}" if "ft" in data else ""
    if ft:
        spacer = data["t7"] if "t7" in data else ", "
        if spacer == "_":
            spacer = " "
        ft = spacer + ft

    return italic(f"{phrase}{ft}:")


template_mapping = {
    "K": render_K,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
