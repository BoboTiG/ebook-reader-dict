"""
eBook Reader Dictionaries

Usage:
    wikidict LOCALE
    wikidict LOCALE -h, --help
    wikidict LOCALE --download
    wikidict LOCALE --parse
    wikidict LOCALE --render
    wikidict LOCALE --convert
    wikidict LOCALE --find-templates
    wikidict LOCALE --check-words [--random] [--count=N] [--offset=M] [--input=FILENAME]
    wikidict LOCALE --check-word=WORD
    wikidict LOCALE --get-word=WORD [--raw]
    wikidict LOCALE --gen-dict=WORDS --output=FILENAME [--format=FORMAT]
    wikidict LOCALE --update-release

Options:
  --download                Retrieve the latest Wiktionary dump into "data/$LOCALE/pages-$DATE.xml".
  --parse                   Parse and store raw Wiktionary data into "data/$LOCALE/data_wikicode-$DATE.json".
  --render                  Render templates from raw data into "data/$LOCALE/data-$DATE.json"
  --convert                 Convert rendered data to working dictionaries into several files:
                                - "data/$LOCALE/dicthtml-$LOCALE-$LOCALE.zip": Kobo format.
                                - "data/$LOCALE/dict-$LOCALE-$LOCALE.df.bz2": DictFile format.
                                - "data/$LOCALE/dict-$LOCALE-$LOCALE.zip": StarDict format.
  --find-templates          DEBUG: Find all templates in use.
  --check-words             Render words, then compare with the rendering done on the Wiktionary to catch errors.
                            --random            randomly if --random
                            --count=N           If -1 check all words [default: 100]
                            --offset=M          Offset will remove words before starting.
                            --input=FILENAME    A list of words, one by line
                            --check-word=WORD   Get and render WORD.
  --get-word=WORD [--raw]   Get and render WORD. Pass --raw to ouput the raw HTML code.
  --gen-dict=WORDS          DEBUG: Generate Kobo/StarDict dictionaries for specific words. Pass multiple words
                            separated with a comma: WORD1,WORD2,WORD3,...
                            The generated filename can be tweaked via the --output=FILENAME argument.
                            --format= FORMAT    Format can be "kobo" or "stardict" [default: kobo]
  --update-release          DEV: Update the release description. Do not use it manually but via the CI only.

If no argument given, --download, --parse, --render, and --convert will be done automatically.
"""
import sys

from docopt import docopt


def main() -> int:  # pragma: nocover
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

    if args["--check-word"] is not None:
        from . import check_word

        return check_word.main(args["LOCALE"], args["--check-word"])

    if args["--check-words"]:
        from . import check_words

        return check_words.main(
            args["LOCALE"],
            int(args["--count"]),
            args["--random"],
            args["--offset"],
            args["--input"],
        )

    if args["--get-word"] is not None:
        from . import get_word

        return get_word.main(args["LOCALE"], args["--get-word"], args["--raw"])

    if args["--gen-dict"] is not None:
        from . import gen_dict

        return gen_dict.main(
            args["LOCALE"], args["--gen-dict"], args["--output"], args["--format"]
        )

    if args["--update-release"]:
        from . import upload

        return upload.main(args["LOCALE"])

    # Run the whole process by default
    from . import convert, download, parse, render

    download.main(args["LOCALE"])
    parse.main(args["LOCALE"])
    render.main(args["LOCALE"])
    convert.main(args["LOCALE"])

    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
