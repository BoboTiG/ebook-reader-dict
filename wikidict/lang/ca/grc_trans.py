import re
import unicodedata

data = {}

macron = chr(0x304)
spacing_macron = chr(0xAF)
modifier_macron = chr(0x2C9)
breve = chr(0x306)
spacing_breve = chr(0x2D8)
rough = chr(0x314)
smooth = chr(0x313)
diaeresis = chr(0x308)
acute = chr(0x301)
grave = chr(0x300)
circum = chr(0x342)
Latin_circum = chr(0x302)
coronis = chr(0x343)
subscript = chr(0x345)
undertie = chr(0x35C)

data["diacritics"] = {
    "macron": macron,
    "spacing_macron": spacing_macron,
    "modifier_macron": modifier_macron,
    "breve": breve,
    "spacing_breve": spacing_breve,
    "rough": rough,
    "smooth": smooth,
    "diaeresis": diaeresis,
    "acute": acute,
    "grave": grave,
    "circum": circum,
    "Latin_circum": Latin_circum,
    "coronis": coronis,
    "subscript": subscript,
}

data["named"] = data["diacritics"]

data["diacritic"] = "[" + "".join(data["diacritics"].values()) + "]"
data["all"] = data["diacritic"]

data["diacritic_groups"] = {
    1: "[" + macron + breve + "]",
    2: "[" + diaeresis + smooth + rough + "]",
    3: "[" + acute + grave + circum + "]",
    4: subscript,
}
data["groups"] = data["diacritic_groups"]
data["diacritic_groups"]["accents"] = data["groups"][3]

data["diacritic_order"] = {
    macron: 1,
    breve: 1,
    rough: 2,
    smooth: 2,
    diaeresis: 2,
    acute: 3,
    grave: 3,
    circum: 3,
    subscript: 4,
}

data["diacritical_conversions"] = {
    spacing_macron: macron,
    modifier_macron: macron,
    spacing_breve: breve,
    "῾": rough,
    "ʽ": rough,
    "᾿": smooth,
    "ʼ": smooth,
    coronis: smooth,
    "´": acute,
    "`": grave,
    "῀": circum,
    "ˆ": circum,
    Latin_circum: circum,
    "῎": smooth + acute,
    "῍": smooth + grave,
    "῏": smooth + circum,
    "῞": rough + acute,
    "῝": rough + grave,
    "῟": rough + circum,
    "¨": diaeresis,
    "΅": diaeresis + acute,
    "῭": diaeresis + grave,
    "῁": diaeresis + circum,
}
data["conversions"] = data["diacritical_conversions"]

data["consonants"] = "ΒβΓγΔδΖζΘθΚκΛλΜμΝνΞξΠπΡρΣσςΤτΦφΧχΨψ"
data["consonant"] = "[" + data["consonants"] + "]"
data["vowels"] = "ΑαΕεΗηΙιΟοΥυΩω"
data["vowel"] = "[" + data["vowels"] + "]"
data["combining_diacritics"] = "".join([macron, breve, rough, smooth, diaeresis, acute, grave, circum, subscript])
data["combining_diacritic"] = "[" + data["combining_diacritics"] + "]"

# Basic letters with and without diacritics
letters_with_diacritics = "ΆΈ-ώϜϝἀ-ᾼῂ-ῌῐ-" + chr(0x1FDB) + "Ὶῠ-Ῥῲ-ῼ"
data["word_characters"] = letters_with_diacritics + data["combining_diacritics"] + undertie
data["word_character"] = "[" + data["word_characters"] + "]"

UTF8_char = r"[\u0001-\u007F\u00C2-\u00F4][\u0080-\u00BF]*"
basic_Greek = r"[\u00CE-\u00CF][\u0080-\u00BF]"  # excluding first line of Greek and Coptic block

info = {}
vowel_t = {"vowel": True}
iota_t = {"vowel": True, "offglide": True}
upsilon_t = {"vowel": True, "offglide": True}
rho_t = {}
diacritic_t = {"diacritic": True}
breathing_t = {"diacritic": True}


def add_info(characters, t):
    if isinstance(characters, str):
        for character in characters:  # TODO filter utf-8 chars ?
            info[character] = t
    else:
        for character in characters:
            info[character] = t


add_info([macron, breve, diaeresis, acute, grave, circum, subscript], diacritic_t)
add_info("ΑΕΗΟΩαεηοω", vowel_t)
add_info("Ιι", iota_t)
add_info("Υυ", upsilon_t)
add_info("Ρρ", rho_t)


def decompose(text):
    return unicodedata.normalize("NFD", text)


def set_list(li, i, v):
    try:
        li[i] = v
    except IndexError:
        for _ in range(i - len(li) + 1):
            li.append(None)
        li[i] = v


def make_tokens(text):
    tokens, prev_info = [], {}
    token_i, vowel_count = 0, 0
    prev = None
    for character in decompose(text):  # TODO filter non UTF8 ?
        curr_info = info.get(character, {})
        if curr_info.get("vowel"):
            vowel_count += 1
            print(character)
            print(curr_info)
            print(prev_info)
            if prev and (
                not (vowel_count == 2 and curr_info.get("offglide") and prev_info.get("vowel"))
                or prev_info.get("offglide")
                and curr_info == upsilon_t
                or curr_info == prev_info
            ):
                token_i += 1
                if prev_info.get("vowel"):
                    vowel_count = 1
            elif vowel_count == 2:
                vowel_count = 0
            set_list(tokens, token_i, (tokens[token_i] if token_i < len(tokens) else "") + character)
        elif curr_info.get("diacritic"):
            vowel_count = 0
            set_list(tokens, token_i, (tokens[token_i] if token_i < len(tokens) else "") + character)
            if prev_info.get("diacritic") or prev_info.get("vowel"):
                if character == diaeresis:
                    previous_vowel, vowel_with_diaeresis = re.match(
                        "^(" + basic_Greek + ")(" + basic_Greek + ".+)", tokens[token_i]
                    ).groups()
                    if previous_vowel:
                        tokens[token_i], tokens[token_i + 1] = previous_vowel, vowel_with_diaeresis
                        token_i += 1
            elif prev_info == rho_t:
                if curr_info != breathing_t:
                    print(f"The character {prev} in {text} should not have the accent {character} on it.")
            else:
                print(f"The character {prev} cannot have a diacritic on it.")
        else:
            vowel_count = 0
            if prev:
                token_i += 1
            set_list(tokens, token_i, (tokens[token_i] if token_i < len(tokens) else "") + character)
        prev = character
        prev_info = curr_info
    return tokens


macron_diaeresis = macron + diaeresis + "?" + Latin_circum
a_subscript = r"^[αΑ].*" + subscript + r"$"
velar = "κγχξ"

tt = {
    "α": "a",
    "ε": "e",
    "η": "e" + macron,
    "ι": "i",
    "ο": "o",
    "υ": "y",
    "ω": "o" + macron,
    "β": "b",
    "γ": "g",
    "δ": "d",
    "ζ": "z",
    "θ": "th",
    "κ": "k",
    "λ": "l",
    "μ": "m",
    "ν": "n",
    "ξ": "x",
    "π": "p",
    "ρ": "r",
    "σ": "s",
    "ς": "s",
    "τ": "t",
    "φ": "ph",
    "χ": "kh",
    "ψ": "ps",
    "ϝ": "w",
    "ϻ": "ś",
    "ϙ": "q",
    "ϡ": "š",
    "ͷ": "v",
    "ϐ": "b",
    "ϑ": "th",
    "ϰ": "k",
    "ϱ": "r",
    "ϲ": "s",
    "ϕ": "ph",
    breve: "",
    smooth: "",
    rough: "",
    circum: Latin_circum,
    subscript: "i",
}


def gsub(pattern, replacements, string):
    def replace(match):
        return replacements.get(match.group(0), match.group(0))

    return re.sub(pattern, replace, string)


def transliterate(text):
    """
    >>> transliterate("λόγος")
    'lógos'
    >>> transliterate("σφίγξ")
    'sphínx'
    >>> transliterate("ϝάναξ")
    'wánax'
    >>> transliterate("οἷαι")
    'hoîai'
    >>> transliterate("ταῦρος")
    'taûros'
    """
    if text == "῾":
        return "h"
    text = re.sub(r"([^A-Za-z0-9])[;" + "\u037E" + r"]", r"\1?", text)
    text = text.replace("·", ";")
    tokens = make_tokens(text)
    output = []
    for i in range(len(tokens)):
        token = tokens[i]
        translit = gsub(UTF8_char, tt, token.lower())
        for char, repl in tt.items():
            translit = translit.replace(char, repl)

        next_token = tokens[i + 1] if i + 1 < len(tokens) else None
        if token == "γ" and next_token and next_token in velar:
            translit = "n"
        elif token == "ρ" and tokens[i - 1] == "ρ":
            translit = "rh"
        elif re.search(r"[αεο][υὐ]", token):
            translit = translit.replace("y", "u")
        elif re.match(a_subscript, token):
            translit = re.sub(r"([aA])", r"\1" + macron, translit)

        if rough in token:
            if token.startswith("Ρ") or token.startswith("ρ"):
                translit += "h"
            else:
                translit = "h" + translit

        if any(char in token for char in [rough, diaeresis, Latin_circum]):
            translit = translit.replace(macron, "")

        if token != token.lower():
            translit = translit[0].upper() + translit[1:]

        output.append(translit)

    return unicodedata.normalize("NFC", "".join(output))


# print(transliterate("ταῦρος"))
print(transliterate("νηῦς"))
# print(transliterate("σῦς"))
# print(transliterate("ὗς"))
# print(transliterate("γυῖον"))
# print(transliterate("ἀναῡ̈τέω"))
# print(transliterate("δαΐφρων"))
