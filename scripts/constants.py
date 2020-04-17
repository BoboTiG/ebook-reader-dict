"""Shared constants."""
import os
from pathlib import Path

# Wiktionary stuff
LOCALE = os.getenv("WIKI_LOCALE", "fr")
WIKI = f"{LOCALE}wiktionary"
BASE_URL = f"https://dumps.wikimedia.org/{WIKI}"

# Snapshot stuff
SNAPSHOT = Path(os.getenv("CWD", "")) / "data" / LOCALE
SNAPSHOT_COUNT = SNAPSHOT / "words.count"
SNAPSHOT_FILE = SNAPSHOT / "words.snapshot"
SNAPSHOT_LIST = SNAPSHOT / "words.list"
SNAPSHOT_DATA = SNAPSHOT / "data.json"

# Temp folder where to generate temp files
WORKING_DIR = SNAPSHOT / "tmp"

# The final ZIP
DICTHTML = SNAPSHOT / f"dicthtml-{LOCALE}.zip"
