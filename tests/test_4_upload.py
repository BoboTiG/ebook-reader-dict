import os
from pathlib import Path
from typing import Any

import pytest
import responses

from wikidict import upload
from wikidict.constants import RELEASE_URL


def test_fetch_release_url() -> None:
    url = upload.fetch_release_url("fr")
    assert isinstance(url, str)
    assert url.startswith("https://api.github.com/repos/")
    assert "/releases/" in url


@responses.activate
def test_main(capsys: pytest.CaptureFixture[Any]) -> None:

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
def test_main_bad_url(capsys: pytest.CaptureFixture[Any]) -> None:
    # Test a bad release URL, fetch_release_url() will return an empty URL
    release_url = RELEASE_URL.format("fr")
    responses.add(responses.GET, release_url, json={"url": ""})

    assert upload.main("fr") == 1
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == " !! Cannot retrieve the release URL."
