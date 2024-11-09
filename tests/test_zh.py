from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "七講八講",
            [],
            [],
            [],
            [
                "(漳泉話，吳語) 亂講、胡說",
                "(柳州官話) 用各種方式解釋",
            ],
            [],
        ),
        (
            "稍後",
            [],
            [],
            [],
            [
                "在短暫的時間之後",
                "稍候的拼寫錯誤。",
            ],
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
    code = page(word, "zh")
    details = parse_word(word, code, "zh", force=True)
    assert pronunciations == details.pronunciations
    assert genders == details.genders
    assert etymology == details.etymology
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{abbreviation of|zh|留名}}", "留名之縮寫。"),
        ("{{gloss|對患者}}", "（對患者）"),
        ("{{gl|對患者}}", "（對患者）"),
        ("{{misspelling of|zh|稍候}}", "稍候的拼寫錯誤。"),
        ("{{n-g|用來表示全範圍}}", "用來表示全範圍"),
        ("{{non-gloss definition|用來表示全範圍}}", "用來表示全範圍"),
        ("{{qual|前句常有“一方面”……}}", "(前句常有“一方面”……)"),
        ("{{qualifier|前句常有“一方面”……}}", "(前句常有“一方面”……)"),
    ],
)
def test_process_template(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "zh") == expected
