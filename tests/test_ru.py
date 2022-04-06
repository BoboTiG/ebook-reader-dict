#Run python -Wd -m pytest tests --doctest-modules wikidict

import pytest

from wikidict.render import parse_word
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, gender, etymology, definitions, variants",
    [
        (
            "страница",
            ["\\страни\\"],
            "f",
            [
                "Происходит от страна, из церк.-слав. страна, далее из праслав. *storna, от кот. в числе прочего произошли: др.-русск. сторона, ст.-слав. страна (др.-греч. χώρα, περίχωρος), русск., укр. сторона́, болг. страна́, сербохорв. стра́на (вин. стра̑ну), словенск. strána, чешск., словацк. strana, польск. strona, в.-луж., н.-луж. strona, полабск. stárna"
            ],
            [
                "одна из сторон листа бумаги в составе книги, газеты и т. п.",
                "написанный или напечатанный текст на такой стороне листа",
                "лист бумаги в составе книги, газеты и т. п.. (Пример: Мне захотелось вырвать страницу, чтоб этого страшного никогда не случилось)",
                "(Комп.) отдельный документ в составе интернет-сайта",
                "(П.) очередной этап в развитии чего-либо. (Пример: Голографический микроскоп откроет новую (Выдел) в исследовании живых клеток.)",
                "(Информ.) блок, регион фиксированного размера физической или виртуальной памяти (выделение памяти, передача данных между диском и оперативной памятью осуществляется целыми страницами)",
            ],
            [],
        ),
    ],
)
def test_parse_word(
    word, pronunciations, gender, etymology, definitions, variants, page
):
    """Test the sections finder and definitions getter."""
    code = page(word, "ru")
    details = parse_word(word, code, "ru", force=True)
    assert pronunciations == details.pronunciations
    assert gender == details.gender
    assert definitions == details.definitions
    assert etymology == details.etymology
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        (
            "{{этимология:страница|да}}",
            "страна, из церк.-слав. страна, далее из праслав. *storna, от кот. в числе прочего произошли: др.-русск. сторона, ст.-слав. страна (др.-греч. χώρα, περίχωρος), русск., укр. сторона́, болг. страна́, сербохорв. стра́на (вин. стра̑ну), словенск. strána, чешск., словацк. strana, польск. strona, в.-луж., н.-луж. strona, полабск. stárna",
        ),
    ],
)
def test_process_templates(wikicode, expected):
    """Test templates handling."""
    assert process_templates("foo", wikicode, "ru") == expected
