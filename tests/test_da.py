from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, etymology, definitions, variants",
    [
        (
            "hund",
            ["[ˈhunə-]", "[ˈhunˀ]"],
            [
                "Menes at stamme fra indoeuropæisk sprog <i>ḱʷn̥tós</i>, fra <i>ḱwṓ</i> og derfra videre til germansk sprog <i>*hundaz</i> og fra oldnordisk hundr."
            ],
            [
                "(<i>zoologi</i>): et pattedyr af underarten <i>Canis lupus familiaris</i>.",
                "(<i>slang</i>): 100 DKK-seddel (bruges ikke i flertal)",
            ],
            [],
        ),
        ("jørme", [], [], ["vrimle, myldre; sværme"], []),
        (
            "mus",
            [],
            [
                "Fra oldnordisk mús.",
                "Fra engelsk mouse.",
            ],
            [
                "(<i>zoologi</i>) pattedyr",
                "(<i>data</i>) en enhed som tilsluttes computere",
            ],
            [],
        ),
        ("skulle", [], [], ["Er nødt til at gøre. Forpligtet til at gøre."], []),
        ("PMV", [], [], ["<i>(militær)</i> <i>Forkortelser på</i> <b>pansret mandskabsvogn</b>"], []),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: list[str],
    etymology: list[Definitions],
    definitions: list[Definitions],
    variants: list[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "da")
    details = parse_word(word, code, "da", force=True)
    assert pronunciations == details.pronunciations
    assert definitions == details.definitions
    assert etymology == details.etymology
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{abbr of|lang=da|pansret mandskabsvogn}}", "<i>Forkortelser på</i> <b>pansret mandskabsvogn</b>"),
        ("{{abbreviation of|lang=da|pansret mandskabsvogn}}", "<i>Forkortelser på</i> <b>pansret mandskabsvogn</b>"),
        ("{{com|hjemme|værn|langa=da}}", "hjemme + værn"),
        ("{{compound|hjemme|værn|langa=da}}", "hjemme + værn"),
        ("{{form of|imperative form|bjerge|lang=da}}", "<i>imperative form of</i> <b>bjerge</b>"),
        ("{{fysik}}", "(<i>fysik</i>)"),
        ("{{init of|lang=da|København}}", "<i>Initialforkortelse af</i> <b>København</b>"),
        ("{{initialism of|lang=da|København}}", "<i>Initialforkortelse af</i> <b>København</b>"),
        ("{{label|militær|våben}}", "(<i>militær</i>, <i>våben</i>)"),
        ("{{suf|Norden|isk|lang=da}}", "Norden + -isk"),
        ("{{suffix|Norden|isk|lang=da}}", "Norden + -isk"),
        ("{{trad|en|limnology}}", "limnology<sup>(en)</sup>"),
        ("{{u|de|Reis}}", "Reis<sup>(de)</sup>"),
    ],
)
def test_process_template(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "da") == expected
