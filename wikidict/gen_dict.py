"""DEBUG: generate the Kobo dictionary for specific words."""
import os
from .get_word import get_word
from .convert import BaseFormat, DictFileFormat, KoboFormat, StarDictFormat
from pathlib import Path
from .stubs import Words


def main(locale: str, words: str, output: str, format: str = "kobo") -> int:
    """Entry point."""

    a_words = words.split(",")
    def_words: Words = {}
    for word in a_words:
        details = get_word(word, locale)
        def_words[word] = details

    output_dir = Path(os.getenv("CWD", "")) / output
    formatter: BaseFormat
    if format == "stardict":
        pre_formatter = DictFileFormat(locale, output_dir, def_words, {}, "")
        pre_formatter.process()
        formatter = StarDictFormat(locale, output_dir, def_words, {}, "")
    else:
        formatter = KoboFormat(locale, output_dir, def_words, {}, "")
    formatter.process()

    return 0
