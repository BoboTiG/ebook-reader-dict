"""DEBUG: generate the dictionary for specific words."""
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple

from .convert import (
    DictFileFormat,
    KoboFormat,
    StarDictFormat,
    make_variants,
    run_formatter,
)
from .get_word import get_word
from .stubs import Variants, Words


def main(locale: str, words: str, output: str, format: str = "kobo") -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / output
    all_words = {word: get_word(word, locale) for word in words.split(",")}
    variants: Variants = make_variants(all_words)
    args: Tuple[str, Path, Words, Variants, str] = (
        locale,
        output_dir,
        all_words,
        variants,
        datetime.utcnow().strftime("%Y%m%d"),
    )

    if format == "stardict":
        run_formatter(DictFileFormat, *args)
        run_formatter(StarDictFormat, *args)
    else:
        run_formatter(KoboFormat, *args)

    return 0
