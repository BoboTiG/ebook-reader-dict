"""Retrieve and purge Wiktionary data."""
import bz2
import json
import os
import re
import sys
from functools import partial
from pathlib import Path
from typing import List

import requests
import wikitextparser as wtp
import xmltodict
from mediawiki_dump.tokenizer import clean as sanitize

DEBUG = False

# Wiktionary stuff
LOCALE = os.getenv("WIKI_LOCALE", "fr")
WIKI = f"{LOCALE}wiktionary"
BASE_URL = f"https://dumps.wikimedia.org/{WIKI}"

# Local stuff
SNAPSHOT = Path("data") / LOCALE
SNAPSHOT_FILE = SNAPSHOT / "SNAPSHOT"
SNAPSHOT_DATA = SNAPSHOT / "data.json"

# Regexps
PRONUNCIATION = re.compile(r"{{pron\|([^}]+)\|(lang=)?%s}}" % LOCALE, flags=re.UNICODE)
GENRE = re.compile(r"{{([fmsingp]+)}}")
EXTRA_SPACES = re.compile(r"\s{2,}")

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

# The final dict
RESULT = {}
if SNAPSHOT_DATA.is_file():
    with SNAPSHOT_DATA.open(encoding="utf-8") as fh:
        RESULT = json.load(fh)
    print(f">>> Loaded {len(RESULT):,} words from {SNAPSHOT_DATA}")


def clean(content: str) -> str:
    """Clean-up WikiText."""
    text = sanitize(content)
    text = text.replace("''", "")
    text = re.sub(EXTRA_SPACES, " ", text)
    return text


def decompress(file: Path) -> Path:
    """Decompress a BZ2 file."""
    output = file.with_suffix(file.suffix.replace(".bz2", ""))

    if output.is_file():
        return output

    comp = bz2.BZ2Decompressor()
    with file.open("rb") as fi, output.open(mode="wb") as fo:
        for data in iter(partial(fi.read, 1024), b""):
            fo.write(comp.decompress(data))


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
    url = f"{BASE_URL}/{date}/{WIKI}-{date}-pages-meta-current.xml.bz2"
    output = SNAPSHOT / f"pages-{date}.xml.bz2"

    if output.is_file():
        return output

    with output.open(mode="wb") as fh:
        fh.write(requests.get(url).content)
    return output


def find_definitions(section: str) -> List[str]:
    """Find all definitions, without eventual subtext."""
    try:
        return [clean(d) for d in section.get_lists()[0].items]
    except IndexError:
        # Page not finished or incomplete?
        return []


def find_genre(content: str) -> str:
    """Find the genre."""
    try:
        return re.search(GENRE, content).group(1)
    except AttributeError:
        # No genre, most likely a verb
        return ""


def find_pronunciation(content: str) -> str:
    """Find the pronunciation."""
    try:
        return re.search(PRONUNCIATION, content).group(1)
    except AttributeError:
        # Maybe an unfinished tanslation
        return ""


def find_sections(content: str) -> List[str]:
    """Find the correct section(s) holding the current locale definition(s)."""
    sections = wtp.parse(content).get_sections(include_subsections=False)

    if DEBUG:
        print([s.title.strip() for s in sections])
    return [s for s in sections if s.title.strip().startswith(LANG[LOCALE])]


def handle_page(_, page, cache=RESULT):
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
        word = page["title"]
    except KeyError:
        return True

    # Skip uninteresting pages such as:
    #   - Discussion utilisateur:...
    #   - MediaWiki:...
    #   - Utilisateur:...
    if ":" in word:
        return True

    rev = page["revision"]["id"]
    if not rev:
        # Should never be there!
        return True

    res = cache.get(word)
    if res and res[0] == rev:
        # Same revision, skip early
        return True

    # The entire content of the global definition
    sections = find_sections(page["revision"]["text"]["#text"])
    if not sections:
        # Maybe an unfinished tanslation, skip it
        # print(f" -- Skipped {word!r}", flush=True)
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

    if not pronunciation:
        # print(f" .. No pronunciation found for {word!r}", flush=True)
        pass

    if not definitions:
        print(f" !! No definition found for {word!r}", flush=True)
        return True

    cache[word] = (rev, pronunciation, genre, definitions)
    print(f">>> Added/Updated {word!r}", flush=True)

    return True


def less_than(old: str, new: str) -> bool:
    """Compare 2 snapshot dates."""
    return len(old) != 8 or old < new


def process(file: Path) -> Path:
    """Process the big XML file and retain only information we are interested in.
    Results are stored into the global *RESULT* dict.
    """
    with file.open("rb") as fh:
        xmltodict.parse(fh, encoding="utf-8", item_depth=2, item_callback=handle_page)


def save() -> None:
    """Persist data to a file."""
    with SNAPSHOT_DATA.open(mode="w", encoding="utf-8") as fh:
        json.dump(RESULT, fh, sort_keys=True)
    print(f">>> Saved {len(RESULT):,} words into {SNAPSHOT_DATA}")


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
    SNAPSHOT.mdkir(exists_ok=True)
    latest_snapshot = max(fetch_snapshots())
    if not less_than(current_snapshot, latest_snapshot):
        return 0
    """

    # Fetch and uncompress
    file = fetch_pages(latest_snapshot)
    file = decompress(file)

    # Purge
    process(file)

    # Save
    save()
    # SNAPSHOT_FILE.write_text(latest_snapshot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
