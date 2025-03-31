"""Generate the description of a GitHub release."""

import os
from pathlib import Path
from zipfile import ZipFile

from . import constants
from .utils import format_description, guess_locales


def main(locale: str) -> int:
    """Entry point."""

    lang_src, lang_dst = guess_locales(locale, use_log=False, uniformize=True)
    output_dir = Path(os.getenv("CWD", "")) / "data" / lang_dst

    # Use the full Kobo dictionary as reference
    with ZipFile(output_dir / f"dicthtml-{lang_src}-{lang_dst}.zip") as fh:
        count = int(fh.read(constants.ZIP_WORDS_COUNT).decode())
        snapshot = fh.read(constants.ZIP_WORDS_SNAPSHOT).decode()

    print(format_description(lang_src, lang_dst, count, snapshot), flush=True)
    return 0
