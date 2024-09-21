# From https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:ca-general&oldid=2255269 24/02/2024

import re


def cal_apostrofar(text: str) -> bool:
    apostrophize = {
        "hakk": False,
        "haus": False,
        "hawa": False,  # h consonant (hakka, haussa, hawaià)
        "hia": False,
        "hie": False,
        "hio": False,
        "hui": False,  # vocal consonant
        "uig": True,
        "uix": True,  # excepció per u vocal
        "ha": True,
        "he": True,
        "hi": True,
        "hí": True,
        "ho": True,
        "hu": True,
        "hy": True,  # excepte anteriors
        "ia": False,
        "ià": False,
        "ie": False,
        "io": False,
        "iu": False,  # i consonant
        "ua": False,
        "ue": False,
        "ui": False,
        "uí": False,
        "uï": False,
        "uo": False,  # u consonant
        "ya": False,
        "ye": False,
        "yi": False,
        "yo": False,
        "yu": False,  # y consonant
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
        "ü": True,  # excepte anteriors
    }
    for i in range(4, 0, -1):
        apostrophized = apostrophize.get(text[:i])
        if apostrophized is not None:
            return True
    return False


def sil(mot: str) -> str:
    if mot == "" or mot is None:
        mot = "Example"  # Example string as fallback
    sil = mot.lower()

    # Prefixes that break rules
    initial = sil[0]
    if initial == "a":
        sil = re.sub("^anae", "0200", sil)  # an-
        sil = re.sub("^anafro", "020110", sil)
        sil = re.sub("^an[aà]l[fg]", "02021", sil)
        sil = re.sub("^an[aà]r([cq])", r"0202\1", sil)
        sil = re.sub("^anè", "020", sil)
        sil = re.sub("^ane([nprs])", r"020\1", sil)
        sil = re.sub("^an[uú]r", "020r", sil)
        sil = re.sub("^autoi([mn])", r"02100\1", sil)  # auto-
    elif initial == "b":
        sil = re.sub("^bena([aàeèéií])", r"1010\1", sil)
        sil = re.sub("^bena([a-z])", r"1020\1", sil)  # ben-
        sil = re.sub("^bene([ns][a-z])", r"1020\1", sil)
        sil = re.sub("^bes[aà]v", "10201", sil)  # bes-
        sil = re.sub("^beson", "10202", sil)
        sil = re.sub("^bisan", "10202", sil)  # bis-
    elif initial == "c":
        sil = re.sub("^coin", "1002", sil)  # co-
        sil = re.sub("^con[ou][nr]", "10202", sil)  # con-
        sil = re.sub("^contrai", "1021100", sil)  # contra-
    elif initial == "d":
        sil = re.sub("^des([aeiouú])", "102\\1", sil)  # des- with pending exceptions
    elif initial == "e":
        sil = re.sub("^enanti", "010210", sil)  # enantio-
        sil = re.sub("^en[oò]([flt])", "010\\1", sil)  # eno-
        sil = re.sub("^enorm", "01021", sil)
        sil = re.sub("^en[aoò]", "020", sil)  # en-, except previous
        sil = re.sub("^exa([bclnrs])", "020\\1", sil)  # ex-
        sil = re.sub("^exo([rs][^cdrpqt])", "020\\1", sil)
    elif initial == "h":
        sil = re.sub("^hiper[ae]", "101020", sil)  # hiper-
    elif initial == "i":
        sil = re.sub("^inani[ct]", "010101", sil)
        sil = re.sub("^inefa", "01010", sil)
        sil = re.sub("^in[eè]p", "0102", sil)
        sil = re.sub("^in[eè]r([^ru])", "0102\\1", sil)
        sil = re.sub("^ino[cs][ei]", "01010", sil)
        sil = re.sub("^in[aeèoò]", "020", sil)  # in-, except previous
        sil = re.sub("^ini([gmn])", "020\\1", sil)
        sil = re.sub("^in[uú]([rst])", "020\\1", sil)
        sil = re.sub("^infra[iu]", "021100", sil)  # infra-
        sil = re.sub("^inter[ao]([^p])", "021020\\1", sil)  # inter
        sil = re.sub("^interest", "02102021", sil)
        sil = re.sub("^intra[iu]", "021100", sil)  # intra-
    elif initial == "m":
        sil = re.sub("^m[ai]cro[iu]", "101100", sil)  # macro-, micro-
    elif initial == "n":
        sil = re.sub("^nosal", "10202", sil)
    elif initial == "p":
        sil = re.sub("^pana([frt][rate][^a])", "1020\\1", sil)  # pan-
        sil = re.sub("^panamer", "1020101", sil)
        sil = re.sub("^panisl", "102021", sil)
        sil = re.sub("^panòpt", "102021", sil)
        sil = re.sub("^posta[bcl]([^$])", "102202\\1", sil)  # post-
        sil = re.sub("^postes([^$])", "102202\\1", sil)
        sil = re.sub("^post[io][mp]", "102202", sil)
        sil = re.sub("^post[^aàeèéioòóu]", "10221", sil)
        sil = re.sub("^pr[eo]i([^x])", "1100\\1", sil)  # pre-, pro-
    elif initial == "r":
        sil = re.sub("^rein[ae]", "10210", sil)
        sil = re.sub("^rei([^aegx])", "100\\1", sil)  # re-
        sil = re.sub("^reun", "1001", sil)
    elif initial == "s":
        sil = re.sub("^sots[ai]", "10220", sil)  # sots-
        sil = re.sub("^sub([aàíour])", "102\\1", sil)  # sub-
        sil = re.sub("^sub[eè]([^r])", "1020\\1", sil)
        sil = re.sub("^subl[iu][nt]", "102101", sil)
    elif initial == "t":
        sil = re.sub("^trans[aeou]", "110220", sil)  # trans-
    elif initial == "u":
        sil = re.sub("^ultra[iu]", "021100", sil)  # ultra-
    elif initial == "v":
        sil = re.sub("^vosal", "10202", sil)

    # Diphthongs with rising movement
    sil = re.sub("[qg][uü][aàeèéiíïoòóuúü]", "110", sil)
    sil = re.sub("[aàeèéiíïoòóuúü][iu][aàeèéiíïoòóuúü]", "010", sil)
    sil = re.sub("^i[oò]ni(.)", r"0010\1", sil)  # Exception for derivatives of ió
    sil = re.sub(r"^(h?)[iu][aàeèéioòóu]", r"\1110", sil)

    # Suffixes and endings with diaeresis savings
    sil = re.sub("[aeou]ir$", "002", sil)  # -ir infinitives
    sil = re.sub("[aeou]int$", "0022", sil)  # gerunds
    sil = re.sub("[aeou]ir[éà]$", "0010", sil)  # future
    sil = re.sub("[aeou]iràs$", "00102", sil)  # future
    sil = re.sub("[aeou]ire[mu]$", "00102", sil)  # future
    sil = re.sub("[aeou]iran$", "00102", sil)  # future
    sil = re.sub("[aeou]iria$", "00100", sil)  # condicional
    sil = re.sub("[aeou]irie[sn]$", "001002", sil)  # condicional
    sil = re.sub("[0iu]um(s?)$", "002\\1", sil)  # llatinismes
    sil = re.sub("[0aeiou]isme(s?)$", "00210\\1", sil)  # -isme
    sil = re.sub("[0aeiou]ist([ae]s?)$", "0021\\1", sil)  # -ista

    # Diphthongs with decreasing movement
    sil = re.sub("[0aàeèéioòóuúü][u]", "02", sil)
    sil = re.sub("[0aàeèéoòóuúü][i]", "02", sil)
    sil = re.sub("ii$", "02", sil)  # Only at the end of a word, not with a prefix

    # Vowel nuclei
    sil = re.sub("[aàeèéiíïoòóuúü]", "0", sil)

    # Final codes
    sil = re.sub(r"[a-z]$", "2", sil)
    sil = re.sub(r"[a-z]2$", "22", sil)
    sil = re.sub(r"[a-z]22$", "222", sil)

    # Opening movements
    sil = re.sub(r"^[a-z]", "1", sil)
    sil = re.sub(r"^1[a-z]", "11", sil)
    sil = re.sub(r"^11[a-z]", "111", sil)
    sil = re.sub("ll0", "110", sil)
    sil = re.sub("ny0", "110", sil)
    sil = re.sub("kh0", "110", sil)
    sil = re.sub("[ptcfbdg]r", "11", sil)
    sil = re.sub("[pcfbg]l", "11", sil)
    sil = re.sub(r"[a-z]0", "10", sil)
    sil = re.sub("[çñ]0", "10", sil)  # [a-z] does not include ç, ñ

    # Inner codes
    sil = re.sub(r"[ps][a-z1]", "21", sil)
    sil = re.sub(r"[a-z]([12])", r"2\1", sil)

    # Separation of syllables
    anterior, actual = "", ""
    mot_sep = []
    for i in range(len(mot)):
        actual = sil[i]
        if (actual in ["0", "1"]) and (anterior in ["0", "2"]):
            mot_sep.append("·")
        if actual == "-":
            mot_sep.append("·")
        else:
            mot_sep.append(mot[i])
        anterior = actual
    return "".join(mot_sep)
