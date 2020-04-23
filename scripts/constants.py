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

# GitHub stuff
REPOS = "BoboTiG/ebook-reader-dict"
RELEASE_URL = f"https://api.github.com/repos/{REPOS}/releases/tags/{LOCALE}"
DOWNLOAD_URL = (
    f"https://github.com/{REPOS}/releases/download/{LOCALE}/dicthtml-{LOCALE}.zip"
)

# HTML formatting for each word:
#   <p>
#       <a name="word"/>
#       <b>word</b> \pronunciation\ <i>genre</i>
#       <br/>
#       <br/>
#       <ol>
#           <li>definition 1</li>
#           <li>definition 2</li>
#       </ol>
#   </p>
WORD_FORMAT = (
    '<w><p><a name="{word}"/><b>{word}</b>{pronunciation}{genre}'
    "<br/><br/><ol>{definitions}</ol></p></w>"
)
