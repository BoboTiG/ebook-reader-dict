"""DEBUG: generate the dictionary for specific words."""
import os
from typing import Tuple
from .get_word import get_word
from .convert import DictFileFormat, KoboFormat, StarDictFormat, run_formatter
from pathlib import Path
from .stubs import Variants, Words


def main(locale: str, words: str, output: str, format: str = "kobo") -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / output
    all_words = {word: get_word(word, locale) for word in words.split(",")}
    args: Tuple[str, Path, Words, Variants, str] = (
        locale,
        output_dir,
        all_words,
        {},
        "",
    )

    if format == "stardict":
        run_formatter(DictFileFormat, *args)
        run_formatter(StarDictFormat, *args)
    else:
        run_formatter(KoboFormat, *args)

    return 0
