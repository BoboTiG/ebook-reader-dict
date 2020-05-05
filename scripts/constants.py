"""Shared constants."""
import os
import re
from pathlib import Path

# Wiktionary stuff
LOCALE = os.getenv("WIKI_LOCALE", "fr")
WIKI = f"{LOCALE}wiktionary"
BASE_URL = f"https://dumps.wikimedia.org/{WIKI}"
WORD_URL = f"https://{LOCALE}.wiktionary.org/w/index.php?title={{}}&action=raw"

# Snapshot stuff
SNAPSHOT = Path(os.getenv("CWD", "")) / "data" / LOCALE
SNAPSHOT_COUNT = SNAPSHOT / "words.count"
SNAPSHOT_FILE = SNAPSHOT / "words.snapshot"
SNAPSHOT_LIST = SNAPSHOT / "words.list"
SNAPSHOT_DATA = SNAPSHOT / "data.json"
SNAPSHOT_DOWNLOADS = SNAPSHOT / "download.count"

# Temp folder where to generate temp files
WORKING_DIR = SNAPSHOT / "tmp"

# The final ZIP
DICTHTML = SNAPSHOT / f"dicthtml-{LOCALE}.zip"

# Regexps
PRONUNCIATION = re.compile(r"{pron\|([^}\|]+)")
GENRE = re.compile(r"{([fmsingp]+)}")

# GitHub stuff
REPOS = "BoboTiG/ebook-reader-dict"
GH_REPOS = f"https://github.com/{REPOS}"
RELEASE_URL = f"https://api.github.com/repos/{REPOS}/releases/tags/{LOCALE}"
DOWNLOAD_URL = f"{GH_REPOS}/releases/download/{LOCALE}/dicthtml-{LOCALE}.zip"

# HTML formatting for each word
WORD_FORMAT = (
    # Word formatting
    '<w><p><a name="{word}"/><b>{word}</b>{pronunciation}{genre}<br/><br/><ol>{definitions}</ol>'
    # The source
    "<br/><i>{source}</i>"
    # Close the paragraph
    "</p>"
    # And add a line break for when there is more that one word displayed
    "<br/>"
    # This is a hell of a hack to hide the harcoded dict name (!)
    # See https://github.com/BoboTiG/ebook-reader-dict/issues/33
    "<span><style>span,span+*{{display:none}}</style></span>"
    # Do not forget to close tag
    "</w>"
)
