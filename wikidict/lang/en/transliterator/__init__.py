"""
Transliterator used across multiple templates.
"""

from .ar import transliterate as transliterate_ar
from .fa import transliterate as transliterate_fa

transliterations = {
    "ar": transliterate_ar,
    "fa": transliterate_fa,
}
transliterations["ady"] = transliterations["ar"]
transliterations["av"] = transliterations["ar"]
transliterations["ce"] = transliterations["ar"]
transliterations["inh"] = transliterations["ar"]
transliterations["kbd"] = transliterations["ar"]


def transliterate(locale: str, text: str) -> str:
    """
    Return the transliterated form of *text*.

    >>> transliterate("ar", "عُظْمَى")
    'ʕuẓmā'
    >>> transliterate("fa", "سَرْاَنْجَام")
    'sar-anjām'
    """
    return func(text, locale=locale) if (func := transliterations.get(locale)) else ""
