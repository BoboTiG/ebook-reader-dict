import sys  # pragma: nocover

from . import convert, get, upload  # pragma: nocover


if __name__ == "__main__":  # pragma: nocover
    # Update the release description
    if "--update-release" in sys.argv:
        sys.exit(upload.main())

    # Launch fetch + convert operations
    if get.main() == 1:
        sys.exit(1)
    sys.exit(convert.main())
