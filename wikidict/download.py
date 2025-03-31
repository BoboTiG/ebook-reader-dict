"""Retrieve Wiktionary data."""

from __future__ import annotations

import bz2
import logging
import os
import re
from datetime import timedelta
from pathlib import Path
from time import monotonic
from typing import TYPE_CHECKING

import requests
from requests.exceptions import HTTPError

from .constants import BASE_URL, DUMP_URL
from .utils import guess_locales

if TYPE_CHECKING:
    from collections.abc import Callable

log = logging.getLogger(__name__)


def callback_progress(text: str, done: int, last: bool) -> None:
    """Progression callback. Used when fetching the Wiktionary dump and when extracting it."""
    size = f"OK [{done:,} bytes]" if last else f"{done:,} bytes"
    log.debug("%s: %s", text, size)


def decompress(file: Path, callback: Callable[[str, int, bool], None]) -> Path:
    """Decompress a BZ2 file."""
    output = file.with_suffix(file.suffix.replace(".bz2", ""))
    msg = f"Uncompressing into {output}"
    log.info(msg)

    if output.is_file():
        return output

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

    with requests.get(BASE_URL.format(locale)) as req:
        req.raise_for_status()
        return sorted(re.findall(r'href="(\d+)/"', req.text))


def fetch_pages(date: str, locale: str, output_dir: Path, *, callback: Callable[[str, int, bool], None]) -> Path:
    """Download all pages, current versions only.
    Return the path of the XML file BZ2 compressed.
    """
    url = DUMP_URL.format(locale, date)
    output_xml = output_dir / f"pages-{date}.xml"
    output = output_dir / f"pages-{date}.xml.bz2"
    msg = f"Fetching {url} into {output}"
    log.info(msg)

    if output.is_file() or output_xml.is_file():
        return output

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

    lang_src, _ = guess_locales(locale)

    # Ensure the folder exists
    output_dir = Path(os.getenv("CWD", "")) / "data" / lang_src
    output_dir.mkdir(exist_ok=True, parents=True)

    start = monotonic()

    # Get the snapshot to handle
    snapshots = fetch_snapshots(lang_src)

    # Fetch and uncompress the snapshot file
    for snapshot in snapshots[::-1]:
        try:
            file = fetch_pages(snapshot, lang_src, output_dir, callback=callback_progress)
            break
        except HTTPError as exc:
            (output_dir / f"pages-{snapshot}.xml.bz2").unlink(missing_ok=True)
            if exc.response.status_code != 404:
                raise
            log.warning("Wiktionary dump is ongoing ... ")
            log.info("Will use the previous one.")
    else:
        log.error("No Wiktionary dump found!")
        return 1

    decompress(file, callback_progress)

    log.info("Retrieval done in %s!", timedelta(seconds=monotonic() - start))
    return 0
