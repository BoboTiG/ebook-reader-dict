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
        ("{{fchim|H|2|O}}", "H<sub>2</sub>O"),
        ("{{fchim|FeCO|3|}}", "FeCO<sub>3</sub>"),
        ('<span style="color:black">[[♣]]</span>', "♣"),
        ("{{unknown}}", "<i>(Unknown)</i>"),
    ],
)
def test_clean_template(wikicode, expected):
    assert utils.clean(wikicode) == expected


@pytest.mark.parametrize(
    "wikicode, expected",
    [(["H", "2", "O"], "H<sub>2</sub>O"), (["FeCO", "3", ""], "FeCO<sub>3</sub>")],
)
def test_format_chimy(wikicode, expected):
    assert utils.format_chimy(wikicode) == expected
