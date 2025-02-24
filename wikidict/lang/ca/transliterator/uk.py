"""
Python conversion of the uk-trans module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:uk-trans

Current version from 2022-12-19 08:37
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:uk-trans&oldid=2110141
"""

import re

from . import general

GR = "\u0300"  # grave =  ̀
AC = "\u0301"  # acute = ˊ
DI = "\u0308"  # diaeresis = ¨

tab = str.maketrans(
    {
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "H",
        "Ґ": "G",
        "Д": "D",
        "Е": "E",
        "Є": "Ie",
        "Ж": "J",
        "З": "Z",
        "И": "I",
        "Й": "I",
        "І": "I",
        "Ї": "Ii",
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
        "Ф": "F",
        "Х": "Kh",
        "Ц": "Ts",
        "Ч": "Tx",
        "Ш": "X",
        "Щ": "Sx",
        "Ь": "",
        "Ю": "Iu",
        "Я": "Ia",
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "ґ": "g",
        "д": "d",
        "е": "e",
        "є": "ie",
        "ж": "j",
        "з": "z",
        "и": "i",
        "й": "i",
        "і": "i",
        "ї": "ii",
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
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "tx",
        "ш": "x",
        "щ": "sx",
        "ь": "",
        "ю": "iu",
        "я": "ia",
        "’": "",
        "'": "",
        "Ё": "Io",
        "Ъ": "",
        "Ы": "I",
        "Ѣ": "I",
        "Э": "E",
        "Ѳ": "F",
        "Ѵ": "I",
        "Ѧ": "E",
        "ё": "io",
        "ъ": "",
        "ы": "i",
        "ѣ": "i",
        "э": "e",
        "ѳ": "f",
        "ѵ": "i",
        "ѧ": "e",
    }
)

char_acc = {
    f"A{AC}": "À",
    f"E{AC}": "È",
    f"I{AC}": "Í",
    f"O{AC}": "Ò",
    f"U{AC}": "Ú",
    f"a{AC}": "à",
    f"e{AC}": "è",
    f"i{AC}": "í",
    f"i{DI}": "ï",
    f"o{AC}": "ò",
    f"u{AC}": "ú",
    f"u{DI}": "ü",
}


def wtr(cyr: str) -> str:
    sub = re.sub
    contain = re.search

    cyr = cyr.replace(GR, AC)

    for pattern in [
        r"([Вв])в",
        r"([Гг])г",
        r"([Жж])ж",
        r"([Кк])к",
        r"([Хх])х",
        r"([Цц])ц",
        r"([Чч])ч",
        r"([Шш])ш",
        r"([Щщ])щ",
    ]:
        cyr = sub(pattern, r"\1", cyr)

    latin = cyr.translate(tab)
    latin = sub(rf"(i{AC}?)i", r"\1", latin)
    latin = latin.replace("ll", "l·l")
    latin = sub(r"([Gg])([ei])", r"\1u\2", latin)

    sil = general.sil(sub(rf".[{AC}{DI}]", lambda m: char_acc.get(m[0], m[0]), latin)).split("·")

    if len(sil) == 1:
        latin = latin.replace(AC, "")
    elif contain(r"[ÀàÈèÍíÒòÚú]", sil[-1]):
        if not contain(rf"[aeiou]{AC}s?$", latin) and not contain(rf"[ei]{AC}n$", latin):
            if not contain(rf"ю{AC}", cyr):
                latin = sub(rf"([aeoiu][iu]){AC}", rf"\1{DI}", latin)
            latin = latin.replace(f"gui{DI}", "gui").replace(AC, "")
    elif contain(r"[ÀàÈèÍíÒòÚú]", sil[-2]):
        if contain(r"[aeiou]s?$", latin) or contain(r"[ei]n$", latin):
            if not contain(r"[aeiou][iu]$", latin):
                latin = sub(rf"([aeoiu][iu]){AC}", rf"\1{DI}", latin)
                latin = latin.replace(f"gui{DI}", "gui").replace(AC, "")

    latin = sub(rf".[{AC}{DI}]", lambda m: char_acc.get(m[0], m[0]), latin)
    latin = sub(r"([AEIOUaeiouÀÈÍÒÚàèíïòúü])s([aeiouàèíòú])", r"\1ss\2", latin)
    return sub(r"([AEOUaeouÀÈÒÚàèòúü])x", r"\1ix", latin)


def transliterate(text: str, locale: str = "") -> str:
    """
    >>> transliterate("Украї́на")
    'Ukraïna'
    """
    return " ".join(wtr(word) for word in text.split())
