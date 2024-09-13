from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, definitions, variants",
    [
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
        (
            "mus",
            [],
            [
                "(<i>zoologi</i>) pattedyr",
                "(<i>data</i>) en enhed som tilsluttes computere",
            ],
            [],
        ),
        ("skulle", [], ["Er nødt til at gøre. Forpligtet til at gøre."], []),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: list[str],
    definitions: list[Definitions],
    variants: list[str],
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
        ("{{compound|hjemme|værn|langa=da}}", "hjemme + værn"),
        ("{{en}}", "Engelsk"),
        ("{{form of|imperative form|bjerge|lang=da}}", "<i>imperative form of</i> <b>bjerge</b>"),
        ("{{fysik}}", "(<i>fysik</i>)"),
        ("{{init of|lang=da|København}}", "<i>Initialforkortelse af</i> <b>København</b>"),
        ("{{initialism of|lang=da|København}}", "<i>Initialforkortelse af</i> <b>København</b>"),
        ("{{label|militær|våben}}", "(<i>militær</i>, <i>våben</i>)"),
        ("{{suffix|Norden|isk|lang=da}}", "Norden + -isk"),
        ("{{term|mouse|lang=en}}", "mouse<sup>(en)</sup>"),
        ("{{trad|en|limnology}}", "limnology<sup>(en)</sup>"),
        ("{{u|de|Reis}}", "Reis<sup>(de)</sup>"),
    ],
)
def test_process_template(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "da") == expected
