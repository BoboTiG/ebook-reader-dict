from collections import defaultdict

from ...user_functions import extract_keywords_from


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_variant("flexion", ["tale"], defaultdict(str))
    'tale'

    >>> render_variant("{{form of", ["imperative form", "bjerge"], defaultdict(str, {"lang": "da"}))
    'bjerge'
    """
    return parts[-1]


template_mapping = {
    #
    # Variants
    #
    "__variant__alternativ stavemåde af": render_variant,
    "__variant__flexion": render_variant,
    "__variant__form of": render_variant,
    "__variant__imperativ af": render_variant,
    "__variant__imperativ form af": render_variant,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
