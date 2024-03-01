"""Generate the description of a GitHub release."""

import os
from pathlib import Path

from .utils import format_description


def main(locale: str) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    print(format_description(locale, output_dir), flush=True)
    return 0
