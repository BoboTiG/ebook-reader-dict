from collections import defaultdict

from ...user_functions import extract_keywords_from


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_variant("böjning", ["sv", "subst", "boll"], defaultdict(str))
    'boll'
    """
    return parts[-1]


template_mapping = {
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
