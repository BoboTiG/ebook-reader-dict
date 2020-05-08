import bz2
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

import pytest

os.environ["CWD"] = str(Path(__file__).parent)


XML = (
    '<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="{locale}">'
)
PAGE_XML = """<page>
    <title>{word}</title>
    <ns>0</ns>
    <id>1</id>
    <revision>
        <id>{revision}</id>
        <parentid>221</parentid>
        <timestamp>2020-04-17T14:21:12Z</timestamp>
        <contributor>
            <username>Alice</username>
            <id>42</id>
        </contributor>
        <comment>/**/</comment>
        <model>wikitext</model>
        <format>text/x-wiki</format>
        <text xml:space="preserve">{text}</text>
    </revision>
</page>
"""


@pytest.fixture(scope="session")
def craft_data():
    def _craft_data(date, locale, to_add=None, to_remove=None, to_alter=None):
        data_dir = Path(os.environ["CWD"]) / "data" / locale
        content = XML.format(locale=locale)
        for file in data_dir.glob("*.wiki"):
            revision = 42

            # Possitility to remove a word
            if to_remove and file.stem in to_remove:
                print(f"[fixture] Removed word {file.stem!r}")
                continue

            text = file.read_text(encoding="utf-8")

            # Possibility to alter the content of a word
            if to_alter and file.stem in to_alter:
                print(f"[fixture] Altered word {file.stem!r}")
                revision += 1

            text = escape(text)
            content += PAGE_XML.format(word=file.stem, revision=revision, text=text)

        # Possibility to add new words
        if to_add:
            skeleton = (data_dir / "page.skeleton").read_text(encoding="utf-8")
            for word, rev in to_add:
                print(f"[fixture] Added word {word!r}")
                text = escape(skeleton.replace("WORD", word))
                content += PAGE_XML.format(word=word, revision=rev, text=text)

        content += "</mediawiki>"
        return bz2.compress(content.encode("utf-8"))

    return _craft_data


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
            "revision": {"text": {"#text": file.read_text()}},
        }

    return _page
