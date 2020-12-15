"""
eBook Reader Dictionaries

Usage:
    wikidict LOCALE
    wikidict LOCALE --download
    wikidict LOCALE --parse
    wikidict LOCALE --render
    wikidict LOCALE --convert
    wikidict LOCALE --find-templates
    wikidict LOCALE --get-word WORD [--raw]

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

    if args["--parse"]:
        from . import parse

        return parse.main(args["LOCALE"])

    if args["--render"]:
        from . import render

        return render.main(args["LOCALE"])

    if args["--convert"]:
        from . import convert

        return convert.main(args["LOCALE"])

    if args["--find-templates"]:
        from . import find_templates

        return find_templates.main(args["LOCALE"])

    if args["--get-word"]:
        from . import get_word

        return get_word.main(args["LOCALE"], args["WORD"], args["--raw"])

    # Run the whole process by default
    from . import download, parse, render

    download.main(args["LOCALE"])
    parse.main(args["LOCALE"])
    render.main(args["LOCALE"])

    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main(sys.argv[1:]))
