"""
Python conversion of the ber-trans module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:ber-trans

Current version from 2020-11-03 14:11
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:zh-trans&oldid=1576088
"""

T2L_COMMON = str.maketrans(
    {
        "ⴰ": "a",
        "ⴱ": "b",
        "ⴲ": "b",
        "ⴳ": "g",
        "ⴴ": "g",
        "ⴵ": "ǧ",
        "ⴶ": "ǧ",
        "ⴷ": "d",
        "ⴸ": "d",
        "ⴹ": "ḍ",
        "ⴺ": "ḍ",
        "ⴻ": "e",
        "ⴼ": "f",
        "ⴽ": "k",
        "ⴾ": "k",
        "ⴿ": "k",
        "ⵀ": "h",
        "ⵁ": "h",
        "ⵂ": "h",
        "ⵃ": "ḥ",
        "ⵄ": "ɛ",
        "ⵅ": "x",
        "ⵆ": "x",
        "ⵇ": "q",
        "ⵈ": "q",
        "ⵉ": "i",
        "ⵊ": "j",
        "ⵋ": "j",
        "ⵌ": "j",
        "ⵍ": "l",
        "ⵎ": "m",
        "ⵏ": "n",
        "ⵐ": "ny",
        "ⵑ": "ng",
        "ⵒ": "p",
        "ⵓ": "u",
        "ⵔ": "r",
        "ⵕ": "ṛ",
        "ⵖ": "ɣ",
        "ⵗ": "ɣ",
        "ⵘ": "j",
        "ⵙ": "s",
        "ⵚ": "ṣ",
        "ⵛ": "c",
        "ⵜ": "t",
        "ⵝ": "t",
        "ⵞ": "č",
        "ⵟ": "ṭ",
        "ⵠ": "v",
        "ⵡ": "w",
        "ⵢ": "y",
        "ⵣ": "z",
        "ⵤ": "z",
        "ⵥ": "ẓ",
        "ⵦ": "e",
        "ⵧ": "o",
        "ⵯ": "ʷ",
        "⵰": ".",
        "⵿": "",
    }
)

T2L_ALT = {
    "tmh": str.maketrans({"ⵀ": "b", "ⵓ": "w"}),
    "thz": str.maketrans({"ⵀ": "b", "ⵓ": "w", "ⵘ": "ɣ"}),
}
for lang in ["thv", "taq", "ttq"]:
    T2L_ALT[lang] = T2L_ALT["tmh"]


def transliterate(text: str, locale: str = "") -> str:
    """
    >>> transliterate("ⴰⴷⵔⴰⵔ", locale="zgh")
    'adrar'
    >>> transliterate("ⴱⵓⵙⵛⴰ", locale="tmh")
    'bwsca'
    """
    if locale and (tt := T2L_ALT.get(locale, {})):
        text = text.translate(tt)
    return text.translate(T2L_COMMON)
