"""Generate the description of a GitHub release."""

import logging
from pathlib import Path
from zipfile import ZipFile

from . import constants, render, utils

log = logging.getLogger(__name__)


def get_source_file(source_dir: Path, lang_src: str, lang_dst: str) -> Path:
    """Use the full Kobo dictionary as reference."""
    return source_dir / "output" / f"dicthtml-{lang_src}-{lang_dst}.zip"


def main(locale: str) -> int:
    """Entry point."""

    lang_src, lang_dst = utils.guess_locales(locale, use_log=False)

    source_dir = render.get_source_dir(lang_src, lang_dst)
    source_file = get_source_file(source_dir, lang_src, lang_dst)
    if not source_file.is_file():
        log.error("No dict found. Run with --convert first ... ")
        return 1

    with ZipFile(source_file) as fh:
        count = int(fh.read(constants.ZIP_WORDS_COUNT).decode())
        snapshot = fh.read(constants.ZIP_WORDS_SNAPSHOT).decode()

    print(utils.format_description(lang_src, lang_dst, count, snapshot), flush=True)
    return 0
