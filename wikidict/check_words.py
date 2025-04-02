"""Get and render N words; then compare with the rendering done on the Wiktionary to catch errors."""

import logging
import random
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

from . import check_word, render, utils

log = logging.getLogger(__name__)


def local_check(
    word: str,
    locale: str,
    *,
    missed_templates: list[tuple[str, str]] | None = None,
) -> int:
    return check_word.check_word(word, locale, standalone=False, missed_templates=missed_templates)


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
        lang_src, lang_dst = utils.guess_locales(locale)
        source_dir = render.get_source_dir(lang_src, lang_dst)
        if not (file := render.get_latest_json_file(source_dir)):
            log.error("No dump found. Run with --parse first ... ")
            return []

        log.info("Loading %s ...", file)
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
    missed_templates: list[tuple[str, str]] = []

    with ThreadPoolExecutor(max_workers=10) as pool:
        err = pool.map(
            partial(local_check, locale=locale, missed_templates=missed_templates),
            words,
        )

    if errors := sum(err):
        log.warning("TOTAL Errors: %s", f"{errors:,}")

    utils.check_for_missing_templates(missed_templates)

    return errors
