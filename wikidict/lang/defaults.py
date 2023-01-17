"""Defaults values for locales without specific needs."""
import re
from collections import defaultdict  # noqa
from typing import Dict, List, Pattern, Tuple

# Float number separator
float_separator = ""

# Thousads separator
thousands_separator = ""

# Markers for sections that contain interesting text to analyse.
section_patterns = (r"\#",)
sublist_patterns = (r"\#",)
section_level = 2
section_sublevels = (3,)
head_sections = ("",)
etyl_section = ("",)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore: Tuple[str, ...] = tuple()

# But some words need to be kept even if they would have been skipped by definitions_to_ignore
words_to_keep: Tuple[str, ...] = tuple()

# Templates to ignore: the text will be deleted.
templates_ignored: Tuple[str, ...] = tuple()

# Templates that will be completed/replaced using italic style.
templates_italic: Dict[str, str] = {}

# More complex templates that will be completed/replaced using custom style.
templates_multi: Dict[str, str] = {}

# Templates that will be completed/replaced using custom style.
templates_other: Dict[str, str] = {}


def find_genders(
    code: str,
    pattern: Pattern[str] = re.compile(r""),
) -> List[str]:
    """Function used to find genders within `code`."""
    return []


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(r""),
) -> List[str]:
    """Function used to find pronunciations within `code`."""
    return []


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
    from ..transliterator import transliterate
    from ..user_functions import capitalize, extract_keywords_from, lookup_italic, term

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

    if italic := lookup_italic(tpl, locale, True):
        return term(capitalize(italic))

    # {{tpl|item1|item2|...}} -> ''
    if len(template) > 2:
        from ..render import LOCK, MISSING_TPL_SEEN

        with LOCK:
            if tpl not in MISSING_TPL_SEEN:
                MISSING_TPL_SEEN.append(tpl)
                print(
                    f" !! Missing {tpl!r} template support for word {word!r}",
                    flush=True,
                )
        return ""

    # {{template}}
    from ..utils import CLOSE_DOUBLE_CURLY, OPEN_DOUBLE_CURLY

    return f"{OPEN_DOUBLE_CURLY}{tpl}{CLOSE_DOUBLE_CURLY}" if tpl else ""


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
    >>> render_wikilink("w", ["Еремеев, Павел Владимирович"], defaultdict(str, {"lang": "ru", "Pavel Vladimirovitch <span style": "'font-variant:small-caps'>Ieremeïev</span>"}))
    "Pavel Vladimirovitch <span style='font-variant:small-caps'>Ieremeïev</span>"
    >>> render_wikilink("w", ["mitrospin obscur 0", "mitrospin obscur 1", "(''Mitrospingus cassinii'')"], defaultdict(str))
    'mitrospin obscur 1'
    """  # noqa
    # Possible imbricated templates: {{w| {{pc|foo bar}} }}
    if data := {k: v for k, v in data.items() if k != "lang"}:
        return "".join(f"{k}={v}" for k, v in data.items())

    try:
        return parts[1]
    except IndexError:
        return parts[0] if parts else ""
