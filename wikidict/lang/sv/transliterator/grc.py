"""
Python conversion of the translit/grc module.
Link:
  - https://sv.wiktionary.org/wiki/Modul:translit/grc

Current version from 2022-09-08 04:54
  - https://sv.wiktionary.org/w/index.php?title=Modul:translit/grc&oldid=3716382
"""

import re
from queue import Queue

multibyte_char_pattern = re.compile(r".[\x80-\xBF]*")
acute_accent = "́"

latin_by_greek = {
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
    "Η": "Ē",
    "η": "ē",
    "Θ": "Th",
    "θ": "th",
    "Ι": "I",
    "ι": "i",
    "Κ": "K",
    "κ": "k",
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
    "Φ": "F",
    "φ": "f",
    "Χ": "Ch",
    "χ": "ch",
    "Ψ": "Ps",
    "ψ": "ps",
    "Ω": "Ō",
    "ω": "ō",
    "ϐ": "b",
    "ϑ": "th",
    "Ϲ": "S",
    "ϲ": "s",
    "Ϝ": "W",
    "ϝ": "w",
    "Ϙ": "Ḳ",
    "ϙ": "ḳ",
}

spiritus_asper = {
    "Ἁ": True,
    "Ἑ": True,
    "Ἡ": True,
    "Ἱ": True,
    "Ὁ": True,
    "Ὑ": True,
    "Ὡ": True,
    "ᾉ": True,
    "ᾙ": True,
    "ᾩ": True,
    "Ῥ": True,
    "Ἅ": True,
    "Ἕ": True,
    "Ἥ": True,
    "Ἵ": True,
    "Ὅ": True,
    "Ὕ": True,
    "Ὥ": True,
    "ᾍ": True,
    "ᾝ": True,
    "ᾭ": True,
    "Ἃ": True,
    "Ἓ": True,
    "Ἣ": True,
    "Ἳ": True,
    "Ὃ": True,
    "Ὓ": True,
    "Ὣ": True,
    "ᾋ": True,
    "ᾛ": True,
    "ᾫ": True,
    "Ἇ": True,
    "Ἧ": True,
    "Ἷ": True,
    "Ὗ": True,
    "Ὧ": True,
    "ᾏ": True,
    "ᾟ": True,
    "ᾯ": True,
    "ἁ": True,
    "ἑ": True,
    "ἡ": True,
    "ἱ": True,
    "ὁ": True,
    "ὑ": True,
    "ὡ": True,
    "ᾁ": True,
    "ᾑ": True,
    "ᾡ": True,
    "ῥ": True,
    "ἅ": True,
    "ἕ": True,
    "ἥ": True,
    "ἵ": True,
    "ὅ": True,
    "ὕ": True,
    "ὥ": True,
    "ᾅ": True,
    "ᾕ": True,
    "ᾥ": True,
    "ἃ": True,
    "ἓ": True,
    "ἣ": True,
    "ἳ": True,
    "ὃ": True,
    "ὓ": True,
    "ὣ": True,
    "ᾃ": True,
    "ᾓ": True,
    "ᾣ": True,
    "ἇ": True,
    "ἧ": True,
    "ἷ": True,
    "ὗ": True,
    "ὧ": True,
    "ᾇ": True,
    "ᾗ": True,
    "ᾧ": True,
}

versaler = {
    "Α",
    "Ε",
    "Η",
    "Ι",
    "Ο",
    "Υ",
    "Ω",
    "ᾼ",
    "ῌ",
    "ῼ",
    "Ρ",
    "Ά",
    "Έ",
    "Ή",
    "Ί",
    "Ό",
    "Ύ",
    "Ώ",
    "Ὰ",
    "Ὲ",
    "Ὴ",
    "Ὶ",
    "Ὸ",
    "Ὺ",
    "Ὼ",
    "Ἀ",
    "Ἐ",
    "Ἠ",
    "Ἰ",
    "Ὀ",
    "Ὠ",
    "ᾈ",
    "ᾘ",
    "ᾨ",
    "Ἄ",
    "Ἔ",
    "Ἤ",
    "Ἴ",
    "Ὄ",
    "Ὤ",
    "ᾌ",
    "ᾜ",
    "ᾬ",
    "Ἂ",
    "Ἒ",
    "Ἢ",
    "Ἲ",
    "Ὂ",
    "Ὢ",
    "ᾊ",
    "ᾚ",
    "ᾪ",
    "Ἆ",
    "Ἦ",
    "Ἶ",
    "Ὦ",
    "ᾎ",
    "ᾞ",
    "ᾮ",
    "Ἁ",
    "Ἑ",
    "Ἡ",
    "Ἱ",
    "Ὁ",
    "Ὑ",
    "Ὡ",
    "ᾉ",
    "ᾙ",
    "ᾩ",
    "Ῥ",
    "Ἅ",
    "Ἕ",
    "Ἥ",
    "Ἵ",
    "Ὅ",
    "Ὕ",
    "Ὥ",
    "ᾍ",
    "ᾝ",
    "ᾭ",
    "Ἃ",
    "Ἓ",
    "Ἣ",
    "Ἳ",
    "Ὃ",
    "Ὓ",
    "Ὣ",
    "ᾋ",
    "ᾛ",
    "ᾫ",
    "Ἇ",
    "Ἧ",
    "Ἷ",
    "Ὗ",
    "Ὧ",
    "ᾏ",
    "ᾟ",
    "ᾯ",
    "Ᾱ",
    "Ῑ",
    "Ῡ",
    "Ᾰ",
    "Ῐ",
    "Ῠ",
}

gemener = {
    "α",
    "ε",
    "η",
    "ι",
    "ο",
    "υ",
    "ω",
    "ᾳ",
    "ῃ",
    "ῳ",
    "ρ",
    "ά",
    "έ",
    "ή",
    "ί",
    "ό",
    "ύ",
    "ώ",
    "ᾴ",
    "ῄ",
    "ῴ",
    "ὰ",
    "ὲ",
    "ὴ",
    "ὶ",
    "ὸ",
    "ὺ",
    "ὼ",
    "ᾲ",
    "ῂ",
    "ῲ",
    "ᾶ",
    "ῆ",
    "ῖ",
    "ῦ",
    "ῶ",
    "ᾷ",
    "ῇ",
    "ῷ",
    "ἀ",
    "ἐ",
    "ἠ",
    "ἰ",
    "ὀ",
    "ὐ",
    "ὠ",
    "ᾀ",
    "ᾐ",
    "ᾠ",
    "ῤ",
    "ἄ",
    "ἔ",
    "ἤ",
    "ἴ",
    "ὄ",
    "ὔ",
    "ὤ",
    "ᾄ",
    "ᾔ",
    "ᾤ",
    "ἂ",
    "ἒ",
    "ἢ",
    "ἲ",
    "ὂ",
    "ὒ",
    "ὢ",
    "ᾂ",
    "ᾒ",
    "ᾢ",
    "ἆ",
    "ἦ",
    "ἶ",
    "ὖ",
    "ὦ",
    "ᾆ",
    "ᾖ",
    "ᾦ",
    "ἁ",
    "ἑ",
    "ἡ",
    "ἱ",
    "ὁ",
    "ὑ",
    "ὡ",
    "ᾁ",
    "ᾑ",
    "ᾡ",
    "ῥ",
    "ἅ",
    "ἕ",
    "ἥ",
    "ἵ",
    "ὅ",
    "ὕ",
    "ὥ",
    "ᾅ",
    "ᾕ",
    "ᾥ",
    "ἃ",
    "ἓ",
    "ἣ",
    "ἳ",
    "ὃ",
    "ὓ",
    "ὣ",
    "ᾃ",
    "ᾓ",
    "ᾣ",
    "ἇ",
    "ἧ",
    "ἷ",
    "ὗ",
    "ὧ",
    "ᾇ",
    "ᾗ",
    "ᾧ",
    "ϊ",
    "ϋ",
    "ΐ",
    "ΰ",
    "ῒ",
    "ῢ",
    "ῗ",
    "ῧ",
    "ᾱ",
    "ῑ",
    "ῡ",
    "ᾰ",
    "ῐ",
    "ῠ",
    "ϱ",
}

with_tonos = {
    "Ά",
    "Έ",
    "Ή",
    "Ί",
    "Ό",
    "Ύ",
    "Ώ",
    "Ἄ",
    "Ἔ",
    "Ἤ",
    "Ἴ",
    "Ὄ",
    "Ὤ",
    "ᾌ",
    "ᾜ",
    "ᾬ",
    "Ἅ",
    "Ἕ",
    "Ἥ",
    "Ἵ",
    "Ὅ",
    "Ὕ",
    "Ὥ",
    "ᾍ",
    "ᾝ",
    "ᾭ",
    "ά",
    "έ",
    "ή",
    "ί",
    "ό",
    "ύ",
    "ώ",
    "ᾴ",
    "ῄ",
    "ῴ",
    "ἄ",
    "ἔ",
    "ἤ",
    "ἴ",
    "ὄ",
    "ὔ",
    "ὤ",
    "ᾄ",
    "ᾔ",
    "ᾤ",
    "ἅ",
    "ἕ",
    "ἥ",
    "ἵ",
    "ὅ",
    "ὕ",
    "ὥ",
    "ᾅ",
    "ᾕ",
    "ᾥ",
    "ΐ",
    "ΰ",
}

alfa = {
    "α",
    "𝛂",
    "𝛼",
    "𝜶",
    "𝝰",
    "𝞪",
    "Α",
    "𝚨",
    "𝛢",
    "𝜜",
    "𝝖",
    "𝞐",
    "ἀ",
    "Ἀ",
    "ἄ",
    "Ἄ",
    "ᾄ",
    "ᾌ",
    "ἂ",
    "Ἂ",
    "ᾂ",
    "ᾊ",
    "ἆ",
    "Ἆ",
    "ᾆ",
    "ᾎ",
    "ᾀ",
    "ᾈ",
    "ἁ",
    "Ἁ",
    "ἅ",
    "Ἅ",
    "ᾅ",
    "ᾍ",
    "ἃ",
    "Ἃ",
    "ᾃ",
    "ᾋ",
    "ἇ",
    "Ἇ",
    "ᾇ",
    "ᾏ",
    "ᾁ",
    "ᾉ",
    "ά",
    "Ά",
    "ᾴ",
    "ὰ",
    "Ὰ",
    "ᾲ",
    "ᾰ",
    "Ᾰ",
    "ᾶ",
    "ᾷ",
    "ᾱ",
    "Ᾱ",
    "ᾳ",
    "ᾼ",
}

gamma = {"γ", "𝛄", "𝛾", "𝜸", "𝝲", "𝞬", "Γ", "𝚪", "𝛤", "𝜞", "𝝘", "𝞒", "ℽ", "ℾ", "ᵞ", "ᵧ", "ᴦ"}

epsilon = {
    "ε",
    "ϵ",
    "𝛆",
    "𝛜",
    "𝜀",
    "𝜖",
    "𝜺",
    "𝝐",
    "𝝴",
    "𝞊",
    "𝞮",
    "𝟄",
    "Ε",
    "𝚬",
    "𝛦",
    "𝜠",
    "𝝚",
    "𝞔",
    "ἐ",
    "Ἐ",
    "ἔ",
    "Ἔ",
    "ἒ",
    "Ἒ",
    "ἑ",
    "Ἑ",
    "ἕ",
    "Ἕ",
    "ἓ",
    "Ἓ",
    "έ",
    "Έ",
    "ὲ",
    "Ὲ",
}

eta = {
    "η",
    "𝛈",
    "𝜂",
    "𝜼",
    "𝝶",
    "𝞰",
    "Η",
    "𝚮",
    "𝛨",
    "𝜢",
    "𝝜",
    "𝞖",
    "ἠ",
    "Ἠ",
    "ἤ",
    "Ἤ",
    "ᾔ",
    "ᾜ",
    "ἢ",
    "Ἢ",
    "ᾒ",
    "ᾚ",
    "ἦ",
    "Ἦ",
    "ᾖ",
    "ᾞ",
    "ᾐ",
    "ᾘ",
    "ἡ",
    "Ἡ",
    "ἥ",
    "Ἥ",
    "ᾕ",
    "ᾝ",
    "ἣ",
    "Ἣ",
    "ᾓ",
    "ᾛ",
    "ἧ",
    "Ἧ",
    "ᾗ",
    "ᾟ",
    "ᾑ",
    "ᾙ",
    "ή",
    "Ή",
    "ῄ",
    "ὴ",
    "Ὴ",
    "ῂ",
    "ῆ",
    "ῇ",
    "ῃ",
    "ῌ",
}

jota = {
    "ι",
    "𝛊",
    "𝜄",
    "𝜾",
    "𝝸",
    "𝞲",
    "Ι",
    "𝚰",
    "𝛪",
    "𝜤",
    "𝝞",
    "𝞘",
    "ἰ",
    "Ἰ",
    "ἴ",
    "Ἴ",
    "ἲ",
    "Ἲ",
    "ἶ",
    "Ἶ",
    "ἱ",
    "Ἱ",
    "ἵ",
    "Ἵ",
    "ἳ",
    "Ἳ",
    "ἷ",
    "Ἷ",
    "ί",
    "Ί",
    "ὶ",
    "Ὶ",
    "ῐ",
    "Ῐ",
    "ῖ",
    "ϊ",
    "Ϊ",
    "ΐ",
    "ῒ",
    "ῗ",
    "ῑ",
    "Ῑ",
    "ͺ",
}

kappa = {"κ", "ϰ", "𝛋", "𝛞", "𝜅", "𝜘", "𝜿", "𝝒", "𝝹", "𝞌", "𝞳", "𝟆", "Κ", "𝚱", "𝛫", "𝜥", "𝝟", "𝞙", "ϗ", "Ϗ"}

xi = {"ξ", "𝛏", "𝜉", "𝝃", "𝝽", "𝞷", "Ξ", "𝚵", "𝛯", "𝜩", "𝝣", "𝞝"}

omikron = {
    "ο",
    "𝛐",
    "𝜊",
    "𝝄",
    "𝝾",
    "𝞸",
    "Ο",
    "𝚶",
    "𝛰",
    "𝜪",
    "𝝤",
    "𝞞",
    "ὀ",
    "Ὀ",
    "ὄ",
    "Ὄ",
    "ὂ",
    "Ὂ",
    "ὁ",
    "Ὁ",
    "ὅ",
    "Ὅ",
    "ὃ",
    "Ὃ",
    "ό",
    "Ό",
    "ὸ",
    "Ὸ",
}

rho = {
    "ρ",
    "ϱ",
    "𝛒",
    "𝛠",
    "𝜌",
    "𝜚",
    "𝝆",
    "𝝔",
    "𝞀",
    "𝞎",
    "𝞺",
    "𝟈",
    "Ρ",
    "𝚸",
    "𝛲",
    "𝜬",
    "𝝦",
    "𝞠",
    "ᵨ",
    "ῤ",
    "ῥ",
    "Ῥ",
    "ᴩ",
    "ϼ",
}

ypsilon = {
    "υ",
    "𝛖",
    "𝜐",
    "𝝊",
    "𝞄",
    "𝞾",
    "Υ",
    "ϒ",
    "𝚼",
    "𝛶",
    "𝜰",
    "𝝪",
    "𝞤",
    "ὐ",
    "ὔ",
    "ὒ",
    "ὖ",
    "ὑ",
    "Ὑ",
    "ὕ",
    "Ὕ",
    "ὓ",
    "Ὓ",
    "ὗ",
    "Ὗ",
    "ύ",
    "Ύ",
    "ὺ",
    "Ὺ",
    "ῠ",
    "Ῠ",
    "ῦ",
    "ϋ",
    "Ϋ",
    "ϔ",
    "ΰ",
    "ῢ",
    "ῧ",
    "ῡ",
    "Ῡ",
}

chi = {"χ", "𝛘", "𝜒", "𝝌", "𝞆", "𝟀", "Χ", "𝚾", "𝛸", "𝜲", "𝝬", "𝞦", "ᵡ", "ᵪ"}

omega = {
    "ω",
    "𝛚",
    "𝜔",
    "𝝎",
    "𝞈",
    "𝟂",
    "Ω",
    "𝛀",
    "𝛺",
    "𝜴",
    "𝝮",
    "𝞨",
    "ὠ",
    "Ὠ",
    "ὤ",
    "Ὤ",
    "ᾤ",
    "ᾬ",
    "ὢ",
    "Ὢ",
    "ᾢ",
    "ᾪ",
    "ὦ",
    "Ὦ",
    "ᾦ",
    "ᾮ",
    "ᾠ",
    "ᾨ",
    "ὡ",
    "Ὡ",
    "ὥ",
    "Ὥ",
    "ᾥ",
    "ᾭ",
    "ὣ",
    "Ὣ",
    "ᾣ",
    "ᾫ",
    "ὧ",
    "Ὧ",
    "ᾧ",
    "ᾯ",
    "ᾡ",
    "ᾩ",
    "ώ",
    "Ώ",
    "ῴ",
    "ὼ",
    "Ὼ",
    "ῲ",
    "ῶ",
    "ῷ",
    "ῳ",
    "ῼ",
    "ꭥ",
    "㏀",
    "㏁",
}

hiatus = {"Ϊ", "Ϋ", "ϊ", "ϋ", "ΐ", "ΰ", "ῒ", "ῢ", "ῗ", "ῧ"}


def generate_latin_by_greek() -> None:
    for i in versaler:
        if i in alfa:
            latin_by_greek[i] = latin_by_greek["Α"]
            if i in spiritus_asper:
                latin_by_greek[i] = f"H{latin_by_greek['α']}"
        elif i in epsilon:
            latin_by_greek[i] = latin_by_greek["Ε"]
            if i in spiritus_asper:
                latin_by_greek[i] = f"H{latin_by_greek['ε']}"
        elif i in eta:
            latin_by_greek[i] = latin_by_greek["Η"]
            if i in spiritus_asper:
                latin_by_greek[i] = f"H{latin_by_greek['η']}"
        elif i in jota:
            latin_by_greek[i] = latin_by_greek["Ι"]
            if i in spiritus_asper:
                latin_by_greek[i] = f"H{latin_by_greek['ι']}"
        elif i in omikron:
            latin_by_greek[i] = latin_by_greek["Ο"]
            if i in spiritus_asper:
                latin_by_greek[i] = f"H{latin_by_greek['ο']}"
        elif i in rho:
            latin_by_greek[i] = latin_by_greek["Ρ"]
            if i in spiritus_asper:
                latin_by_greek[i] += "h"
        elif i in ypsilon:
            latin_by_greek[i] = latin_by_greek["Υ"]
            if i in spiritus_asper:
                latin_by_greek[i] = f"H{latin_by_greek['υ']}"
        elif i in omega:
            latin_by_greek[i] = latin_by_greek["Ω"]
            if i in spiritus_asper:
                latin_by_greek[i] = f"H{latin_by_greek['ω']}"
        if i in with_tonos:
            latin_by_greek[i] += acute_accent

    for i in gemener:
        if i in alfa:
            latin_by_greek[i] = latin_by_greek["α"]
        elif i in epsilon:
            latin_by_greek[i] = latin_by_greek["ε"]
        elif i in eta:
            latin_by_greek[i] = latin_by_greek["η"]
        elif i in jota:
            latin_by_greek[i] = latin_by_greek["ι"]
        elif i in omikron:
            latin_by_greek[i] = latin_by_greek["ο"]
        elif i in rho:
            latin_by_greek[i] = latin_by_greek["ρ"]
        elif i in ypsilon:
            latin_by_greek[i] = latin_by_greek["υ"]
        elif i in omega:
            latin_by_greek[i] = latin_by_greek["ω"]
        if i in spiritus_asper:
            if i in rho:
                latin_by_greek[i] += "h"
            else:
                latin_by_greek[i] = f"h{latin_by_greek[i]}"
        if i in with_tonos:
            latin_by_greek[i] += acute_accent


# Populate the latin_by_greek dictionary
generate_latin_by_greek()


def transliterate(text: str) -> str:
    """
    >>> transliterate("Μ,Ν,Ξ,Ο,Π,Ρ")
    'M,N,X,O,P,R'
    >>> transliterate("ς,τ,υ,φ,χ,ψ,ω")
    's,t,y,f,ch,ps,ō'
    >>> transliterate("Ἐγχειρίδιον")
    'Encheirídion'
    >>> transliterate("ὄστϱακον")
    'óstrakon'
    >>> transliterate("μετάϑεσις")
    'metáthesis'
    >>> transliterate("Τοῦ Κατὰ πασῶν αἱρέσεων ἐλέγχου βιβλίον αʹ")
    'Tou Kata pasōn hairéseōn elénchou biblíon aʹ'
    >>> transliterate("Ὦ φῶς, τελευταῖόν σε προσϐλέψαιμι νῦν,")
    'Ō fōs, teleutaión se prosblépsaimi nyn,'
    """
    greek_q: Queue[str] = Queue()
    latin_q: Queue[str] = Queue()

    for c in re.findall(multibyte_char_pattern, text):
        greek_q.put(c)

    while not greek_q.empty():
        x = greek_q.get()
        y = greek_q.queue[0] if not greek_q.empty() else None
        greek_q.queue[1] if greek_q.qsize() > 1 else None
        u = latin_q.queue[-1] if not latin_q.empty() else None
        reversed_comma_above = "̔"

        if x not in latin_by_greek:  # Non-Greek character
            latin_q.put(x)
        elif (latin_q.empty() or u == " ") and y in spiritus_asper:
            latin_q.put(latin_by_greek[y][0])  # Capital "H" or lowercase "h"
            if x in ypsilon and y in jota and y not in hiatus:
                latin_q.put("ú" if x in with_tonos else "u")
            else:
                latin_q.put(latin_by_greek[x])
            if (
                (x in alfa or x in epsilon or x in eta or x in omikron or x in omega)
                and y in ypsilon
                and y not in hiatus
            ):
                latin_q.put("ú" if y in with_tonos else "u")
            else:
                latin_q.put(latin_by_greek[y][1:])
            greek_q.get()
        elif (x in alfa or x in epsilon or x in eta or x in omikron or x in omega) and y in ypsilon and y not in hiatus:
            latin_q.put(latin_by_greek[x])
            latin_q.put("ú" if y in with_tonos else "u")
            greek_q.get()
        elif x in ypsilon and y in jota and y not in hiatus:
            if x in with_tonos and x in spiritus_asper:
                latin_q.put("hú")
            elif x in with_tonos:
                latin_q.put("ú")
            elif x in spiritus_asper:
                latin_q.put("hu")
            else:
                latin_q.put("u")
            latin_q.put(latin_by_greek[y])
            greek_q.get()
        elif x in gamma and y in gamma:
            latin_q.put("n")
            latin_q.put(latin_by_greek["γ"])
            greek_q.get()
        elif x in gamma and y in kappa:
            latin_q.put("n")
            latin_q.put(latin_by_greek["κ"])
            greek_q.get()
        elif x in gamma and y in xi:
            latin_q.put("n")
            latin_q.put(latin_by_greek["ξ"])
            greek_q.get()
        elif x in gamma and y in chi:
            latin_q.put("n")
            latin_q.put(latin_by_greek["χ"])
            greek_q.get()
        elif y == reversed_comma_above:
            latin_q.put("h")  # TODO: Can this be capital "H"? Diphthongs?
            latin_q.put(latin_by_greek[x])
            greek_q.get()
        else:
            latin_q.put(latin_by_greek[x])

    result: list[str] = []
    while not latin_q.empty():
        result.append(latin_q.get())

    return "".join(result)
