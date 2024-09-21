import re

from .general import sil as general_sil


def wtr(cyr: str) -> str:
    GR = "\u0300"  # grave =  ̀
    AC = "\u0301"  # acute = ˊ
    DI = "\u0308"  # diaeresis = ¨

    tab = {
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
        # archaic, pre-1918 letters
        "І": "I",
        "і": "i",
        "Ѳ": "F",
        "ѳ": "f",
        "Ѣ": "E",
        "ѣ": "e",
        "Ѵ": "I",
        "ѵ": "i",
        # composed combinations with grave accents map to uncomposed letters
        # for consistency with other char+grave combinations
        "ѐ": "e" + GR,
        "Ѐ": "E" + GR,
        "ѝ": "i" + GR,
        "Ѝ": "I" + GR,
    }

    # FIXME! Doesn't work with ɣ, which gets included in this character set
    non_consonants = r"[АОУҮЫЭЯЁЮИЕЪЬІѢѴаоуүыэяёюиеъьіѣѵAEIOUYƐaeiouyɛʹʺ\W]"

    def map_to_je(pre: str, e: str = "") -> str:
        map_to_je_map = {"Е": "Ie", "е": "ie", "Ѣ": "Ie", "ѣ": "ie"}
        if not e:
            return map_to_je_map.get(pre, "")
        return pre + map_to_je_map.get(e, "")

    def ureverse(s: str) -> str:
        return s[::-1]

    cyr = re.sub(GR, AC, cyr)

    # reducció de consonants duplicades no usades en català
    no_dobles = ["([Вв])в", "([Жж])ж", "([Кк])к", "([Хх])х", "([Цц])ц", "([Чч])ч", "([Шш])ш", "([Щщ])щ"]
    for regex in no_dobles:
        cyr = re.sub(regex, r"\1", cyr)

    # si no hi ha cap accent i alguna ё, accentuem la darrera
    if "ё" in cyr or "Ё" in cyr:
        if AC not in cyr:
            cyr = ureverse(re.sub("([Ёё])", AC + r"\1", ureverse(cyr), 1))

    # ё after a "hushing" consonant becomes o
    cyr = re.sub("([жшчщЖШЧЩ])ё", r"\1o", cyr)

    # е after a vowel or at the beginning of a word becomes ie
    cyr = re.sub(r"^([ЕеѢѣ])", lambda m: map_to_je(m.group()), cyr)
    cyr = re.sub("(" + non_consonants + ")([ЕеѢѣ])", lambda m: map_to_je(m.group(1), m.group(2)), cyr)
    # need to do it twice in case of sequences of such vowels
    cyr = re.sub("(" + non_consonants + ")([ЕеѢѣ])", lambda m: map_to_je(m.group(1), m.group(2)), cyr)

    latin = "".join(tab.get(char, char) for char in cyr)

    # simplificació de dues i
    latin = re.sub(r"(i" + AC + r"?)i", r"\1", latin)

    # doble ela a ela geminada
    latin = re.sub(r"([Ll])([Ll])", r"\1·\2", latin)

    # correcció gue/gui
    latin = re.sub(r"([Gg])([ei])", r"\1u\2", latin)

    # regles d'accentuació en català
    char_acc = {
        "A" + AC: "À",
        "E" + AC: "É",
        "I" + AC: "Í",
        "O" + AC: "Ó",
        "U" + AC: "Ú",
        "a" + AC: "à",
        "e" + AC: "é",
        "i" + AC: "í",
        "i" + DI: "ï",
        "o" + AC: "ó",
        "u" + AC: "ú",
        "u" + DI: "ü",
    }
    latin_with_accent = re.sub(rf".{AC}", lambda match: char_acc[match.group()], latin)
    sil = general_sil(latin_with_accent).split("·")

    if len(sil) == 1:  # monosíl·laba sense accent
        latin = re.sub(AC, "", latin)
    elif re.search("[ÀàÉéÍíÓóÚú]", sil[-1]):  # aguda
        if not (re.search(r"[aeiou]" + AC + r"s?$", latin) or re.search(r"[ei]" + AC + r"n$", latin)):
            if "ю" + AC not in cyr:  # hiatus except diphthong iu
                latin = re.sub(r"([aeoiu][iu])" + AC, r"\1" + DI, latin)
            latin = re.sub(r"gui" + DI, "gui", latin)
            latin = re.sub(AC, "", latin)
    elif re.search("[ÀàÉéÍíÓóÚú]", sil[-2]):  # plana
        if re.search(r"[aeiou]s?$", latin) or re.search(r"[ei]n$", latin):
            if not re.search(r"[aeiou][iu]$", latin):
                latin = re.sub(r"([aeoiu][iu])" + AC, r"\1" + DI, latin)
                latin = re.sub(r"gui" + DI, "gui", latin)
                latin = re.sub(AC, "", latin)
    # accent obert à
    latin = re.sub(".[" + AC + DI + "]", lambda m: char_acc.get(m.group(), ""), latin)

    # correcció intervocàlica ss, ix
    latin = re.sub(r"([AEIOUaeiouÀÉÍÓÚàéíóúü])s([aeiouàéíóú])", r"\1ss\2", latin)
    latin = re.sub(r"([AEOUaeouÀÉÓÚàéóúü])x", r"\1ix", latin)
    return latin


def transliterate(text: str) -> str:
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
    trwords = [wtr(word) for word in text.split()]
    return " ".join(trwords)
