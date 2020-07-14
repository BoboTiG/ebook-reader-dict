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
WORD_FORMAT = (
    # Word formatting
    '<w><p><a name="{word}"/><b>{word}</b>{pronunciation}{genre}{etymology}<br/><br/><ol>{definitions}</ol></p>'
    # The source
    '<p style="text-align:right"><i>{source}</i></p>'
    # And add a line break for when there is more that one word displayed
    "<br/>"
    # This is a hell of a hack to hide the harcoded dict name (!)
    # See https://github.com/BoboTiG/ebook-reader-dict/issues/33
    '<span class="e"><style>.e,.e+*{{display:none}}</style></span>'
    # Do not forget to close tag
    "</w>"
)
