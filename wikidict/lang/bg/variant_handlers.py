from collections import defaultdict


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], word: str) -> str:
    return parts[0]


handlers = {
    "flexion": render_variant,
}
