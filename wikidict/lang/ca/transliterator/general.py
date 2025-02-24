"""
Python conversion of the ca-general module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:ca-general

Current version from 2025-01-22 18:04
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:ca-general&oldid=2445064
"""

import re
import sys

LOWER_CHARS = "".join([chr(i) for i in range(sys.maxunicode) if chr(i).islower()])


def sil(word: str) -> str:
    sub = re.sub

    sil = word.lower()

    # Prefixos que trenquen regles
    initial = sil[0]
    if initial == "a":
        sil = sub(r"^anae", "0200", sil)  # an-
        sil = sub(r"^anafro", "020110", sil)
        sil = sub(r"^an[aà]l[fg]", "02021", sil)
        sil = sub(r"^an[aà]r([cq])", "0202\\1", sil)
        sil = sub(r"^ane([npr])", "020\\1", sil)
        sil = sub(r"^an[uú]r", "020r", sil)
        sil = sub(r"^autoi([mn])", "02100\\1", sil)  # auto-
    elif initial == "b":
        sil = sub(r"^bena([a-z]+è)", "1010\\1", sil)
        sil = sub(r"^bena([a-z])", "1020\\1", sil)  # ben-
        sil = sub(r"^bene([ns][a-z])", "1020\\1", sil)
        sil = sub(r"^bisan", "10202", sil)  # bis-
    elif initial == "c":
        sil = sub(r"^coin", "1002", sil)  # co-
    elif initial == "d":
        sil = sub(r"^des([aeoú])", "102\\1", sil)  # des- amb excepcions des+e/i
    elif initial == "e":
        sil = sub(r"^enanti", "010210", sil)  # enantio-
        sil = sub(r"^en[oò]([flt])", "010\\1", sil)  # eno-
        sil = sub(r"^enorm", "01021", sil)
        sil = sub(r"^en[aoò]", "020", sil)  # en-, excepte anteriors
        sil = sub(r"^exa([bclnrs])", "020\\1", sil)  # ex-
        sil = sub(r"^exo([rs][^cdrpqt])", "020\\1", sil)
    elif initial == "h":
        sil = sub(r"^hiper[ae]", "101020", sil)  # hiper-
    elif initial == "i":
        sil = sub(r"^inaug", "01021", sil)
        sil = sub(r"^ini([^gmn])", "010\\1", sil)
        sil = sub(r"^inocul", "01010l", sil)
        sil = sub(r"^in[uú]([^rst])", "010\\1", sil)
        sil = sub(r"^in[aeèioòuú]", "020", sil)  # in-, excepte anteriors
        sil = sub(r"^infra[iu]", "021100", sil)  # infra-
        sil = sub(r"^inter[ao]([^p])", "021020\\1", sil)  # inter
        sil = sub(r"^interest", "02102021", sil)
        sil = sub(r"^intra[iu]", "021100", sil)  # intra-
    elif initial == "m":
        sil = sub(r"^m[ai]cro[iu]", "101100", sil)  # macro-, micro-
    elif initial == "n":
        sil = sub(r"^nosal", "10202", sil)
    elif initial == "p":
        sil = sub(r"^peral", "10202", sil)  # per-
    elif initial == "r":
        sil = sub(r"^rein[ae]", "10210", sil)
        sil = sub(r"^rei([^aegx])([^$])", "100\\1\\2", sil)  # re-
        sil = sub(r"^reun", "1001", sil)
    elif initial == "s":
        sil = sub(r"^sots[ai]", "10220", sil)  # sots-
        sil = sub(r"^sub([aàír])", "102\\1", sil)  # sub-
        sil = sub(r"^sub[eè]([^r])", "1020\\1", sil)
    elif initial == "t":
        sil = sub(r"^trans[aou]", "110220", sil)  # trans-

    # Diftongs creixents
    sil = sub(r"[qg][uü][aàeèéiíïoòóuúü]", "110", sil)
    sil = sub(r"[aàeèéiíïoòóuúü][iu][aàeèéiíïoòóuúü]", "010", sil)
    sil = sub(r"^i[oò]ni(.)", "0010\\1", sil)  # excepció pels derivant de ió
    sil = sub(r"^(h?)[iu][aàeèéioòóu]", "\\110", sil)

    # Sufixos i desinències amb estalvi de dièresi
    sil = sub(r"[aeou]ir$", "002", sil)  # infinitius -ir
    sil = sub(r"[aeou]int$", "0022", sil)  # gerundis
    sil = sub(r"[aeou]ir[éà]$", "0010", sil)  # futur
    sil = sub(r"[aeou]iràs$", "00102", sil)  # futur
    sil = sub(r"[aeou]ire[mu]$", "00102", sil)  # futur
    sil = sub(r"[aeou]iran$", "00102", sil)  # futur
    sil = sub(r"[aeou]iria$", "00100", sil)  # condicional
    sil = sub(r"[aeou]irie[sn]$", "001002", sil)  # condicional
    sil = sub(r"[0iu]um(s?)$", "002\\1", sil)  # llatinismes
    sil = sub(r"[0aeiou]isme(s?)$", "00210\\1", sil)  # -isme
    sil = sub(r"[0aeiou]ist([ae]s?)$", "0021\\1", sil)  # -ista

    # Diftongs decreixents
    sil = sub(r"[0aàeèéioòóu][u]", "02", sil)  # inclou triftongs: creixent 10 + decreixent 2
    sil = sub(r"[0aàeèéoòóuúü][i]", "02", sil)
    sil = sub(r"ii$", "02", sil)  # només final de mot, no amb prefix

    # Nuclis vocàlics
    sil = sub(r"[aàeèéiíïoòóuúü]", "0", sil)

    # Codes finals
    sil = sub(rf"{LOWER_CHARS}$", "2", sil)
    sil = sub(rf"{LOWER_CHARS}2$", "22", sil)
    sil = sub(rf"{LOWER_CHARS}22$", "222", sil)

    # Obertures
    sil = sub(rf"^{LOWER_CHARS}", "1", sil)
    sil = sub(rf"^1{LOWER_CHARS}", "11", sil)
    sil = sub(rf"^11{LOWER_CHARS}", "111", sil)
    sil = sub(r"ll0", "110", sil)
    sil = sub(r"ny0", "110", sil)
    sil = sub(r"kh0", "110", sil)
    sil = sub(r"[ptcfbdg]r", "11", sil)
    sil = sub(r"[pcfbg]l", "11", sil)
    sil = sub(rf"{LOWER_CHARS}0", "10", sil)
    sil = sub(r"[çñ]0", "10", sil)  # \l (all ASCII lowercase letters) no inclou ç, ñ

    # Codes interiors
    sil = sub(rf"[ps]{LOWER_CHARS}1", "21", sil)
    sil = sub(rf"{LOWER_CHARS}([12])", "2\\1", sil)

    # Separació de síl·labes
    anterior, actual = "", ""
    mot_sep: list[str] = []
    for i in range(len(word)):
        actual = sil[i]
        if (actual == "0" or actual == "1") and (anterior == "0" or anterior == "2"):
            mot_sep.append("·")
        if actual == "-":
            mot_sep.append("·")
        else:
            mot_sep.append(word[i])
        anterior = actual

    return "".join(mot_sep)
