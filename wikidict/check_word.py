"""Get and render a word; then compare with the rendering done on the Wiktionary to catch errors."""
import re
from functools import partial

from .render import parse_word
from .stubs import Word
from .user_functions import int_to_roman

import requests
from bs4 import BeautifulSoup


# Remove all kind of spaces and some unicode characters
_replace_noisy_chars = re.compile(r"[\s\u200e]").sub
no_spaces = partial(_replace_noisy_chars, "")


def check(text: str, html: str, message: str) -> int:
    """Run checks and return the error count to increment."""
    clean_text = get_text(html)
    if not contains(clean_text, text):
        print(message, flush=True)
        print(clean_text, flush=True)
        return 1
    return 0


def contains(pattern: str, text: str) -> bool:
    """Check if *pattern* is in *text*, with all spaces removed.
    *text* is already stripped from spaces in get_wiktionary_page().
    """
    return no_spaces(pattern) in text


def filter_html(html: str, locale: str) -> str:
    """Some parts of the Wiktionary HTML."""
    bs = BeautifulSoup(markup=html, features="html.parser")

    # Filter out warnings about obsolete template models used
    for span in bs.find_all("span", {"id": "FormattingError"}):
        span.decompose()

    # Filter out Wikispecies links
    for span in bs.find_all("span", {"class": "trad-exposant"}):
        span.decompose()

    # Adapt the formatting for the ES locale as it differs from other locales
    if locale == "es":
        dts = bs.find_all("dt")
        for dt in dts:
            dt_array = dt.text.split(" ", 1)
            if len(dt_array) == 2:
                dt.string = dt_array[0] + " " + f'({dt_array[1].strip(".")}):'

    if locale == "fr":
        # Filter out refnec tags
        for span in bs.find_all("span", {"id": "refnec"}):
            span.previous_sibling.decompose()
            span.decompose()
        # Filter out citation reference as they are ignored from templates
        for a in bs.find_all("a", href=True):
            if any(a["href"].startswith(exclude) for exclude in ("#ref", "#cite")):
                a.decompose()
    else:
        # Filter out anchors as they are ignored from templates
        for a in bs.find_all("a", href=True):
            if a["href"].startswith("#"):
                a.decompose()

    return no_spaces(bs.text)


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
        return filter_html(req.text, locale)


def main(locale: str, word: str) -> int:
    """Entry point."""
    details = get_word(word, locale)
    text = get_wiktionary_page(word, locale)
    errors = 0

    if details.etymology:
        errors += check(text, details.etymology, " !! Etymology")

    for num, definition in enumerate(details.definitions, start=1):
        message = f"\n !! Definition n°{num}"
        if isinstance(definition, str):
            errors += check(text, definition, message)
            continue

        # Sublist
        for subnum, subdef in enumerate(definition, start=1):
            errors += check(text, subdef, f"{message}.{int_to_roman(subnum).lower()}")

    if errors:
        print("\n >>> Errors:", errors)

    return errors
