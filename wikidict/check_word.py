"""Get and render a word; then compare with the rendering done on the Wiktionary to catch errors."""
import re
from functools import partial

from .render import parse_word
from .stubs import Word
from .user_functions import int_to_roman
from .utils import get_word_of_the_day

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

    # Filter out result of <math> and <chem>
    for span in bs.find_all("span", {"class": "mwe-math-element"}):
        span.decompose()

    # Adapt the formatting for the ES locale as it differs from other locales
    if locale == "es":
        dts = bs.find_all("dt")
        for dt in dts:

            dt_array = dt.text.split(" ", 1)
            if len(dt_array) == 2:
                dt.string = dt_array[0] + " "
                if "." in dt_array[1]:
                    dt_array_dot = dt_array[1].split(".")
                    for da in dt_array_dot[:-1]:
                        dt.string += f"({da})"
                    dt.string += f" {dt_array_dot[-1]}:"
                else:
                    dt.string += f"({dt_array[1]}):"

    if locale == "fr":
        # Filter out refnec tags
        for span in bs.find_all("span", {"id": "refnec"}):
            span.previous_sibling.decompose()
            span.decompose()
        # Cette information a besoin d’être précisée
        for span in bs.find_all(
            "span", {"title": "Cette information a besoin d’être précisée"}
        ):
            span.decompose()
        # — (Richelet, Dictionnaire français 1680)
        for span in bs.find_all("span", {"class": "sources"}):
            span.decompose()
        # → consulter cet ouvrage
        for a in bs.find_all("a", {"class": "external text"}):
            if "consulter cet ouvrage" in a.text:
                a.decompose()
        # sur Wikispecies
        for a in bs.find_all("a", {"class": "extiw"}):
            if (
                a["title"].startswith("wikispecies")
                and a.parent.next_sibling
                and "sur Wikispecies" in a.parent.next_sibling
            ):
                a.parent.next_sibling.replaceWith("")
            # {{LienRouge|lang=en|trad=Reconstruction
            if "Reconstruction" in a["title"]:
                a.decompose()
        # external autonumber
        for a in bs.find_all("a", {"class": "external autonumber"}):
            a.decompose()
        # attention image
        for a in bs.find_all("a", {"title": "alt = attention"}):
            a.replaceWith("⚠")
        # other anchors
        for a in bs.find_all("a", href=True):
            if a["href"].lower().startswith(("#cite", "#ref", "#voir")):
                a.decompose()
        return no_spaces(bs.text)

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
    errors = 0

    # If *word* is empty, get the word of the day
    if not word:
        word = get_word_of_the_day(locale)

    details = get_word(word, locale)
    if not details.etymology and not details.definitions:
        return errors
    text = get_wiktionary_page(word, locale)

    if details.etymology:
        for etymology in details.etymology:
            if isinstance(etymology, tuple):
                for i, sub_etymology in enumerate(etymology, 1):
                    errors += check(text, sub_etymology, f"\n !! Etymology {i}")
            else:
                errors += check(text, etymology, "\n !! Etymology")

    index = 1
    for definition in details.definitions:
        message = f"\n !! Definition n°{index}"
        if isinstance(definition, tuple):
            for a, subdef in zip("abcdefghijklmopqrstuvwxz", definition):
                if isinstance(subdef, tuple):
                    for rn, subsubdef in enumerate(subdef, 1):
                        errors += check(
                            text, subsubdef, f"{message}.{int_to_roman(rn).lower()}"
                        )
                else:
                    errors += check(text, subdef, f"{message}.{a}")
        else:
            errors += check(text, definition, message)
            index += 1

    if errors:
        print(f"\n >>> [{word}] - Errors:", errors)

    return errors
