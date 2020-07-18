import os
from pathlib import Path

import responses

from scripts import upload
from scripts.constants import DOWNLOAD_URL, RELEASE_URL


def test_fetch_release_url():
    url = upload.fetch_release_url("fr")
    assert isinstance(url, str)
    assert url.startswith("https://api.github.com/repos/")
    assert "/releases/" in url


def test_format_description():
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    (output_dir / "words.count").write_text("123456789")
    (output_dir / "words.snapshot").write_text("20200220")
    url = DOWNLOAD_URL.format("fr")
    expected = f"""\
Nombre de mots : 123 456 789
Export Wiktionnaire : 2020-02-20

:arrow_right: Téléchargement : [dicthtml-fr.zip]({url})

---

Installation :

1. Copier le fichier `dicthtml-fr.zip` dans le dossier `.kobo/dict/` de la liseuse.
2. Redémarrer la liseuse.

---

Caractéristiques :

- Les mots comportant moins de 2 caractères ne sont pas inclus.
- Les noms propres ne sont pas inclus.
- Les conjugaisons ne sont pas incluses.
"""

    try:
        desc = upload.format_description("fr", output_dir).strip()
        assert desc.startswith(expected)

        # 1: URL name
        # 2: URL link
        # 3: installation process
        assert desc.count("dicthtml-fr.zip") == 3

        last_line = desc.splitlines()[-1]
        assert last_line.startswith("<sub>Mis à jour le 202")
        assert last_line.endswith("</sub>")
    finally:
        (output_dir / "words.count").unlink()
        (output_dir / "words.snapshot").unlink()


@responses.activate
def test_main(capsys):

    # List of requests responses to falsify:
    #   - fetch_release_url() -> GET $RELEASE_URL
    #   - update_release() -> POST https://api.github.com/repos/.../releses/$UID
    release_url = RELEASE_URL.format("fr")
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
    release_url = RELEASE_URL.format("fr")
    responses.add(responses.GET, release_url, json={"url": ""})

    assert upload.main("fr") == 1
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == " !! Cannot retrieve the release URL."
