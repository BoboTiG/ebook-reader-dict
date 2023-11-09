from typing import Callable, List

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "bare",
            [],
            [],
            [],
            [
                "begrensende, kun",
                "Gir dempende effekt",
                "Gir forsterkende effekt",
                "Gir en sitatfunksjon, særlig i muntlig språk.",
            ],
            ["bar"],
        ),
        (
            "funnet",
            [],
            [],
            [],
            [],
            ["finne", "funn"],
        ),
        (
            "konsentrasjon",
            [],
            ["m"],
            ["Fra <i>konsentrere</i> + -<i>sjon</i>"],
            [
                "Det å konsentrere seg; ha stort fokus på noe.",
                "<i>(kjemi)</i> Andelen stoff i noe; mengde stoff løst pr. enhet.",
            ],
            [],
        ),
        (
            "lumpen",
            [],
            [],
            [""],
            ["tarvelig, nedrig"],
            ["lump"],
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
    code = page(word, "no")
    details = parse_word(word, code, "no", force=True)
    assert pronunciations == details.pronunciations
    assert genders == details.genders
    assert etymology == details.etymology
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{alternativ skrivemåte|be}}", "<i>alternativ skrivemåte av</i> <b>be</b>"),
        (
            "{{bøyningsform|no|sub|korp}}",
            "<i>bøyningsform av</i> <b>korp</b>",
        ),
        (
            "{{feilstaving av|førstvoterende|språk=no}}",
            "Feilstaving av førstvoterende.",
        ),
        ("{{l|no|god, snill}}", "god, snill"),
        ("{{opphav|norrønt|språk=no}}", "norrønt"),
        ("{{prefiks|a|biotisk|språk=no}}", "<i>a</i>- + <i>biotisk</i>"),
        ("{{qualifier|idiomatisk}}", "<i>(idiomatisk)</i>"),
        ("{{suffiks|konsentrere|sjon|språk=no}}", "<i>konsentrere</i> + -<i>sjon</i>"),
        (
            "{{tidligere bøyningsform|no|sub|jul}}",
            "<i>tidligere bøyningsform av</i> <b>jul</b>",
        ),
        (
            "{{tidligere skriveform|no|kunstnarleg}}",
            "<i>tidligere skriveform av</i> <b>kunstnarleg</b>",
        ),
        (
            "{{tidligere skrivemåte|no|naturlig tall}}",
            "<i>tidligere skrivemåte av</i> <b>naturlig tall</b>",
        ),
        ("{{vokabular|overført}}", "<i>(overført)</i>"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "no") == expected
