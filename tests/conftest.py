import os
from pathlib import Path

import pytest


@pytest.fixture
def page():
    def _page(word):
        data = Path(__file__).parent / "data" / os.getenv("WIKI_LOCALE")
        file = data / f"{word}.wiki"
        return {
            "title": file.stem,
            "revision": {"id": "test", "text": {"#text": file.read_text()}},
        }

    return _page
