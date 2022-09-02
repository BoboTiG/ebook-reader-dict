import pytest

from wikidict.lang.no import find_pronunciations
from wikidict.render import parse_word
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "code, expected",
    [
        ("", []),
    ],
)
def test_find_pronunciations(code, expected):
    assert find_pronunciations(code) == expected


@pytest.mark.parametrize(
    "word, pronunciations, etymology, definitions",
    [
        (
            "konsentrasjon",
            [],
            ["Fra"],
            [
                "Det å konsentrere seg; ha stort fokus på noe.",
                "<i>(Kjemi)</i> Andelen stoff i noe; mengde stoff løst pr. enhet.",
            ],
        ),
    ],
)
def test_parse_word(word, pronunciations, etymology, definitions, page):
    """Test the sections finder and definitions getter."""
    code = page(word, "no")
    details = parse_word(word, code, "no", force=True)
    assert pronunciations == details.pronunciations
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
    assert process_templates("foo", wikicode, "no") == expected
