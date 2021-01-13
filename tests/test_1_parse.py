import bz2
import os
from pathlib import Path
from unittest.mock import patch

from wikidict import parse


def test_simple(craft_data):
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"

    # Delete an previously created file to cover the save() part
    for file in output_dir.glob("data_wikicode-*.json"):
        file.unlink()

    # Ensure there is data to process.
    compressed = craft_data("20201217", "fr")
    raw = bz2.decompress(compressed)
    (output_dir / "pages-20201217.xml").write_bytes(raw)

    assert parse.main("fr") == 0


def test_no_xml_file():
    with patch.object(parse, "get_latest_xml_file", return_value=None):
        assert parse.main("fr") == 1


def test_parse_restricted_word(tmp_path):
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

    assert parse.process(file, "fr")


def test_parse_redirected_word(tmp_path):
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

    assert not parse.process(file, "fr")


def test_parse_word_without_definitions(tmp_path):
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

    assert not parse.process(file, "fr")


def test_parse_word_with_colons(tmp_path):
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

    assert not parse.process(file, "fr")
