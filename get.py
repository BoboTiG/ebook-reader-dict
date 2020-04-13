"""Retrieve and purge Wiktionary data."""
import bz2
import os
import re
import sys
from functools import partial
from pathlib import Path
from typing import List

import requests
import wikitextparser as wtp
import xmltodict
from mediawiki_dump.tokenizer import clean

# Wiktionary stuff
LOCALE = os.getenv("WIKI_LOCALE", "fr")
WIKI = f"{LOCALE}wiktionary"
BASE_URL = f"https://dumps.wikimedia.org/{WIKI}"

# Local stuff
SNAPSHOT = Path(LOCALE)
SNAPSHOT_FILE = SNAPSHOT / "SNAPSHOT"

# Regexps
PRONUNCIATION = re.compile(r"{{pron\|(\S+)\|%s}}" % LOCALE)
GENRE = re.compile(r"{{([fmsingp]+)}}")


def decompress(file: Path) -> Path:
    """Decompress a BZ2 file."""
    output = file.with_suffix(file.suffix.replace(".bz2", ""))

    if output.is_file():
        return output

    comp = bz2.BZ2Decompressor()
    with file.open("rb") as fi, output.open(mode="wb") as fo:
        for data in iter(partial(fi.read, 1024), b""):
            fo.write(comp.decompress(data))


def less_than(old: str, new: str) -> bool:
    """Compare 2 snapshot dates."""
    return len(old) != 8 or old < new


def get_dates() -> List[str]:
    """Fetch available snapshots.
    Return a list of sorted dates.
    """
    content = requests.get(BASE_URL).text
    return sorted(re.findall(r'href="(\d+)/"', content))


def get_pages(date: str) -> Path:
    """Download all pages, current versions only.
    Return the path of the XML file BZ2 compressed.
    """
    url = f"{BASE_URL}/{date}/{WIKI}-{date}-pages-meta-current.xml.bz2"
    output = SNAPSHOT / f"pages-{date}.xml.bz2"

    if output.is_file():
        return output

    with output.open(mode="wb") as fh:
        fh.write(requests.get(url).content)
    return output


from time import sleep

def purge(file: Path) -> Path:
    """
    """

    c = 0

    def handle_page(_, page):
        """
        The function must return True or the parser will raise ParsingInterrupted.

        We need to keep:
            - the word itself
            - revision number
            - its pronunciation
            - its genre (it depends of the LOCALE and the type of the word, defaults to empty string)
            - list of definitions
        """
        try:
            # This is also the word
            title = page["title"]
        except KeyError:
            return True

        # Skip uninteresting pages
        #   - Discussion utilisateur:...
        #   - MediaWiki:...
        #   - Utilisateur:...
        if ":" in title:
            return True

        # The revision
        rev = page["revision"]["id"]

        # The entire content of the global definition
        sections = wtp.parse(page["revision"]["text"]["#text"]).get_sections(include_subsections=False)
        for number in (3, 2):
            # 3 for regular words
            # 2 for verbs
            try:
                section = sections[number]
                break
            except IndexError:
                pass
        else:
            # Most likely a redirection
            return True

        # Find the pronunciation
        try:
            pronunciation = re.search(PRONUNCIATION, str(section)).group(1)
        except AttributeError:
            # Maybe an unfinished tanslation, skip it
            return True

        # Find the genre, if any
        try:
            genre = re.search(GENRE, str(section)).group(1)
        except AttributeError:
            # No genre
            genre = ""

        # All definitions, without eventual subtext
        definitions = [clean(d) for d in section.get_lists()[0].items]

        yield title, rev, pronunciation, genre, definitions

        return True

    with file.open("rb") as fh:
        xmltodict.parse(fh, encoding="utf-8", item_depth=2, item_callback=handle_page)

    print(c)


def main() -> int:
    """Extry point."""
    # Get the current snapshot
    latest_snapshot = "20200401"
    """
    try:
        current_snapshot = SNAPSHOT_FILE.read_text().strip()
    except FileNotFoundError:
        current_snapshot = ""

    # Get the latest available snapshot
    latest_snapshot = max(get_dates())
    if not less_than(current_snapshot, latest_snapshot):
        return 0
    """

    # Fetch and uncompress
    file = get_pages(latest_snapshot)
    file = decompress(file)

    # Purge
    purge(file)

    # Save the new snapshot
    SNAPSHOT_FILE.write_text(latest_snapshot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
