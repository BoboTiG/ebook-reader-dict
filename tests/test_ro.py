from typing import Callable, List

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, etymology, definitions, variants",
    [
        (
            "paronim",
            [
                "/pa.ro'nim/",
            ],
            [
                "Din franceză <i>paronyme</i>, latină <i>paronymon</i>, originar format din greacă παρα + <b>ονομα</b> -onym"  # noqa
            ],
            [
                "cuvânt asemănător cu altul din punctul de vedere al formei, dar deosebit de acesta ca sens (și ca origine).",  # noqa
                "cuvânt care se aseamănă parțial cu altul din punctul de vedere al formei, dar se deosebește ca sens de acesta.",  # noqa
            ],
            [],
        ),
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
    [],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "ro") == expected
