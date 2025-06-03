"""
Python conversion of the ru-trans module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:ru-trans

Current version from 2022-09-19 06:55
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:ru-trans&oldid=2091459
"""

import re

from .. import general

GR = "\u0300"  # grave =  ̀
AC = "\u0301"  # acute = ˊ
DI = "\u0308"  # diaeresis = ¨

tab = str.maketrans(
    {
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "Io",
        "Ж": "J",
        "З": "Z",
        "И": "I",
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
        "Ф": "F",
        "Х": "Kh",
        "Ц": "Ts",
        "Ч": "Tx",
        "Ш": "X",
        "Щ": "Sx",
        "Ъ": "",
        "Ы": "I",
        "Ь": "",
        "Э": "E",
        "Ю": "Iu",
        "Я": "Ia",
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "io",
        "ж": "j",
        "з": "z",
        "и": "i",
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
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "tx",
        "ш": "x",
        "щ": "sx",
        "ъ": "",
        "ы": "i",
        "ь": "",
        "э": "e",
        "ю": "iu",
        "я": "ia",
        "І": "I",
        "і": "i",
        "Ѳ": "F",
        "ѳ": "f",
        "Ѣ": "E",
        "ѣ": "e",
        "Ѵ": "I",
        "ѵ": "i",
        "ѐ": f"e{GR}",
        "Ѐ": f"E{GR}",
        "ѝ": f"i{GR}",
        "Ѝ": f"I{GR}",
    }
)

non_consonants = r"[АОУҮЫЭЯЁЮИЕЪЬІѢѴаоуүыэяёюиеъьіѣѵAEIOUYƐaeiouyɛʹʺ\W]"
map_to_je_map = {"Е": "Ie", "е": "ie", "Ѣ": "Ie", "ѣ": "ie"}
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


def map_to_je(pre: str, e: str | None = None) -> str:
    if not e:
        return map_to_je_map[pre]
    return f"{pre}{map_to_je_map[e]}"


def wtr(cyr: str) -> str:
    sub = re.sub
    contain = re.search

    cyr = cyr.replace(GR, AC)

    for pattern in [
        r"([Вв])в",
        r"([Жж])ж",
        r"([Кк])к",
        r"([Хх])х",
        r"([Цц])ц",
        r"([Чч])ч",
        r"([Шш])ш",
        r"([Щщ])щ",
    ]:
        cyr = sub(pattern, r"\1", cyr)

    if ("ё" in cyr or "Ё" in cyr) and AC not in cyr:
        cyr = sub(r"([Ёё])", rf"{AC}\1", cyr[::-1], count=1)[::-1]

    cyr = sub(r"([жшчщЖШЧЩ])ё", r"\1o", cyr)
    cyr = sub(r"^([ЕеѢѣ])", lambda m: map_to_je(m[0]), cyr)
    cyr = sub(rf"({non_consonants})([ЕеѢѣ])", lambda m: map_to_je(m[1], m[2]), cyr)
    cyr = sub(rf"({non_consonants})([ЕеѢѣ])", lambda m: map_to_je(m[1], m[2]), cyr)

    latin = cyr.translate(tab)
    latin = sub(rf"(i{AC}?)i", r"\1", latin)
    latin = sub(r"([Ll])([Ll])", r"\1·\2", latin)
    latin = sub(r"([Gg])([ei])", r"\1u\2", latin)

    sil = general.sil(sub(rf".{AC}", lambda m: char_acc[m[0]], latin)).split("·")

    if len(sil) == 1:
        latin = latin.replace(AC, "")
    elif contain(r"[ÀàÉéÍíÓóÚú]", sil[-1]):
        if not contain(rf"[aeiou]{AC}s?$", latin) and not contain(rf"[ei]{AC}n$", latin):
            if f"ю{AC}" not in cyr:
                latin = sub(rf"([aeoiu][iu]){AC}", rf"\1{DI}", latin)
            latin = latin.replace(f"gui{DI}", "gui").replace(AC, "")
    elif contain(r"[ÀàÉéÍíÓóÚú]", sil[-2]):
        if contain(r"[aeiou]s?$", latin) or contain(r"[ei]n$", latin):
            if not contain(r"[aeiou][iu]$", latin):
                latin = sub(rf"([aeoiu][iu]){AC}", rf"\1{DI}", latin)
                latin = latin.replace(f"gui{DI}", "gui").replace(AC, "")

    latin = sub(rf".[{AC}{DI}]", lambda m: char_acc[m[0]], latin)
    latin = sub(r"([AEIOUaeiouÀÉÍÓÚàéíóúü])s([aeiouàéíóú])", r"\1ss\2", latin)
    return sub(r"([AEOUaeouÀÉÓÚàéóúü])x", r"\1ix", latin)


def transliterate(text: str, locale: str = "") -> str:
    """
    >>> transliterate("абха́з")
    'abkhaz'
    >>> transliterate("алеу́т")
    'aleüt'
    >>> transliterate("адыге́йский")
    'adigueiski'
    >>> transliterate("чеченец")
    'txetxenets'
    >>> transliterate("белору́с")
    'belorús'
    >>> transliterate("Катю́ша")
    'Katiüixa'
    >>> transliterate("Ка́тя")
    'Kàtia'
    >>> transliterate("Екатери́на")
    'Iekaterina'
    >>> transliterate("ё")
    'io'
    >>> transliterate("ЯЕ")
    'IaIe'
    """
    return " ".join(wtr(word) for word in text.split())
