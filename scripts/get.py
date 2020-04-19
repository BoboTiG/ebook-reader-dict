"""Retrieve and purge Wiktionary data."""
import bz2
import json
import re
import sys
from functools import partial
from pathlib import Path
from typing import List, Tuple

import requests

import wikitextparser as wtp
import xmltodict
from mediawiki_dump.tokenizer import clean as sanitize

from .lang import language
from .utils import is_ignored
from . import annotations as T
from . import constants as C


def clean(content: str) -> str:
    """Clean-up wikicode."""
    text: str = sanitize(content)
    text = text.replace("''", "")
    text = re.sub(C.EXTRA_SPACES, " ", text)
    text = re.sub(C.EXTRA_SPACES_DOT, ".", text)
    return text


def decompress(file: Path) -> Path:
    """Decompress a BZ2 file."""
    output = file.with_suffix(file.suffix.replace(".bz2", ""))
    if output.is_file():
        return output

    print(f">>> Decompressing {file.name} ", end="", flush=True)

    comp = bz2.BZ2Decompressor()
    with file.open("rb") as fi, output.open(mode="wb") as fo:
        for data in iter(partial(fi.read, 1024 * 1024), b""):
            fo.write(comp.decompress(data))
            print(".", end="", flush=True)
    print("", flush=True)

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

    print(f">>> Fetching {output.name} ", end="", flush=True)
    url = f"{C.BASE_URL}/{date}/{C.WIKI}-{date}-pages-meta-current.xml.bz2"

    with output.open(mode="wb") as fh, requests.get(url, stream=True) as req:
        req.raise_for_status()
        for chunk in req.iter_content(chunk_size=1024 * 1024):
            if chunk:
                fh.write(chunk)
                print(".", end="", flush=True)
        print("", flush=True)

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


def load() -> Tuple[T.Words, T.WordList, bool]:
    """Load the big JSON file containing all words and their details,
    also load the words list to catch obsoletes words and updates.
    """
    cache: T.Words = {}
    wordlist: T.WordList = {}
    first_pass = True

    if C.SNAPSHOT_DATA.is_file():
        # Load the whole list
        with C.SNAPSHOT_DATA.open(encoding="utf-8") as fh:
            cache = json.load(fh)

        # Load the word|revision list to detect changes
        if C.SNAPSHOT_LIST.is_file():
            words = C.SNAPSHOT_LIST.read_text(encoding="utf-8")
            for line in words.splitlines():
                word, rev = line.split("|")
                wordlist[word] = rev.rstrip("\n")
            del words

        first_pass = False
        print(f">>> Loaded {len(cache):,} words from {C.SNAPSHOT_DATA}", flush=True)

    return cache, wordlist, first_pass


def process(
    file: Path, cache: T.Words, wordlist: T.WordList, first_pass: bool
) -> T.Words:
    """Process the big XML file and retain only information we are interested in.
    Results are stored into the global *RESULT* dict, see handle_page() for details.
    """

    def handle_page(
        _: T.Attribs,
        page: T.Item,
        cache: T.Words = cache,
        wordlist: T.WordList = wordlist,
        first_pass: bool = first_pass,
    ) -> bool:
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

        rev = page["revision"]["id"]

        # Handle word with no changes
        if not first_pass:
            word_rev = wordlist.pop(word, None)
            if word_rev and word_rev == rev:
                # Same revision, skip early
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

        cache[word] = (rev, pronunciation, genre, definitions)
        if not first_pass:
            action = "Updated" if word_rev else "Added"
            print(f" ++ {action} {word!r}", flush=True)

        return True

    with file.open("rb") as fh:
        xmltodict.parse(fh, encoding="utf-8", item_depth=2, item_callback=handle_page)

    # Remove obsolete words between 2 snapshots
    for word in sorted(wordlist.keys()):
        cache.pop(word, None)
        print(f" -- Removed {word!r}", flush=True)

    return cache


def save(snapshot: str, cache: T.Words) -> None:
    """Persist data."""
    # This file is needed by convert.py
    with C.SNAPSHOT_DATA.open(mode="w", encoding="utf-8") as fh:
        json.dump(cache, fh, sort_keys=True)

    C.SNAPSHOT_COUNT.write_text(str(len(cache)))
    C.SNAPSHOT_FILE.write_text(snapshot)

    # Save the list of "word|revision" for later runs
    with C.SNAPSHOT_LIST.open("w", encoding="utf-8") as fh:
        for word, (rev, *_) in sorted(cache.items()):
            fh.write(word)
            fh.write("|")
            fh.write(rev)
            fh.write("\n")

    print(f">>> Saved {len(cache):,} words into {C.SNAPSHOT_DATA}", flush=True)


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

    # Load all data
    cache, wordlist, first_pass = load()

    # Fetch and uncompress the snapshot file
    file = fetch_pages(snapshot)
    file = decompress(file)

    # Process the big XML to retain only primary information
    cache = process(file, cache, wordlist, first_pass)

    # Save data for next runs
    save(snapshot, cache)

    print(">>> Retrieval done!", flush=True)
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
