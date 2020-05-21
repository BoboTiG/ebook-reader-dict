import os

import responses

os.environ["WIKI_LOCALE"] = "fr"

# Must be imported after *WIKI_LOCALE* is set
from scripts import constants as C  # noqa
from scripts import upload  # noqa


def test_fetch_release_url():
    url = upload.fetch_release_url()
    assert isinstance(url, str)
    assert url.startswith("https://api.github.com/repos/")
    assert "/releases/" in url


def test_format_description():
    C.SNAPSHOT_COUNT.write_text("123456789")
    C.SNAPSHOT_FILE.write_text("20200220")
    url = C.DOWNLOAD_URL.format(C.LOCALE)
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
        desc = upload.format_description().strip()
        lines = desc.splitlines()
        assert lines[:-1] == expected
        assert lines[-1].startswith("<sub>Mis à jour le 202")
        assert lines[-1].endswith("</sub>")
        assert desc.count("dicthtml-fr.zip") == 2
    finally:
        C.SNAPSHOT_COUNT.unlink()
        C.SNAPSHOT_FILE.unlink()


@responses.activate
def test_main(capsys):

    # List of requests responses to falsify:
    #   - fetch_release_url() -> GET $RELEASE_URL
    #   - update_release() -> POST https://api.github.com/repos/.../releses/$UID
    release_url = C.RELEASE_URL.format(C.LOCALE)
    responses.add(responses.GET, release_url, json={"url": release_url})
    responses.add(responses.PATCH, release_url, json={"url": release_url})

    # Start the whole process
    os.environ["GITHUB_TOKEN"] = "token"
    C.SNAPSHOT_COUNT.write_text("123456789")
    C.SNAPSHOT_FILE.write_text("20200220")
    try:
        assert upload.main() == 0
    finally:
        C.SNAPSHOT_COUNT.unlink()
        C.SNAPSHOT_FILE.unlink()
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == ">>> Release updated!"


@responses.activate
def test_main_bad_url(capsys):
    # Test a bad release URL, fetch_release_url() will return an empty URL
    release_url = C.RELEASE_URL.format(C.LOCALE)
    responses.add(responses.GET, release_url, json={"url": ""})

    assert upload.main() == 1
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == " !! Cannot retrieve the release URL."
