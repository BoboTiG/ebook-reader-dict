import sys
from argparse import ArgumentParser
from typing import List

from . import convert, get, upload


def main(argv: List[str]) -> int:
    """Main entry point."""

    parser = ArgumentParser(description="eBook Reader Dictionaries")
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

    args = parser.parse_args(args=argv)

    if args.update_release:
        return upload.main()
    elif args.fetch_only:
        return get.main()
    elif args.convert_only:
        return convert.main()
    else:
        if get.main() == 1:
            return 1
        return convert.main()


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main(sys.argv[1:]))
