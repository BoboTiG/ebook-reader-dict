import bz2
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

import pytest

os.environ["CWD"] = str(Path(__file__).parent)


XML = """<mediawiki xml:lang="{locale}">
<siteinfo>
    <sitename>Wiktionnaire</sitename>
    <dbname>frwiktionary</dbname>
    <base>https://fr.wiktionary.org/wiki/Wiktionnaire:Page_d%E2%80%99accueil</base>
    <generator>MediaWiki 1.35.0-wmf.25</generator>
    <case>case-sensitive</case>
    <namespaces>
        <namespace key="-2" case="case-sensitive">Média</namespace>
        <namespace key="-1" case="first-letter">Spécial</namespace>
        <namespace key="0" case="case-sensitive" />
    </namespaces>
</siteinfo>

<!-- To cover word containing a ":" -->
<page>
    <title>MediaWiki:Sitetitle</title>
    <ns>8</ns>
    <id>12</id>
    <revision>
        <id>403956</id>
        <parentid>33016</parentid>
        <timestamp>2006-02-13T09:08:31Z</timestamp>
        <contributor>
        <username>Bob</username>
        <id>-42</id>
        </contributor>
        <comment>changement de titre pour meilleur référencement dans les moteurs de recherche</comment>
        <model>wikitext</model>
        <format>text/x-wiki</format>
        <text bytes="46" xml:space="preserve">Wiktionnaire : dictionnaire libre et universel</text>
        <sha1>40helna9646ffk0utvwm8bkdlzi1eck</sha1>
    </revision>
</page>

"""
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
        """
        """

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
            for addition in to_add:
                print(f"[fixture] Added word {addition['word']!r}")
                addition["text"] = escape(skeleton.replace("WORD", addition["word"]))
                content += PAGE_XML.format(**addition)

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
            "revision": {"id": "test", "text": {"#text": file.read_text()}},
        }

    return _page
