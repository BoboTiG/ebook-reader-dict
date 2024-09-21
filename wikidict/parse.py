"""Parse and store raw Wiktionary data."""

import json
import os
from collections import defaultdict
from collections.abc import Generator
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from .lang import head_sections


def xml_iter_parse(file: Path) -> Generator[Element, None, None]:
    """Efficient XML parsing for big files.
    Elements are yielded when they meet the "page" tag.
    """

    doc = ElementTree.iterparse(file, events=("start", "end"))
    _, root = next(doc)

    start_tag = None

    for event, element in doc:
        if start_tag is None and event == "start" and element.tag == "{http://www.mediawiki.org/xml/export-0.11/}page":
            start_tag = element.tag
        elif start_tag is not None and event == "end" and element.tag == start_tag:
            yield element
            start_tag = None

            # Keep memory low
            root.clear()


def xml_parse_element(element: Element, locale: str) -> tuple[str, str]:
    """Parse the *element* to retrieve the word and its definitions."""
    revision = element[3]
    if revision.tag == "{http://www.mediawiki.org/xml/export-0.11/}restrictions":
        # When a word is "restricted", then the revision comes just after
        revision = element[4]
    elif not len(revision):
        # This is a "redirect" page, not interesting.
        return "", ""

    # The Wikicode can be at different indexes, but not ones lower than 5
    for info in revision[5:]:
        if info.tag == "{http://www.mediawiki.org/xml/export-0.11/}text":
            code = info.text or ""
            break
    else:
        # No Wikicode, maybe an unfinished page.
        return "", ""

    # no interesting head section, a foreign word?
    if all(section not in code for section in head_sections[locale]):
        return "", ""

    word = element[0].text or ""  # title
    return word, code


def process(file: Path, locale: str) -> dict[str, str]:
    """Process the big XML file and retain only information we are interested in."""
    words: dict[str, str] = defaultdict(str)

    print(f">>> Processing {file} ...", flush=True)
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

    print(f">>> Saved {len(words):,} words into {raw_data}", flush=True)


def get_latest_xml_file(output_dir: Path) -> Path | None:
    """Get the name of the last pages-*.xml file."""
    files = list(output_dir.glob("pages-*.xml"))
    return sorted(files)[-1] if files else None


def main(locale: str) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    file = get_latest_xml_file(output_dir)
    if not file:
        print(">>> No dump found. Run with --download first ... ", flush=True)
        return 1

    date = file.stem.split("-")[1]
    if not (output_dir / f"data_wikicode-{date}.json").is_file():
        words = process(file, locale)
        save(date, words, output_dir)
    print(">>> Parse done!", flush=True)
    return 0
