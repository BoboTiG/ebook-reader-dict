from typing import Callable, List

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "λαμβάνω",
            ["/laɱˈva.no/"],
            [],
            [
                "<b>λαμβάνω</b> < (διαχρονικό δάνειο) <i>αρχαία ελληνική</i> λαμβάνω < <i>(Ετυμ)</i> *<i>sleh₂gʷ</i>-"
            ],
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
    word: str,
    pronunciations: List[str],
    genders: List[str],
    etymology: List[Definitions],
    definitions: List[Definitions],
    variants: List[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "el")
    details = parse_word(word, code, "el", force=True)
    assert pronunciations == details.pronunciations
    assert genders == details.genders
    assert definitions == details.definitions
    assert etymology == details.etymology
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [("{{resize|Βικιλεξικό|140}}", '<span style="font-size:140%;">Βικιλεξικό</span>')],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "el") == expected
