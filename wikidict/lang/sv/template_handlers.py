from collections import defaultdict

from ...user_functions import extract_keywords_from

REFORMERS = {
    "sv|wv": "övergången från fraktur till antikva",
    "sv|th": "förenklingen under 1800-talet",
    "sv|eä": "sjätte upplagan av SAOL (1889)",
    "sv|qv": "sjätte upplagan av SAOL (1889)",
    "sv|gk": "sjunde upplagan av SAOL (1900)",
    "sv|hv": "stavningsreformen 1906",
    "sv|dt": "stavningsreformen 1906",
    "sv|f": "stavningsreformen 1906",
    "sv|fv": "stavningsreformen 1906",
    "da|aa": "rättskrivningsreformen 1948",
    "da|dl": "rättskrivningsreformen 1948",
    "da|ld": "rättskrivningsreformen 1948",
    "de|ss": "rättskrivningsreformen 1996",
    "de|auh": "rättskrivningsreformen 1996",
    "de|ff": "rättskrivningsreformen 1996",
    "de|sär": "rättskrivningsreformen 1996",
    "de|eä": "rättskrivningsreformen 1996",
    "is|zs": "stavningsreformen 1973",
    "nn|gk": "reformen år 1917",
    "es|ch": "successiva stavningsreformer under 1700-talet",
    "es|ph": "successiva stavningsreformer under 1700-talet",
    "es|th": "successiva stavningsreformer under 1700-talet",
    "es|mn": "stavningsreformen år 1763",
    "es|qc": "stavningsreformen år 1815 och en tid därefter",
}


def render_gammalstavning(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_gammalstavning("gammalstavning", ["sv", "fv", "brev"], defaultdict(str))
    '<i>(gammalstavning) genom stavningsreformen 1906 ersatt av</i> brev'
    >>> render_gammalstavning("gammalstavning", ["sv", "fv", "brev"], defaultdict(str, {"ejtagg": "1"}))
    '<i>genom stavningsreformen 1906 ersatt av</i> brev'
    """
    # Source: https://sv.wiktionary.org/w/index.php?title=Modul:gammalstavning&oldid=4112967
    lang_code, reform_code, new_spelling = parts[0:3]
    text = "<i>"
    if not data["ejtagg"]:
        text += "(gammalstavning) "

    if reform_code != "-":
        if reform_desc := REFORMERS.get(f"{lang_code}|{reform_code}"):
            text += f"genom {reform_desc} "

    return f"{text}ersatt av</i> {new_spelling}"


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_variant("böjning", ["sv", "subst", "boll"], defaultdict(str))
    'boll'
    >>> render_variant("avledning", ["sv", "abnorm", "adj"], defaultdict(str))
    'abnorm'
    """
    return parts[1 if tpl.endswith("avledning") else -1]


template_mapping = {
    "gammalstavning": render_gammalstavning,
    #
    # Variants
    #
    "__variant__avledning": render_variant,
    "__variant__böjning": render_variant,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
