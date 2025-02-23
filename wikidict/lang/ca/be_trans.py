"""
Python conversion of the be-trans module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:be-trans

Current version from 2022-12-19 09:45
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:be-trans&oldid=2110144
"""

import re

GR = "\u0300"  # grave =  ̀
AC = "\u0301"  # acute = ˊ
DI = "\u0308"  # diaeresis = ¨

# Transliteration table
tab = str.maketrans(
    {
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "H",
        "Ґ": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "Io",
        "Ж": "J",
        "З": "Z",
        "І": "I",
        "Й": "I",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ў": "U",
        "Ф": "F",
        "Х": "Kh",
        "Ц": "Ts",
        "Ч": "Tx",
        "Ш": "X",
        "Ы": "I",
        "Ь": "",
        "Э": "E",
        "Ю": "Iu",
        "Я": "Ia",
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "ґ": "g",
        "д": "d",
        "е": "e",
        "ё": "io",
        "ж": "j",
        "з": "z",
        "і": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ў": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "tx",
        "ш": "x",
        "ы": "i",
        "ь": "",
        "э": "e",
        "ю": "iu",
        "я": "ia",
        "’": "",
        "ʹ": "",
    }
)
non_consonants = "[АЁОУЎЬЭЯЮЕѴаёоуўьэяюеѵAEIOUYĚƐaeiouyěɛʹ’]"
map_to_je_map = {"Е": "Ie", "е": "ie"}

# Character accent correction
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


def map_to_je(match: re.Match[str]) -> str:
    pre, e = match.groups()
    return pre + map_to_je_map.get(e, "")


def wtr(cyr: str) -> str:
    contain = re.search
    sub = re.sub

    cyr = cyr.replace(GR, AC)

    for pattern in [r"([Вв])в", r"([Жж])ж", r"([Кк])к", r"([Хх])х", r"([Цц])ц", r"([Чч])ч", r"([Шш])ш"]:
        cyr = sub(pattern, r"\1", cyr)

    if ("Ё" in cyr or "ё" in cyr) and AC not in cyr:
        cyr = sub(r"([Ёё])", rf"{AC}\1", cyr[::-1], 1)[::-1]

    cyr = sub(r"([жшчщЖШЧЩ])ё", r"\1o", cyr)
    cyr = sub(r"^([Ее])", map_to_je, cyr)
    cyr = sub(rf"({non_consonants})([Ее])", map_to_je, cyr)
    cyr = sub(rf"({non_consonants})([Ее])", map_to_je, cyr)

    latin = cyr.translate(tab)
    latin = sub(rf"(i{AC}?)i", r"\1", latin).replace("ll", "l·l")
    latin = sub(r"([Gg])([ei])", r"\1u\2", latin)

    sil = sub(rf".{AC}", lambda m: char_acc.get(m[0], m[0]), latin).split("·")

    if contain(r"[ÀàÉéÍíÓóÚú]", sil[-1]):
        if not (contain(rf"[aeiou]{AC}s?$", latin) or contain(rf"[ei]{AC}n$", latin)):
            if f"ю{AC}" not in cyr:
                latin = sub(rf"([aeoiu][iu]){AC}", rf"\1{DI}", latin)
            latin = latin.replace(f"gui{DI}", "gui").replace(AC, "")
    elif contain(r"[ÀàÉéÍíÓóÚú]", sil[-2]):
        if contain(r"[aeiou]s?$", latin) or contain(r"[ei]n$", latin):
            if not contain(r"[aeiou][iu]$", latin):
                latin = sub(rf"([aeoiu][iu]){AC}", rf"\1{DI}", latin)
                latin = latin.replace(f"gui{DI}", "gui").replace(AC, "")

    latin = sub(rf".[{AC}{DI}]", lambda m: char_acc.get(m[0], m[0]), latin)
    latin = sub(r"([AEIOUaeiouÀÉÍÓÚàéíóúü])s([aeiouàéíóú])", r"\1ss\2", latin)
    latin = sub(r"([AEOUaeouÀÉÓÚàéóúü])x", r"\1ix", latin)

    return latin


def transliterate(text: str, locale: str = "") -> str:
    """
    >>> transliterate("Белару́сь")
    'Belarús'
    """
    return " ".join(wtr(word) for word in text.split())
