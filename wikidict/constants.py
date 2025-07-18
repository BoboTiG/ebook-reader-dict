"""Shared constants."""

from pathlib import Path

import requests

# Dictionaries metadata
PROJECT = "Wiktionary"
# {0}: project
# {1}: lang source
# {2}: lang destination
TITLE = "{0} {1}-{2}"

# Wiktionary dump URL
# {0}: lang source
# {1}: dump date
BASE_URL = "https://dumps.wikimedia.org/{0}wiktionary"
DUMP_URL = f"{BASE_URL}/{{1}}/{{0}}wiktionary-{{1}}-pages-articles.xml.bz2"

# GitHub stuff
# {0}: lang source
# {1}: lang destination
# {2}: etymology-free suffix
REPOS = "BoboTiG/ebook-reader-dict"
GH_REPOS = f"https://github.com/{REPOS}"
DOWNLOAD_URL_DICTFILE = f"{GH_REPOS}/releases/download/{{0}}/dict-{{0}}-{{1}}{{2}}.df.bz2"
DOWNLOAD_URL_DICTORGFILE = f"{GH_REPOS}/releases/download/{{0}}/dictorg-{{0}}-{{1}}{{2}}.zip"
DOWNLOAD_URL_KOBO = f"{GH_REPOS}/releases/download/{{0}}/dicthtml-{{0}}-{{1}}{{2}}.zip"
DOWNLOAD_URL_MOBI = f"{GH_REPOS}/releases/download/{{0}}/dict-{{0}}-{{1}}{{2}}.mobi.zip"
DOWNLOAD_URL_STARDICT = f"{GH_REPOS}/releases/download/{{0}}/dict-{{0}}-{{1}}{{2}}.zip"
ASSET_CHECKSUM_ALGO = "sha256"

# Wikimedia REST API
WIKIMEDIA_HEADERS = {"User-Agent": GH_REPOS}
WIKIMEDIA_URL_BASE = "https://en.wikipedia.org/api/rest_v1"
WIKIMEDIA_URL_MATH_CHECK = f"{WIKIMEDIA_URL_BASE}/media/math/check/{{type}}"
WIKIMEDIA_URL_MATH_RENDER = f"{WIKIMEDIA_URL_BASE}/media/math/render/{{format}}/{{hash}}"

# Dictionary file suffix for etymology-free files
NO_ETYMOLOGY_SUFFIX = "-noetym"

# ZIP files
ZIP_INSTALL = "INSTALL.txt"
ZIP_WORDS_COUNT = "words.count"
ZIP_WORDS_SNAPSHOT = "words.snapshot"

# Locales relations
# Example with FRO (Old French) that uses the FR (French) Wiktionary dump as source.
# Syntax: "locale": "origin locale"
LOCALE_ORIGIN = {"fro": "fr"}

# Mobi
COVER_FILE = Path(__file__).parent / "cover.png"
KINDLEGEN_FILE = Path.home() / ".local" / "bin" / "kindlegen"

# HTTP requests
SESSION = requests.Session()
