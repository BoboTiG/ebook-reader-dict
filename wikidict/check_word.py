"""Get and render a word."""
import requests
from bs4 import BeautifulSoup

from .render import parse_word
from .stubs import Word


def get_word(word: str, locale: str) -> Word:
    """Get a *word* wikicode and parse it."""
    url = f"https://{locale}.wiktionary.org/w/index.php?title={word}&action=raw"
    with requests.get(url) as req:
        code = req.text

    details = parse_word(word, code, locale, force=True)
    return details


def get_wiktionary_page(word: str, locale: str) -> str:
    url = f"https://{locale}.wiktionary.org/w/index.php?title={word}"
    req = requests.get(url)
    page = req.content
    bs = BeautifulSoup(page, features="html.parser")
    return str(bs.get_text())


def main(locale: str, word: str) -> int:
    """Entry point."""
    details = get_word(word, locale)
    text = get_wiktionary_page(word, locale)
    if details.etymology:
        clean_text = BeautifulSoup(details.etymology, features="html.parser").text
        if clean_text not in text:
            print("Etymology KO")
            print(clean_text)

    for definition in details.definitions:
        if definition:
            clean_text = BeautifulSoup(definition, features="html.parser").text
            if clean_text not in text:
                print("definition KO")
                print(clean_text)

    return 0
