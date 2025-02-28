"""
Python conversion of the xib-trans module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:xib-trans

Current version from 2024-07-10 11:18
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:xib-trans&oldid=2349253
"""

import re

from .xib import table_dual, table_epigraphy, table_no_dual


def transliterate(text: str, locale: str = "") -> str:
    """
    >>> transliterate("ba")  # doctest: +ELLIPSIS
    '<svg ...'
    """
    dual = "dual" if re.search(r"[áéíóúgḱdâřŝ]", text) else ""
    table_tr = table_epigraphy if re.search(r"\d", text) else table_dual if dual == "dual" else table_no_dual
    syllabic = {"b": True, "k": True, "g": True, "t": True, "d": True}
    sign = ""
    tr = []

    for i in range(len(text)):
        letter = text[i]
        if letter != "-":
            sign += letter
            if not (text[i + 1 : i + 2].isdigit() or syllabic.get(letter)):
                if not (file := table_tr.get(sign.removesuffix("01"))):  # Support both `a1`, and `a101`, keys
                    return ""
                if not file.startswith("<svg"):
                    assert 0, (
                        f"Missing xib-trans SVG: {file!r}, https://commons.wikimedia.org/wiki/File:{file.replace(' ', '_')}.svg"
                    )
                svg = f'{file[:4]} style="width:24px;height:auto;vertical-align:middle" {file[6:]}'
                tr.append(svg)
                sign = ""

    return "".join(tr)
