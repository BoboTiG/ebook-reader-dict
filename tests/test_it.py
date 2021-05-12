import pytest

from wikidict.render import parse_word
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genre, etymology, definitions",
    [
        (
            "debolmente",
            ["debolˈmente"],
            "",
            ["composto dall'aggettivo debole e dal suffisso -mente"],
            [
                "in maniera debole, con debolezza",
            ],
        ),
    ],
)
def test_parse_word(word, pronunciations, genre, etymology, definitions, page):
    """Test the sections finder and definitions getter."""
    code = page(word, "it")
    details = parse_word(word, code, "it", force=True)
    assert pronunciations == details.pronunciations
    assert genre == details.genre
    assert etymology == details.etymology
    assert definitions == details.definitions


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("", ""),
    ],
)
def test_process_templates(wikicode, expected):
    """Test templates handling."""
    assert process_templates("foo", wikicode, "it") == expected
