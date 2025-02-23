"""
Python conversion of the el-trans module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:el-trans

Current version from 2020-05-30 18:13
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:el-trans&oldid=1570860
"""

import re
import unicodedata

tt = str.maketrans(
    {
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
)


def transliterate(text: str) -> str:
    """
    >>> transliterate("Υ")
    'I'
    """
    acute = "\u0301"
    diaeresis = "\u0308"
    vowels = f"αΑεΕηΗιΙυΥοΟωΩ{acute}{diaeresis}"

    contain = re.search
    sub = re.sub

    text = unicodedata.normalize("NFD", text.strip())
    text = text.replace(f"{acute}{diaeresis}", f"{diaeresis}{acute}")

    text = sub(r"([βκπτ])\1", r"\1", text)
    text = sub(r"(.?)γ[ιΙ]", lambda m: "i" if m[1] in {"", " ", "-"} else m[0], text)
    text = sub(r"γγ(.)", lambda m: ("ngu" if contain(r"[ει]", m[1]) else "ng") + m[1], text)
    text = sub(
        r"(.?)γ[κΚ](.)",
        lambda m: m[1] + ("Ng" if m[2].isupper() else "ng") + ("u" + m[3] if contain(r"[ει]", m[3]) else m[3]),
        text,
    )
    text = sub(r"γ([ξχ])", r"n\1", text)
    text = text.replace("μβ", "mb")
    text = sub(
        r"(.?)μ[πΠ]",
        lambda m: (
            m[1] + ("B" if m[2].isupper() else "b") if m[1] in {"", " ", "-"} or not contain(vowels, m[1]) else "mb"
        ),
        text,
    )
    text = sub(
        r"(.?)ν[τΤ](.?)",
        lambda m: (
            m[1] + ("D" if m[2].isupper() else "d") + m[3]
            if m[1] in {"", " ", "-"} or not contain(vowels, m[1])
            else f"nd{m[3]}"
            if m[3] != "ζ"
            else m[0]
        ),
        text,
    )
    text = sub(
        r"(.?)σ(.?)",
        lambda m: f"{m[1]}ss{m[2]}" if contain(vowels, m[1]) and contain(vowels, m[2]) else m[0],
        text,
    )
    text = sub(
        r"([αεοΑΕΟ])ι(.?)",
        lambda m: {"α": "e", "Α": "E", "ε": "i", "Ε": "I", "ο": "i", "Ο": "I"}[m[1]] + m[2]
        if m[2] != diaeresis
        else m[0],
        text,
    )
    text = sub(r"([αεΑΕ])υ(.?)", lambda m: f"{tt[ord(m[1])]}v" + m[2] if m[2] != diaeresis else m[0], text)
    text = sub(r"([αεοωΑΕΟΩ])η", lambda m: f"{tt[ord(m[1])]}i{diaeresis}", text)
    text = sub(r"([οΟ])υ", lambda m: "u" if m[1] == "ο" else "U", text)
    text = text.translate(tt).replace("ll", "l·l").replace(diaeresis, "")

    latin = unicodedata.normalize("NFC", text).replace("á", "à").replace("Á", "À")

    if len(sil := latin.split("·")) == 1:
        latin = text.replace(acute, "")
    elif (
        contain(r"[ÀàÉéÍíÓóÚú]", sil[-1]) and not contain(r"[àéíóú]s?$", latin) and not contain(r"[éí]n$", latin)
    ) or (
        contain(r"[ÀàÉéÍíÓóÚú]", sil[-2])
        and (contain(r"[aeiou]s?$", text) or contain(r"[ei]n$", text))
        and not contain(r"[aeiou][iu]$", text)
    ):
        text = sub(rf"([aeoiu][iu]){acute}", rf"\1{diaeresis}", text)
        latin = text.replace(f"gui{diaeresis}", "gui").replace(acute, "")

    return latin
