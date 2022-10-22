"""
https://fr.wiktionary.org/wiki/Modèle:ko-pron
Ce modèle montre les sons ou les phonèmes du mot coréen.
"""
import math
from re import sub
from types import SimpleNamespace
from typing import Callable, Match

# https://fr.wiktionary.org/wiki/Module:ko-hangeul/data (2018-05-26T03:08:13)
hangeul = SimpleNamespace(
    # Jamos d’initiale
    initiale=[
        "ㄱ",
        "ㄲ",
        "ㄴ",
        "ㄷ",
        "ㄸ",
        "ㄹ",
        "ㅁ",
        "ㅂ",
        "ㅃ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅉ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ],
    # Jamos de voyelle
    voyelle=[
        "ㅏ",
        "ㅐ",
        "ㅑ",
        "ㅒ",
        "ㅓ",
        "ㅔ",
        "ㅕ",
        "ㅖ",
        "ㅗ",
        "ㅘ",
        "ㅙ",
        "ㅚ",
        "ㅛ",
        "ㅜ",
        "ㅝ",
        "ㅞ",
        "ㅟ",
        "ㅠ",
        "ㅡ",
        "ㅢ",
        "ㅣ",
    ],
    # Jamos de finale
    finale=[
        "",
        "ㄱ",
        "ㄲ",
        "ㄳ",
        "ㄴ",
        "ㄵ",
        "ㄶ",
        "ㄷ",
        "ㄹ",
        "ㄺ",
        "ㄻ",
        "ㄼ",
        "ㄽ",
        "ㄾ",
        "ㄿ",
        "ㅀ",
        "ㅁ",
        "ㅂ",
        "ㅄ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ],
    # Changements phonologiques de deux consonnes
    frontiere={  # Article 11
        "ㄺㄱ": "ㄹ'ㄱ",
        # Article 12-1
        "ㅎㄱ": "ㅋ",
        "ㄱㅎ": "ㅋ",
        "ㄲㅎ": "ㅋ",
        "ㅋㅎ": "ㅋ",
        "ㅎㄷ": "ㅌ",
        "ㄷㅎ": "ㅌ",
        "ㅅㅎ": "ㅌ",
        "ㅊㅎ": "ㅌ",
        "ㅌㅎ": "ㅌ",
        "ㅎㅈ": "ㅊ",
        "ㅈㅎ": "ㅊ",
        "ㄶㄱ": "ㄴㅋ",
        "ㄶㄷ": "ㄴㅌ",
        "ㄶㅈ": "ㄴㅊ",
        "ㄵㅎ": "ㄴㅊ",
        "ㅀㄱ": "ㄹㅋ",
        "ㄺㅎ": "ㄹㅋ",
        "ㅀㄷ": "ㄹㅌ",
        "ㅀㅈ": "ㄹㅊ",
        "ㅂㅎ": "ㅍ",
        "ㄼㅎ": "ㄹㅍ",
        # inexpliqués dans le Standard mais clairs (nom + 하고)
        "ㄳㅎ": "ㅋ",
        "ㅄㅎ": "ㅍ",
        "ㅍㅎ": "ㅍ",
        # inexistants en coréen mais logiquement clairs
        "ㄿㅎ": "ㅍ",
        "ㅆㅎ": "ㅌ",
        # Article 12-2
        "ㅎㅅ": "'ㅅ",
        "ㄶㅅ": "ㄴ'ㅅ",
        "ㅀㅅ": "ㄹ'ㅅ",
        # Article 12-3
        "ㅎㄴ": "ㄴㄴ",
        "ㄶㄴ": "ㄴㄴ",
        # Article 12-4 : ㄹㅎ, ㄴㅎ, ㅁㅎ et ㅇㅎ sont traités en API
        "ㅎㅇ": "ㅇ",
        # Article 13 : ㅇㅇ est traité en API
        "ㄱㅇ": "ㄱ",
        "ㄲㅇ": "ㄲ",
        "ㅋㅇ": "ㅋ",
        "ㄴㅇ": "ㄴ",
        "ㄶㅇ": "ㄴ",
        "ㄷㅇ": "ㄷ",
        "ㅅㅇ": "ㅅ",
        "ㅆㅇ": "ㅆ",
        "ㅈㅇ": "ㅈ",
        "ㅊㅇ": "ㅊ",
        "ㅌㅇ": "ㅌ",
        "ㄹㅇ": "ㄹ",
        "ㅀㅇ": "ㄹ",
        "ㅁㅇ": "ㅁ",
        "ㅂㅇ": "ㅂ",
        "ㅍㅇ": "ㅍ",
        # Article 14
        "ㄳㅇ": "ㄱ'ㅅ",
        "ㄽㅇ": "ㄹ'ㅅ",
        "ㅄㅇ": "ㅂ'ㅅ",
        "ㄵㅇ": "ㄴㅈ",
        "ㄺㅇ": "ㄹㄱ",
        "ㄻㅇ": "ㄹㅁ",
        "ㄼㅇ": "ㄹㅂ",
        "ㄾㅇ": "ㄹㅌ",
        "ㄿㅇ": "ㄹㅍ",
        # Article 18
        "ㄱㅁ": "ㅇㅁ",
        "ㄲㅁ": "ㅇㅁ",
        "ㄳㅁ": "ㅇㅁ",
        "ㄺㅁ": "ㅇㅁ",
        "ㅋㅁ": "ㅇㅁ",
        "ㄷㅁ": "ㄴㅁ",
        "ㅅㅁ": "ㄴㅁ",
        "ㅆㅁ": "ㄴㅁ",
        "ㅈㅁ": "ㄴㅁ",
        "ㅊㅁ": "ㄴㅁ",
        "ㅌㅁ": "ㄴㅁ",
        "ㅎㅁ": "ㄴㅁ",
        "ㄿㅁ": "ㅁㅁ",
        "ㅂㅁ": "ㅁㅁ",
        "ㅄㅁ": "ㅁㅁ",
        "ㅍㅁ": "ㅁㅁ",
        "ㄱㄴ": "ㅇㄴ",
        "ㄲㄴ": "ㅇㄴ",
        "ㄳㄴ": "ㅇㄴ",
        "ㄺㄴ": "ㅇㄴ",
        "ㅋㄴ": "ㅇㄴ",
        "ㄷㄴ": "ㄴㄴ",
        "ㅅㄴ": "ㄴㄴ",
        "ㅆㄴ": "ㄴㄴ",
        "ㅈㄴ": "ㄴㄴ",
        "ㅊㄴ": "ㄴㄴ",
        "ㅌㄴ": "ㄴㄴ",
        "ㅎㄴ": "ㄴㄴ",
        "ㄿㄴ": "ㅁㄴ",
        "ㅂㄴ": "ㅁㄴ",
        "ㅄㄴ": "ㅁㄴ",
        "ㅍㄴ": "ㅁㄴ",
        # Article 19
        "ㄱㄹ": "ㅇㄴ",
        "ㄲㄹ": "ㅇㄴ",
        "ㄳㄹ": "ㅇㄴ",
        "ㄺㄹ": "ㅇㄴ",
        "ㅇㄹ": "ㅇㄴ",
        "ㅋㄹ": "ㅇㄴ",
        "ㄻㄹ": "ㅁㄴ",
        "ㅁㄹ": "ㅁㄴ",
        "ㄿㄹ": "ㅁㄴ",
        "ㅂㄹ": "ㅁㄴ",
        "ㅄㄹ": "ㅁㄴ",
        "ㅍㄹ": "ㅁㄴ",
        # inexpliqués dans le Standard
        "ㄷㄹ": "ㄴㄴ",
        "ㅅㄹ": "ㄴㄴ",
        "ㅆㄹ": "ㄴㄴ",
        "ㅈㄹ": "ㄴㄴ",
        "ㅊㄹ": "ㄴㄴ",
        "ㅌㄹ": "ㄴㄴ",
        # Article 20
        "ㄹㄴ": "ㄹㄹ",
        "ㄼㄴ": "ㄹㄹ",
        "ㄽㄴ": "ㄹㄹ",
        "ㄾㄴ": "ㄹㄹ",
        "ㅀㄴ": "ㄹㄹ",
        "ㄴㄹ": "ㄹㄹ",
        "ㄵㄹ": "ㄹㄹ",
        "ㄶㄹ": "ㄹㄹ",
        "ㄼㄹ": "ㄹㄹ",
        "ㄽㄹ": "ㄹㄹ",
        "ㄾㄹ": "ㄹㄹ",
        "ㅀㄹ": "ㄹㄹ",
        # Article 24 ; ㄴ, ㅁ et ㄻ sont traités par [[Modèle:ko-conj]]
        "ㄵㄱ": "ㄴ'ㄱ",
        "ㄵㄷ": "ㄴ'ㄷ",
        "ㄵㅅ": "ㄴ'ㅅ",
        "ㄵㅈ": "ㄴ'ㅈ",
        # Article 25
        "ㄼㄱ": "ㄹ'ㄱ",
        "ㄼㄷ": "ㄹ'ㄷ",
        "ㄼㅅ": "ㄹ'ㅅ",
        "ㄼㅈ": "ㄹ'ㅈ",
        "ㄾㄱ": "ㄹ'ㄱ",
        "ㄾㄷ": "ㄹ'ㄷ",
        "ㄾㅅ": "ㄹ'ㅅ",
        "ㄾㅈ": "ㄹ'ㅈ",
    },
    # Articles 9, 10 et 11 : neutralisation des finales
    neutralisation={
        "": "",
        "ㄱ": "ㄱ",
        "ㄲ": "ㄱ",
        "ㄳ": "ㄱ",
        "ㄴ": "ㄴ",
        "ㄵ": "ㄴ",
        "ㄶ": "ㄴ",
        "ㄷ": "ㄷ",
        "ㄹ": "ㄹ",
        "ㄺ": "ㄱ",
        "ㄻ": "ㅁ",
        "ㄼ": "ㄹ",
        "ㄽ": "ㄹ",
        "ㄾ": "ㄹ",
        "ㄿ": "ㅂ",
        "ㅀ": "ㄹ",
        "ㅁ": "ㅁ",
        "ㅂ": "ㅂ",
        "ㅄ": "ㅂ",
        "ㅅ": "ㄷ",
        "ㅆ": "ㄷ",
        "ㅇ": "ㅇ",
        "ㅈ": "ㄷ",
        "ㅊ": "ㄷ",
        "ㅋ": "ㄱ",
        "ㅌ": "ㄷ",
        "ㅍ": "ㅂ",
        "ㅎ": "",
    },
    # Article 23 : consonnes fortes
    forte={"ㄱ": "ㄲ", "ㄷ": "ㄸ", "ㅂ": "ㅃ", "ㅅ": "ㅆ", "ㅈ": "ㅉ"},
    # Article 17 : palatalisation
    # "ㅀ디" n’existe pas
    palatale={"ㄷㅇ": "ㅈ", "ㅌㅇ": "ㅊ", "ㄾㅇ": "ㄹㅊ", "ㄷㅎ": "ㅊ"},
    # ㅈ, ㅉ et ㅊ sont déjà palatales
    non_palatale={"ㅑ": "ㅏ", "ㅒ": "ㅐ", "ㅕ": "ㅓ", "ㅖ": "ㅔ", "ㅛ": "ㅗ", "ㅠ": "ㅜ"},
    # Prononciations modernes sans géminée
    sans_geminee={"ㄱㄲ": "ㄲ", "ㄷㄸ": "ㄸ", "ㄷㅉ": "ㅉ", "ㄷㅆ": "ㅆ", "ㅂㅃ": "ㅃ"},
    # Phonèmes d’initiale
    # pour sub (y compris les finales) : ˀ?[hklmnŋpst]ɕ?ʰ?
    phoneme_initiale={
        "ㄱ": "k",
        "ㄲ": "ˀk",
        "ㄴ": "n",
        "ㄷ": "t",
        "ㄸ": "ˀt",
        "ㄹ": "l",
        "ㅁ": "m",
        "ㅂ": "p",
        "ㅃ": "ˀp",
        "ㅅ": "s",
        "ㅆ": "ˀs",
        "ㅇ": "",
        "ㅈ": "tɕ",
        "ㅉ": "ˀtɕ",
        "ㅊ": "tɕʰ",
        "ㅋ": "kʰ",
        "ㅌ": "tʰ",
        "ㅍ": "pʰ",
        "ㅎ": "h",
    },
    # Phonèmes de voyelle
    # pour sub : [aeɛijouʌwɯ]+
    phoneme_voyelle={
        "ㅏ": "a",
        "ㅐ": "ɛ",
        "ㅑ": "ja",
        "ㅒ": "jɛ",
        "ㅓ": "ʌ",
        "ㅔ": "e",
        "ㅕ": "jʌ",
        "ㅖ": "je",
        "ㅗ": "o",
        "ㅘ": "wa",
        "ㅙ": "wɛ",
        "ㅚ": "we",
        "ㅛ": "jo",
        "ㅜ": "u",
        "ㅝ": "wʌ",
        "ㅞ": "we",
        "ㅟ": "wi",
        "ㅠ": "ju",
        "ㅡ": "ɯ",
        "ㅢ": "ɯj",
        "ㅣ": "i",
    },
    # Phonèmes de finale
    phoneme_finale={
        "": "",
        "ㄱ": "k",
        "ㄲ": "k",
        "ㄳ": "k",
        "ㄴ": "n",
        "ㄵ": "n",
        "ㄶ": "n",
        "ㄷ": "t",
        "ㄹ": "l",
        "ㄺ": "k",
        "ㄻ": "m",
        "ㄼ": "l",
        "ㄽ": "l",
        "ㄾ": "l",
        "ㄿ": "p",
        "ㅀ": "l",
        "ㅁ": "m",
        "ㅂ": "p",
        "ㅄ": "p",
        "ㅅ": "t",
        "ㅆ": "t",
        "ㅇ": "ŋ",
        "ㅈ": "t",
        "ㅊ": "t",
        "ㅋ": "k",
        "ㅌ": "t",
        "ㅍ": "p",
        "ㅎ": "",
    },
    # Consonnes sonores
    sonorisation={"k": "ɡ", "t": "d", "p": "b", "tɕ": "dʑ", "h": "ɦ"},
    # Translittérations
    translit={
        "ㄱ": "g",
        "ㄲ": "kk",
        "ㄳ": "gs",
        "ㄴ": "n",
        "ㄵ": "nj",
        "ㄶ": "nh",
        "ㄷ": "d",
        "ㄸ": "tt",
        "ㄹ": "l",
        "ㄺ": "lg",
        "ㄻ": "lm",
        "ㄼ": "lb",
        "ㄽ": "ls",
        "ㄾ": "lt",
        "ㄿ": "lp",
        "ㅀ": "lh",
        "ㅁ": "m",
        "ㅂ": "b",
        "ㅃ": "pp",
        "ㅄ": "bs",
        "ㅅ": "s",
        "ㅆ": "ss",
        "ㅇ": "ng",
        "ㅈ": "j",
        "ㅉ": "jj",
        "ㅊ": "ch",
        "ㅋ": "k",
        "ㅌ": "t",
        "ㅍ": "p",
        "ㅎ": "h",
        "ㅏ": "a",
        "ㅐ": "ae",
        "ㅑ": "ya",
        "ㅒ": "yae",
        "ㅓ": "eo",
        "ㅔ": "e",
        "ㅕ": "yeo",
        "ㅖ": "ye",
        "ㅗ": "o",
        "ㅘ": "wa",
        "ㅙ": "wae",
        "ㅚ": "oe",
        "ㅛ": "yo",
        "ㅜ": "u",
        "ㅝ": "wo",
        "ㅞ": "we",
        "ㅟ": "wi",
        "ㅠ": "yu",
        "ㅡ": "eu",
        "ㅢ": "ui",
        "ㅣ": "i",
    },
    # Romanisations de finale sourde
    roman_finale={"g": "k", "d": "t", "b": "p"},
    # Voyelles yin-yang pour les formes en -아/어
    yinyang={
        "ㅏ": "ㅏ",
        "ㅐ": "ㅓ",
        "ㅑ": "ㅏ",
        "ㅒ": "ㅓ",
        "ㅓ": "ㅓ",
        "ㅔ": "ㅓ",
        "ㅕ": "ㅓ",
        "ㅖ": "ㅓ",
        "ㅗ": "ㅏ",
        "ㅘ": "ㅏ",
        "ㅙ": "ㅓ",
        "ㅚ": "ㅓ",
        "ㅛ": "ㅏ",
        "ㅜ": "ㅓ",
        "ㅝ": "ㅓ",
        "ㅞ": "ㅓ",
        "ㅟ": "ㅓ",
        "ㅠ": "ㅓ",
        "ㅡ": "ㅓ",
        "ㅢ": "ㅓ",
        "ㅣ": "ㅓ",
        "": "ㅓ",
    },
    # Voyelles pour les formes en -아/어
    diphtongue_verbale={"ㅗ": "ㅘ", "ㅜ": "ㅝ", "ㅐ": "ㅐ", "ㅔ": "ㅔ", "ㅚ": "ㅙ", "ㅣ": "ㅕ"},
)

# Indices des jamos d’initiale
hangeul.indice_initiale = {v: i for i, v in enumerate(hangeul.initiale)}

# Indices des jamos de voyelle
hangeul.indice_voyelle = {v: i for i, v in enumerate(hangeul.voyelle)}

# Indices des jamos de finale
hangeul.indice_finale = {v: i for i, v in enumerate(hangeul.finale)}

# Article 23 : consonnes fortes
plosive = {"ㄱ", "ㄲ", "ㅋ", "ㄳ", "ㄺ", "ㄷ", "ㅅ", "ㅆ", "ㅈ", "ㅊ", "ㅌ", "ㅂ", "ㅍ", "ㄿ", "ㅄ"}
for finale in plosive:
    for douce, forte in hangeul.forte.items():
        index = f"{finale}{douce}"
        if index not in hangeul.frontiere:
            hangeul.frontiere[index] = f"{hangeul.neutralisation[finale]}'{douce}"


# Le reste du code a été retranscrit depuis:
# https://fr.wiktionary.org/wiki/Module:ko-hangeul (2019-04-29T12:09:31)


def jamos(match: Match[str], floor: Callable[[float], int] = math.floor) -> str:
    """Fonction internelle pour décomposer un hangeul en jamos."""
    char = match.group(1)
    code = ord(char)
    return str(
        hangeul.initiale[floor((code - 0xAC00) / (21 * 28))]
        + hangeul.voyelle[floor((code - 0xAC00) / 28) % 21]
        + hangeul.finale[(code - 0xAC00) % 28]
    )


def decompos(text: str) -> str:
    """Cette fonction décompose des hangeuls en jamos.
    La barre oblique supprime un rieul précédent s’il y en a.
    """
    text = sub(r"([가-힣])", jamos, text)
    text = sub(r"ㄹ?/", "", text)
    text = sub(r"[ㄱ-ㅎ]+([ㄱ-ㅎ][ㄱ-ㅎ])", r"\1", text)  # au plus deux consonnes
    text = sub(r"[ㄱ-ㅎ]+([ㄱ-ㅎ])$", r"\1", text)  # au plus une seule consonne à la fin
    return text


def hangeul_sans_finale(match: Match[str]) -> str:
    """Fonction internelle."""
    initiale, voyelle = match.groups()
    return chr(
        (hangeul.indice_initiale[initiale] - 1) * 21 * 28
        + (hangeul.indice_voyelle[voyelle] - 1) * 28
        + 0xAC00
    )


def hangeul_avec_finale(match: Match[str]) -> str:
    """Fonction internelle."""
    caractere, finale = match.groups()
    return chr(ord(caractere) + hangeul.indice_finale[finale] - 1)


def compos(text: str, conserver: bool) -> str:
    """Cette fonction supprime tous les clés de prononciation ("'", "-", "." et "s")
    et elle compose des hangeuls.
    """
    if not conserver:
        # conserver seulement les hangeuls, les jamos et les espaces
        text = sub(r"[^가-힣ㄱ-ㅣ ]", "", text)

    text = sub(r"([ㄱ-ㅎ])([ㅏ-ㅣ])", hangeul_sans_finale, text)
    text = sub(r"([가-히])([ㄱ-ㅎ])", hangeul_avec_finale, text)
    return text


def consonne_forte(match: Match[str]) -> str:
    """Fonction internelle des consonnes fortes."""
    jamo = match.group(1)
    return str(hangeul.forte.get(jamo, jamo))


def palatale(match: Match[str]) -> str:
    frontiere, voyelle = match.groups()
    return str(hangeul.palatale.get(frontiere, frontiere)) + voyelle


def non_palatale(match: Match[str]) -> str:
    consonne, voyelle = match.groups()
    return f"{consonne}{hangeul.non_palatale.get(voyelle, voyelle)}"


def neutralisation(match: Match[str]) -> str:
    """Fonction internelle de la neutralisation des finales."""
    jamo = match.group(1)
    return str(hangeul.neutralisation.get(jamo, jamo))


def pron_frontiere(match: Match[str]) -> str:
    """Fonction internelle pour la prononciation."""
    finale, initiale, voyelle = match.groups()
    res = hangeul.frontiere.get(
        f"{finale}{initiale}", hangeul.neutralisation[finale] + initiale
    )
    return f"{res}{voyelle}"


def modif_jamo(text: str, pron: bool, changer_oe: bool) -> str:
    """Cette fonction modifie des hangeuls selon les règles du Standard
    et les clés de prononciation ("'", "-", "." et "s").
    """
    text = decompos(text)

    # apostrophes (Articles 26-29)
    if pron:  # pour la prononciation
        text = sub(r"'ㅇ", "ㄴ", text)  # Article 29
        text = sub(r"'([ㄱㄷㅂㅅㅈ])", consonne_forte, text)  # Articles 26, 27 et 28
    else:  # pour la romanisation
        text = sub(r"([^ ])'ㅇ", r"\1ㄴ", text)  # Article 29

    text = sub(r"'", "", text)

    # s (Article 16)
    text = sub(r"([ㄱ-ㅎ])s", "ㅅ", text)

    # changements phonologiques qu’il faut traiter avant la supression des traits d’union
    # Article 17
    text = sub(r"([ㄷㅌㄾ][ㅇㅎ])([ㅣㅕ])", palatale, text)
    if pron:
        # Article 4
        if changer_oe:
            text = sub(r"ㅚ", "ㅞ", text)

        # Article 5
        text = sub(r"([ㄱㄹㅁㅎㅍ])ㅖ", r"\1ㅔ", text)  # ㅖ est prononcé ㅔ dans 계, 례, 몌, 혜 et 폐
        text = sub(r"([ㄱ-ㅆㅈ-ㅎ])ㅢ", r"\1ㅣ", text)  # ㅢ est prononcé ㅣ après une consonne
        text = sub(
            r"([ㄱ-ㅣ]ㅇ)ㅢ", r"\1ㅣ", text
        )  # ㅢ est prononcé ㅣ au milieu du mot ; -의 sera conservé

    # traits d’union et espaces (Articles 20 et 15)
    text = sub(r"[ㄴㄵㄶ]-ㄹ", "ㄴㄴ", text)  # Article 20
    if pron:  # pour la prononciation
        text = sub(r"[ㄴㄵㄶ] ㄹ", "ㄴㄴ", text)  # Article 20
    else:  # pour la romanisation
        text = sub(r"([ㄱ-ㅎ])-ㅎ", r"\1#ㅎ", text)  # pour éviter la suppression
        text = sub(r"([ㄱ-ㅣ]) ", r"\1- ", text)  # pour éviter la suppression

    text = sub(r"([ㄱ-ㅣ])[\- ]", neutralisation, text)  # Article 15

    # fin du mot
    text = sub(r"([ㄱ-ㅎ])$", neutralisation, text)  # Articles 9, 10 et 11

    # frontières
    text = sub(r"([ㄱ-ㅎ]?)([ㄱ-ㅎ])([ㅏ-ㅣ])", pron_frontiere, text)
    if pron:  # pour la prononciation
        text = sub(r"'([ㄱㄷㅂㅅㅈ])", consonne_forte, text)
        # Article 5
        # # ㅈ, ㅉ et ㅊ sont déjà palatales
        text = sub(r"([ㅈㅉㅊ])([ㅑㅕㅖㅛㅠ])", non_palatale, text)
    else:  # pour la romanisation
        text = sub(r"['\-\.]", "", text)  # consonnes fortes pas romanisées

    return text


def sans_geminee(match: Match[str]) -> str:
    frontiere = match.group(1)
    return str(hangeul.sans_geminee.get(frontiere, frontiere))


def phoneme_initiale(match: Match[str]) -> str:
    initiale, voyelle = match.groups()
    return f".{hangeul.phoneme_initiale[initiale]}{hangeul.phoneme_voyelle[voyelle]}"


def phoneme_finale(match: Match[str]) -> str:
    finale = match.group(1)
    return str(hangeul.phoneme_finale[finale])


def sonorisation(match: Match[str]) -> str:
    consonne, voyelle = match.groups()
    return f".{hangeul.sonorisation[consonne]}{voyelle}"


def phoneme(text: str, son: bool, sonore: bool) -> str:
    """Cette fonction change des hangeuls en phonèmes"""
    text = modif_jamo(text, True, False)

    # prononciations modernes sans géminée
    text = sub(r"([ㄱㄷㅂ][ㄲㄸㅆㅉㅃ])", sans_geminee, text)
    # phonèmes d’une initiale et d’une voyelle
    text = sub(r"ㅅㅞ", "sjwe", text)  # prononciation populaire de 쉐
    text = sub(r"([ㄱ-ㅎ])([ㅏ-ㅣ])", phoneme_initiale, text)
    # phonème d’une finale
    text = sub(r"([ㄱ-ㅎ])", phoneme_finale, text)
    # Article 12-4 : ㄹㅎ, ㄴㅎ, ㅁㅎ et ㅇㅎ
    # Article 13 : ㅇㅇ
    text = sub(r"([lnmŋ])\.(h?[aeɛijouʌwɯ])", r".\1\2", text)

    # réalisation des phonèmes
    if son:
        # sonorisation après une voyelle ou une consonne sonore
        if not sonore:
            text = sub(r"^\.", "", text)

        text = sub(r"\.([hkpt]ɕ?)([aeɛijouʌwɯ])", sonorisation, text)
        # implosives
        text = sub(r"([kpt])\.(ˀ?[kpt])", r"\1̚.\2", text)  # pas implosive devant ㅅ
        text = sub(r"([kpt])$", r"\1̚", text)
        # ㄹㄹ
        text = sub(r"l\.l", "ɭ.ɭ", text)
        # ㄹ devant une voyelle
        text = sub(r"l(h?[aeɛijouʌwɯ])", r"ɾ\1", text)
        # ㄹ de finale
        text = sub(r"l", "ɭ", text)
        # Article 12-4 : ㄹㅎ, ㄴㅎ, ㅁㅎ et ㅇㅎ
        text = sub(r"([ɾnmŋ])h", r"\1ʱ", text)
        # distinction perdue entre 에 et 애
        text = sub(r"[eɛ]", "e̞", text)
        # palatalisation de 위
        text = sub(r"wi", "ɥi", text)
        # palatalisation de ㅅ et ㅆ
        text = sub(r"sjw", "ʃw", text)  # prononciation populaire de 쉐
        text = sub(r"sj", "ɕ", text)
        text = sub(r"si", "ɕi", text)
        text = sub(r"sɥi", "ʃɥi", text)
        # palatalisation de ㅎ
        text = sub(r"hj", "ç", text)
        text = sub(r"h(ɥ?i)", r"ç\1", text)
        # palatalisation de ㅋ, ㅌ, ㅍ
        text = sub(r"([ktp])ʰj", r"\1ç", text)
        text = sub(r"([ktp])ʰ(ɥ?i)", r"\1ç\2", text)
        # /w/ après une consonne
        text = sub(r"([^\.])w", r"\1ʷ", text)
        # le suffixe -요
        text = sub(r"o\.$", "o̞", text)

    # suppression des points au début et à la fin
    text = sub(r"^\.", "", text)
    text = sub(r"\.$", "", text)
    return text


def roman_finale(match: Match[str]) -> str:
    """Fonction internelle pour la romanisation des finales"""
    finale, initiale = match.groups()
    return f"{hangeul.roman_finale.get(finale, finale)}{initiale or ''}"
