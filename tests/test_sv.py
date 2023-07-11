from typing import Callable, List

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, definitions, variants",
    [
        ("auto", [], ["automatisk; självgående", "automatiskt läge", "autostart"], []),
        (
            "en",
            ["/eːn/, /ɛn/, /en/"],
            [
                "ungefär; omkring",
                "obestämd artikel singular utrum",
                "objektsform av <i>man</i>",
                "<i>(vardagligt, dialektalt)</i> man",
                "<i>(dialektalt)</i> honom, 'an",
                "syftar tillbaka på det tidigare nämnda substantivet",
                "<i>(träd)</i> en vintergrön barrväxt, en buske eller ett träd med tätt "
                "grenverk och vassa barr, av arten <i>Juniperus communis</i> inom släktet "
                "enar (<i>Juniperus</i>) och familjen cypressväxter (Cupressaceae)",
            ],
            [],
        ),
        ("dufvor", [], [], ["dufva"]),
        ("harmonierar", [], [], ["harmoniera"]),
        (
            "-hörning",
            [],
            [
                "<i>(geometri, vardagligt)</i> <i>suffix för månghörningar</i>",
                "<i>suffix i ord som har med djurs horn att göra</i>",
            ],
            [],
        ),
        (
            "min",
            ["/miːn/", "/mɪn/"],
            [
                "possessivt pronomen som indikerar ägande av eller tillhörighet till den talande (jag) om det ägda eller tillhörande är i ental och har n-genus; possessivt pronomen i första person singular med huvudordet i singular utrum",  # noqa
                "ovanstående i självständig form",
                "reflexivt possessivt pronomen som syftar tillbaka på och indikerar ägande av eller tillhörighet till subjektet om subjektet är i första person singular (jag) och om det ägda eller tillhörande är i ental och har n-genus; reflexivt possessivt pronomen i första person singular med huvudordet i singular utrum",  # noqa
                "känslouttryck i ansiktet",
                "<i>förkortning för</i> minut",
                "<i>förkortning för</i> minimum",
            ],
            [],
        ),
        ("og", [], [], []),
        (
            "sand",
            ["/sand/"],
            [
                "sten som blivit till små korn, antingen genom väder och vind eller på konstgjord väg",
                "<i>(geologi)</i> jordart med kornstorlek mellan 0,06 och 2 mm",
            ],
            [],
        ),
        (
            "svenska",
            [],
            [
                "nordiskt språk som talas i Sverige och Finland (officiellt i båda länderna)",
                "svensk kvinna",
                "<i>(mindre brukligt)</i> tala svenska",
            ],
            ["svensk"],
        ),
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
    code = page(word, "sv")
    details = parse_word(word, code, "sv", force=True)
    assert pronunciations == details.pronunciations
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{led|sv|f|gata}}", "<i>förled tillhörigt ordet</i> gata"),
        ("{{led|sv|e|hand}}", "<i>efterled tillhörigt ordet</i> hand"),
        ("{{ö|en|test}}", "test"),
        ("{{ö+|en|test}}", "test <sup>(en)</sup>"),
        ("{{ö-inte|en|test}}", "<b>inte</b> <i><s>test</s></i>"),
        ("{{övrigatecken|punkt|.}}", '"<code>.</code>"'),
        ('{{övrigatecken|punkt|"}}', '"<code>"</code>"'),
        ("{{tagg|historia}}", "<i>(historia)</i>"),
        (
            "{{tagg|kat=nedsättande|text=något nedsättande}}",
            "<i>(något nedsättande)</i>",
        ),
        ("{{uttal|sv|ipa=mɪn}}", "<b>uttal:</b> /mɪn/"),
        ("{{uttal|sv|ipa=eːn/, /ɛn/, /en}}", "<b>uttal:</b> /eːn/, /ɛn/, /en/"),
    ],
)
def test_process_template(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "sv") == expected
