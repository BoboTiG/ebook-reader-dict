"""
Python conversion of the translit/got module.
Link:
  - https://sv.wiktionary.org/wiki/Modul:translit/got

Current version from 2024-09-26 21:48
  - https://sv.wiktionary.org/w/index.php?title=Modul:translit/got&oldid=4064411
"""

import re
from collections import deque

multibyte_char_pattern = re.compile(r".[\x80-\xBF]*")
latin_by_gothic = {
    "𐌰": "a",
    "𐌱": "b",
    "𐌲": "g",
    "𐌳": "d",
    "𐌴": "e",
    "𐌵": "q",
    "𐌶": "z",
    "𐌷": "h",
    "𐌸": "þ",
    "𐌹": "i",
    "𐌺": "k",
    "𐌻": "l",
    "𐌼": "m",
    "𐌽": "n",
    "𐌾": "j",
    "𐌿": "u",
    "𐍀": "p",
    "𐍁": "?",
    "𐍂": "r",
    "𐍃": "s",
    "𐍄": "t",
    "𐍅": "w",
    "𐍆": "f",
    "𐍇": "x",
    "𐍈": "ƕ",
    "𐍉": "o",
    "𐍊": "?",
}


def transliterate(text: str) -> str:
    """
    >>> transliterate("𐌰,𐌱,𐌲,𐌳,𐌴")
    'a,b,g,d,e'
    >>> transliterate("𐌰𐍄𐍄𐌰 𐌿𐌽𐍃𐌰𐍂, 𐌸𐌿 𐌹𐌽 𐌷𐌹𐌼𐌹𐌽𐌰𐌼,")
    'atta unsar, þu in himinam,'
    """
    gothic_q: deque[str] = deque(re.findall(multibyte_char_pattern, text))
    latin_q: deque[str] = deque()

    while gothic_q:
        x = gothic_q.popleft()

        if x not in latin_by_gothic:
            latin_q.append(x)
        else:
            latin_q.append(latin_by_gothic[x])

    return "".join(latin_q)
