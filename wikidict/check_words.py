"""Get and render N words; then compare with the rendering done on the Wiktionary to catch errors."""
import datetime
import os
from pathlib import Path
from random import choice
from typing import List

from . import check_word, render


def main(locale: str, count: int, random: bool, offset: str, input: str) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    all_words: List[str] = []
    if input:
        with open(input) as fp:
            all_words = fp.read().splitlines()
    else:
        file = render.get_latest_json_file(output_dir)
        if not file:
            print(">>> No dump found. Run with --parse first ... ", flush=True)
            return 1

        print(f">>> Loading {file} ...")
        all_words = list(render.load(file).keys())

    if count == -1:
        count = len(all_words)

    if offset:
        if offset.isnumeric():  # offset = "42"
            offset_int = int(offset)
            all_words = all_words[offset_int:]
        else:  # offset = "some word"
            for i, word in enumerate(all_words):
                if word == offset:
                    all_words = all_words[i:]
                    break

    count = min(count, len(all_words))
    errors = 0
    for n in range(count):
        word = choice(all_words) if random else all_words[n]
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{now}] - [{n + 1}/{count}] Checking {word!r}", flush=True)
        errors += check_word.main(locale, word)

    if errors:
        print("\n >>> TOTAL Errors:", errors)

    return errors
