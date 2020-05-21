import os
from pathlib import Path

import responses

from scripts import constants as C
from scripts import upload


def test_fetch_release_url():
    url = upload.fetch_release_url("fr")
    assert isinstance(url, str)
    assert url.startswith("https://api.github.com/repos/")
    assert "/releases/" in url


def test_format_description():
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    (output_dir / "words.count").write_text("123456789")
    (output_dir / "words.snapshot").write_text("20200220")
    url = C.DOWNLOAD_URL.format("fr")
    expected = [
        "Nombre de mots : 123 456 789",
        "Export Wiktionnaire : 2020-02-20",
        "",
        f":arrow_right: Téléchargement : [dicthtml-fr.zip]({url})",
        "",
        "---",
        "",
        "Caractéristiques :",
        "",
        "- Seules les définitions sont incluses : il n'y a ni les citations ni l'éthymologie.",
        "- Les mots comportant moins de 2 caractères ne sont pas inclus.",
        "- Les noms propres ne sont pas inclus.",
        "- Les conjugaisons ne sont pas incluses.",
        "",
    ]
    try:
        desc = upload.format_description("fr", output_dir).strip()
        lines = desc.splitlines()
        assert lines[:-1] == expected
        assert lines[-1].startswith("<sub>Mis à jour le 202")
        assert lines[-1].endswith("</sub>")
        assert desc.count("dicthtml-fr.zip") == 2
    finally:
        (output_dir / "words.count").unlink()
        (output_dir / "words.snapshot").unlink()


@responses.activate
def test_main(capsys):

    # List of requests responses to falsify:
    #   - fetch_release_url() -> GET $RELEASE_URL
    #   - update_release() -> POST https://api.github.com/repos/.../releses/$UID
    release_url = C.RELEASE_URL.format("fr")
    responses.add(responses.GET, release_url, json={"url": release_url})
    responses.add(responses.PATCH, release_url, json={"url": release_url})

    # Start the whole process
    os.environ["GITHUB_TOKEN"] = "token"
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    (output_dir / "words.count").write_text("123456789")
    (output_dir / "words.snapshot").write_text("20200220")
    try:
        assert upload.main("fr") == 0
    finally:
        (output_dir / "words.count").unlink()
        (output_dir / "words.snapshot").unlink()
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == ">>> Release updated!"


@responses.activate
def test_main_bad_url(capsys):
    # Test a bad release URL, fetch_release_url() will return an empty URL
    release_url = C.RELEASE_URL.format("fr")
    responses.add(responses.GET, release_url, json={"url": ""})

    assert upload.main("fr") == 1
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == " !! Cannot retrieve the release URL."
