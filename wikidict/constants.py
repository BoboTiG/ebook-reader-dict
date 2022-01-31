"""Shared constants."""

# Wiktionary dump URL
# {0}: current locale
# {1}: dump date
BASE_URL = "https://dumps.wikimedia.org/{0}wiktionary"
DUMP_URL = f"{BASE_URL}/{{1}}/{{0}}wiktionary-{{1}}-pages-meta-current.xml.bz2"

# GitHub stuff
# {0}: current locale
REPOS = "BoboTiG/ebook-reader-dict"
GH_REPOS = f"https://github.com/{REPOS}"
RELEASE_URL = f"https://api.github.com/repos/{REPOS}/releases/tags/{{0}}"
DOWNLOAD_URL_DICTFILE = f"{GH_REPOS}/releases/download/{{0}}/dict-{{0}}-{{0}}.df.bz2"
DOWNLOAD_URL_KOBO = f"{GH_REPOS}/releases/download/{{0}}/dicthtml-{{0}}-{{0}}.zip"
DOWNLOAD_URL_STARDICT = f"{GH_REPOS}/releases/download/{{0}}/dict-{{0}}-{{0}}.zip"

# HTML formatting for each word
# TODO: move that into the dict specific class
WORD_FORMAT = """
<w>
    <p>
        <a name="{word}"/><b>{current_word}</b>{pronunciation}{gender}
        <br/>
        <br/>
        {etymology}
        <ol>{definitions}</ol>
    </p>
    {var}
</w>
"""

# Inline CSS for inline images handling <math> tags.
IMG_CSS = ";".join(
    [
        # try to keep a height proportional to the current font height
        "height: 100%",
        "max-height: 0.8em",
        "width: auto",
        # and adjust the vertical alignment to not alter the line height
        "vertical-align: bottom",
    ]
).replace(" ", "")
