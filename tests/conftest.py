import json
import os
from pathlib import Path

import pytest

os.environ["CI"] = "1"
os.environ["CWD"] = str(Path(__file__).parent)


@pytest.fixture
def data():
    def _data(file):
        data_dir = Path(os.environ["CWD"]) / "data" / os.environ["WIKI_LOCALE"]
        with (data_dir / file).open(encoding="utf-8") as fh:
            return json.load(fh)

    return _data


@pytest.fixture
def page():
    def _page(word):
        data = Path(os.environ["CWD"]) / "data" / os.environ["WIKI_LOCALE"]
        file = data / f"{word}.wiki"
        return {
            "title": file.stem,
            "revision": {"id": "test", "text": {"#text": file.read_text()}},
        }

    return _page
