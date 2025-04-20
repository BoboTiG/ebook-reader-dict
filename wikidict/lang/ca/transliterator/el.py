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


def transliterate(text: str, locale: str = "") -> str:
    """
    >>> transliterate("Υ")
    'I'
    >>> transliterate("υφαντής")
    'ifandis'
    """
    acute = "\u0301"
    diaeresis = "\u0308"
    vowels = rf"[αΑεΕηΗιΙυΥοΟωΩ{acute}{diaeresis}]"

    contain = re.search
    sub = re.sub

    text = unicodedata.normalize("NFD", text.strip())
    text = text.replace(f"{acute}{diaeresis}", f"{diaeresis}{acute}")

    # no dobles ββ, κκ, ππ, ττ
    text = sub(r"([βκπτ])([βκπτ])", lambda m: m[1] if m[1] == m[2] else m[0], text)

    # γι (inicial) > i
    def matcher(m: re.Match[str]) -> str:
        before, current = m.groups()
        if before in {"", " ", "-"}:
            return "I" if current == "Γι" else "i"
        return m[0]

    text = sub(r"(.?)([γΓ]ι)", matcher, text)

    # γγ > ng(u)
    text = sub(r"γγ(.)", lambda m: ("ngu" if contain(r"[ει]", m[1]) else "ng") + m[1], text)

    # γκ (inicial, medial) > (n)g(u)
    def matcher2(m: re.Match[str]) -> str:
        before, gamma, following = m.groups()
        ucase = gamma == "Γ"
        cons = "G" if ucase else "g"
        if before not in {"", " ", "-"}:
            cons = "Ng" if ucase else "ng"
        if contain(r"[ει]", following):
            return f"{before}{cons}u{following}"
        return f"{before}{cons}{following}"

    text = sub(r"(.?)([γΓ])κ(.)", matcher2, text)

    text = sub(r"γ([ξχ])", r"n\1", text)
    text = text.replace("μβ", "mb")

    # μπ (inicial o rere consonant, medial) > (m)b
    def matcher3(m: re.Match[str]) -> str:
        before, mi = m.groups()
        ucase = mi == "Μ"
        if before in {"", " ", "-"} or not contain(vowels, before):
            return f"{before}{'B' if ucase else 'b'}"
        return f"{before}mb"

    text = sub(r"(.?)([μΜ])π", matcher3, text)

    # ντ (inicial o rere consonant, medial) > (n)d, excepte τζ > tz
    def matcher4(m: re.Match[str]) -> str:
        before, ni, following = m.groups()
        ucase = ni == "Ν"
        if before in {"", " ", "-"} or not contain(vowels, before):
            return f"{before}{'D' if ucase else 'd'}{following}"
        return f"{before}nd{following}" if following != "ζ" else m[0]

    text = sub(r"(.?)([νΝ])τ(.?)", matcher4, text)

    # ss entre vocals
    def matcher5(m: re.Match[str]) -> str:
        before, following = m.groups()
        if contain(vowels, before) and contain(vowels, following):
            return f"{before}ss{following}"
        return m[0]

    text = sub(r"(.?)σ(.?)", matcher5, text)

    # αι > e, ει > i, οι > i, excepte ϊ
    def matcher6(m: re.Match[str]) -> str:
        vowel, following = m.groups()
        if following != diaeresis:
            tr = str.maketrans({"α": "e", "Α": "E", "ε": "i", "Ε": "I", "ο": "i", "Ο": "I"})
            return f"{vowel.translate(tr)}{following}"
        return m[0]

    text = sub(r"([αεοΑΕΟ])ι(.?)", matcher6, text)

    # αυ > av, ευ > ev, excepte ϋ
    def matcher7(m: re.Match[str]) -> str:
        vowel, following = m.groups()
        return f"{tt[ord(vowel)]}v{following}" if following != diaeresis else m[0]

    text = sub(r"([αεΑΕ])υ(.?)", matcher7, text)

    text = sub(r"([αεοωΑΕΟΩ])η", lambda m: f"{tt[ord(m[1])]}i{diaeresis}", text)

    text = sub(r"([οΟ])υ", lambda m: "u" if m[1] == "ο" else "U", text)

    text = text.translate(tt)
    text = text.replace("ll", "l·l")

    # regles d'accentuació en català
    text = text.replace(diaeresis, "")

    latin = unicodedata.normalize("NFC", text)
    text = text.replace("á", "à").replace("Á", "À")

    if len(sil := latin.split("·")) == 1:  # monosíl·laba sense accent
        latin = text.replace(acute, "")
    elif contain(r"[ÀàÉéÍíÓóÚú]", sil[-1]):  # aguda
        if not (contain(r"[àéíóú]s?$", latin) or contain(r"[éí]n$", latin)):
            text = sub(rf"([aeoiu][iu]){acute}", rf"\1{diaeresis}", text)
            latin = text.replace(f"gui{diaeresis}", "gui").replace(acute, "")
    elif contain(r"[ÀàÉéÍíÓóÚú]", sil[-1]):  # plana
        if contain(r"[aeiou]s?$", text) or contain(r"[ei]n$", text):
            if not contain(r"[aeiou][iu]$", text):
                text = sub(rf"([aeoiu][iu]){acute}", rf"\1{diaeresis}", text)
                latin = text.replace(f"gui{diaeresis}", "gui").replace(acute, "")

    return latin
