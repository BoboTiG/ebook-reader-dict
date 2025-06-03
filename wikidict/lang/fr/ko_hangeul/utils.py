"""
Python conversion of the ko-hangeul module.
Link:
  - https://fr.wiktionary.org/wiki/Module:ko-hangeul

Current version from 2019-04-29 12:09:31
  - https://fr.wiktionary.org/w/index.php?title=Module:ko-hangeul&oldid=26279590
"""

import math
import re
from collections.abc import Callable

from .data import hangeul


def consonne_forte(match: re.Match[str]) -> str:
    jamo: str = match[1]
    return str(hangeul.forte.get(jamo, jamo))


def decompos(text: str) -> str:
    text = re.sub(r"([가-힣])", jamos, text)
    text = re.sub(r"ㄹ?/", "", text)
    text = re.sub(r"[ㄱ-ㅎ]+([ㄱ-ㅎ][ㄱ-ㅎ])", r"\1", text)  # au plus deux consonnes
    return re.sub(r"[ㄱ-ㅎ]+([ㄱ-ㅎ])$", r"\1", text)  # au plus une seule consonne à la fin


def jamos(match: re.Match[str], *, floor: Callable[[float], int] = math.floor) -> str:
    char = match[1]
    code = ord(char)
    return str(
        hangeul.initiale[floor((code - 0xAC00) / (21 * 28))]
        + hangeul.voyelle[floor((code - 0xAC00) / 28) % 21]
        + hangeul.finale[(code - 0xAC00) % 28]
    )


def modif_jamo(text: str, pron: bool, changer_oe: bool) -> str:
    text = decompos(text)

    # apostrophes (Articles 26-29)
    if pron:  # pour la prononciation
        text = re.sub(r"'ㅇ", "ㄴ", text)  # Article 29
        text = re.sub(r"'([ㄱㄷㅂㅅㅈ])", consonne_forte, text)  # Articles 26, 27 et 28
    else:  # pour la romanisation
        text = re.sub(r"([^ ])'ㅇ", r"\1ㄴ", text)  # Article 29

    text = re.sub(r"'", "", text)
    # s (Article 16)
    text = re.sub(r"([ㄱ-ㅎ])s", "ㅅ", text)

    text = re.sub(r"([ㄷㅌㄾ][ㅇㅎ])([ㅣㅕ])", lambda match: hangeul.palatale.get(match[1], match[1]) + match[2], text)
    if pron:
        # Article 4
        if changer_oe:
            text = re.sub(r"ㅚ", "ㅞ", text)

        # Article 5
        text = re.sub(r"([ㄱㄹㅁㅎㅍ])ㅖ", r"\1ㅔ", text)  # ㅖ est prononcé ㅔ dans 계, 례, 몌, 혜 et 폐
        text = re.sub(r"([ㄱ-ㅆㅈ-ㅎ])ㅢ", r"\1ㅣ", text)  # ㅢ est prononcé ㅣ après une consonne
        text = re.sub(r"([ㄱ-ㅣ]ㅇ)ㅢ", r"\1ㅣ", text)  # ㅢ est prononcé ㅣ au milieu du mot ; -의 sera conservé

    # traits d’union et espaces (Articles 20 et 15)
    text = re.sub(r"[ㄴㄵㄶ]\-ㄹ", "ㄴㄴ", text)  # Article 20
    if pron:  # pour la prononciation
        text = re.sub(r"[ㄴㄵㄶ] ㄹ", "ㄴㄴ", text)  # Article 20
    else:  # pour la romanisation
        text = re.sub(r"([ㄱ-ㅎ])\-ㅎ", r"\1#ㅎ", text)  # pour éviter la suppression
        text = re.sub(r"([ㄱ-ㅣ]) ", r"\1- ", text)  # pour éviter la suppression

    text = re.sub(r"([ㄱ-ㅣ])[\- ]", neutralisation, text)  # Article 15

    # fin du mot
    text = re.sub(r"([ㄱ-ㅎ])$", neutralisation, text)  # Articles 9, 10 et 11
    # frontières
    text = re.sub(r"([ㄱ-ㅎ]?)([ㄱ-ㅎ])([ㅏ-ㅣ])", pron_frontiere, text)
    if pron:  # pour la prononciation
        text = re.sub(r"'([ㄱㄷㅂㅅㅈ])", consonne_forte, text)
        # Article 5
        text = re.sub(
            r"([ㅈㅉㅊ])([ㅑㅕㅖㅛㅠ])",  # ㅈ, ㅉ et ㅊ sont déjà palatales
            lambda match: match[1] + hangeul.non_palatale.get(match[2], match[2]),
            text,
        )
    else:  # pour la romanisation
        text = re.sub(r"['\-\.]", "", text)  # consonnes fortes pas romanisées

    return text


def neutralisation(match: re.Match[str]) -> str:
    jamo: str = match[1]
    return str(hangeul.neutralisation.get(jamo, jamo))


def pron_frontiere(match: re.Match[str]) -> str:
    finale, initiale, voyelle = match.groups()
    res = hangeul.frontiere.get(f"{finale}{initiale}", hangeul.neutralisation[finale] + initiale)
    return f"{res}{voyelle}"
