"""Retrieve Wiktionary data."""
import bz2
import os
import re
from functools import partial
from pathlib import Path
from typing import Callable, List

import requests
from requests.exceptions import HTTPError

from .constants import BASE_URL, DUMP_URL


def callback_progress(text: str, total: int, last: bool) -> None:
    """Progression callback. Used when fetching the Wiktionary dump and when extracting it."""
    msg = f"{text}OK [{total:,} bytes]\n" if last else f"{text}{total:,} bytes"
    print(f"\r{msg}", end="", flush=True)


def callback_progress_ci(text: str, total: int, last: bool) -> None:
    """
    Progression callback. Used when fetching the Wiktionary dump and when extracting it.
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


def main(locale: str) -> int:
    """Entry point."""

    # Ensure the folder exists
    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    output_dir.mkdir(exist_ok=True, parents=True)

    # Get the snapshot to handle
    snapshots = fetch_snapshots(locale)
    snapshot = snapshots[-1]

    # The output style is different if run from a workflow
    # Note: "CI" is automatically set in every GitHub workflow
    # https://help.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables#default-environment-variables
    cb = callback_progress_ci if "CI" in os.environ else callback_progress

    # Fetch and uncompress the snapshot file
    try:
        file = fetch_pages(snapshot, locale, output_dir, cb)
    except HTTPError:
        (output_dir / f"pages-{snapshot}.xml.bz2").unlink(missing_ok=True)
        print("FAIL", flush=True)
        print(">>> Wiktionary dump is ongoing ... ", flush=True)
        print(">>> Will use the previous one.", flush=True)
        snapshot = snapshots[-2]
        file = fetch_pages(snapshot, locale, output_dir, cb)

    decompress(file, cb)

    print(">>> Retrieval done!", flush=True)
    return 0
