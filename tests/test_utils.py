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
    [("{{méton|fr}}", ""), ("{{pronl|fr}}", ""), ("{{région}}", "")],
)
def test_clean_template_delete(wikicode, expected):
    assert utils.clean(wikicode) == expected


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{term|ne … guère que}}", "(Ne … guère que)"),
        ("{{term|Avec un mot négatif}} Presque.", "(Avec un mot négatif) Presque."),
    ],
)
def test_clean_template_term(wikicode, expected):
    assert utils.clean(wikicode) == expected
