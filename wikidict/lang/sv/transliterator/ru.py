"""
Python conversion of the translit/ru module.
Link:
  - https://sv.wiktionary.org/wiki/Modul:translit/ru

Current version from 2022-09-03 12:48
  - https://sv.wiktionary.org/w/index.php?title=Modul:translit/ru&oldid=3714700
"""

import re
import string
from collections import deque

multibyte_char_pattern = re.compile(r".[\x80-\xBF]*")
punctuations = string.punctuation

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
    "Ё": "Jo",
    "ё": "jo",
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


def split_string_and_keep_separator(text: str, separator_pattern: str) -> list[str]:
    parts = re.split(rf"({separator_pattern})", text)
    return parts if parts[0] else parts[1:]


def add_accent_to_yo_if_polysyllabic(words_and_punctuations: list[str]) -> list[str]:
    vowels = "АЕЁИОУЭЮЫЯаеёиоуэюыя"

    def is_polysyllabic(word: str) -> bool:
        return sum(1 for char in word if char in vowels) > 1

    return [word.replace("ё", "ё́") if is_polysyllabic(word) else word for word in words_and_punctuations]


def add_accent_to_yo_in_polysyllabic_words(text: str) -> str:
    text = text.replace("ё́", "ё")
    words_and_punctuations = split_string_and_keep_separator(text, rf"[\s{punctuations}]")
    words_and_punctuations = add_accent_to_yo_if_polysyllabic(words_and_punctuations)
    return "".join(words_and_punctuations)


def transliterate(text: str) -> str:
    """
    >>> transliterate("Ш,Щ,Ы,Э,Ю,Я")
    'Sj,Sjtj,Y,E,Ju,Ja'
    >>> transliterate("о,п,р,с,т")
    'o,p,r,s,t'
    >>> transliterate("ЖА,Жa")
    'ZjA,Zja'
    >>> transliterate("Ъ,ъ")
    ','
    >>> transliterate("Игорь")
    'Igor'
    >>> transliterate("Михаил Горбачёв")
    'Michail Gorbatjov'
    >>> transliterate("Алексеев")
    'Aleksejev'
    >>> transliterate("Фёдор")
    'Fjodor'
    >>> transliterate("Пeтр")
    'Petr'
    >>> transliterate("замок")
    'zamok'
    >>> transliterate("IP-адрес")
    'IP-adres'
    >>> transliterate("Евгений")
    'Jevgenij'
    >>> transliterate("Я Тарзан. Ты Джейн.")
    'Ja Tarzan. Ty Dzjejn.'
    >>> transliterate("сё,сю,ся")
    'sio,siu,sia'
    >>> transliterate("Шё,Щё,Чё,Жё")
    'Sjo,Sjtjo,Tjo,Zjo'
    >>> transliterate("Когда́ вы прие́хали?")
    'Kogdá vy prijéchali?'
    >>> transliterate("Анна")
    'Anna'
    """
    cyrillic_q: deque[str] = deque(re.findall(multibyte_char_pattern, text))
    latin_q: deque[str] = deque()

    text = add_accent_to_yo_in_polysyllabic_words(text)

    while cyrillic_q:
        x = cyrillic_q.popleft()
        y = cyrillic_q[0] if cyrillic_q else ""
        z = cyrillic_q[1] if len(cyrillic_q) > 1 else ""
        u = latin_q[-1] if latin_q else ""
        accent = "́"

        if x not in latin_by_cyrillic:
            latin_q.append(x)
        elif (not latin_q or u == " ") and x == "Е":
            latin_q.append("Je")
        elif (not latin_q or u == " ") and x == "е":
            latin_q.append("je")
        elif x == "ь":
            if y == "и":
                latin_q.append("ji")
                cyrillic_q.popleft()
        elif x == "Ь":
            if y == "и":
                latin_q.append("Ji")
                cyrillic_q.popleft()
            elif y == "И":
                latin_q.append("JI")
                cyrillic_q.popleft()
        elif x in "стзСТЗ":
            latin_q.append(latin_by_cyrillic[x])
            if y == "ь":
                if z == "е":
                    latin_q.append("ie")
                    cyrillic_q.popleft()
                    cyrillic_q.popleft()
                elif z == "ё":
                    latin_q.append("io")
                    cyrillic_q.popleft()
                    cyrillic_q.popleft()
                elif z == "ю":
                    latin_q.append("iu")
                    cyrillic_q.popleft()
                    cyrillic_q.popleft()
                elif z == "я":
                    latin_q.append("ia")
                    cyrillic_q.popleft()
                    cyrillic_q.popleft()
            elif y == "ё":
                latin_q.append("io")
                cyrillic_q.popleft()
            elif y == "ю":
                latin_q.append("iu")
                cyrillic_q.popleft()
            elif y == "я":
                latin_q.append("ia")
                cyrillic_q.popleft()
        elif x in "шщчжШЩЧЖ":
            latin_q.append(latin_by_cyrillic[x])
            if y == "ё":
                latin_q.append("o")
                cyrillic_q.popleft()
        elif x == "е":
            if u in "aeouiyAEOUIY" or u == accent:
                latin_q.append("je")
            else:
                latin_q.append("e")
        else:
            latin_q.append(latin_by_cyrillic[x])

    result = []
    while latin_q:
        x = latin_q.popleft()
        y = latin_q[0] if latin_q else ""
        if y == accent:
            x = x + y
            latin_q.popleft()
        result.append(x)

    return "".join(result)
