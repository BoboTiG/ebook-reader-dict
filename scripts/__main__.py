import sys
from argparse import ArgumentParser
from typing import List


def main(argv: List[str]) -> int:
    """Main entry point."""

    parser = ArgumentParser(description="eBook Reader Dictionaries")
    parser.add_argument(
        "--locale",
        required=True,
        help="the target locale",
    )
    parser.add_argument(
        "--convert-only",
        dest="convert_only",
        action="store_true",
        default=False,
        help="generate the dictionary",
    )
    parser.add_argument(
        "--fetch-only",
        dest="fetch_only",
        action="store_true",
        default=False,
        help="download definitions and do the clean-up",
    )
    parser.add_argument(
        "--update-release",
        dest="update_release",
        action="store_true",
        default=False,
        help="update the release description",
    )
    parser.add_argument(
        "--get-word",
        dest="get_word",
        help="download and parse the word Wikicode",
    )
    parser.add_argument(
        "--raw",
        "--html",
        dest="raw_output",
        action="store_true",
        default=False,
        help="display the raw output (for --get-word)",
    )

    args = parser.parse_args(args=argv)

    if args.update_release:
        from . import upload

        return upload.main(args.locale)
    elif args.get_word:
        from . import get

        return get.main(args.locale, word=args.get_word, raw=args.raw_output)
    elif args.fetch_only:
        from . import get

        return get.main(args.locale)
    elif args.convert_only:
        from . import convert

        return convert.main(args.locale)
    else:
        from . import convert, get

        if get.main(args.locale) == 1:
            return 1
        return convert.main(args.locale)


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main(sys.argv[1:]))
