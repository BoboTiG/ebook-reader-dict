"""Generate the description of a GitHub release."""

import os
from pathlib import Path
from zipfile import ZipFile

from . import constants
from .utils import format_description


def main(locale: str) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale

    # Use the full Kobo dictionary as reference
    with ZipFile(output_dir / f"dicthtml-{locale}-{locale}.zip") as fh:
        count = int(fh.read(constants.ZIP_WORDS_COUNT).decode())
        snapshot = fh.read(constants.ZIP_WORDS_SNAPSHOT).decode()

    print(format_description(locale, count, snapshot), flush=True)
    return 0
