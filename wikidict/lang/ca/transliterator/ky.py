"""
Python conversion of the ky-trans module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:ky-trans

Current version from 2022-12-19 09:52
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:ky-trans&oldid=2110146
"""

import re

GR = "\u0300"  # grave =  ̀
AC = "\u0301"  # acute = ˊ
DI = "\u0308"  # diaeresis = ¨

tab_tcrip = str.maketrans(
    {
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
        "Ё": "Io",
        "ё": "io",
        "Ж": "Dj",
        "ж": "dj",
        "З": "Z",
        "з": "z",
        "И": "I",
        "и": "i",
        "Й": "I",
        "й": "i",
        "К": "K",
        "к": "k",
        "Л": "L",
        "л": "l",
        "М": "M",
        "м": "m",
        "Н": "N",
        "н": "n",
        "Ң": "Ng",
        "ң": "ng",
        "О": "O",
        "о": "o",
        "Ө": "O",
        "ө": "o",
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
        "Ү": "U",
        "ү": "u",
        "Ф": "F",
        "ф": "f",
        "Х": "Kh",
        "х": "kh",
        "Ц": "Ts",
        "ц": "ts",
        "Ч": "Tx",
        "ч": "tx",
        "Ш": "X",
        "ш": "x",
        "Щ": "Sx",
        "щ": "sx",
        "Ъ": "",
        "ъ": "",
        "Ы": "U",
        "ы": "u",
        "Ь": "",
        "ь": "",
        "Э": "E",
        "э": "e",
        "Ю": "Iu",
        "ю": "iu",
        "Я": "Ia",
        "я": "ia",
    }
)

non_consonants = "[АЕЁИОӨҮЫЭЮЯаеёиоөүыэюяʹʺ]"


def map_to_je(pre: str, e: str | None = None) -> str:
    map_to_je_map = {"Е": "Ie", "е": "ie"}
    if e is None:
        return map_to_je_map.get(pre, "")
    return pre + map_to_je_map.get(e, "")


def wtr(cyr: str) -> str:
    sub = re.sub

    cyr = cyr.replace(GR, AC)

    for pattern in [
        "([Вв])в",
        "([Жж])ж",
        "([Кк])к",
        "([Ққ])қ",
        "([Ңң])ң",
        "([Хх])х",
        "([Һһ])һ",
        "([Цц])ц",
        "([Чч])ч",
        "([Шш])ш",
        "([Щщ])щ",
    ]:
        cyr = sub(pattern, r"\1", cyr)

    cyr = sub(r"^([Ее])", lambda m: map_to_je(m[1]), cyr)
    cyr = sub(rf"({non_consonants})([Ее])", lambda m: map_to_je(m[1], m[2]), cyr)
    cyr = sub(rf"({non_consonants})([Ее])", lambda m: map_to_je(m[1], m[2]), cyr)

    latin = cyr.translate(tab_tcrip)
    latin = sub(rf"(i{AC}?)i$", r"\1", latin)
    latin = sub(rf"(i{AC}?)i([^{AC}])", r"\1\2", latin)
    latin = latin.replace("ll", "l·l").replace("ngg", "ng")
    latin = sub(r"([Gg])([ei])", r"\1u\2", latin)

    char_acc = {
        f"A{AC}": "À",
        f"E{AC}": "É",
        f"I{AC}": "Í",
        f"O{AC}": "Ó",
        f"U{AC}": "Ú",
        f"a{AC}": "à",
        f"e{AC}": "é",
        f"i{AC}": "í",
        f"i{DI}": "ï",
        f"o{AC}": "ó",
        f"u{AC}": "ú",
        f"u{DI}": "ü",
    }
    latin = sub(rf".[{AC}{DI}]", lambda m: char_acc.get(m[0], m[0]), latin)

    latin = sub(r"([AEIOUaeiouÀÉÍÓÚàéíóúü])s([aeiouàéíóú])", r"\1ss\2", latin)
    latin = sub(r"([AEOUaeouÀÉÓÚàéóúü])x", r"\1ix", latin)
    return latin


def transliterate(text: str, locale: str = "") -> str:
    """
    >>> transliterate("кырк")
    'kurk'
    """
    return " ".join(wtr(word) for word in text.split())
