import pytest

from scripts import utils


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("du XX{{e}} siècle", "du XXème siècle"),
        ("{{méton|fr}}", "(Par métonymie)"),
        ("{{par ext}} ou {{figuré|fr}}", "(Par extension) ou (Figuré)"),
        ("{{pronl|fr}}", "(Pronominal)"),
        ("{{région}}", "(Régionalisme)"),
    ],
)
def test_clean_template(wikicode, expected):
    assert utils.clean(wikicode) == expected
