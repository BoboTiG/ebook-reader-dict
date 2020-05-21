"""Update the description of a release."""
import json
import os
from datetime import datetime
from pathlib import Path

import requests

from .constants import DOWNLOAD_URL, RELEASE_URL
from .lang import release_description, thousands_separator


def fetch_release_url(locale: str) -> str:
    """Retrieve the *url* of the release of the current *locale*."""
    url = ""
    with requests.get(RELEASE_URL.format(locale)) as req:
        req.raise_for_status()
        data = req.json()
        url = data["url"]
    return url


def format_description(locale: str, output_dir: Path) -> str:
    """Generate the release description."""

    # Get the words count
    count = (output_dir / "words.count").read_text().strip()

    # Format the words count
    thousands_sep = thousands_separator[locale]
    count = f"{int(count):,}".replace(",", thousands_sep)

    # Format the snapshot's date
    date = (output_dir / "words.snapshot").read_text().strip()
    date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"

    # The current date, UTC
    now = datetime.utcnow().isoformat()

    # The download link
    url = DOWNLOAD_URL.format(locale)

    return release_description[locale].format(
        creation_date=now, dump_date=date, url=url, words_count=count,
    )


def update_release(url: str, locale: str, output_dir: Path) -> None:
    """Update the release description."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
    }
    data = json.dumps({"body": format_description(locale, output_dir)})
    print(f">>> Updating release at {url} ...", flush=True)
    with requests.patch(url, data=data, headers=headers) as req:
        req.raise_for_status()


def main(locale: str) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale

    # Get the release URL
    url = fetch_release_url(locale)
    if not url:
        print(" !! Cannot retrieve the release URL.")
        return 1

    # Update the release description
    update_release(url, locale, output_dir)

    print(">>> Release updated!")
    return 0
