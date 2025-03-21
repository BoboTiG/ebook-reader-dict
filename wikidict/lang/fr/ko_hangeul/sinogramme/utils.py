"""
Python conversion of the sinogramme module.
Link:
  - https://fr.wiktionary.org/wiki/Module:sinogramme

Current version from 2019-02-20 13:07:41
  - https://fr.wiktionary.org/w/index.php?title=Module:sinogramme&oldid=26091473
"""

import logging
import re
from importlib import import_module

log = logging.getLogger(__name__)
tableau_radical_trait: dict[int, dict[str, str]] = {}


def code_radical_trait(match: re.Match[str]) -> str:
    global tableau_radical_trait
    char = match[0]
    page = ord(char) // 0x1000
    if not (tableau := tableau_radical_trait.get(page)):
        tableau = tableau_radical_trait[page] = import_trait(page)
    return tableau[char]


def chaine_radical_trait(text: str) -> str:
    return re.sub(r"[⺀-⿕々-〇ヶ㐀-䶿一-鿿﨎-﨩𠀀-𪜇𪜉-𬻿𬼁-𯿿]", code_radical_trait, text)


def import_trait(page: int) -> dict[str, str]:
    file = f"traits_{page}000"
    module = import_module(f"{__package__}.data.{file}")
    tableau = getattr(module, "radical_trait")
    log.debug("Imported the data.%s module with %s items", file, f"{len(tableau):,}")
    assert isinstance(tableau, dict)
    return tableau
