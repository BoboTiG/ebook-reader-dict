"""
Python conversion of the sinogramme module.
Link:
  - https://fr.wiktionary.org/wiki/Module:sinogramme

Current version from 2019-02-20 13:07:41
  - https://fr.wiktionary.org/w/index.php?title=Module:sinogramme&oldid=26091473
"""

from .utils import chaine_radical_trait


def radical_trait(text: str) -> str:
    return chaine_radical_trait(text[0])
