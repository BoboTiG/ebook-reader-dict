from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "♍",
            [],
            [],
            [],
            {"Signifo": ["<i>(astrologio)</i> zodiaka signo de Virgulino (<i>Virgo</i>)"]},
            [],
        ),
        (
            "💀",
            [],
            [],
            [],
            {"Signifo": ["morto"]},
            [],
        ),
        (
            "alkazabo",
            [],
            [],
            ["el la andalus-araba <i>alqaṣába</i>, kaj tiu ĉi el la klasika araba <i>qaṣabah</i>, قصبة"],
            {
                "Signifo": [
                    "<i>(historio; arkitekturo; militado)</i> fortikita konstruaĵaro; citadelo aŭ palaco de araba ĉefo en Nord-Afriko kaj Suda-Hispanio"
                ]
            },
            [],
        ),
        (
            "ekamus",
            [],
            [],
            [],
            {},
            ["ekami"],
        ),
        (
            "kaskedo",
            ["kasked/o"],
            [],
            [],
            {
                "Signifo": [
                    "Ĉapo kun viziero, civilvesta aŭ uniforma: <i>homoj armitaj en nigraj kaskedetoj; la hotela pordisto levis sian kaskedon.</i>"
                ]
            },
            [],
        ),
        (
            "komputilo",
            [],
            [],
            [],
            {
                "Signifo": [
                    "<i>(komputado)</i> maŝino aŭ elektronikaĵo kiu kapablas kalkuli, precipe sen intervenoj de homoj, aŭ rapide trakti, stori, kaj preni larĝajn kvantojn de datumo"
                ]
            },
            [],
        ),
        (
            "latina",
            [],
            [],
            ["De Latino"],
            {"Adjektivo": ["rilata al Latino."]},
            [],
        ),
        (
            "luko",
            ["luk/o"],
            [],
            ["el la germana <i>Luke</i>"],
            {
                "Signifo": [
                    "ordinare vitrita aŭ kradita, en tegmento, plafono aŭ kelo, por enlasi lumon: <i>mansarda luko</i>.",
                    "fermebla per pordo aŭ tabuloj, en la ferdeko de ŝipo, por ebligi penetron en la holdon (pli precize: holdluko).",
                    "fermita per kovrilo el giso, kiu en la strato, sur trotuaro ks ebligas al metiisto malsupreniri en kloakon, aŭ subteran galerion.",
                ]
            },
            [],
        ),
        (
            "Teodoriko",
            [],
            ["m"],
            [],
            {},
            [],
        ),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: list[str],
    genders: list[str],
    etymology: list[Definitions],
    definitions: list[Definitions],
    variants: list[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "eo")
    details = parse_word(word, code, "eo", force=True)
    assert pronunciations == details.pronunciations
    assert genders == details.genders
    assert etymology == details.etymology
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{fina|o}}", "o"),
        ("{{inte|o}}", "o"),
        ("{{lite|ŭ}}", "ŭ"),
        ("{{mems|du}}", "du"),
        ("{{pref|mis}}", "mis"),
        ("{{radi|vort}}", "vort"),
        ("{{sufi|il}}", "il"),
        ("{{Vortospeco|mona nomo|eo}}", "Mona nomo"),
        ("{{📷}}", "📷 <i>fotografio kaj kinotekniko</i>"),
    ],
)
def test_process_template(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "eo") == expected
