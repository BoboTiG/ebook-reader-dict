"""
eBook Reader Dictionaries

Usage:
    wikidict LOCALE
    wikidict LOCALE --download
"""
import sys
from typing import List

from docopt import docopt


def main(argv: List[str]) -> int:
    """Main entry point."""

    args = docopt(__doc__)

    if args["--download"]:
        from . import download

        return download.main(args["LOCALE"])

    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main(sys.argv[1:]))
