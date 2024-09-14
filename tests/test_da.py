from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, etymology, definitions, variants",
    [
        (
            "bakterie",
            [],
            [
                "fra latin <i>bacterium</i>, latinisering af græsk <i>bakterion</i> (βακτήριον\xa0- lille stav), diminutiv af <i>baktron</i> (βάκτρον - stav)"
            ],
            ["(mikrobiologi) en encellet mikroskopisk organisme uden cellekerne"],
            [],
        ),
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
        ("PMV", [], [], ["<i>(militær)</i> <i>Forkortelse af</i> <b>pansret mandskabsvogn</b>"], []),
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
        ("{{form of|imperative form|bjerge|lang=da}}", "<i>imperative form of</i> <b>bjerge</b>"),
        ("{{fysik}}", "(<i>fysik</i>)"),
        ("{{label|militær|våben}}", "(<i>militær</i>, <i>våben</i>)"),
        ("{{trad|en|limnology}}", "limnology<sup>(en)</sup>"),
        ("{{ZHchar|北京}}", "北京"),
    ],
)
def test_process_template(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "da") == expected
