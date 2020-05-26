"""Retrieve and purge Wiktionary data."""
import bz2
import json
import os
import re
from collections import defaultdict
from functools import partial
from itertools import chain
from pathlib import Path
from typing import Callable, Generator, List, Optional, Pattern, Tuple, TYPE_CHECKING

import requests
from requests.exceptions import HTTPError
import wikitextparser as wtp
import wikitextparser._spans

from .constants import BASE_URL, DUMP_URL
from .lang import genre, pronunciation, patterns
from .stubs import Words
from .utils import clean

if TYPE_CHECKING:  # pragma: nocover
    from xml.etree.ElementTree import Element


# As stated in wikitextparser._spans.parse_pm_pf_tl():
#   If the byte_array passed to parse_to_spans contains n WikiLinks, then
#   this function will be called n + 1 times. One time for the whole byte_array
#   and n times for each of the n WikiLinks.
#
# We do not care about links, let's speed-up the all process by skipping the n times call.
# Doing that is a ~30% optimization.
wikitextparser._spans.WIKILINK_FINDITER = lambda *_: ()


Sections = Generator[str, None, None]


def callback_progress(text: str, total: int, last: bool) -> None:
    """Progression callback. USed when fetching the Wiktionary dump and when extracting it."""
    msg = f"{text}OK [{total:,} bytes]\n" if last else f"{text}{total:,} bytes"
    print(f"\r{msg}", end="", flush=True)


def callback_progress_ci(text: str, total: int, last: bool) -> None:
    """
    Progression callback. USed when fetching the Wiktionary dump and when extracting it.
    This version is targeting the CI, it prints less lines and it is easier to follow.
    """
    msg = f". OK [{total:,} bytes]\n" if last else "."
    print(msg, end="", flush=True)


def decompress(file: Path, callback: Callable[[str, int, bool], None]) -> Path:
    """Decompress a BZ2 file."""
    output = file.with_suffix(file.suffix.replace(".bz2", ""))
    if output.is_file():
        return output

    msg = f">>> Uncompressing into {output.name}: "
    print(msg, end="", flush=True)

    comp = bz2.BZ2Decompressor()
    with file.open("rb") as fi, output.open(mode="wb") as fo:
        total = 0
        for data in iter(partial(fi.read, 1024 * 1024), b""):
            uncompressed = comp.decompress(data)
            fo.write(uncompressed)
            total += len(uncompressed)
            callback(msg, total, False)

    callback(msg, output.stat().st_size, True)

    return output


def fetch_snapshots(locale: str) -> List[str]:
    """Fetch available snapshots.
    Return a list of sorted dates.
    """
    url = BASE_URL.format(locale)
    with requests.get(url) as req:
        req.raise_for_status()
        return sorted(re.findall(r'href="(\d+)/"', req.text))


def fetch_pages(
    date: str, locale: str, output_dir: Path, callback: Callable[[str, int, bool], None]
) -> Path:
    """Download all pages, current versions only.
    Return the path of the XML file BZ2 compressed.
    """
    output_xml = output_dir / f"pages-{date}.xml"
    output = output_dir / f"pages-{date}.xml.bz2"
    if output.is_file() or output_xml.is_file():
        return output

    url = DUMP_URL.format(locale, date)
    msg = f">>> Fetching {url}: "
    print(msg, end="", flush=True)

    with output.open(mode="wb") as fh, requests.get(url, stream=True) as req:
        req.raise_for_status()
        total = 0
        for chunk in req.iter_content(chunk_size=1024 * 1024):
            if chunk:
                fh.write(chunk)
                total += len(chunk)
                callback(msg, total, False)

    callback(msg, output.stat().st_size, True)

    return output


def find_definitions(word: str, sections: Sections, locale: str) -> List[str]:
    """Find all definitions, without eventual subtext."""
    definitions = list(
        chain.from_iterable(
            find_section_definitions(word, section, locale) for section in sections
        )
    )
    if not definitions:
        return []

    # Remove duplicates
    seen = set()
    return [d for d in definitions if not (d in seen or seen.add(d))]  # type: ignore


def find_section_definitions(
    word: str,
    section: wtp.Section,
    locale: str,
    pattern: Pattern[str] = re.compile(r"^((?:<i>)?\([\w ]+\)(?:</i>)?\.? ?\??…?,?)*$"),
) -> Generator[str, None, None]:
    """Find definitions from the given *section*, without eventual subtext.

    The *pattern* will be used to filter out:
        - empty definitions like "(Maçonnerie) (Reliquat)"
        - almost-empty definitions, like "(Poésie) …"
        (or definitions using a sublist, it is not yet handled)
    """
    lists = section.get_lists()
    if lists:
        definitions = (clean(word, d.strip(), locale) for d in lists[0].items)
        yield from (d for d in definitions if not pattern.match(d))


def find_genre(code: str, pattern: Pattern[str]) -> str:
    """Find the genre."""
    match = pattern.search(code)
    return match.group(1) if match else ""


def find_pronunciation(code: str, pattern: Pattern[str]) -> str:
    """Find the pronunciation."""
    match = pattern.search(code)
    return match.group(1) if match else ""


def find_all_sections(code: str) -> Generator[str, None, None]:
    """Find all sections holding definitions."""
    yield from wtp.parse(code).get_sections(include_subsections=False, level=3)


def find_sections(code: str, locale: str) -> Generator[str, None, None]:
    """Find the correct section(s) holding the current locale definition(s)."""
    yield from (
        section
        for section in find_all_sections(code)
        if section.title and section.title.lstrip().startswith(patterns[locale])  # type: ignore
    )


def find_titles(code: str) -> Generator[str, None, None]:
    """Find the correct section(s) holding the current locale definition(s)."""
    yield from (
        section.title.strip() for section in find_all_sections(code) if section.title  # type: ignore
    )


def get_and_parse_word(word: str, locale: str, raw: bool = False) -> None:
    """Get a *word* wikicode and parse it."""
    url = f"https://{locale}.wiktionary.org/w/index.php?title={word}&action=raw"
    with requests.get(url) as req:
        code = req.text

    pron, nature, defs = parse_word(word, code, locale, force=True)

    print(word, f"\\{pron}\\", f"({nature}.)", "\n")
    for i, definition in enumerate(defs, start=1):
        if not raw:
            # Strip HTML tags
            definition = re.sub(r"<[^>]+/?>", "", definition)
        print(f"{i}.".rjust(4), definition)


def guess_snapshots(locale: str) -> List[str]:
    """Retrieve available snapshots."""
    # Check if we want to force the use of a specific snapshot
    from_env = os.getenv("WIKI_DUMP", "")
    if from_env:  # pragma: nocover
        print(
            f">>> WIKI_DUMP is set to {from_env}, regenerating dictionaries ...",
            flush=True,
        )
        return [from_env]

    # Get all available snapshots
    return fetch_snapshots(locale)


def parse_word(
    word: str, code: str, locale: str, force: bool = False
) -> Tuple[str, str, List[str]]:
    """Parse *code* Wikicode to find word details.
    *force* can be set to True to force the pronunciation and genre guessing.
    It is disabled by default t spee-up the overall process, but enabled when
    called from get_and_parse_word().
    """
    sections = find_sections(code, locale)
    pron = ""
    nature = ""
    definitions = find_definitions(word, sections, locale)

    if definitions or force:
        pron = find_pronunciation(code, pronunciation[locale])
        nature = find_genre(code, genre[locale])

    return pron, nature, definitions


def process(file: Path, locale: str, debug: bool = False) -> Words:
    """Process the big XML file and retain only information we are interested in."""

    words: Words = {}

    if debug:
        sections = defaultdict(list)

    print(f">>> Processing {file} ...", flush=True)

    for total, element in enumerate(xml_iter_parse(str(file)), 1):
        word, code = xml_parse_element(element)
        if len(word) < 2 or ":" in word:
            continue

        if debug:
            for title in find_titles(code):
                sections[title].append(word)
            continue

        try:
            pronunciation, genre, definitions = parse_word(word, code, locale)
        except Exception:  # pragma: nocover
            print(f"ERROR with {word!r}")
        else:
            if definitions:
                words[word] = pronunciation, genre, definitions

    if debug:
        print(" === Sections ===", flush=True)
        for title, entries in sorted(sections.items()):
            print(f"  {title!r} ({len(entries):,})", flush=True)
            if len(entries) < 10:
                # Most likely errors/mispellings
                for entry in entries:
                    print(f"    - {entry!r}", flush=True)
        print(f"=== Total number of words: {total:,} ===", flush=True)

    return words


def save(snapshot: str, words: Words, output_dir: Path) -> None:
    """Persist data."""
    # This file is needed by convert.py
    raw_data = output_dir / "data.json"
    with raw_data.open(mode="w", encoding="utf-8") as fh:
        json.dump(words, fh, indent=4, sort_keys=True)

    (output_dir / "words.count").write_text(str(len(words)))
    (output_dir / "words.snapshot").write_text(snapshot)

    print(f">>> Saved {len(words):,} words into {raw_data}", flush=True)


def xml_iter_parse(file: str) -> Generator["Element", None, None]:
    """Efficient XML parsing for big files.
    Elements are yielded when they meet the "page" tag.
    """
    import xml.etree.ElementTree as etree

    doc = etree.iterparse(file, events=("start", "end"))
    _, root = next(doc)

    start_tag = None

    for event, element in doc:
        if (
            start_tag is None
            and event == "start"
            and element.tag == "{http://www.mediawiki.org/xml/export-0.10/}page"
        ):
            start_tag = element.tag
        elif start_tag is not None and event == "end" and element.tag == start_tag:
            yield element
            start_tag = None

            # Keep memory low
            root.clear()


def xml_parse_element(element: "Element") -> Tuple[str, str]:
    """Parse the *element* to retrieve the word and its definitions."""
    revision = element[3]
    if revision.tag == "{http://www.mediawiki.org/xml/export-0.10/}restrictions":
        # When a word is "restricted", then the revision comes just after
        revision = element[4]
    elif not revision:
        # This is a "redirect" page, not interesting.
        return "", ""

    # The Wikicode can be at different indexes, but not ones lower than 5
    for info in revision[5:]:
        if info.tag == "{http://www.mediawiki.org/xml/export-0.10/}text":
            code = info.text or ""
            break
    else:
        # No Wikicode, maybe an unfinished page.
        return "", ""

    word = element[0].text or ""  # title
    return word, code


def main(locale: str, word: Optional[str] = "", raw: bool = False) -> int:
    """Extry point."""

    # Fetch one word and parse it, used for testing mainly
    if word:
        get_and_parse_word(word, locale, raw=raw)
        return 0

    # Ensure the folder exists
    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    output_dir.mkdir(exist_ok=True, parents=True)

    # Get the snapshot to handle
    snapshots = guess_snapshots(locale)
    snapshot = snapshots[-1]

    # The output style is different if run from a workflow
    # Note: "CI"is automatically set in every GitHub workflow
    # https://help.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables#default-environment-variables
    cb = callback_progress_ci if "CI" in os.environ else callback_progress

    # Fetch and uncompress the snapshot file
    try:
        file = fetch_pages(snapshot, locale, output_dir, cb)
    except HTTPError:
        print("FAIL", flush=True)
        print(">>> Wiktionary dump is ongoing ... ", flush=True)
        print(">>> Will use the previous one.", flush=True)
        snapshot = snapshots[-2]
        file = fetch_pages(snapshot, locale, output_dir, cb)

    file = decompress(file, cb)

    # Process the XML to retain only primary information
    debug = "DEBUG" in os.environ
    words = process(file, locale, debug=debug)
    if not (words or debug):  # pragma: nocover
        raise ValueError("Empty dictionary?!")

    # Save data for the next step
    save(snapshot, words, output_dir)

    print(">>> Retrieval done!", flush=True)
    return 0
