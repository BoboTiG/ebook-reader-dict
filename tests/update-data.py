import sys
from pathlib import Path

import requests


def fetch_and_store_if_updated(file: Path, url: str) -> None:
    current_content = file.read_text().strip()
    with requests.get(url) as req:
        if not req.ok:
            return
        new_content = req.text.strip()
    if current_content != new_content:
        file.write_text(req.text + "\n")
        print(f"Updated {file}", flush=True)


def main() -> int:
    url_fmt = "https://{}.wiktionary.org/w/index.php?title={}&action=raw"
    folder = Path(__file__).parent / "data"
    for locale in folder.iterdir():
        for file in locale.glob("*.wiki"):
            url = url_fmt.format(locale.name, file.stem)
            fetch_and_store_if_updated(file, url)

            html_file = file.with_suffix(".html")
            if html_file.is_file():
                url = url.replace("&action=raw", "")
                fetch_and_store_if_updated(html_file, url)

    return 0


if __name__ == "__main__":
    sys.exit(main())
