from collections import defaultdict

from ...user_functions import extract_keywords_from


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_variant("__variant__", ["foo"], defaultdict(str))
    'foo'

    >>> render_variant("tabs", ["muratore", "muratori", "muratrice", "muratore"], defaultdict(str, {"f2": "muratora", "fp2": "muratrici"}))
    'muratore'
    >>> render_variant("tabs", [], defaultdict(str, {"f": "tradotta", "m": "tradotto", "mp": "tradotti", "fp": "tradotte"}))
    'tradotto'
    """
    return data["m"] or parts[0] if "tabs" in tpl else parts[0]


template_mapping = {
    # "flexion": lambda *_, **__: "",
    #
    # Variants
    #
    "__variant__flexion": render_variant,
    "__variant__tabs": render_variant,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
