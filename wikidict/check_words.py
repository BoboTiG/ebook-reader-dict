"""Get and render N words; then compare with the rendering done on the Wiktionary to catch errors."""

import logging
import os
import random
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

from . import check_word, render

log = logging.getLogger(__name__)


def local_check(word: str, locale: str) -> int:
    return check_word.check_word(word, locale)


def get_words_to_tackle(
    locale: str,
    *,
    count: int = 100,
    is_random: bool = False,
    offset: str = "",
    input_file: str = "",
) -> list[str]:
    words: list[str] = []

    if input_file:
        words = Path(input_file).read_text().splitlines()
    else:
        output_dir = Path(os.getenv("CWD", "")) / "data" / locale
        if not (file := render.get_latest_json_file(output_dir)):
            log.error(">>> No dump found. Run with --parse first ... ")
            return []

        log.info(">>> Loading %s ...", file)
        words = list(render.load(file).keys())

    if count == -1:
        count = len(words)

    if offset:
        if offset.isnumeric():  # offset = "42"
            words = words[int(offset) :]
        else:  # offset = "some word"
            for i, word in enumerate(words):
                if word == offset:
                    words = words[i:]
                    break

    if is_random:
        words = random.sample(words, min(count, len(words)))
    elif count < len(words):
        words = words[: min(count, len(words))]

    return words


def main(locale: str, count: int, is_random: bool, offset: str, input_file: str) -> int:
    """Entry point."""

    words = get_words_to_tackle(locale, count=count, is_random=is_random, offset=offset, input_file=input_file)

    with ThreadPoolExecutor(10) as pool:
        err = pool.map(partial(local_check, locale=locale), words)

    if errors := sum(err):
        log.warning(">>> TOTAL Errors: %d", errors)

    return errors
