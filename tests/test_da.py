from typing import Callable, List

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, definitions, variants",
    [
        ("skulle", [], ["Er nødt til at gøre. Forpligtet til at gøre."], []),
        (
            "mus",
            [],
            [
                "(<i>zoologi</i>) pattedyr",
                "(<i>data</i>) en enhed som tilsluttes computere",
            ],
            [],
        ),
        (
            "hund",
            ["[ˈhunə-]", "[ˈhunˀ]"],
            [
                "(<i>zoologi</i>): et pattedyr af underarten <i>Canis lupus familiaris</i>.",
                "(<i>slang</i>): 100 DKK-seddel (bruges ikke i flertal)",
            ],
            [],
        ),
        ("jørme", [], ["vrimle, myldre; sværme"], []),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: List[str],
    definitions: List[Definitions],
    variants: List[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "da")
    details = parse_word(word, code, "da", force=True)
    assert pronunciations == details.pronunciations
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{form of|imperative form|bjerge|lang=da}}", "<i>imperative form of</i> <b>bjerge</b>"),
        ("{{term|mouse|lang=en}}", "mouse<sup>(en)</sup>"),
        ("{{fysik}}", "(<i>fysik</i>)"),
        ("{{u|de|Reis}}", "Reis<sup>(de)</sup>"),
        ("{{compound|hjemme|værn}}", "hjemme + værn"),
        ("{{trad|en|limnology}}", "limnology<sup>(en)</sup>"),
        ("{{en}}", "Engelsk"),
        ("{{suffix|Norden|isk|lang=da}}", "Norden + -isk"),
    ],
)
def test_process_template(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "da") == expected
