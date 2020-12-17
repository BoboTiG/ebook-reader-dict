"""Get and render a word."""
import re

import requests

from .render import parse_word
from .user_functions import int_to_roman
from .utils import convert_pronunciation, convert_genre


def get_and_parse_word(word: str, locale: str, raw: bool = False) -> None:
    """Get a *word* wikicode and parse it."""
    url = f"https://{locale}.wiktionary.org/w/index.php?title={word}&action=raw"
    with requests.get(url) as req:
        code = req.text

    details = parse_word(word, code, locale, force=True)

    def strip_html(text: str) -> str:
        """Stip HTML chars."""
        if raw:
            return text
        text = re.sub(r"<[^>]+/?>", "", text)
        text = text.replace("&minus;", "-")
        text = text.replace("&nbsp;", " ")
        text = text.replace("&thinsp;", " ")
        text = text.replace("&times;", "×")
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        return text

    print(
        word,
        convert_pronunciation(details.pronunciations).lstrip(),
        strip_html(convert_genre(details.genre).lstrip()),
        "\n",
    )

    if details.etymology:
        print(strip_html(details.etymology), "\n")

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

    if details.variants:
        print("[variants]", ", ".join(iter(details.variants)))


def main(locale: str, word: str, raw: bool = False) -> int:
    """Entry point."""

    get_and_parse_word(word, locale, raw)
    return 0
