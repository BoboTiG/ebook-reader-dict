"""
Transliterator used across multiple templates.
"""

from .fa import transliterate as transliterate_fa

transliterations = {
    "fa": transliterate_fa,
}


def transliterate(locale: str, text: str) -> str:
    """
    Return the transliterated form of *text*.

    >>> transliterate("fa", "سَرْاَنْجَام")
    'sar-anjām'
    """
    return func(text, locale=locale) if (func := transliterations.get(locale)) else ""
