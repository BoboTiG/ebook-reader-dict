"""Retrieve Wiktionary data."""

import bz2
import logging
import os
import re
from collections.abc import Callable
from pathlib import Path

import requests
from requests.exceptions import HTTPError

from .constants import BASE_URL, DUMP_URL

log = logging.getLogger(__name__)


def callback_progress(text: str, done: int, last: bool) -> None:
    """Progression callback. Used when fetching the Wiktionary dump and when extracting it."""
    size = f"OK [{done:,} bytes]" if last else f"{done:,} bytes"
    log.debug("%s: %s", text, size)


def decompress(file: Path, callback: Callable[[str, int, bool], None]) -> Path:
    """Decompress a BZ2 file."""
    output = file.with_suffix(file.suffix.replace(".bz2", ""))
    if output.is_file():
        return output

    msg = f"Uncompressing into {output.name}"
    log.info(msg)

    comp = bz2.BZ2Decompressor()
    with file.open("rb") as fi, output.open(mode="wb") as fo:
        done = 0
        while data := fi.read(1024**2):
            uncompressed = comp.decompress(data)
            done += fo.write(uncompressed)
            callback(msg, done, False)

    callback(msg, output.stat().st_size, True)
    return output


def fetch_snapshots(locale: str) -> list[str]:
    """Fetch available snapshots.
    Return a list of sorted dates.
    """
    if forced_snapshot := os.environ.get("FORCE_SNAPSHOT"):
        return [forced_snapshot]
    url = BASE_URL.format(locale)
    with requests.get(url) as req:
        req.raise_for_status()
        return sorted(re.findall(r'href="(\d+)/"', req.text))


def fetch_pages(date: str, locale: str, output_dir: Path, callback: Callable[[str, int, bool], None]) -> Path:
    """Download all pages, current versions only.
    Return the path of the XML file BZ2 compressed.
    """
    output_xml = output_dir / f"pages-{date}.xml"
    output = output_dir / f"pages-{date}.xml.bz2"
    if output.is_file() or output_xml.is_file():
        return output

    url = DUMP_URL.format(locale, date)
    msg = f"Fetching {url}"
    log.info(msg)

    with output.open(mode="wb") as fh, requests.get(url, stream=True) as req:
        req.raise_for_status()
        done = 0
        for chunk in req.iter_content(chunk_size=1024**2):
            done += fh.write(chunk)
            callback(msg, done, False)

    callback(msg, output.stat().st_size, True)
    return output


def main(locale: str) -> int:
    """Entry point."""

    # Ensure the folder exists
    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    output_dir.mkdir(exist_ok=True, parents=True)

    # Get the snapshot to handle
    snapshots = fetch_snapshots(locale)
    snapshot = snapshots[-1]

    # Fetch and uncompress the snapshot file
    try:
        file = fetch_pages(snapshot, locale, output_dir, callback_progress)
    except HTTPError:
        (output_dir / f"pages-{snapshot}.xml.bz2").unlink(missing_ok=True)
        log.exception("Wiktionary dump is ongoing ... ")
        log.info("Will use the previous one.")
        snapshot = snapshots[-2]
        file = fetch_pages(snapshot, locale, output_dir, callback_progress)

    decompress(file, callback_progress)

    log.info("Retrieval done!")
    return 0
