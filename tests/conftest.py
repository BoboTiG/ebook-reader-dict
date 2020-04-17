import bz2
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

import pytest

os.environ["CI"] = "1"
os.environ["CWD"] = str(Path(__file__).parent)


@pytest.fixture(scope="session")
def craft_data():
    def _data(date, locale):
        data_dir = Path(os.environ["CWD"]) / "data" / locale
        pages_xml = data_dir / f"pages-{date}.xml"
        pages_bz2 = data_dir / f"pages-{date}.xml.bz2"

        with pages_xml.open(mode="w", encoding="utf-8") as fh:
            fh.write(f'<mediawiki xml:lang="{locale}">\n')
            xml = """\
<page>
    <title>{word}</title>
    <ns>0</ns>
    <id>1</id>
    <revision>
        <id>222</id>
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
            for file in data_dir.glob("*.wiki"):
                text = file.read_text(encoding="utf-8")
                text = escape(text)
                fh.write(xml.format(word=file.stem, text=text))
            fh.write("</mediawiki>\n")

        # Compress the XML
        with pages_xml.open(mode="rb") as fi, bz2.open(pages_bz2, "wb") as fo:
            fo.writelines(fi)

    return _data


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
