"""
Python conversion of the translit/bg module.
Link:
  - https://sv.wiktionary.org/wiki/Modul:translit/bg

Current version from 2022-08-28 18:51
  - https://sv.wiktionary.org/w/index.php?title=Modul:translit/bg&oldid=3705145
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
    "Г": "G",
    "г": "g",
    "Д": "D",
    "д": "d",
    "Е": "E",
    "е": "e",
    "Ж": "Zj",
    "ж": "zj",
    "З": "Z",
    "з": "z",
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
    "Щ": "Sjt",
    "щ": "sjt",
    "Ъ": "Ă",
    "ъ": "ă",
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
    >>> transliterate("Жуковский")
    'Zjukovskij'
    """
    cyrillic_q: deque[str] = deque(re.findall(multibyte_char_pattern, text))
    latin_q: deque[str] = deque()

    while cyrillic_q:
        x = cyrillic_q.popleft()
        y = cyrillic_q[0] if cyrillic_q else None
        z = cyrillic_q[1] if len(cyrillic_q) > 1 else None

        if x not in latin_by_cyrillic:
            latin_q.append(x)
        elif x in "стзСТЗ":
            latin_q.append(latin_by_cyrillic[x])
            if y == "ь":
                if z == "ю":
                    latin_q.append("iu")
                    cyrillic_q.popleft()
                    cyrillic_q.popleft()
                elif z == "я":
                    latin_q.append("ia")
                    cyrillic_q.popleft()
                    cyrillic_q.popleft()
            elif y == "ю":
                latin_q.append("iu")
                cyrillic_q.popleft()
            elif y == "я":
                latin_q.append("ia")
                cyrillic_q.popleft()
        else:
            latin_q.append(latin_by_cyrillic[x])

    return "".join(latin_q)
