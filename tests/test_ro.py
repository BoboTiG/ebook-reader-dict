from typing import Callable, List

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, etymology, definitions, variants",
    [
        (
            "aventurierul",
            ["/a.ven.tu.riˈe.rul/"],
            ["Din <i>aventurier</i>."],
            [],
            ["aventurier"],
        ),
        (
            "cânta",
            ["/kɨnˈta/"],
            ["Din latină <i>cantare</i>."],
            [
                "(<i>v.intranz. și tranz.</i>) a emite cu vocea sau cu un instrument un șir de sunete muzicale care se rânduiesc într-o melodie, într-un acord etc.",  # noqa
                "(<i>despre păsări, insecte etc.</i>) a scoate sunete plăcute la auz. caracteristice speciei.",
                "(<i>v.intranz. și tranz.</i>) a scrie versuri în cinstea cuiva sau a ceva, a elogia (în versuri) pe cineva sau ceva; a descrie, a povesti ceva în versuri.",  # noqa
                "(<i>v.tranz.</i>) (<i>fam.</i>) a îndruga, a înșira vorbe goale.",
            ],
            [],
        ),
        ("frumoasă", ["/fru'mo̯a.sə/"], ["Din <i>frumos</i>."], [], ["frumos"]),
        ("frumoși", ["[fruˈmoʃʲ]"], [], [], ["frumos"]),
        (
            "paronim",
            ["/pa.ro'nim/"],
            [
                "Din franceză <i>paronyme</i>, latină <i>paronymon</i>, originar format din greacă παρα + <b>ονομα</b> -onym"  # noqa
            ],
            [
                "cuvânt asemănător cu altul din punctul de vedere al formei, dar deosebit de acesta ca sens (și ca origine).",  # noqa
                "cuvânt care se aseamănă parțial cu altul din punctul de vedere al formei, dar se deosebește ca sens de acesta.",  # noqa
            ],
            [],
        ),
        ("portocale", ["/por.toˈka.le/"], ["Din <i>portocală</i>."], [], ["portocală"]),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: List[str],
    etymology: List[Definitions],
    definitions: List[Definitions],
    variants: List[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "ro")
    details = parse_word(word, code, "ro", force=True)
    assert pronunciations == details.pronunciations
    assert etymology == details.etymology
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{n}}", "<i>n.</i>"),
        ("{{p}}", "<i>pl.</i>"),
        ("{{trad|el|παρα}}", "παρα"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "ro") == expected
