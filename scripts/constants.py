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
DOWNLOAD_URL = f"{GH_REPOS}/releases/download/{{0}}/dicthtml-{{0}}.zip"

# HTML formatting for each word
WORD_FORMAT = """
<w>
    <p>
        <a name="{word}"/><b>{word}</b>{pronunciation}{genre}
        <br/>
        <br/>
        {etymology}
        <ol>{definitions}</ol>
    </p>
    {var}
</w>
"""
