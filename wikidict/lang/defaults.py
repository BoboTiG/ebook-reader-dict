"""Defaults values for locales without specific needs."""

import logging
from collections import defaultdict

log = logging.getLogger(__name__)

# Float number separator
float_separator = ""

# Thousands separator
thousands_separator = ""

# Markers for sections that contain interesting text to analyse.
section_patterns = ("#",)
sublist_patterns = ("#",)
section_level = 2
section_sublevels = (3,)
head_sections = ("",)
etyl_section = ("",)

# Variants
variant_titles: tuple[str, ...] = ()
variant_templates: tuple[str, ...] = ()

# Some definitions are not good to keep
definitions_to_ignore: tuple[str, ...] = ()

# Templates to ignore: the text will be deleted.
templates_ignored: tuple[str, ...] = ()

# Templates that will be completed/replaced using italic style.
templates_italic: dict[str, str] = {}

# More complex templates that will be completed/replaced using custom style.
templates_multi: dict[str, str] = {}

# Templates that will be completed/replaced using custom style.
templates_other: dict[str, str] = {}


def find_genders(code: str, locale: str) -> list[str]:
    """Function used to find genders within `code`."""
    return []


def find_pronunciations(code: str, locale: str) -> list[str]:
    """Function used to find pronunciations within `code`."""
    return []


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    all_templates: list[tuple[str, str, str]] | None = None,
    variant_only: bool = False,
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["formatnum", "42000"], "es")
        '42 000'
        >>> last_template_handler(["formatnum", "42000"], "it")
        '42 000'
        >>> last_template_handler(["formatnum", "42000"], "no")
        '42 000'

        >>> last_template_handler(["transliterator", "ar", "سم"], "fr")
        'sm'
        >>> last_template_handler(["transliterator", "ar"], "fr", word="زب")
        'zb'
    """
    from ..transliterator import transliterate
    from ..user_functions import capitalize, extract_keywords_from, lookup_italic, number, term

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "BASEPAGENAME":
        return word

    if tpl == "formatnum":
        from . import float_separator as locale_aware_fs
        from . import thousands_separator as locale_aware_ts

        return number(parts[0], locale_aware_fs[locale], locale_aware_ts[locale])

    if tpl in {"w", "W"}:
        return render_wikilink(tpl, parts, data)

    # Handle the specific {{transliterator}} template (which is a Wiktionary module)
    if tpl == "transliterator":
        lang = parts[0]
        text = parts[1] if len(parts) == 2 else word
        return transliterate(lang, text)

    if tpl == "!":
        return "|"

    if italic := lookup_italic(tpl, locale, empty_default=True):
        return term(capitalize(italic))

    if all_templates is not None:
        all_templates.append((tpl, word, "missed"))

    from ..utils import CLOSE_DOUBLE_CURLY, OPEN_DOUBLE_CURLY

    return f"{OPEN_DOUBLE_CURLY}{tpl}{CLOSE_DOUBLE_CURLY}"


def render_wikilink(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
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
    >>> render_wikilink("W", ["Nomenclature de l'UICPA"], defaultdict(str, {"dif": "Nom UICPA"}))
    "Nomenclature de l'UICPA"
    """
    # Possible imbricated templates: {{w| {{pc|foo bar}} }}
    if wiki_data := {k: v for k, v in data.items() if k not in ("lang", "dif")}:
        return "".join(f"{k}={v}" for k, v in wiki_data.items())

    try:
        return parts[1]
    except IndexError:
        return parts[0] if parts else ""


def adjust_wikicode(code: str, locale: str) -> str:
    return code
