"""
Python conversion of the ca-general module.
Link:
  - https://ca.wiktionary.org/wiki/M%C3%B2dul:ca-general

Current version from 2025-01-22 18:04
  - https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:ca-general&oldid=2445064
"""

import re
import sys

# Lua `%l` regex match pattern equivalent.
# Source: https://stackoverflow.com/a/68432752/1117028
LOWER_CHARS = "".join([char for i in range(sys.maxunicode) if (char := chr(i)).islower()])


def cal_apostrofar(text: str) -> bool:
    """
    >>> cal_apostrofar("islandès")
    True
    >>> cal_apostrofar("llatí")
    False
    """
    apostrophize = {
        "hakk": False,
        "haus": False,
        "hawa": False,
        "hia": False,
        "hie": False,
        "hio": False,
        "hui": False,
        "uig": True,
        "uix": True,
        "ha": True,
        "he": True,
        "hi": True,
        "hí": True,
        "ho": True,
        "hu": True,
        "hy": True,
        "ia": False,
        "ià": False,
        "ie": False,
        "io": False,
        "iu": False,
        "ua": False,
        "ue": False,
        "ui": False,
        "uí": False,
        "uï": False,
        "uo": False,
        "ya": False,
        "ye": False,
        "yi": False,
        "yo": False,
        "yu": False,
        "a": True,
        "à": True,
        "e": True,
        "è": True,
        "é": True,
        "i": True,
        "í": True,
        "ï": True,
        "y": True,
        "o": True,
        "ò": True,
        "ó": True,
        "u": True,
        "ú": True,
        "ü": True,
    }
    return any(text[:i] in apostrophize for i in range(4, 0, -1))


def sil(mot: str) -> str:
    sub = re.sub

    _sil = mot.lower()

    # Prefixes that break rules
    match _sil[0]:
        case "a":
            _sil = sub(r"^anae", "0200", _sil)
            _sil = sub(r"^anafro", "020110", _sil)
            _sil = sub(r"^an[aà]l[fg]", "02021", _sil)
            _sil = sub(r"^an[aà]r([cq])", r"0202\1", _sil)
            _sil = sub(r"^ane([npr])", r"020\1", _sil)
            _sil = sub(r"^an[uú]r", "020r", _sil)
            _sil = sub(r"^autoi([mn])", r"02100\1", _sil)
        case "b":
            _sil = sub(rf"^bena([{LOWER_CHARS}]+è)", r"1010\1", _sil)
            _sil = sub(rf"^bena([{LOWER_CHARS}])", r"1020\1", _sil)
            _sil = sub(rf"^bene([ns][{LOWER_CHARS}])", r"1020\1", _sil)
            _sil = sub(r"^bisan", "10202", _sil)
        case "c":
            _sil = sub(r"^coin", "1002", _sil)
        case "d":
            _sil = sub(r"^des([aeoú])", r"102\1", _sil)
        case "e":
            _sil = sub(r"^enanti", "010210", _sil)
            _sil = sub(r"^en[oò]([flt])", r"010\1", _sil)
            _sil = sub(r"^enorm", "01021", _sil)
            _sil = sub(r"^en[aoò]", "020", _sil)
            _sil = sub(r"^exa([bclnrs])", r"020\1", _sil)
            _sil = sub(r"^exo([rs][^cdrpqt])", r"020\1", _sil)
        case "h":
            _sil = sub(r"^hiper[ae]", "101020", _sil)
        case "i":
            _sil = sub(r"^inaug", "01021", _sil)
            _sil = sub(r"^ini([^gmn])", r"010\1", _sil)
            _sil = sub(r"^inocul", "01010l", _sil)
            _sil = sub(r"^in[uú]([^rst])", r"010\1", _sil)
            _sil = sub(r"^in[aeèioòuú]", "020", _sil)
            _sil = sub(r"^infra[iu]", "021100", _sil)
            _sil = sub(r"^inter[ao]([^p])", r"021020\1", _sil)
            _sil = sub(r"^interest", "02102021", _sil)
            _sil = sub(r"^intra[iu]", "021100", _sil)
        case "m":
            _sil = sub(r"^m[ai]cro[iu]", "101100", _sil)
        case "n":
            _sil = sub(r"^nosal", "10202", _sil)
        case "p":
            _sil = sub(r"^peral", "10202", _sil)
        case "r":
            _sil = sub(r"^rein[ae]", "10210", _sil)
            _sil = sub(r"^rei([^aegx])([^$])", r"100\1\2", _sil)
            _sil = sub(r"^reun", "1001", _sil)
        case "s":
            _sil = sub(r"^sots[ai]", "10220", _sil)
            _sil = sub(r"^sub([aàír])", r"102\1", _sil)
            _sil = sub(r"^sub[eè]([^r])", r"1020\1", _sil)
        case "t":
            _sil = sub(r"^trans[aou]", "110220", _sil)

    # Diphthongs with rising movement
    _sil = sub(r"[qg][uü][aàeèéiíïoòóuúü]", "110", _sil)
    _sil = sub(r"[aàeèéiíïoòóuúü][iu][aàeèéiíïoòóuúü]", "010", _sil)
    _sil = sub(r"^i[oò]ni(.)", r"0010\1", _sil)
    _sil = sub(r"^(h?)[iu][aàeèéioòóu]", r"\1110", _sil)

    # Suffixes and endings with diaeresis savings
    _sil = sub(r"[aeou]ir$", "002", _sil)
    _sil = sub(r"[aeou]int$", "0022", _sil)
    _sil = sub(r"[aeou]ir[éà]$", "0010", _sil)
    _sil = sub(r"[aeou]iràs$", "00102", _sil)
    _sil = sub(r"[aeou]ire[mu]$", "00102", _sil)
    _sil = sub(r"[aeou]iran$", "00102", _sil)
    _sil = sub(r"[aeou]iria$", "00100", _sil)
    _sil = sub(r"[aeou]irie[sn]$", "001002", _sil)
    _sil = sub(r"[0iu]um(s?)$", r"002\1", _sil)
    _sil = sub(r"[0aeiou]isme(s?)$", r"00210\1", _sil)
    _sil = sub(r"[0aeiou]ist([ae]s?)$", r"0021\1", _sil)

    # Diphthongs with decreasing movement
    _sil = sub(r"[0aàeèéioòóu][u]", "02", _sil)
    _sil = sub(r"[0aàeèéoòóuúü][i]", "02", _sil)
    _sil = sub(r"ii$", "02", _sil)

    # Vowel nuclei
    _sil = sub(r"[aàeèéiíïoòóuúü]", "0", _sil)

    # Final codes
    _sil = sub(rf"[{LOWER_CHARS}]$", "2", _sil)
    _sil = sub(rf"[{LOWER_CHARS}]2$", "22", _sil)
    _sil = sub(rf"[{LOWER_CHARS}]22$", "222", _sil)

    # Opening movements
    _sil = sub(rf"^[{LOWER_CHARS}]", "1", _sil)
    _sil = sub(rf"^1[{LOWER_CHARS}]", "11", _sil)
    _sil = sub(rf"^11[{LOWER_CHARS}]", "111", _sil)
    _sil = _sil.replace("ll0", "110").replace("ny0", "110").replace("kh0", "110")
    _sil = sub(r"[ptcfbdg]r", "11", _sil)
    _sil = sub(r"[pcfbg]l", "11", _sil)
    _sil = sub(rf"[{LOWER_CHARS}]0", "10", _sil)

    # Inner codes
    _sil = sub(rf"[ps][{LOWER_CHARS}1]", "21", _sil)
    _sil = sub(rf"[{LOWER_CHARS}]([12])", r"2\1", _sil)

    # Separation of syllables
    anterior = actual = ""
    mot_sep = []
    for i in range(len(mot)):
        actual = _sil[i]
        if actual in {"0", "1"} and anterior in {"0", "2"}:
            mot_sep.append("·")
        if actual == "-":
            mot_sep.append("·")
        else:
            mot_sep.append(mot[i])
        anterior = actual

    return "".join(mot_sep)
