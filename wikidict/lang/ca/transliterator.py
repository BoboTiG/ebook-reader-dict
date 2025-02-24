"""
Transliterator used across multiple templates.
"""

from .be_trans import transliterate as transliterate_be
from .ber_trans import transliterate as transliterate_ber
from .el_trans import transliterate as transliterate_el
from .grc_trans import transliterate as transliterate_grc
from .ky_trans import transliterate as transliterate_ky
from .ru_trans import transliterate as transliterate_ru
from .zh_trans import transliterate as transliterate_zh

transliterations = {
    "be": transliterate_be,
    "ber": transliterate_ber,
    "el": transliterate_el,
    "grc": transliterate_grc,
    "ky": transliterate_ky,
    "ru": transliterate_ru,
    "zh": transliterate_zh,
}
transliterations["taq"] = transliterations["ber"]
transliterations["thv"] = transliterations["ber"]
transliterations["thz"] = transliterations["ber"]
transliterations["tmh"] = transliterations["ber"]
transliterations["ttq"] = transliterations["ber"]
transliterations["zgh"] = transliterations["ber"]


def transliterate(locale: str, text: str) -> str:
    """
    Return the transliterated form of *text*.

        >>> transliterate("be", "Белару́сь")
        'Belarús'
        >>> transliterate("ber", "ⴰⴷⵔⴰⵔ")
        'adrar'
        >>> transliterate("el", "Υ")
        'I'
        >>> transliterate("grc", "λόγος")
        'lógos'
        >>> transliterate("ky", "кырк")
        'kurk'
        >>> transliterate("ru", "абха́з")
        'abkhaz'
        >>> transliterate("zh", "汉字")
        'hànzì'
    """
    return func(text, locale=locale) if (func := transliterations.get(locale)) else ""
