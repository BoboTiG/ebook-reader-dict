"""Parse and store raw Wiktionary data."""

import json
import logging
import os
import re
from collections import defaultdict
from collections.abc import Generator
from pathlib import Path

from .lang import head_sections

log = logging.getLogger(__name__)

RE_TEXT = re.compile(r"<text[^>]*>(.*)</text>", flags=re.DOTALL).finditer
RE_TITLE = re.compile(r"<title>(.*)</title>").finditer


def xml_iter_parse(file: Path) -> Generator[str, None, None]:
    """Efficient XML parsing for big files.
    Elements are yielded when they meet the "page" tag.
    """
    element: list[str] = []
    is_element = False

    with file.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line == "<page>":
                is_element = True
            elif line == "</page>":
                yield "\n".join(element)
                element = []
                is_element = False
            elif is_element:
                element.append(line)


def xml_parse_element(element: str, locale: str) -> tuple[str, str]:
    """Parse the *element* to retrieve the word and its definitions."""
    for match in RE_TEXT(element):
        code = match[1]
        break
    else:
        # No Wikicode, maybe an unfinished page.
        return "", ""

    # No interesting head section, a foreign word?
    if all(section not in code for section in head_sections[locale]):
        return "", ""

    word = next(RE_TITLE(element))[1]
    return word, code


def process(file: Path, locale: str) -> dict[str, str]:
    """Process the big XML file and retain only information we are interested in."""
    words: dict[str, str] = defaultdict(str)

    log.info("Processing %s ...", file)
    for element in xml_iter_parse(file):
        word, code = xml_parse_element(element, locale)
        if word and code and ":" not in word:
            words[word] = code

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
    if not (output_dir / f"data_wikicode-{date}.json").is_file():
        words = process(file, locale)
        save(date, words, output_dir)
    log.info("Parse done!")
    return 0
