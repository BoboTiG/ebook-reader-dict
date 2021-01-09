"""Get and render N words; then compare with the rendering done on the Wiktionary to catch errors."""
import os
from pathlib import Path
from random import choice
from typing import List

from . import check_word
from .render import get_latest_json_file, load


def main(locale: str, count: int) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    file = get_latest_json_file(output_dir)
    if not file:
        print(">>> No dump found. Run with --parse first ... ", flush=True)
        return 1

    print(f">>> Loading {file} ...")
    all_words: List[str] = list(load(file).keys())

    errors = 0
    for n in range(count):
        word = choice(all_words)
        print(f"\n[{n + 1}/{count}] Checking {word!r}", flush=True)
        errors += check_word.main(locale, word)

    if errors:
        print("\n >>> TOTAL Errors:", errors)

    return errors
