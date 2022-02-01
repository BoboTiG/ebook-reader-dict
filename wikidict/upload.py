"""Update the description of a release."""
import json
import os
from pathlib import Path

import requests

from .constants import RELEASE_URL
from .utils import format_description


def fetch_release_url(locale: str) -> str:
    """Retrieve the *url* of the release of the current *locale*."""
    url = ""
    with requests.get(RELEASE_URL.format(locale), timeout=10) as req:
        req.raise_for_status()
        data = req.json()
        url = data["url"]
    return url


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
        print(" !! Cannot retrieve the release URL.", flush=True)
        return 1

    # Update the release description
    update_release(url, locale, output_dir)

    print(">>> Release updated!", flush=True)
    return 0
