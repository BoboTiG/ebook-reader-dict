from typing import Callable, List

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


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
def test_parse_word(
    word: str,
    pronunciations: List[str],
    etymology: List[Definitions],
    definitions: List[Definitions],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "no")
    details = parse_word(word, code, "no", force=True)
    assert pronunciations == details.pronunciations
    assert etymology == details.etymology
    assert definitions == details.definitions


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        (
            "{{feilstaving av|førstvoterende|språk=no}}",
            "Feilstaving av førstvoterende.",
        ),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "no") == expected
