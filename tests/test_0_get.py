import json
import os
from contextlib import suppress
from pathlib import Path

import responses

from scripts import get
from scripts.constants import BASE_URL, DUMP_URL

WIKTIONARY_INDEX = """<html>
<head><title>Index of /frwiktionary/</title></head>
<body bgcolor="white">
<h1>Index of /frwiktionary/</h1><hr><pre><a href="../">../</a>
<a href="20191120/">20191120/</a>                                          02-Jan-2020 01:29                   -
<a href="20191201/">20191201/</a>                                          21-Jan-2020 01:36                   -
<a href="20191220/">20191220/</a>                                          02-Feb-2020 01:28                   -
<a href="20200101/">20200101/</a>                                          21-Feb-2020 01:38                   -
<a href="20200120/">20200120/</a>                                          02-Mar-2020 01:28                   -
<a href="20200201/">20200201/</a>                                          02-Apr-2020 01:36                   -
<a href="20200220/">20200220/</a>                                          24-Feb-2020 17:32                   -
<a href="20200301/">20200301/</a>                                          09-Mar-2020 03:42                   -
<a href="{date}/">{date}/</a>                                          17-Apr-2020 15:20                   -
<a href="latest/">latest/</a>                                            17-Apr-2020 15:20                   -
</pre><hr></body>
</html>
"""


@responses.activate
def test_main_0(craft_data, capsys):
    """Test the whole script. It will generate data for test_1_convert.py."""

    output_dir = Path(os.environ["CWD"]) / "data" / "fr"

    date = "20200417"
    pages_xml = output_dir / f"pages-{date}.xml"
    pages_bz2 = output_dir / f"pages-{date}.xml.bz2"

    # Clean-up before we start
    for file in (
        output_dir / "data.json",
        output_dir / "words.count",
        output_dir / "words.snaphot",
        pages_xml,
        pages_bz2,
    ):
        with suppress(FileNotFoundError):
            file.unlink()

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages()
    responses.add(
        responses.GET, BASE_URL.format("fr"), body=WIKTIONARY_INDEX.format(date=date),
    )
    responses.add(
        responses.GET, DUMP_URL.format("fr", date), body=craft_data(date, "fr"),
    )

    # Start the whole process
    with capsys.disabled():
        assert get.main("fr") == 0

    # Check for generated files

    # Check that files are created
    assert pages_xml.is_file()
    assert pages_bz2.is_file()
    assert (output_dir / "data.json").is_file()

    # Here we do -4 because of:
    #   - "Bogotanais.wiki" (no definition found)
    #   - "corollaires.wiki" (plural)
    #   - "no section.wiki"
    #   - "suis.wiki" (conjugated verb)
    expected_count = len(list(output_dir.glob("*.wiki"))) - 4

    # Check the words data
    words = json.loads((output_dir / "data.json").read_text(encoding="utf-8"))
    assert len(words.keys()) == expected_count

    # Check other files
    assert int((output_dir / "words.count").read_text()) == expected_count
    assert (output_dir / "words.snapshot").read_text() == "20200417"


@responses.activate
def test_main_1(craft_data, capsys):
    """Test the whole script again. There should be updates."""

    output_dir = Path(os.environ["CWD"]) / "data" / "fr"

    date = "20200418"
    pages_xml = output_dir / f"pages-{date}.xml"
    pages_bz2 = output_dir / f"pages-{date}.xml.bz2"

    # Clean-up before we start
    for file in (pages_xml, pages_bz2):
        with suppress(FileNotFoundError):
            file.unlink()

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages()
    responses.add(
        responses.GET, BASE_URL.format("fr"), body=WIKTIONARY_INDEX.format(date=date),
    )
    responses.add(
        responses.GET,
        DUMP_URL.format("fr", date),
        body=craft_data(
            date,
            "fr",
            to_add=(("mot el", "42"), ("mot us", "42")),
            to_alter=("aux",),
            to_remove=("suis",),
        ),
    )

    # Run against the new snapshot
    assert get.main("fr") == 0

    # Files should be created
    assert pages_xml.is_file()
    assert pages_bz2.is_file()
    assert (output_dir / "data.json").is_file()

    # Trigger manual calls for coverage
    file = get.fetch_pages(date, "fr", output_dir, get.callback_progress_ci)
    get.decompress(file, get.callback_progress_ci)

    # Check the words list has been updated
    # Here we do -4 because of:
    #   - "Bogotanais.wiki" (no definition found)
    #   - "corollaires.wiki" (plural)
    #   - "no section.wiki"
    #   - "suis" dynamically removed
    # And we do +2 because of:
    #   - "mot el" dynamically added
    #   - "mot us" dynamically added
    expected_count = len(list(output_dir.glob("*.wiki"))) - 4 + 2

    # Check the words data
    words = json.loads((output_dir / "data.json").read_text(encoding="utf-8"))
    assert len(words.keys()) == expected_count


@responses.activate
def test_main_2(craft_data, capsys):
    """Test the whole script when the DEBUG envar is set."""

    output_dir = Path(os.environ["CWD"]) / "data" / "fr"

    date = "20200514"
    with suppress(FileNotFoundError):
        (output_dir / f"pages-{date}.xml").unlink()
    with suppress(FileNotFoundError):
        (output_dir / f"pages-{date}.xml.bz2").unlink()

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages()
    responses.add(
        responses.GET, BASE_URL.format("fr"), body=WIKTIONARY_INDEX.format(date=date),
    )
    responses.add(
        responses.GET, DUMP_URL.format("fr", date), body=craft_data(date, "fr"),
    )

    # Start the whole process
    os.environ["DEBUG"] = "1"
    try:
        assert get.main("fr") == 0
    finally:
        del os.environ["DEBUG"]


@responses.activate
def test_main_3(craft_data, capsys):
    """Test the whole script when the dump is not finished on the Wiktionary side."""

    output_dir = Path(os.environ["CWD"]) / "data" / "fr"

    # Clean-up before we start
    for date in ("20200301", "20200514"):
        with suppress(FileNotFoundError):
            (output_dir / f"pages-{date}.xml").unlink()
        with suppress(FileNotFoundError):
            (output_dir / f"pages-{date}.xml.bz2").unlink()

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages()
    responses.add(
        responses.GET,
        BASE_URL.format("fr"),
        body=WIKTIONARY_INDEX.format(date="20200514"),
    )
    responses.add(
        responses.GET, DUMP_URL.format("fr", "20200514"), status=404,
    )
    responses.add(
        responses.GET,
        DUMP_URL.format("fr", "20200301"),
        body=craft_data(
            date,
            "fr",
            to_add=(("mot el", "42"), ("mot us", "42")),
            to_alter=("aux",),
            to_remove=("suis",),
        ),
    )

    # Start the whole process
    assert get.main("fr") == 0


def test_xml_parse_word_with_colons(tmp_path):
    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
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
</mediawiki>
"""
    )

    words = get.process(file, "fr")
    assert not words


def test_xml_parse_not_word(tmp_path):
    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
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
</mediawiki>
"""
    )

    words = get.process(file, "fr")
    assert not words


def test_xml_parse_redirected_word(tmp_path):
    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
<page>
    <title>MediaWiki:Sitetitle</title>
    <ns>8</ns>
    <id>12</id>
    <redirect></redirect>
</page>
</mediawiki>
"""
    )

    words = get.process(file, "fr")
    assert not words


def test_xml_parse_restricted_word(tmp_path):
    """For instance, "cunnilingus" was filtered out. Ensure no regressions."""

    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
<page>
    <title>cunnilingus</title>
    <ns>0</ns>
    <id>27758</id>
    <restrictions>edit=autoconfirmed:move=autoconfirmed</restrictions>
    <revision>
        <id>27636792</id>
        <parentid>27249625</parentid>
        <timestamp>2020-04-05T23:27:40Z</timestamp>
        <contributor>
            <username>Alice</username>
            <id>-42</id>
        </contributor>
        <minor />
        <comment></comment>
        <model>wikitext</model>
        <format>text/x-wiki</format>
        <text bytes="292" xml:space="preserve">{{voir|Cunnilingus}}

== {{langue|fr}} ==
=== {{S|nom|fr}} ===
{{fr-inv|ky.ni.lɛ̃.gys|sp=1}}
[[Fichier:Édouard-Henri Avril (23).jpg|thumb|Un '''cunnilingus''']]
'''cunnilingus''' {{pron|ky.ni.lɛ̃.ɡys|fr}} {{m}}, {{sp}}
# {{sexe|fr}} [[excitation|Excitation]] [[buccal]]e des [[organe]]s [[génitaux]] [[féminins]].</text>
        <sha1>aimljsg0qagdsp5yyz38fgv3rh0ksm1</sha1>
    </revision>
</page>
</mediawiki>
"""
    )

    words = get.process(file, "fr")
    assert len(words) == 1

    word, details = list(words.items())[0]
    assert word == "cunnilingus"
    assert details.pronunciation == "ky.ni.lɛ̃.ɡys"
    assert details.genre == "m"
    assert not details.etymology
    assert len(details.definitions) == 1
    assert len(details.definitions[0]) == 68


def test_xml_parse_word_without_definitions(tmp_path):
    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
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
        <sha1>40helna9646ffk0utvwm8bkdlzi1eck</sha1>
    </revision>
</page>
</mediawiki>
"""
    )

    words = get.process(file, "fr")
    assert not words


def test_get_and_parse_word():
    get.get_and_parse_word("fondation", "fr")
    get.get_and_parse_word("fondation", "fr", raw=True)
