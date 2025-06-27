"""Get and render a word."""

from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

from . import constants, utils
from .render import parse_word
from .user_functions import int_to_roman

if TYPE_CHECKING:
    from .stubs import Word


def get_word(word: str, locale: str, *, all_templates: list[tuple[str, str, str]] | None = None) -> Word:
    """Get a *word* wikicode and parse it."""
    url = f"https://{utils.guess_lang_origin(locale)}.wiktionary.org/w/index.php?title={word}&action=raw"
    with constants.SESSION.get(url) as req:
        code = req.text
    return parse_word(word, code, locale, force=True, all_templates=all_templates)


def get_and_parse_word(word: str, locale: str, *, raw: bool = False) -> None:
    """Get a *word* wikicode, parse it and print it."""

    def strip_html(text: str) -> str:
        """Strip HTML chars."""
        if raw:
            return repr(text)
        text = text.replace("<br>", "\n")
        text = text.replace("<br/>", "\n")
        text = re.sub(r"<[^>]+/?>", "", text)
        text = text.replace("&minus;", "-")
        text = text.replace("&nbsp;", " ")
        text = text.replace("&thinsp;", " ")
        text = text.replace("&times;", "×")
        text = text.replace("&lsaquo;", "‹")
        text = text.replace("&rsaquo;", "›")
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        return text

    all_templates: list[tuple[str, str, str]] = []
    details = get_word(word, locale, all_templates=all_templates)
    print(
        word,
        utils.convert_pronunciation(details.pronunciations).lstrip(),
        strip_html(utils.convert_gender(details.genders).lstrip()),
    )

    for pos, definitions in sorted(details.definitions.items(), key=lambda kv: kv[0]):
        print("\n", pos)
        index = 1
        for definition in definitions:
            if isinstance(definition, tuple):
                for a, subdef in zip("abcdefghijklmopqrstuvwxz", definition):
                    if isinstance(subdef, tuple):
                        for rn, subsubdef in enumerate(subdef, 1):
                            print(
                                f"{int_to_roman(rn).lower()}.".rjust(12),
                                strip_html(subsubdef),
                            )
                    else:
                        print(f"{a}.".rjust(8), strip_html(subdef))
            else:
                print(f"{index}.".rjust(4), strip_html(definition))
                index = index + 1

    if details.etymology:
        print("\n")
        for etymology in details.etymology:
            if isinstance(etymology, tuple):
                for i, sub_etymology in enumerate(etymology, 1):
                    print(f"{i}.".rjust(8), strip_html(sub_etymology))  # type: ignore[arg-type]
            else:
                print(strip_html(etymology))

    if details.variants:
        print("\n[variants]", ", ".join(iter(details.variants)))

    print()
    utils.check_for_missing_templates(all_templates)


def set_output(locale: str, word: str) -> None:
    """It is very specific to GitHub Actions, and will set the job summary with helpful information."""
    if "CI" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "ab") as fh:
            fh.write(f"[{locale.upper()}] {word!r}\n".encode())


def main(locale: str, word: str, *, raw: bool = False) -> int:
    """Entry point."""

    _, lang_dst = utils.guess_locales(locale, use_log=False)

    # If *word* is empty, get a random word
    word = word or utils.get_random_word(lang_dst)

    set_output(locale, word)
    get_and_parse_word(word, locale, raw=raw)
    return 0
