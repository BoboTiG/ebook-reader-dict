"""Defaults values for locales without specific needs."""
from collections import defaultdict  # noqa
from typing import Dict, List, Tuple

# Regex to find the genre
genre = r""

# Markers for sections that contain interesting text to analyse.
section_patterns = (r"\#",)
sublist_patterns = (r"\#",)
section_level = 2
section_sublevels = (3,)

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore: Tuple[str, ...] = tuple()

# But some words need to be kept even if they would have been skipped by definitions_to_ignore
words_to_keep: Tuple[str, ...] = tuple()

# Templates to ignore: the text will be deleted.
templates_ignored: Tuple[str, ...] = tuple()

# Templates that will be completed/replaced using italic style.
templates_italic: Dict[str, str] = {}

# Templates that will be completed/replaced using custom style.
templates_other: Dict[str, str] = {}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["transliterator", "ar", "سم"], "fr")
        'sm'
        >>> last_template_handler(["transliterator", "ar"], "fr", word="زب")
        'zb'
    """
    from ..user_functions import capitalize, extract_keywords_from, lookup_italic, term
    from ..transliterator import transliterate

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "w":
        return render_wikilink(tpl, parts, data)

    # Handle the specific {{transliterator}} template (which is a Wiktionary module)
    if tpl == "transliterator":
        lang = parts[0]
        text = parts[1] if len(parts) == 2 else word
        return transliterate(lang, text)

    # {{tpl|item}} -> <i>(Templatet gf)</i>
    if len(template) == 2:
        return term(capitalize(lookup_italic(tpl, locale)))

    italic = lookup_italic(tpl, locale, True)
    if italic:
        return term(capitalize(italic))

    # {{tpl|item1|item2|...}} -> ''
    if len(template) > 2:
        return ""

    # <i>(Template)</i>
    return term(capitalize(lookup_italic(tpl, locale))) if tpl else ""


def render_wikilink(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_wikilink("w", [], defaultdict(str))
    ''
    >>> render_wikilink("w", ["Li Ptit Prince (roman)", "Li Ptit Prince"], defaultdict(str, {"lang": "wa"}))
    'Li Ptit Prince'
    >>> render_wikilink("w", ["Gesse aphaca", "Lathyrus aphaca"], defaultdict(str))
    'Lathyrus aphaca'
    >>> render_wikilink("w", [], defaultdict(str, {"Paulin <span style": "'font-variant:small-caps'>Paris</span>", "lang": "fr"}))
    "Paulin <span style='font-variant:small-caps'>Paris</span>"
    """  # noqa
    if parts:
        return parts[-1]

    # Possible imbricated templates: {{w| {{pc|foo bar}} }}
    if data:
        return "".join(f"{k}={v}" for k, v in data.items() if k != "lang")

    # Should not happen as it is already handled in utils.transform()
    return ""
