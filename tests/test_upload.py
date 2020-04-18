import os
import re

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
    text = upload.format_description()
    reg = r"^Nombre de mots : \d+\nDate : \d{4}-\d{2}-\d{2}$"
    assert re.match(reg, text)


@responses.activate
def test_main(capsys):

    # List of requests responses to falsify:
    #   - fetch_release_url() -> GET $RELEASE_URL
    #   - update_release() -> POST https://api.github.com/repos/.../releses/$UID
    responses.add(responses.GET, C.RELEASE_URL, json={"url": C.RELEASE_URL})
    responses.add(responses.PATCH, C.RELEASE_URL, json={"url": C.RELEASE_URL})

    # Start the whole process
    os.environ["GITHUB_TOKEN"] = "token"
    assert upload.main() == 0
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == ">>> Release updated!"


@responses.activate
def test_main_bad_url(capsys):
    # Test a bad release URL, fetch_release_url() will return an empty URL
    responses.add(responses.GET, C.RELEASE_URL, json={"url": ""})

    assert upload.main() == 1
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == " !! Cannot retrieve the release URL."
