import sys  # pragma: nocover

from . import convert, get  # pragma: nocover


if __name__ == "__main__":  # pragma: nocover
    if get.main() == 1:
        sys.exit(1)
    sys.exit(convert.main())
