"""Shared constants."""
import os
import re
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

# Regexps
PRONUNCIATION = re.compile(r"{{pron\|([^}]+)\|(lang=)?%s}}" % LOCALE, flags=re.UNICODE)
GENRE = re.compile(r"{{([fmsingp]+)}}")
EXTRA_SPACES = re.compile(r"\s{2,}")
EXTRA_SPACES_DOT = re.compile(r"\s{1,}\.")

# GitHub stuff
RELEASE_URL = (
    f"https://api.github.com/repos/BoboTiG/ebook-reader-dict/releases/tags/{LOCALE}"
)
