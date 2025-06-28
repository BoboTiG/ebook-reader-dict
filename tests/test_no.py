from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "aberrasjon",
            [],
            ["m"],
            [
                "Fra latin <i>aberrātiō</i> («lindring, avvikelse») , fra <i>aberrō</i> («gå unna/bort, gå vill»), fra <i>ab</i> («bort») + <i>errō</i> («vandre/gå»).",
                "Se aberrate.",
            ],
            {
                "Substantiv": [
                    "avvik, avvikelse",
                    "<i>(astronomi)</i> avvik i en stjernes avbildede posisjon relativ til dens sanne posisjon.",
                    "<i>(optikk)</i> avbildningsfeil i linser og speil.",
                    "<i>(biologi)</i> endring i et kromosom mens celledeling pågår.",
                ]
            },
            [],
        ),
        (
            "-bar",
            [],
            [],
            ["Fra nedertysk, egentlig «bærende»"],
            {
                "Suffiks": [
                    "suffiks som lager adjektiv av substantiv (<i>fruktbar</i>), verb (<i>sammenlignbar</i>) og adjektiv (<i>åpenbar</i>)"
                ]
            },
            [],
        ),
        (
            "bak lås og slå",
            [],
            [],
            [],
            {"Frase": ["<i>(om straffedømt)</i> i fengsel"]},
            [],
        ),
        (
            "bare",
            [],
            [],
            [],
            {
                "Adverb": [
                    "begrensende, kun",
                    "Gir dempende effekt",
                    "Gir forsterkende effekt",
                    "Gir en sitatfunksjon, særlig i muntlig språk.",
                ]
            },
            ["bar"],
        ),
        (
            "én svale gjør ingen sommer",
            [],
            [],
            [],
            {"Ordtak": ["Det at noen har vært observert én gang betyr ikke at det er en regel eller et sikkert tegn"]},
            [],
        ),
        (
            "et",
            [],
            [],
            [],
            {"Artikkel": ["artikkel for substantiv i ubestemt entall, av intetkjønn"]},
            ["ete"],
        ),
        (
            "funnet",
            [],
            [],
            [],
            {},
            ["finne", "funn"],
        ),
        (
            "gjente",
            [],
            [],
            [],
            {"Subjektiv": ["jente"]},
            [],
        ),
        (
            "hand",
            [],
            [],
            [],
            {
                "Substantiv": [
                    "<i>(anatomi)</i> kroppsdel ved enden av underarmen som gjør mennesker og aper i stand til å gripe",
                    "side",
                    "<i>(kortspill)</i> kortene en spiller sitter med",
                ]
            },
            [],
        ),
        (
            "Kiberg",
            [],
            [],
            [],
            {"Ordklasse": ["et tettsted i Vardø kommune i Finnmark"]},
            [],
        ),
        (
            "konsentrasjon",
            [],
            ["m"],
            ["Fra <i>konsentrere</i> + -<i>sjon</i>"],
            {
                "Substantiv": [
                    "Det å konsentrere seg; ha stort fokus på noe.",
                    "<i>(kjemi)</i> Andelen stoff i noe; mengde stoff løst pr. enhet.",
                ]
            },
            [],
        ),
        (
            "krokodille",
            [],
            ["m"],
            [
                "Fra middelalderlatin <i>cocodrillus</i> («krokodille»), fra gammelgresk κροκόδειλος (<i>krokodeilos</i>)"
            ],
            {"Substantiv": ["stort reptil, lever i og nær vann. <i>(lat. Crocodylia)</i>"]},
            [],
        ),
        (
            "liksom",
            [],
            [],
            [],
            {
                "Subjunksjon": [
                    "Antyder at noe er på lek, at man later som noe.",
                    "Antyder en sammenligning, brukes ofte som et slags fyllord, særlig i muntlig språk.",
                ]
            },
            [],
        ),
        (
            "lumpen",
            [],
            [],
            [],
            {"Adjektiv": ["tarvelig, nedrig"]},
            ["lump"],
        ),
        (
            "NS",
            [],
            [],
            [],
            {"Initialord": ["<i>initialord for</i> partiet Nasjonal Samling", "<i>initialord for</i> Norsk Standard"]},
            [],
        ),
        (
            "rasshol",
            [],
            ["n"],
            [],
            {
                "Interjeksjon": ["<i>(brukt som skjellsord)</i> utropsord med samme betydning som substantivet"],
                "Substantiv": ["anus; brukt som skjellsord"],
            },
            [],
        ),
        (
            "seg",
            [],
            [],
            ["Av norrønt <i>sik</i>."],
            {"Pronomen": ["refleksivt pronomen, tredje person entall og flertall"]},
            [],
        ),
        (
            "slå to fluer i en smekk",
            [],
            [],
            [],
            {"Idiom": ["<i>(idiomatisk)</i> få gjort to ting med én handling"]},
            [],
        ),
        (
            "sviger-",
            [],
            [],
            [],
            {"Prefiks": ["som befinner seg i inngiftet familie"]},
            [],
        ),
        (
            "tolvte",
            [],
            [],
            ["Fra norrønt <i>tolfti</i>; <i>tolv</i> + -<i>te</i>"],
            {"Tallord": ["ordenstallet til tolv"]},
            [],
        ),
        (
            "uten",
            [],
            [],
            [],
            {"Preposisjon": ["som ikke har;som mangler"]},
            [],
        ),
        (
            "verken",
            [],
            [],
            ["Fra gammeldansk: hwærki/hwærkin via dansk: hverken. Jamfør norrønt: hvárki."],
            {"Konjunksjon": ["danner sammen med eller en konjunksjon som binder sammen to nektinger"]},
            ["verk"],
        ),
        (
            "vg.",
            [],
            [],
            [],
            {"Forkortelse": ["forkortelse for <i>videregående</i>/<i>videregåande</i>"]},
            [],
        ),
        (
            "Øyvind",
            [],
            [],
            [],
            {"Egennavn": ["Norsk mannsnavn"]},
            [],
        ),
        (
            "ØNH",
            [],
            [],
            [],
            {"Forklaring": ["forkortelse for <i>øre-nese-hals</i>"]},
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
            "{{feilstaving av|førstvoterende|språk=no}}",
            "Feilstaving av førstvoterende.",
        ),
        ("{{l|no|god, snill}}", "god, snill"),
        ("{{opphav|norrønt|språk=no}}", "norrønt"),
        ("{{prefiks|a|biotisk|språk=no}}", "<i>a</i>- + <i>biotisk</i>"),
        ("{{qualifier|idiomatisk}}", "<i>(idiomatisk)</i>"),
        ("{{suffiks|konsentrere|sjon|språk=no}}", "<i>konsentrere</i> + -<i>sjon</i>"),
        ("{{Sup|1}}", "<sup>1</sup>"),
        ("{{teleskopord|nei|ja|språk=no}}", "teleskopord sammensatt av nei og ja"),
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
            "<i>tidligere skriveform av</i> <b>naturlig tall</b>",
        ),
        ("{{urspråk|germansk|daigjōn}}", "urgermansk *daigjōn"),
        ("{{vokabular|overført}}", "<i>(overført)</i>"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "no") == expected
