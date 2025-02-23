"""
Python conversion of the el-trans module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:el-trans

Current version from 2020-05-30 18:13
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:el-trans&oldid=1570860
"""

import re
import unicodedata

tt = {
    "α": "a",
    "β": "v",
    "γ": "g",
    "δ": "d",
    "ε": "e",
    "ζ": "z",
    "η": "i",
    "θ": "th",
    "ι": "i",
    "κ": "k",
    "λ": "l",
    "μ": "m",
    "ν": "n",
    "ξ": "x",
    "ο": "o",
    "π": "p",
    "ρ": "r",
    "σ": "s",
    "ς": "s",
    "τ": "t",
    "υ": "i",
    "φ": "f",
    "χ": "kh",
    "ψ": "ps",
    "ω": "o",
    "Α": "A",
    "Β": "V",
    "Γ": "G",
    "Δ": "D",
    "Ε": "E",
    "Ζ": "Z",
    "Η": "I",
    "Θ": "Th",
    "Ι": "I",
    "Κ": "K",
    "Λ": "L",
    "Μ": "M",
    "Ν": "N",
    "Ξ": "X",
    "Ο": "O",
    "Π": "P",
    "Ρ": "R",
    "Σ": "S",
    "Τ": "T",
    "Υ": "I",
    "Φ": "F",
    "Χ": "Kh",
    "Ψ": "Ps",
    "Ω": "O",
    ";": "?",
    "·": ";",
}


def transliterate(text: str) -> str:
    """
    >>> transliterate("Υ")
    'I'
    """
    acute = "\u0301"
    diaeresis = "\u0308"
    vowels = "αΑεΕηΗιΙυΥοΟωΩ" + acute + diaeresis

    find = re.search
    gsub = re.sub

    text = text.strip()
    text = unicodedata.normalize("NFD", text)
    text = re.sub(acute + diaeresis, diaeresis + acute, text)

    text = gsub(r"([βκπτ])\1", r"\1", text)
    text = gsub(r"(.?)γ[ιΙ]", lambda m: "i" if m.group(1) in ["", " ", "-"] else m.group(0), text)
    text = gsub(r"γγ(.)", lambda m: "ngu" + m.group(1) if find(r"[ει]", m.group(1)) else "ng" + m.group(1), text)
    text = gsub(
        r"(.?)γ[κΚ](.)",
        lambda m: m.group(1)
        + ("Ng" if m.group(2).isupper() else "ng")
        + ("u" + m.group(3) if find(r"[ει]", m.group(3)) else m.group(3)),
        text,
    )
    text = gsub(r"γ([ξχ])", r"n\1", text)
    text = gsub(r"μβ", "mb", text)
    text = gsub(
        r"(.?)μ[πΠ]",
        lambda m: m.group(1) + ("B" if m.group(2).isupper() else "b")
        if m.group(1) in ["", " ", "-"] or not find(vowels, m.group(1))
        else "mb",
        text,
    )
    text = gsub(
        r"(.?)ν[τΤ](.?)",
        lambda m: m.group(1) + ("D" if m.group(2).isupper() else "d") + m.group(3)
        if m.group(1) in ["", " ", "-"] or not find(vowels, m.group(1))
        else "nd" + m.group(3)
        if m.group(3) != "ζ"
        else m.group(0),
        text,
    )
    text = gsub(
        r"(.?)σ(.?)",
        lambda m: m.group(1) + "ss" + m.group(2)
        if find(vowels, m.group(1)) and find(vowels, m.group(2))
        else m.group(0),
        text,
    )
    text = gsub(
        r"([αεοΑΕΟ])ι(.?)",
        lambda m: {"α": "e", "Α": "E", "ε": "i", "Ε": "I", "ο": "i", "Ο": "I"}[m.group(1)] + m.group(2)
        if m.group(2) != diaeresis
        else m.group(0),
        text,
    )
    text = gsub(
        r"([αεΑΕ])υ(.?)", lambda m: tt[m.group(1)] + "v" + m.group(2) if m.group(2) != diaeresis else m.group(0), text
    )
    text = gsub(r"([αεοωΑΕΟΩ])η", lambda m: tt[m.group(1)] + "i" + diaeresis, text)
    text = gsub(r"([οΟ])υ", lambda m: "u" if m.group(1) == "ο" else "U", text)
    text = gsub(r".", lambda m: tt.get(m.group(0), m.group(0)), text)
    text = gsub(r"ll", "l·l", text)
    text = gsub(diaeresis, "", text)

    latin = unicodedata.normalize("NFC", text)
    latin = gsub(r"([áÁ])", lambda m: "à" if m.group(1) == "á" else "À", latin)
    sil = latin.split("·")

    if len(sil) == 1:
        latin = gsub(acute, "", text)
    elif find(r"[ÀàÉéÍíÓóÚú]", sil[-1]):
        if not find(r"[àéíóú]s?$", latin) and not find(r"[éí]n$", latin):
            text = gsub(r"([aeoiu][iu])" + acute, r"\1" + diaeresis, text)
            text = gsub(r"gui" + diaeresis, "gui", text)
            latin = gsub(acute, "", text)
    elif find(r"[ÀàÉéÍíÓóÚú]", sil[-2]):
        if find(r"[aeiou]s?$", text) or find(r"[ei]n$", text):
            if not find(r"[aeiou][iu]$", text):
                text = gsub(r"([aeoiu][iu])" + acute, r"\1" + diaeresis, text)
                text = gsub(r"gui" + diaeresis, "gui", text)
                latin = gsub(acute, "", text)

    return latin
