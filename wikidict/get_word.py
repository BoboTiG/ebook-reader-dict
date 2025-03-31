"""Get and render a word."""

from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

import requests

from .render import parse_word
from .user_functions import int_to_roman
from .utils import check_for_missing_templates, convert_gender, convert_pronunciation, get_random_word, guess_locales

if TYPE_CHECKING:
    from .stubs import Word


def get_word(word: str, lang_src: str, lang_dst: str, *, missed_templates: list[tuple[str, str]] | None = None) -> Word:
    """Get a *word* wikicode and parse it."""
    url = f"https://{lang_src}.wiktionary.org/w/index.php?title={word}&action=raw"
    with requests.get(url) as req:
        code = req.text
    return parse_word(word, code, lang_dst, force=True, missed_templates=missed_templates)


def get_and_parse_word(word: str, lang_src: str, lang_dst: str, *, raw: bool = False) -> None:
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
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        return text

    missed_templates: list[tuple[str, str]] = []
    details = get_word(word, lang_src, lang_dst, missed_templates=missed_templates)
    print(
        word,
        convert_pronunciation(details.pronunciations).lstrip(),
        strip_html(convert_gender(details.genders).lstrip()),
        "\n",
    )

    index = 1
    for definition in details.definitions:
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

    check_for_missing_templates(missed_templates)


def set_output(locale: str, word: str) -> None:
    """It is very specific to GitHub Actions, and will set the job summary with helpful information."""
    if "CI" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "ab") as fh:
            fh.write(f"[{locale.upper()}] {word!r}\n".encode())


def main(locale: str, word: str, *, raw: bool = False) -> int:
    """Entry point."""

    lang_src, lang_dst = guess_locales(locale, use_log=False)

    # If *word* is empty, get a random word
    word = word or get_random_word(lang_dst)

    set_output(lang_dst, word)
    get_and_parse_word(word, lang_src, lang_dst, raw=raw)
    return 0
