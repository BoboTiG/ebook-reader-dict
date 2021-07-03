import pytest

from wikidict.render import parse_word
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, gender, etymology, definitions, variants",
    [
        (
            "λαμβάνω",
            ["lam.ˈva.nɔ"],
            "",
            ["<b>λαμβάνω</b> < < <i>(Ετυμ)</i> *<i>sleh₂gʷ</i>-"],
            [
                "παίρνω, δέχομαι",  # noqa
                "εντοπίζω επιθυμητό σήμα",  # noqa
                "<i>(Μτφρ)</i> καταλαβαίνω",  # noqa
            ],
            [],
        ),
    ],
)
def test_parse_word(
    word, pronunciations, gender, etymology, definitions, variants, page
):
    """Test the sections finder and definitions getter."""
    code = page(word, "el")
    details = parse_word(word, code, "el", force=True)
    assert pronunciations == details.pronunciations
    assert gender == details.gender
    assert definitions == details.definitions
    assert etymology == details.etymology
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [],
)
def test_process_templates(wikicode, expected):
    """Test templates handling."""
    assert process_templates("foo", wikicode, "el") == expected
