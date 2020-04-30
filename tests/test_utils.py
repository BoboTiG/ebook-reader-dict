import pytest

from scripts import utils


@pytest.mark.parametrize(
    "word, ignored",
    [
        ("accueil", False),
        ("2", True),
        ("22", True),
        ("222", True),
        ("222" * 12, True),
        ("en", True),
        ("", True),
        (" ", True),
    ],
)
def test_is_ignored(word, ignored):
    """Test words filtering."""
    assert utils.is_ignored(word) is ignored


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{pronl|fr}}", ""),
    ],
)
def test_clean(wikicode, expected):
    assert utils.clean(wikicode) == expected
