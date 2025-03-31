"""DEBUG: generate the dictionary for specific words."""

import os
from datetime import UTC, datetime
from pathlib import Path

from .convert import (
    DictFileFormat,
    DictOrgFormat,
    KoboFormat,
    StarDictFormat,
    make_variants,
    run_formatter,
    run_mobi_formatter,
)
from .get_word import get_word
from .stubs import Variants, Words
from .utils import guess_locales


def main(locale: str, words: str, output: str, *, format: str = "kobo") -> int:
    """Entry point."""

    lang_src, lang_dst = guess_locales(locale, use_log=False)

    output_dir = Path(os.getenv("CWD", "")) / output
    output_dir.mkdir(parents=True, exist_ok=True)
    words_stripped = [word_stripped for word in words.split(",") if (word_stripped := word.strip())]
    all_words = {word: get_word(word, lang_src, lang_dst) for word in words_stripped}
    variants: Variants = make_variants(all_words)
    args: tuple[str, Path, Words, Variants, str] = (
        locale,
        output_dir,
        all_words,
        variants,
        datetime.now(tz=UTC).strftime("%Y%m%d"),
    )

    match format:
        case "dictorg":
            run_formatter(DictFileFormat, *args)
            run_formatter(DictOrgFormat, *args)
        case "mobi":
            run_mobi_formatter(output_dir, Path(f"data-{args[-1]}.json"), locale, all_words, variants)
        case "stardict":
            run_formatter(DictFileFormat, *args)
            run_formatter(StarDictFormat, *args)
        case _:
            run_formatter(KoboFormat, *args)

    return 0
