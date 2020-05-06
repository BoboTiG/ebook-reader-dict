"""Retrieve and purge Wiktionary data."""
import bz2
import json
import os
import re
import sys
import xml.sax
import xml.sax.handler
from functools import partial
from itertools import chain
from pathlib import Path
from typing import (
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Pattern,
)

import requests
from requests import codes
from requests.exceptions import HTTPError

import wikitextparser as wtp

from .lang import patterns
from .utils import clean
from . import annotations as T
from . import constants as C


def parse_word(code: str, force: bool = False) -> T.Word:
    """Parse *code* Wikicode to find word details.
    *force* can be set to True to force the pronunciation and genre guessing.
    It is disabled by default t spee-up the overall process, but enabled when
    called from get_and_parse_word().
    """
    sections = find_sections(code)
    pronunciation = ""
    genre = ""
    definitions = find_definitions(sections)

    if definitions or force:
        pronunciation = find_pronunciation(code)
        genre = find_genre(code)

    return pronunciation, genre, definitions


class PageHandler(xml.sax.handler.ContentHandler):
    """XML content handler passed to the SAX parser."""

    __slots__ = ("_current_tag", "_is_page", "code", "word", "words")

    def __init__(self) -> None:
        # Will contain the Wikicode
        self.code = ""
        # Will contain the word
        self.word = ""
        # Will contain all words and their data
        self.words: T.Words = {}

        self._current_tag = ""
        self._is_page = False

    def reset(self) -> None:
        """Reset attributes."""
        self.code = ""
        self.word = ""
        self._is_page = False

    def startElement(self, tag: str, attributes: Dict[str, str]) -> None:
        """Signals the start of an element."""
        if tag == "page":
            self._is_page = True
        elif tag in ("title", "text"):
            self._current_tag = tag

    def endElement(self, tag: str) -> None:
        """Signals the end of an element."""
        if self._current_tag == "text":
            if self.word:
                # The parsing is complete!
                self.process()
            self.reset()
        self._current_tag = ""

    def process(self, parse_word: Callable[[str], T.Word] = parse_word) -> None:
        """Process a word: find its metadata and definitions.
        On success, the *.words* attribute is populated with the data.
        """
        try:
            pronunciation, genre, definitions = parse_word(self.code)
        except Exception:
            # Do not break the whole thing, just report the issue
            # and finger crossed for someone to have a look :)
            print(f"ERROR with {self.word!r}")
        else:
            if definitions:
                self.words[self.word] = pronunciation, genre, definitions

    def characters(self, content: str) -> None:
        """Receive notification of character data."""
        if not self._is_page:
            # We are not traiting a <page> element, not interesting
            pass
        elif self._current_tag == "title":
            if ":" in content or len(content) < 3 or content.isnumeric():
                # Skip words with colons, small words and numbers
                self.reset()
            else:
                self.word = content
        elif self._current_tag == "text":
            # Aggregate all the Wikicode
            self.code += content


def decompress(file: Path) -> Path:
    """Decompress a BZ2 file."""
    output = file.with_suffix(file.suffix.replace(".bz2", ""))
    if output.is_file():
        return output

    msg = f">>> Uncompressing into {output.name}:"
    print(msg, end="", flush=True)

    comp = bz2.BZ2Decompressor()
    with file.open("rb") as fi, output.open(mode="wb") as fo:
        total = 0
        for data in iter(partial(fi.read, 1024 * 1024), b""):
            uncompressed = comp.decompress(data)
            fo.write(uncompressed)
            total += len(uncompressed)
            print(f"\r{msg} {total:,} bytes", end="", flush=True)
    print(f"\r{msg} OK [{output.stat().st_size:,} bytes]", flush=True)

    return output


def fetch_snapshots() -> List[str]:
    """Fetch available snapshots.
    Return a list of sorted dates.
    """
    with requests.get(C.BASE_URL) as req:
        req.raise_for_status()
        return sorted(re.findall(r'href="(\d+)/"', req.text))


def fetch_pages(date: str) -> Path:
    """Download all pages, current versions only.
    Return the path of the XML file BZ2 compressed.
    """
    output_xml = C.SNAPSHOT / f"pages-{date}.xml"
    output = C.SNAPSHOT / f"pages-{date}.xml.bz2"
    if output.is_file() or output_xml.is_file():
        return output

    msg = f">>> Fetching {C.WIKI}-{date}-pages-meta-current.xml.bz2:"
    print(msg, end="", flush=True)

    url = f"{C.BASE_URL}/{date}/{C.WIKI}-{date}-pages-meta-current.xml.bz2"
    with output.open(mode="wb") as fh, requests.get(url, stream=True) as req:
        req.raise_for_status()
        total = 0
        for chunk in req.iter_content(chunk_size=1024 * 1024):
            if chunk:
                fh.write(chunk)
                total += len(chunk)
                print(f"\r{msg} {total:,} bytes", end="", flush=True)
    print(f"\r{msg} OK [{output.stat().st_size:,} bytes]", flush=True)

    return output


def find_definitions(sections: T.Sections) -> List[str]:
    """Find all definitions, without eventual subtext."""
    definitions = list(
        chain.from_iterable(find_section_definitions(section) for section in sections)
    )
    if not definitions:
        return []
    # Remove duplicates
    return sorted(set(definitions), key=definitions.index)


def find_section_definitions(
    section: wtp.Section,
    pattern: Pattern[str] = re.compile(r"^(<i>\([\w ]+\)</i>\.? ?\??…?)*$"),
    clean: Callable[[str], str] = clean,
) -> Generator[str, None, None]:
    """Find definitions from the given *section*, without eventual subtext.

    The *pattern* will be used to filter out:
        - empty definitions like "(Maçonnerie) (Reliquat)"
        - almost-empty definitions, like "(Poésie) …"
        (or definitions using a sublist, it is not yet handled)
    """
    lists = section.get_lists()
    if lists:
        definitions = (clean(d.strip()) for d in lists[0].items)
        yield from (d for d in definitions if not pattern.match(d))


def find_genre(code: str, pattern: Pattern[str] = C.GENRE) -> str:
    """Find the genre."""
    match = pattern.search(code)
    return match.group(1) if match else ""


def find_pronunciation(code: str, pattern: Pattern[str] = C.PRONUNCIATION) -> str:
    """Find the pronunciation."""
    match = pattern.search(code)
    return match.group(1) if match else ""


def find_sections(code: str) -> Generator[str, None, None]:
    """Find the correct section(s) holding the current locale definition(s)."""
    sections = wtp.parse(code).get_sections(include_subsections=False)
    yield from (
        section
        for section in sections
        if section.title and section.title.lstrip().startswith(patterns[C.LOCALE])
    )


def get_and_parse_word(word: str) -> None:
    """Get a *word* wikicode and parse it."""
    with requests.get(C.WORD_URL.format(word)) as req:
        code = req.text

    pronunciation, genre, defs = parse_word(code, force=True)

    print(word, f"\\{pronunciation}\\", f"({genre}.)", "\n")
    for i, definition in enumerate(defs, start=1):
        # Strip HTML tags
        print(f"{i}.".rjust(4), re.sub(r"<[^>]+/?>", "", definition))


def guess_snapshot() -> str:
    """Guess the next snapshot to process.
    Return an empty string if there is nothing to do,
    e.g. when the current snapshot is up-to-date.
    """
    # Check if we want to force the use of a specific snapshot
    from_env = os.getenv("WIKI_DUMP", "")
    if from_env:
        print(
            f">>> WIKI_DUMP is set to {from_env}, regenerating dictionaries ...",
            flush=True,
        )
        return from_env

    # Get the current snapshot, if any
    try:
        current = C.SNAPSHOT_FILE.read_text().strip()
    except FileNotFoundError:
        current = ""

    # Get the latest available snapshot
    snapshot = max(fetch_snapshots())
    return snapshot if less_than(current, snapshot) else ""


def less_than(old: str, new: str) -> bool:
    """Compare 2 snapshot dates."""
    return len(old) != 8 or old < new


def process(file: Path) -> T.Words:
    """Process the big XML file and retain only information we are interested in."""

    print(f">>> Processing {file} ...", flush=True)

    parser = xml.sax.make_parser()

    # All element names, prefixes, attribute names, Namespace URIs, and local names
    # are interned using the built-in intern function.
    parser.setFeature(xml.sax.handler.feature_string_interning, 1)  # type: ignore

    handler = PageHandler()
    parser.setContentHandler(handler)  # type: ignore
    parser.parse(str(file))  # type: ignore

    return handler.words


def save(snapshot: str, words: T.Words) -> None:
    """Persist data."""
    # This file is needed by convert.py
    with C.SNAPSHOT_DATA.open(mode="w", encoding="utf-8") as fh:
        json.dump(words, fh, sort_keys=True)

    C.SNAPSHOT_COUNT.write_text(str(len(words)))
    C.SNAPSHOT_FILE.write_text(snapshot)

    # Save the word list for later runs
    with C.SNAPSHOT_LIST.open("w", encoding="utf-8") as fh:
        for word in sorted(words.keys()):
            fh.write(word)
            fh.write("\n")

    print(f">>> Saved {len(words):,} words into {C.SNAPSHOT_DATA}", flush=True)


def main(word: Optional[str] = "") -> int:
    """Extry point."""

    # Fetch one word and parse it, used for testing mainly
    if word:
        get_and_parse_word(word)
        return 0

    # Ensure the folder exists
    C.SNAPSHOT.mkdir(exist_ok=True, parents=True)

    # Get the snapshot to handle
    snapshot = guess_snapshot()
    if not snapshot:
        print(">>> Snapshot up-to-date!", flush=True)
        # Return 1 to break the script and so the GitHub workflow
        return 1

    # Fetch and uncompress the snapshot file
    try:
        file = fetch_pages(snapshot)
    except HTTPError as exc:
        print("", flush=True)
        if exc.response.status_code != codes.NOT_FOUND:
            raise
        print(">>> Wiktionary dump is ongoing ... ", flush=True)
        # Return 1 to break the script and so the GitHub workflow
        return 1

    file = decompress(file)

    # Process the XML to retain only primary information
    words = process(file)

    # Save data for next runs
    save(snapshot, words)

    print(">>> Retrieval done!", flush=True)
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
