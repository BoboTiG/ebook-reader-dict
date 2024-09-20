from optparse import Values

from scour.scour import scourString

from .svg_cache import CACHE

SCOUR_OPTIONS = Values(
    defaults={
        "enable_viewboxing": True,
        "group_create": True,
        "newlines": False,
        "quiet": True,
        "remove_descriptions": True,
        "remove_descriptive_elements": True,
        "remove_metadata": True,
        # "shorten_ids": True,  # /!\ When set to True, display will be incorrect
        "strip_comments": True,
        "strip_xml_prolog": True,
    }
)


def get(formula: str) -> str:
    return CACHE.get(formula, "")


def set(formula: str, svg_raw: str) -> None:
    print(f"{formula!r}: {svg_raw!r},")
    CACHE[formula] = svg_raw


def optimize(svg_raw: str) -> str:
    """Optimize a given SVG."""
    return str(scourString(svg_raw, options=SCOUR_OPTIONS))
