"""
Python conversion of the Module:transliterator.
Links:
  - https://fr.wiktionary.org/wiki/Module:transliterator
  - https://fr.wiktionary.org/wiki/Module:transliterator/data

Current version from 2022-06-21T22:56:30
  - https://fr.wiktionary.org/w/index.php?title=Module:transliterator/data&oldid=30570377
"""

transliterations_common = {
    "-": "-",
    "=": "=",
    ",": ",",
    ".": ".",
    "/": "/",
    ";": ";",
    "'": "'",
    "[": "[",
    "]": "]",
    "\\": "\\",
    "`": "`",
    "~": "~",
    "!": "!",
    "@": "@",
    "#": "#",
    "$": "$",
    "%": "%",
    "^": "^",
    "&": "&",
    "*": "*",
    "(": "(",
    ")": ")",
    "_": "_",
    "+": "+",
    "{": "{",
    "}": "}",
    "|": "|",
    ":": ":",
    '"': '"',
    "<": "<",
    ">": ">",
    "?": "?",
    " ": " ",
    "’": "’",
}

transliterations_ar = {
    "ء": "ʾ",
    "ا": "ā",
    "ب": "b",
    "ت": "t",
    "ث": "ṯ",
    "ج": "ǧ",
    "ح": "ḥ",
    "خ": "ḫ",
    "د": "d",
    "ذ": "ḏ",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ش": "š",
    "ص": "ṣ",
    "ض": "ḍ",
    "ط": "ṭ",
    "ظ": "ẓ",
    "ع": "ʿ",
    "غ": "ġ",
    "ف": "f",
    "ق": "q",
    "ك": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    "و": "w",
    "ى": "y",
    "ي": "ī",
}

transliterations_bg = {
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
    "Е": "E",
    "е": "e",
    "Ж": "Ž",
    "ж": "ž",
    "З": "Z",
    "з": "z",
    "И": "I",
    "и": "i",
    "Й": "J",
    "й": "i",
    "Ф": "F",
    "ф": "f",
    "Х": "H",
    "х": "h",
    "Ц": "C",
    "ц": "c",
    "Ч": "Č",
    "ч": "č",
    "Ш": "Š",
    "ш": "š",
    "Щ": "Ŝ",
    "щ": "ŝ",
    "Ъ": "″",
    "ъ": "″",
    "Ю": "Û",
    "ю": "û",
    "Я": "Â",
    "я": "â",
}

transliterations_by = {
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
    "Ё": "Ё",
    "ё": "ё",
    "Ж": "Ž",
    "ж": "ž",
    "З": "Z",
    "з": "z",
    "І": "Ì",
    "і": "ì",
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
    "Х": "H",
    "х": "h",
    "Ц": "C",
    "ц": "c",
    "Ч": "Č",
    "ч": "č",
    "Ш": "Š",
    "ш": "š",
    "Ы": "Y",
    "ы": "y",
    "Ь": "ʹ",
    "ь": "ʹ",
    "Э": "È",
    "э": "è",
    "Ю": "Û",
    "ю": "û",
    "Я": "Â",
    "я": "â",
}

transliterations_el = {
    "Α": "A",
    "α": "a",
    "Β": "B",
    "β": "b",
    "Γ": "G",
    "γ": "g",
    "Δ": "D",
    "δ": "d",
    "Ε": "E",
    "ε": "e",
    "Ζ": "Z",
    "ζ": "z",
    "Η": "E",
    "η": "e",
    "Θ": "TH",
    "θ": "th",
    "Ι": "I",
    "ι": "i",
    "Κ": "C",
    "κ": "c",
    "Λ": "L",
    "λ": "l",
    "Μ": "M",
    "μ": "m",
    "Ν": "N",
    "ν": "n",
    "Ξ": "X",
    "ξ": "x",
    "Ο": "O",
    "ο": "o",
    "Π": "P",
    "π": "p",
    "Ρ": "R",
    "ρ": "r",
    "Σ": "S",
    "σ": "s",
    "ς": "s",
    "Τ": "T",
    "τ": "t",
    "Υ": "Y",
    "υ": "y",
    "Φ": "PH",
    "φ": "ph",
    "Χ": "CH",
    "χ": "ch",
    "Ψ": "PS",
    "ψ": "ps",
    "Ω": "O",
    "ω": "o",
}

transliterations_hi = {
    "अ": "a",
    "आ": "ā",
    "इ": "i",
    "ई": "ī",
    "उ": "u",
    "ऊ": "ū",
    "ऋ": "ṛ",
    "ॠ": "ṝ",
    "ऌ": "ḷ",
    "ॡ": "ḹ",
    "ए": "e",
    "ऐ": "ai",
    "ओ": "o",
    "औ": "au",
    "अं": "ṃ",
    "अः": "ḥ",
    "क": "k",
    "च": "c",
    "ट": "ṭ",
    "त": "t",
    "प": "p",
    "ख": "kh",
    "छ": "ch",
    "ठ": "ṭh",
    "थ": "th",
    "फ": "ph",
    "ग": "g",
    "ज": "j",
    "ड": "ḍ",
    "द": "d",
    "ब": "b",
    "घ": "gh",
    "झ": "jh",
    "ढ": "ḍh",
    "ध": "dh",
    "भ": "bh",
    "ङ": "ṅ",
    "ञ": "ñ",
    "ण": "ṇ",
    "न": "n",
    "म": "m",
    "य": "y",
    "र": "r",
    "ल": "l",
    "व": "v",
    "श": "ś",
    "ष": "ṣ",
    "स": "s",
    "ह": "h",
}

transliterations_hy = {
    "Ա": "A",
    "ա": "a",
    "Բ": "B",
    "բ": "b",
    "Գ": "G",
    "գ": "g",
    "Դ": "D",
    "դ": "d",
    "Ե": "E",
    "ե": "e",
    "Զ": "Z",
    "զ": "z",
    "Է": "Ē",
    "է": "ē",
    "Ը": "Ë",
    "ը": "ë",
    "Թ": "T’",
    "թ": "t’",
    "Ժ": "Ž",
    "ժ": "ž",
    "Ի": "I",
    "ի": "i",
    "Լ": "L",
    "լ": "l",
    "Խ": "X",
    "խ": "x",
    "Ծ": "Ç",
    "ծ": "ç",
    "Կ": "K",
    "կ": "k",
    "Հ": "H",
    "հ": "h",
    "Ձ": "J",
    "ձ": "j",
    "Ղ": "Ġ",
    "ղ": "ġ",
    "Ճ": "Č̣",
    "ճ": "č̣",
    "Մ": "M",
    "մ": "m",
    "Յ": "Y",
    "յ": "y",
    "Ն": "N",
    "ն": "n",
    "Շ": "Š",
    "շ": "š",
    "Ո": "O",
    "ո": "o",
    "Չ": "Č",
    "չ": "č",
    "Պ": "P",
    "պ": "p",
    "Ջ": "J̌",
    "ջ": "ǰ",
    "Ռ": "Ṙ",
    "ռ": "ṙ",
    "Ս": "S",
    "ս": "s",
    "Վ": "V",
    "վ": "v",
    "Տ": "T",
    "տ": "t",
    "Ր": "R",
    "ր": "r",
    "Ց": "c’",
    "ց": "c’",
    "Ւ": "W",
    "ւ": "w",
    "ՈՒ": "OW",
    "ու": "ow",
    "Փ": "P’",
    "փ": "p’",
    "Ք": "K’",
    "ք": "k’",
    "ԵՒ": "EW",
    "և": "ew",
    "Օ": "Ò",
    "օ": "ò",
    "Ֆ": "F",
    "ֆ": "f",
}

transliterations_kk = {
    "А": "A",
    "а": "a",
    "Ә": "Ä",
    "ә": "ä",
    "Б": "B",
    "б": "b",
    "В": "V",
    "в": "v",
    "Г": "G",
    "г": "g",
    "Ғ": "Ğ",
    "ғ": "ğ",
    "Д": "D",
    "д": "d",
    "Е": "E",
    "е": "e",
    "Ё": "Yo",
    "ё": "yo",
    "Ж": "J",
    "ж": "j",
    "З": "Z",
    "з": "z",
    "И": "Ï",
    "и": "ï",
    "Й": "Y",
    "й": "y",
    "К": "K",
    "к": "k",
    "Қ": "Q",
    "қ": "q",
    "Л": "L",
    "л": "l",
    "М": "M",
    "м": "m",
    "Н": "N",
    "н": "n",
    "Ң": "Ñ",
    "ң": "ñ",
    "О": "O",
    "о": "o",
    "Ө": "Ö",
    "ө": "ö",
    "П": "P",
    "п": "p",
    "Р": "R",
    "р": "r",
    "С": "S",
    "с": "s",
    "Т": "T",
    "т": "t",
    "У": "W",
    "у": "w",
    "Ұ": "U",
    "ұ": "u",
    "Ү": "Ü",
    "ү": "ü",
    "Ф": "F",
    "ф": "f",
    "Х": "X",
    "х": "x",
    "Һ": "H",
    "һ": "h",
    "Ц": "C",
    "ц": "c",
    "Ч": "Ç",
    "ч": "ç",
    "Ш": "Ș",
    "ш": "ş",
    "Щ": "Șş",
    "щ": "şş",
    "Ъ": "",
    "ъ": "",
    "Ы": "I",
    "ы": "ı",
    "І": "İ",
    "і": "i",
    "Ь": "",
    "ь": "",
    "Э": "E",
    "э": "e",
    "Ю": "Yu",
    "ю": "yu",
    "Я": "Ya",
    "я": "ya",
}

transliterations_mk = {
    "А": "A",
    "а": "a",
    "Б": "B",
    "б": "b",
    "В": "V",
    "в": "v",
    "Г": "G",
    "г": "g",
    "Ѓ": "Ǵ",
    "ѓ": "ǵ",
    "Д": "D",
    "д": "d",
    "Е": "E",
    "е": "e",
    "Ж": "Ž",
    "ж": "ž",
    "З": "Z",
    "з": "z",
    "Ѕ": "DZ",
    "ѕ": "dz",
    "И": "I",
    "и": "i",
    "Ј": "J",
    "ј": "j",
    "К": "K",
    "к": "k",
    "Л": "L",
    "л": "l",
    "Љ": "LJ",
    "љ": "lj",
    "М": "M",
    "м": "m",
    "Н": "N",
    "н": "n",
    "Њ": "NJ",
    "њ": "nj",
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
    "Ќ": "Ḱ",
    "ќ": "ḱ",
    "У": "U",
    "у": "u",
    "Ф": "F",
    "ф": "f",
    "Х": "H",
    "х": "h",
    "Ц": "TS",
    "ц": "ts",
    "Ч": "Č",
    "ч": "č",
    "Џ": "DŽ",
    "џ": "dž",
    "Ш": "Š",
    "ш": "š",
}

transliterations_ru = {
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
    "Ё": "JO",
    "ё": "jo",
    "Ж": "Ž",
    "ж": "ž",
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
    "Х": "KH",
    "х": "kh",
    "Ц": "TS",
    "ц": "ts",
    "Ч": "Č",
    "ч": "č",
    "Ш": "Š",
    "ш": "š",
    "Щ": "ŠTŠ",
    "щ": "štš",
    "Ъ": "<i>″</i>",
    "ъ": "<i>″</i>",
    "Ы": "Y",
    "ы": "y",
    "Ь": "ʹ",
    "ь": "ʹ",
    "Э": "É",
    "э": "é",
    "Ю": "JU",
    "ю": "ju",
    "Я": "JA",
    "я": "ja",
}

transliterations_sr = {
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
    "Ђ": "Đ",
    "ђ": "đ",
    "Е": "E",
    "е": "e",
    "Ж": "Ž",
    "ж": "ž",
    "Њ": "NJ",
    "њ": "nj",
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
    "Ћ": "Ć",
    "ћ": "ć",
    "З": "Z",
    "з": "z",
    "И": "I",
    "и": "i",
    "Ј": "J",
    "ј": "j",
    "К": "K",
    "к": "k",
    "Л": "L",
    "л": "l",
    "Љ": "LJ",
    "љ": "lj",
    "М": "M",
    "м": "m",
    "Н": "N",
    "н": "n",
    "У": "U",
    "у": "u",
    "Ф": "F",
    "ф": "f",
    "Х": "H",
    "х": "h",
    "Ц": "C",
    "ц": "c",
    "Ч": "Č",
    "ч": "č",
    "Џ": "DŽ",
    "џ": "dž",
    "Ш": "Š",
    "ш": "š",
}

transliterations_uk = {
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
    "Ж": "Ž",
    "ж": "ž",
    "З": "Z",
    "з": "z",
    "И": "Y",
    "и": "y",
    "І": "I",
    "і": "i",
    "Ї": "Ji",
    "ї": "ji",
    "Й": "Ï",
    "й": "ï",
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
    "Х": "Kh",
    "х": "kh",
    "Ц": "Ts",
    "ц": "ts",
    "Ч": "Tš",
    "ч": "tš",
    "Ш": "Š",
    "ш": "š",
    "Щ": "Štš",
    "щ": "štš",
    "Ь": "ʹ",
    "ь": "ʹ",
    "Ю": "Ju",
    "ю": "ju",
    "Я": "Ja",
    "я": "ja",
}

transliterations = {
    "common": transliterations_common,
    "ar": transliterations_ar,
    "bg": transliterations_bg,
    "by": transliterations_by,
    "el": transliterations_el,
    "hi": transliterations_hi,
    "hy": transliterations_hy,
    "kk": transliterations_kk,
    "mk": transliterations_mk,
    "ru": transliterations_ru,
    "sr": transliterations_sr,
    "uk": transliterations_uk,
}


def transliterate(locale: str, text: str) -> str:
    """
    Return the transliterated form of *text*.

        >>> transliterate("ar", "ا")
        'ā'
        >>> transliterate("ar", "بطيخ")
        'bṭīḫ'
        >>> transliterate("el", "α")
        'a'
        >>> transliterate("hi", "अ")
        'a'
        >>> transliterate("ru", "а")
        'a'
        >>> transliterate("ru", "дед")
        'ded'
        >>> transliterate("fr", "bim")
        ''
    """
    try:
        table = transliterations[locale]
    except KeyError:
        return ""
    return "".join(table.get(char, "") for char in text)
