import logging
import re
import unicodedata

log = logging.getLogger(__name__)

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
basic_Greek = r"[\u0384-\u03FF]"  # excluding first line of Greek and Coptic block

info = {}
vowel_t = {"vowel": True}
iota_t = {"vowel": True, "offglide": True}
upsilon_t = {"vowel": True, "offglide": True}
rho_t: dict[str, bool] = {}
diacritic_t = {"diacritic": True}
breathing_t = {"diacritic": True}


def add_info(characters: str | list[str], t: dict[str, bool]) -> None:
    if isinstance(characters, str):
        for character in characters:  # TODO filter utf-8 chars ?
            info[character] = t
    else:
        for character in characters:
            info[character] = t


add_info([macron, breve, diaeresis, acute, grave, circum, subscript], diacritic_t)
add_info([rough, smooth], breathing_t)
add_info("ΑΕΗΟΩαεηοω", vowel_t)
add_info("Ιι", iota_t)
add_info("Υυ", upsilon_t)
add_info("Ρρ", rho_t)


def decompose(text: str) -> str:
    return unicodedata.normalize("NFD", text)


def set_list(li: list[str], i: int, v: str) -> None:
    try:
        li[i] = v
    except IndexError:
        for _ in range(i - len(li) + 1):
            li.append("")
        li[i] = v


def make_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    prev_info: dict[str, bool] = {}
    token_i, vowel_count = 0, 0
    prev = None
    for character in decompose(text):  # TODO filter non UTF8 ?
        curr_info = info.get(character, {})
        if curr_info.get("vowel"):
            vowel_count += 1
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
                    previous_vowel = ""
                    vowel_with_diaeresis = ""
                    if matches := re.match("^(" + basic_Greek + ")(" + basic_Greek + ".+)", tokens[token_i]):
                        previous_vowel, vowel_with_diaeresis = matches.groups()
                    if previous_vowel:
                        set_list(tokens, token_i, previous_vowel)
                        set_list(tokens, token_i + 1, vowel_with_diaeresis)
                        token_i += 1
            elif prev_info == rho_t:
                if curr_info != breathing_t:
                    log.error("The character %s in %s should not have the accent {character} on it.", prev, text)
            else:
                log.error("The character %s cannot have a diacritic on it.", prev)
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


def gsub(pattern: str, replacements: dict[str, str], string: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return replacements.get(match.group(0), match.group(0))

    return re.sub(pattern, replace, string)


# see https://en.wiktionary.org/wiki/Module:grc-translit/testcases for test cases
def transliterate(text: str) -> str:
    """
    >>> transliterate("λόγος")
    'lógos'
    >>> transliterate("σφίγξ")
    'sphínx'
    >>> transliterate("ϝάναξ")
    'wánax'
    >>> transliterate("οἷαι")
    'hoîai'
    >>> transliterate("ΙΧΘΥΣ")
    'IKhThYS'
    >>> transliterate("Υἱός")
    'Yhiós'
    >>> transliterate("ταῦρος")
    'taûros'
    >>> transliterate("νηῦς")
    'nēŷs'
    >>> transliterate("σῦς")
    'sŷs'
    >>> transliterate("ὗς")
    'hŷs'
    >>> transliterate("γυῖον")
    'gyîon'
    >>> transliterate("ἀναῡ̈τέω")
    'anaȳ̈téō'
    >>> transliterate("δαΐφρων")
    'daḯphrōn'
    >>> transliterate("τῶν")
    'tôn'
    >>> transliterate("τοὶ")
    'toì'
    >>> transliterate("τῷ")
    'tôi'
    >>> transliterate("τούτῳ")
    'toútōi'
    >>> transliterate("σοφίᾳ")
    'sophíāi'
    >>> transliterate("μᾱ̆νός")
    'mānós'
    >>> transliterate("ὁ")
    'ho'
    >>> transliterate("οἱ")
    'hoi'
    >>> transliterate("εὕρισκε")
    'heúriske'
    >>> transliterate("ὑϊκός")
    'hyïkós'
    >>> transliterate("πυρρός")
    'pyrrhós'
    >>> transliterate("ῥέω")
    'rhéō'
    >>> transliterate("σάἁμον")
    'sáhamon'
    >>> transliterate("Ὀδυσσεύς")
    'Odysseús'
    >>> transliterate("Εἵλως")
    'Heílōs'
    >>> transliterate("ᾍδης")
    'Hā́idēs'
    >>> transliterate("ἡ Ἑλήνη")
    'hē Helḗnē'
    >>> transliterate("ἔχεις μοι εἰπεῖν, ὦ Σώκρατες, ἆρα διδακτὸν ἡ ἀρετή?")
    'ékheis moi eipeîn, ô Sṓkrates, âra didaktòn hē aretḗ?'
    >>> transliterate("τί τηνικάδε ἀφῖξαι, ὦ Κρίτων? ἢ οὐ πρῲ ἔτι ἐστίν?")
    'tí tēnikáde aphîxai, ô Krítōn? ḕ ou prṑi éti estín?'
    >>> transliterate("τούτων φωνήεντα μέν ἐστιν ἑπτά· α ε η ι ο υ ω.")
    'toútōn phōnḗenta mén estin heptá; a e ē i o y ō.'
    >>> transliterate("πήγ(νῡμῐ)")
    'pḗg(nȳmi)'
    >>> transliterate("καλός&nbsp;καὶ&nbsp;ἀγαθός")
    'kalós&nbsp;kaì&nbsp;agathós'
    >>> transliterate("καλός&#32;καὶ&#32;ἀγαθός")
    'kalós&#32;kaì&#32;agathós'
    """
    if text == "῾":
        return "h"
    text = re.sub(r"([^A-Za-z0-9])[;" + "\u037e" + r"]", r"\1?", text)
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

        if re.search(macron_diaeresis, translit):
            translit = translit.replace(macron, "")
        if token != token.lower():
            translit = translit[0].upper() + translit[1:]
        output.append(translit)

    return unicodedata.normalize("NFC", "".join(output))
