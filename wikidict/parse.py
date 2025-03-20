"""Parse and store raw Wiktionary data."""

from __future__ import annotations

import json
import logging
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING
from xml.sax.saxutils import unescape

from .lang import head_sections

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Iterator


log = logging.getLogger(__name__)

RE_TEXT = re.compile(r"<text[^>]*>(.*)</text>", flags=re.DOTALL).finditer
RE_TITLE = re.compile(r"<title>([^:]*)</title>").finditer

# To list all words not taken into account with current head sections:
#    DEBUG_PARSE=1 python -m wikidict LOCALE --parse >out.log
DEBUG_PARSE = "DEBUG_PARSE" in os.environ


def xml_iter_parse(file: Path) -> Generator[str]:
    """Efficient XML parsing for big files."""
    element: list[str] = []
    is_element = False

    with file.open(encoding="utf-8") as fh:
        for line in fh:
            if is_element:
                if "/page>" in line:
                    yield "".join(element)
                    element = []
                    is_element = False
                else:
                    element.append(line)
            elif "<page" in line:
                is_element = True


def xml_parse_element(element: str, head_sections_matcher: Callable[[str], Iterator[str]]) -> tuple[str, str]:
    """Parse the XML `element` to retrieve the word and its definitions."""
    if title_match := next(RE_TITLE(element), None):
        for text_match in RE_TEXT(element, pos=element.find("<text", title_match.endpos)):
            if next(head_sections_matcher(wikicode := text_match[1]), None):
                return title_match[1], wikicode

        if DEBUG_PARSE:
            try:
                print(f"{title_match[1]!r}: {wikicode[:200]!r}", flush=True)
            except UnboundLocalError:
                print(f"{title_match[1]!r}: NO TEXT", flush=True)

    # No Wikicode; unfinished page; no interesting head section; a foreign word, etc. Who knows?
    return "", ""


def process(file: Path, locale: str) -> dict[str, str]:
    """Process the big XML file and retain only information we are interested in."""
    words: dict[str, str] = defaultdict(str)

    log.info("Processing %s ...", file)

    if locale in {"ca", "da", "el", "en", "it", "no", "pt", "sv"}:
        # For several locales it is more accurate to use a regexp matcher
        head_sections_matcher = re.compile(
            rf"^=*\s*({'|'.join(head_sections[locale])})",
            flags=re.IGNORECASE | re.MULTILINE,
        ).finditer
    else:
        # While for others, a simple check is better because it is either more accurate, or simply impossible to rely on the former
        assert locale in {"de", "es", "eo", "fr", "fro", "ro", "ru"}

        def head_sections_matcher(wikicode: str) -> Iterator[str]:  # type: ignore[misc]
            return (s for s in head_sections[locale] if s in wikicode.lower())

    for element in xml_iter_parse(file):
        word, code = xml_parse_element(element, head_sections_matcher)  # type: ignore[arg-type]
        if word and code:
            words[unescape(word)] = unescape(code)

    return words


def save(snapshot: str, words: dict[str, str], output_dir: Path) -> None:
    """Persist data."""
    raw_data = output_dir / f"data_wikicode-{snapshot}.json"
    with raw_data.open(mode="w", encoding="utf-8") as fh:
        json.dump(words, fh, indent=4, sort_keys=True)

    log.info("Saved %s words into %s", f"{len(words):,}", raw_data)


def get_latest_xml_file(output_dir: Path) -> Path | None:
    """Get the name of the last pages-*.xml file."""
    files = list(output_dir.glob("pages-*.xml"))
    return sorted(files)[-1] if files else None


def main(locale: str) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    file = get_latest_xml_file(output_dir)
    if not file:
        log.error("No dump found. Run with --download first ... ")
        return 1

    date = file.stem.split("-")[1]
    output = output_dir / f"data_wikicode-{date}.json"
    if not output.is_file():
        words = process(file, locale)
        save(date, words, output_dir)
    log.info("Parse done in %s!", output)
    return 0
