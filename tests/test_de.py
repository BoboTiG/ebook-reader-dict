import pytest

from wikidict.render import parse_word
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "CIA",
            ["[siːaɪ̯ˈɛɪ̯]"],
            ["mf"],
            ["Abkürzung von Central Intelligence Agency"],
            ["US-amerikanischer Auslandsnachrichtendienst"],
            [],
        ),
        (
            "volley",
            ["[ˈvɔli]", "[ˈvɔle]", "[ˈvɔlɛɪ̯]"],
            [],
            [
                "Dem seit 1960 im Duden lexikalisierten Wort liegt die englische Kollokation <i>at/on the <i>volley</i></i> ‚aus der Luft‘ zugrunde.",  # noqa
            ],
            [
                "<i>Sport:</i> aus der Luft (angenommen und direkt kraftvoll abgespielt), ohne dass eine Bodenberührung des Sportgeräts vorher stattgefunden hat",  # noqa
            ],
            [],
        ),
        ("trage", ["[ˈtʁaːɡə]"], [], [], [], ["tragen"]),
        ("daß", [], [], [], [], ["dass"]),
    ],
)
def test_parse_word(
    word, pronunciations, genders, etymology, definitions, variants, page
):
    """Test the sections finder and definitions getter."""
    code = page(word, "de")
    details = parse_word(word, code, "de", force=True)
    assert pronunciations == details.pronunciations
    assert genders == details.genders
    assert etymology == details.etymology
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{Ü|pl|dzień}}", "<i>dzień</i>"),
        ("{{übertr.}}", "<i>übertragen</i>"),
        ("{{übertr.|:}}", "<i>übertragen:</i>"),
    ],
)
def test_process_templates(wikicode, expected):
    """Test templates handling."""
    assert process_templates("foo", wikicode, "de") == expected
