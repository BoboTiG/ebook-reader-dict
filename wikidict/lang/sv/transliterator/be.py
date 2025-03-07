"""
Python conversion of the translit/be module.
Link:
  - https://sv.wiktionary.org/wiki/Modul:translit/be

Current version from 2022-08-28 17:35
  - https://sv.wiktionary.org/w/index.php?title=Modul:translit/be&oldid=3705112
"""

import re
from collections import deque

multibyte_char_pattern = re.compile(r".[\x80-\xBF]*")
latin_by_cyrillic = {
    "А": "A",
    "а": "a",
    "Б": "B",
    "б": "b",
    "В": "V",
    "в": "v",
    "Г": "H",
    "г": "h",
    "Д": "D",
    "д": "d",
    "Е": "E",
    "е": "e",
    "Ё": "Jo",
    "ё": "jo",
    "Ж": "Zj",
    "ж": "zj",
    "З": "Z",
    "з": "z",
    "І": "I",
    "і": "i",
    "И": "I",
    "и": "i",
    "Й": "J",
    "й": "j",
    "К": "K",
    "к": "k",
    "Л": "L",
    "л": "l",
    "М": "M",
    "м": "m",
    "Н": "N",
    "н": "n",
    "О": "O",
    "о": "o",
    "П": "P",
    "п": "p",
    "Р": "R",
    "р": "r",
    "С": "S",
    "с": "s",
    "Т": "T",
    "т": "t",
    "У": "U",
    "у": "u",
    "Ў": "Ŭ",
    "ў": "ŭ",
    "Ф": "F",
    "ф": "f",
    "Х": "Ch",
    "х": "ch",
    "Ц": "Ts",
    "ц": "ts",
    "Ч": "Tj",
    "ч": "tj",
    "Ш": "Sj",
    "ш": "sj",
    "Щ": "Sjtj",
    "щ": "sjtj",
    "Ъ": "",
    "ъ": "",
    "Ы": "Y",
    "ы": "y",
    "Ь": "J",
    "ь": "j",
    "Э": "E",
    "э": "e",
    "Ю": "Ju",
    "ю": "ju",
    "Я": "Ja",
    "я": "ja",
}


def transliterate(text: str) -> str:
    """
    >>> transliterate("арты́кул")
    'artýkul'
    >>> transliterate("Анна")
    'Anna'
    """
    cyrillic_q: deque[str] = deque(re.findall(multibyte_char_pattern, text))
    latin_q: deque[str] = deque()

    while cyrillic_q:
        x = cyrillic_q.popleft()
        y = cyrillic_q[0] if cyrillic_q else None
        z = cyrillic_q[1] if len(cyrillic_q) > 1 else None
        u = latin_q[-1] if latin_q else None

        if x not in latin_by_cyrillic:
            latin_q.append(x)
        elif (not latin_q or u == " ") and x in ["Е", "е"]:
            latin_q.append("Je" if x == "Е" else "je")
        elif x == "ь" and y == "и":
            latin_q.append("ji")
            cyrillic_q.popleft()
        elif x == "Ь" and y in ["и", "И"]:
            latin_q.append("Ji" if y == "и" else "JI")
            cyrillic_q.popleft()
        elif re.match(r"[стзСТЗ]", x):
            latin_q.append(latin_by_cyrillic[x])
            if y == "ь" and z in ["е", "ё", "ю", "я"]:
                latin_q.append(f"i{latin_by_cyrillic[z]}")
                cyrillic_q.popleft()
                cyrillic_q.popleft()
            elif y in ["ё", "ю", "я"]:
                latin_q.append(f"i{latin_by_cyrillic[y]}")
                cyrillic_q.popleft()
        elif re.match(r"[шщчжШЩЧЖ]", x):
            latin_q.append(latin_by_cyrillic[x])
            if y == "ё":
                latin_q.append("o")
                cyrillic_q.popleft()
        elif x == "е" and ((u and re.match(r"[aeouiAEOUI]", u)) or u == "́"):
            latin_q.append("je")
        else:
            latin_q.append(latin_by_cyrillic[x])

    result = []
    accent = "́"

    while latin_q:
        x = latin_q.popleft()
        y = latin_q[0] if latin_q else ""

        if y == accent:
            x += y
            latin_q.popleft()

        result.append(x)

    return "".join(result)
