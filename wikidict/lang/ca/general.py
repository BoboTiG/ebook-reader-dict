# From https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:ca-general&oldid=2255269 24/02/2024


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
