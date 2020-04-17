"""Retrieve and purge Wiktionary data."""
import bz2
import json
import os
import re
import sys
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests

import wikitextparser as wtp
import xmltodict
from mediawiki_dump.tokenizer import clean as sanitize

# Wiktionary stuff
LOCALE = os.getenv("WIKI_LOCALE", "fr")
WIKI = f"{LOCALE}wiktionary"
BASE_URL = f"https://dumps.wikimedia.org/{WIKI}"

# Local stuff
SNAPSHOT = Path(os.getenv("CWD", "")) / "data" / LOCALE
SNAPSHOT_DATA = SNAPSHOT / "data.json"
SNAPSHOT_COUNT = SNAPSHOT / "words.count"
SNAPSHOT_FILE = SNAPSHOT / "words.snapshot"
SNAPSHOT_LIST = SNAPSHOT / "words.list"
SNAPSHOT.mkdir(exist_ok=True, parents=True)

# Regexps
PRONUNCIATION = re.compile(r"{{pron\|([^}]+)\|(lang=)?%s}}" % LOCALE, flags=re.UNICODE)
GENRE = re.compile(r"{{([fmsingp]+)}}")
EXTRA_SPACES = re.compile(r"\s{2,}")
EXTRA_SPACES_DOT = re.compile(r"\s{1,}\.")

# Marker for sections of the current locale
LANG = {
    "fr": (
        "{{S|adjectif|fr}",
        "{{S|adjectif|fr|",
        "{{S|adverbe|fr}",
        "{{S|adverbe|fr|",
        "{{S|article défini|fr}",
        "{{S|article défini|fr|",
        "{{S|lettre|fr}",
        "{{S|lettre|fr|",
        "{{S|nom|fr}",
        "{{S|nom|fr|",
        "{{S|nom propre|fr}",
        "{{S|nom propre|fr|",
        "{{S|numéral|conv}",
        "{{S|préposition|fr}",
        "{{S|préposition|fr|",
        "{{S|pronom indéfini|fr}",
        "{{S|pronom indéfini|fr|",
        "{{S|pronom personnel|fr}",
        "{{S|pronom personnel|fr|",
        "{{S|symbole|conv}",
        "{{S|verbe|fr}",
        "{{S|verbe|fr|",
    ),
}

# Types
Attribs = List[Tuple[str, Any]]
Item = Dict[str, Any]
Word = Tuple[str, str, str, List[str]]
Words = Dict[str, Word]

# Internal use
RESULT: Words = {}
WORDLIST: Dict[str, str] = {}
FIRST_PASS = True

if os.getenv("CI", "0") != "1" and SNAPSHOT_DATA.is_file():
    # Load the whole list
    with SNAPSHOT_DATA.open(encoding="utf-8") as fh:
        RESULT = json.load(fh)

    # Load the word|revision list to detect changes
    words = SNAPSHOT_LIST.read_text(encoding="utf-8")
    for line in words.splitlines():
        word, rev = line.split("|")
        WORDLIST[word] = rev.rstrip("\n")
    del words

    FIRST_PASS = False
    print(f">>> Loaded {len(RESULT):,} words from {SNAPSHOT_DATA}")


def clean(content: str) -> str:
    """Clean-up WikiText."""
    text: str = sanitize(content)
    text = text.replace("''", "")
    text = re.sub(EXTRA_SPACES, " ", text)
    text = re.sub(EXTRA_SPACES_DOT, ".", text)
    return text


def decompress(file: Path) -> Path:
    """Decompress a BZ2 file."""
    output = file.with_suffix(file.suffix.replace(".bz2", ""))
    if output.is_file():
        return output

    print(f">>> Decompressing {output.name} ... ", flush=True)
    comp = bz2.BZ2Decompressor()
    with file.open("rb") as fi, output.open(mode="wb") as fo:
        for data in iter(partial(fi.read, 1024), b""):
            fo.write(comp.decompress(data))

    return output


def fetch_snapshots() -> List[str]:
    """Fetch available snapshots.
    Return a list of sorted dates.
    """
    content = requests.get(BASE_URL).text
    return sorted(re.findall(r'href="(\d+)/"', content))


def fetch_pages(date: str) -> Path:
    """Download all pages, current versions only.
    Return the path of the XML file BZ2 compressed.
    """
    output = SNAPSHOT / f"pages-{date}.xml.bz2"
    if output.is_file():
        return output

    print(f">>> Fetching {output.name} ... ", flush=True)
    with output.open(mode="wb") as fh:
        url = f"{BASE_URL}/{date}/{WIKI}-{date}-pages-meta-current.xml.bz2"
        fh.write(requests.get(url).content)
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
    match = re.search(GENRE, content)
    return match.group(1) if match else ""


def find_pronunciation(content: str) -> str:
    """Find the pronunciation."""
    match = re.search(PRONUNCIATION, content)
    return match.group(1) if match else ""


def find_sections(content: str) -> List[str]:
    """Find the correct section(s) holding the current locale definition(s)."""
    sections = wtp.parse(content).get_sections(include_subsections=False)
    return [s for s in sections if s.title.strip().startswith(LANG[LOCALE])]


def guess_snapshot() -> str:
    """Guess the next snapshot to process.
    Return an empty string if there is nothing to do,
    e.g. when the current snapshot is up-to-date.
    """
    # Get the current snapshot, if any
    try:
        current = SNAPSHOT_FILE.read_text().strip()
    except FileNotFoundError:
        current = ""

    # Get the latest available snapshot
    snapshot = max(fetch_snapshots())
    return snapshot if less_than(current, snapshot) else ""


def handle_page(
    _: Attribs, page: Item, cache: Words = RESULT, wordlist: Dict[str, str] = WORDLIST
) -> bool:
    """
    Callback passed to xmltodict.parse() in process().
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
    if not FIRST_PASS:
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
    if not FIRST_PASS:
        action = "Updated" if word_rev else "Added"
        print(f" ++ {action} {word!r}", flush=True)

    return True


def is_ignored(word: str) -> bool:
    """Helper to filter out words from the final dictionary."""
    # Filter out "small" words and numbers
    return len(word) < 3 or word.isnumeric()


def less_than(old: str, new: str) -> bool:
    """Compare 2 snapshot dates."""
    return len(old) != 8 or old < new


def process(file: Path) -> None:
    """Process the big XML file and retain only information we are interested in.
    Results are stored into the global *RESULT* dict, see handle_page() for details.
    """
    with file.open("rb") as fh:
        xmltodict.parse(fh, encoding="utf-8", item_depth=2, item_callback=handle_page)

    # Remove obsolete words between 2 snapshots
    for word in sorted(WORDLIST):
        RESULT.pop(word, None)
        print(f" -- Removed {word}", flush=True)


def save(snapshot: str) -> None:
    """Persist data."""
    # This file is needed by convert.py
    with SNAPSHOT_DATA.open(mode="w", encoding="utf-8") as fh:
        json.dump(RESULT, fh, sort_keys=True)

    SNAPSHOT_COUNT.write_text(str(len(RESULT)))
    SNAPSHOT_FILE.write_text(snapshot)

    # Save the list of "word|revision" for later runs
    with SNAPSHOT_LIST.open("w", encoding="utf-8") as fh:
        for word, (rev, *_) in RESULT.items():
            fh.write(word)
            fh.write("|")
            fh.write(rev)
            fh.write("\n")

    print(f">>> Saved {len(RESULT):,} words into {SNAPSHOT_DATA}", flush=True)


def main() -> int:
    """Extry point."""

    # Get the snapshot to handle
    snapshot = guess_snapshot()
    if not snapshot:
        print(">>> Snapshot up-to-date!", flush=True)
        return 0

    # Fetch and uncompress the snapshot file
    file = fetch_pages(snapshot)
    file = decompress(file)

    # Process the big XML to retain only primary information
    process(file)

    # Save data for next runs
    save(snapshot)

    return 0


if __name__ == "__main__":
    sys.exit(main())
