"""
Python conversion of the ko-hangeul module.
Link:
  - https://fr.wiktionary.org/wiki/Module:ko-hangeul

Current version from 2019-04-29 12:09:31
  - https://fr.wiktionary.org/w/index.php?title=Module:ko-hangeul&oldid=26279590
"""

import re

from .data import hangeul
from .utils import decompos, modif_jamo


def phoneme(text: str, son: bool, sonore: bool) -> str:
    text = modif_jamo(text, True, False)

    sub = re.sub

    # prononciations modernes sans géminée
    text = sub(r"([ㄱㄷㅂ][ㄲㄸㅆㅉㅃ])", lambda match: hangeul.sans_geminee.get(match[1], match[1]), text)

    # phonèmes d’une initiale et d’une voyelle
    text = sub(r"ㅅㅞ", "sjwe", text)  # prononciation populaire de 쉐
    text = sub(
        r"([ㄱ-ㅎ])([ㅏ-ㅣ])",
        lambda match: f".{hangeul.phoneme_initiale[match[1]]}{hangeul.phoneme_voyelle[match[2]]}",
        text,
    )

    # phonème d’une finale
    text = sub(r"([ㄱ-ㅎ])", lambda match: hangeul.phoneme_finale[match[1]], text)

    # Article 12-4 : ㄹㅎ, ㄴㅎ, ㅁㅎ et ㅇㅎ
    # Article 13 : ㅇㅇ
    text = sub(r"([lnmŋ])\.(h?[aeɛijouʌwɯ])", r".\1\2", text)

    # réalisation des phonèmes
    if son:
        # sonorisation après une voyelle ou une consonne sonore
        if not sonore:
            text = sub(r"^\.", "", text)

        text = sub(
            r"\.([hkpt]ɕ?)([aeɛijouʌwɯ])",
            lambda match: f".{hangeul.sonorisation[match[1]]}{match[2]}",
            text,
        )

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
    return sub(r"\.$", "", text)


def translit(text: str) -> str:
    """Translittération (Modèle:ko-translit)."""
    text = decompos(text)
    text = re.sub(r"['\-s]", "", text)
    text = re.sub(r"ㅇ([ㅏ-ㅣ])", "-\1", text)
    text = re.sub(r"^\-", "", text)
    text = re.sub(r" \-", " ", text)
    return re.sub(r"([ㄱ-ㅣ])", lambda match: hangeul.translit[match[1]], text)
