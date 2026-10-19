from collections import OrderedDict
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import pytest

from wikidict import context
from wikidict.render import parse_word
from wikidict.stubs import Definitions

LANG = __name__.split("_", 1)[1]


@pytest.fixture(scope="module", autouse=True)
def setup_lua_ctx() -> None:
    with patch.dict("os.environ", {"CWD": str(Path(context.__file__).parent.parent)}):
        assert context.reset(LANG)


@pytest.mark.parametrize(
    "word, pronunciations, etymology, definitions, variants, reverse_variants",
    [
        (
            "България",
            [],
            ['"българ" + "-ия". За народното име виж корена.'],
            {
                "Съществително Собствено Име|ж.": [
                    "Държава в Югоизточна Европа. Официално име: <i>Република България</i>."
                ]
            },
            [],
            [],
        ),
        (
            "давя",
            [],
            [],
            {
                "Глагол": [
                    "стремя се да причиня смърт чрез прекъсване на дишането, задушавам, обикн. чрез потапяне във вода",
                    (
                        "не мога да плувам. <i>Някой се дави там, жалко, че водоемът е неохраняем.</i>",
                        "заседнала ми е храна, задавям се",
                    ),
                ],
                "Синоними": [
                    "душа, удушавам, задушавам, задавям",
                    "потъпквам, подтискам, удавям, умъртвявам, убивам",
                    "хапя, ръфам",
                ],
            },
            [],
            [],
        ),
        (
            "карам",
            [],
            [
                "от къснолат. *<i>carriare</i>, произв. от <i>carrus</i> „кола“, срв. рум. <i>cărа</i>, итал. диал. <i>carriare</i> (калабр.), <i>carreare</i> (неап.), фр. <i>charrier</i> „возя, превозвам, извозвам (c кола)“.",
                "праслав. *<i>karati</i> „ругая, хокам“ е сродно с лат. <i>carināre</i> „използвам неприличен език“, ст.в.нем. <i>harawēn</i> „подигравам“, от ИЕ *<i>kōr</i>-.",
            ],
            {
                "Синоними": [
                    (
                        "возя, тегля, влача, дърпам, издърпвам, изтеглям, отвеждам, "
                        "откарвам, водя, бутам, тикам, подкарвам, закарвам, завеждам"
                    ),
                    "принуждавам, насилвам, заставям, задължавам, натоварвам, накарвам, подтиквам",
                    "почвам, започвам, начевам, захващам",
                    "докарвам, превозвам",
                    "изкарвам, отбивам, излежавам",
                    "подбуждам, пришпорвам",
                    "прекарвам",
                    "тласкам, движа, предвижвам",
                    "убеждавам, увещавам, предумвам, скланям",
                    "управлявам",
                    "насочвам, направлявам",
                ],
            },
            [],
            [],
        ),
        (
            "неологизъм",
            [],
            ["От гр. νέος „нов“ + λόγος „дума“."],
            {
                "Съществително Нарицателно Име|м.": [
                    "<i>езикозн.</i> Дума или израз, създаден за обозначаване на ново понятие или за даване на ново наименование на вече съществуващо явление."
                ]
            },
            [],
            [],
        ),
        (
            "изменнически",
            [],
            [],
            {
                "Синоними": ["коварен, вероломен, неверен, предателски", "подъл"],
            },
            [],
            [],
        ),
        ("кума", [], [], {}, ["кум"], []),
        ("паса", [], [], {}, ["пас"], []),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: list[str],
    etymology: list[Definitions],
    definitions: Definitions,
    variants: list[str],
    reverse_variants: list[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    print(f"{word = }")
    code = page(word, LANG)
    details = parse_word(word, code, LANG, force=True)
    assert details
    assert pronunciations == details.pronunciations
    assert etymology == details.etymology
    assert OrderedDict(definitions) == details.definitions
    assert variants == details.variants
    assert reverse_variants == details.reverse_variants

    assert not context.get_then_clear_errors()
