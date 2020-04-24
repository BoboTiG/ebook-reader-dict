"""Retrieve and purge Wiktionary data."""
import bz2
import json
import re
import sys
from functools import partial
from pathlib import Path
from typing import List

import requests
from requests import codes
from requests.exceptions import HTTPError

import wikitextparser as wtp
import xmltodict

from .lang import language
from .utils import is_ignored, clean
from . import annotations as T
from . import constants as C


def decompress(file: Path) -> Path:
    """Decompress a BZ2 file."""
    output = file.with_suffix(file.suffix.replace(".bz2", ""))
    if output.is_file():
        return output

    msg = f">>> Uncompressing into {output.name}:"
    print(msg, end="", flush=True)

    total = 0
    comp = bz2.BZ2Decompressor()
    with file.open("rb") as fi, output.open(mode="wb") as fo:
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


def find_definitions(section: wtp.Section) -> List[str]:
    """Find all definitions, without eventual subtext."""
    try:
        return [clean(d) for d in section.get_lists()[0].items]
    except IndexError:
        # Page not finished or incomplete?
        return []


def find_genre(content: str) -> str:
    """Find the genre."""
    match = re.search(C.GENRE, content)
    return match.group(1) if match else ""


def find_pronunciation(content: str) -> str:
    """Find the pronunciation."""
    match = re.search(C.PRONUNCIATION, content)
    return match.group(1) if match else ""


def find_sections(content: str) -> List[str]:
    """Find the correct section(s) holding the current locale definition(s)."""
    sections = wtp.parse(content).get_sections(include_subsections=False)
    return [s for s in sections if s.title.strip().startswith(language[C.LOCALE])]


def guess_snapshot() -> str:
    """Guess the next snapshot to process.
    Return an empty string if there is nothing to do,
    e.g. when the current snapshot is up-to-date.
    """
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


def load() -> T.WordList:
    """Load the words list to catch obsoletes words and updates.
    """
    wordlist: T.WordList = {}

    # Load the word|revision list to detect changes
    if C.SNAPSHOT_LIST.is_file():
        content = C.SNAPSHOT_LIST.read_text(encoding="utf-8")
        for line in content.splitlines():
            word, rev = line.split("|")
            wordlist[word] = rev.rstrip("\n")
        print(
            f">>> Loaded {len(wordlist):,} revisions from {C.SNAPSHOT_LIST}",
            flush=True,
        )

    return wordlist


def process(file: Path, wordlist: T.WordList) -> T.Words:
    """Process the big XML file and retain only information we are interested in.
    Results are stored into the global *RESULT* dict, see handle_page() for details.
    """
    words: T.Words = {}
    first_pass = not bool(wordlist)

    print(f">>> Processing {file} ...", flush=True)

    def handle_page(_: T.Attribs, page: T.Item) -> bool:
        """
        Callback passed to xmltodict.parse().
        The function must return True or the parser will raise ParsingInterrupted
        (https://github.com/martinblech/xmltodict/blob/d6a8377/xmltodict.py#L227-L230).

        Details are stored into the *RESULT* dict where the word the key.
        Each entry in the dict is a tuple(
            0: the revision number
            1: its pronunciation (defaults to empty string)
            2: its genre (defaults to empty string)
            3: list of definitions
        )
        """

        try:
            word = page["title"]
        except KeyError:
            return True

        # Skip uninteresting pages such as:
        #   - Discussion utilisateur:...
        #   - MediaWiki:...
        #   - Utilisateur:...
        if ":" in word:
            return True

        if is_ignored(word):
            return True

        # The entire content of the global definition
        sections = find_sections(page["revision"]["text"]["#text"])
        if not sections:
            # Maybe an unfinished tanslation, skip it
            return True

        pronunciation = ""
        genre = ""
        definitions = []

        for section in sections:
            # Find the pronunciation
            if not pronunciation:
                pronunciation = find_pronunciation(str(section))

            # Find the genre, if any
            if not genre:
                genre = find_genre(str(section))

            # All definitions, without eventual subtext
            definitions.extend(find_definitions(section))

        if not definitions:
            print(f" !! No definition found for {word!r}", flush=True)
            return True

        rev = page["revision"]["id"]
        word_rev = wordlist.pop(word, None)

        # Log the appropriate action to ease tracking changes
        action = ""
        if word_rev and word_rev != rev:
            action = "Updated"
        elif not (word_rev or first_pass):
            action = "Added"
        if action:
            print(f" ++ {action} {word!r}", flush=True)

        words[word] = (rev, pronunciation, genre, definitions)
        return True

    with file.open("rb") as fh:
        xmltodict.parse(fh, encoding="utf-8", item_depth=2, item_callback=handle_page)

    # Remove obsolete words between 2 snapshots
    for word in sorted(wordlist.keys()):
        words.pop(word, None)
        print(f" -- Removed {word!r}", flush=True)

    return words


def save(snapshot: str, words: T.Words) -> None:
    """Persist data."""
    # This file is needed by convert.py
    with C.SNAPSHOT_DATA.open(mode="w", encoding="utf-8") as fh:
        json.dump(words, fh, sort_keys=True)

    C.SNAPSHOT_COUNT.write_text(str(len(words)))
    C.SNAPSHOT_FILE.write_text(snapshot)

    # Save the list of "word|revision" for later runs
    with C.SNAPSHOT_LIST.open("w", encoding="utf-8") as fh:
        for word, (rev, *_) in sorted(words.items()):
            fh.write(word)
            fh.write("|")
            fh.write(rev)
            fh.write("\n")

    print(f">>> Saved {len(words):,} words into {C.SNAPSHOT_DATA}", flush=True)


def main() -> int:
    """Extry point."""

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

    # Load all data
    wordlist = load()

    # Process the big XML to retain only primary information
    words = process(file, wordlist)

    # Save data for next runs
    save(snapshot, words)

    print(">>> Retrieval done!", flush=True)
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
