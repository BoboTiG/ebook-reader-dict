"""Get and render a word; then compare with the rendering done on the Wiktionary to catch errors."""
from .render import parse_word
from .stubs import Word

import requests
from bs4 import BeautifulSoup


def get_text(html: str) -> str:
    """Parse the HTML code and return it as a string."""
    return str(BeautifulSoup(markup=html, features="html.parser").text)


def get_word(word: str, locale: str) -> Word:
    """Get a *word* wikicode and parse it."""
    url = f"https://{locale}.wiktionary.org/w/index.php?title={word}&action=raw"
    with requests.get(url) as req:
        return parse_word(word, req.text, locale)


def get_wiktionary_page(word: str, locale: str) -> str:
    """Get a *word* HTML."""
    url = f"https://{locale}.wiktionary.org/w/index.php?title={word}"
    with requests.get(url) as req:
        return get_text(req.text)


def main(locale: str, word: str) -> int:
    """Entry point."""
    details = get_word(word, locale)
    text = get_wiktionary_page(word, locale)
    errors = 0

    if details.etymology:
        clean_text = get_text(details.etymology)
        if clean_text not in text:
            print(" !! Etymology")
            print(clean_text)
            errors += 1

    for num, definition in enumerate(details.definitions, start=1):
        clean_text = get_text(definition)
        if clean_text not in text:
            print(f"\n !! Definition n°{num}")
            print(clean_text)
            errors += 1

    if errors:
        print("\n >>> Errors:", errors)

    return 0
