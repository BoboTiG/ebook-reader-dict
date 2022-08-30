import pytest

from wikidict.render import parse_word
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, gender, etymology, definitions, variants",
    [
        (
            "λαμβάνω",
            ["el"],
            "",
            ["<b>λαμβάνω</b> < < <i>(Ετυμ)</i> *<i>sleh₂gʷ</i>-"],
            [
                "παίρνω, δέχομαι",
                "εντοπίζω επιθυμητό σήμα (όπως από ασύρματο)",
                "<i>(Ετ)</i> καταλαβαίνω",
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
    [("{{resize|Βικιλεξικό|140}}", '<span style="font-size:140%;">Βικιλεξικό</span>')],
)
def test_process_templates(wikicode, expected):
    """Test templates handling."""
    assert process_templates("foo", wikicode, "el") == expected
