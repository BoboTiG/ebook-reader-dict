"""
Transliterator used across multiple templates.

Link:
  - https://sv.wiktionary.org/wiki/Modul:translit

Current version from 2024-09-26 21:31
  - https://sv.wiktionary.org/w/index.php?title=Modul:translit&oldid=4064405
"""

from .be import transliterate as transliterate_be
from .bg import transliterate as transliterate_bg
from .got import transliterate as transliterate_got
from .grc import transliterate as transliterate_grc
from .ru import transliterate as transliterate_ru
from .uk import transliterate as transliterate_uk

transliterations = {
    # "ar": transliterate_ar,
    "be": transliterate_be,
    "bg": transliterate_bg,
    "got": transliterate_got,
    "grc": transliterate_grc,
    "ru": transliterate_ru,
    "uk": transliterate_uk,
}


def transliterate(locale: str, text: str) -> str:
    """
    Return the transliterated form of *text*.

        >>> transliterate("ar", "")
        ''
        >>> transliterate("be", "арты́кул")
        'artýkul'
        >>> transliterate("bg", "Жуковский")
        'Zjukovskij'
        >>> transliterate("got", "𐌰𐍄𐍄𐌰 𐌿𐌽𐍃𐌰𐍂, 𐌸𐌿 𐌹𐌽 𐌷𐌹𐌼𐌹𐌽𐌰𐌼,")
        'atta unsar, þu in himinam,'
        >>> transliterate("grc", "Ὦ φῶς, τελευταῖόν σε προσϐλέψαιμι νῦν,")
        'Ō fōs, teleutaión se prosblépsaimi nyn,'
        >>> transliterate("ru", "Анна")
        'Anna'
        >>> transliterate("uk", "Ґалаґан")
        'Galagan'
    """
    return func(text) if (func := transliterations.get(locale)) else ""
