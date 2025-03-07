"""
Python conversion of the translit/uk module.
Link:
  - https://sv.wiktionary.org/wiki/Modul:translit/uk

Current version from 2022-08-26 18:19
  - https://sv.wiktionary.org/w/index.php?title=Modul:translit/uk&oldid=3704710
"""

import re
import unicodedata
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
    "Ґ": "G",
    "ґ": "g",
    "Д": "D",
    "д": "d",
    "Е": "E",
    "е": "e",
    "Є": "Je",
    "є": "je",
    "Ж": "Zj",
    "ж": "zj",
    "З": "Z",
    "з": "z",
    "И": "Y",
    "и": "y",
    "І": "I",
    "і": "i",
    "Ї": "Ji",
    "ї": "ji",
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
    "Щ": "Sjtj",
    "щ": "sjtj",
    "Ъ": "",
    "ъ": "",
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
    >>> transliterate("А,Б,В,Г,Ґ,Д")
    'A,B,V,H,G,D'
    >>> transliterate("о,п,р,с,т,у")
    'o,p,r,s,t,u'
    >>> transliterate("Ъ,Ь")
    ','
    >>> transliterate("сю,ся")
    'siu,sia'
    >>> transliterate("Ґалаґан")
    'Galagan'
    """
    cyrillic_q: deque[str] = deque(re.findall(multibyte_char_pattern, text))
    latin_q: deque[str] = deque()

    while cyrillic_q:
        x = cyrillic_q.popleft()
        y = cyrillic_q[0] if cyrillic_q else ""
        z = cyrillic_q[1] if len(cyrillic_q) > 1 else ""
        latin_q[-1] if latin_q else ""
        accent = "́"

        if x not in latin_by_cyrillic:
            latin_q.append(x)
        elif x == "ь":
            if y == "и":
                latin_q.append("j")
        elif x == "Ь":
            if y in ("и", "И"):
                latin_q.append("J")
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

    result = []

    while latin_q:
        x = latin_q.popleft()
        y = latin_q[0] if latin_q else ""

        if y == accent:
            x = unicodedata.normalize("NFC", f"{x}{y}")
            latin_q.popleft()

        result.append(x)

    return "".join(result)
