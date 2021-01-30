from unittest.mock import patch

from wikidict import check_word


def test_simple():
    assert check_word.main("fr", "vendre") == 0


def test_sublist():
    assert check_word.main("fr", "éperon") == 0


def test_error():
    with patch.object(check_word, "contains", return_value=False):
        assert check_word.main("fr", "42") > 0


def test_no_definition_nor_etymology():
    assert check_word.main("es", "42") == 0


def test_filter_anchors():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += '<a href="#cite">[1]</a>'
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_es():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += "<dl><dt>1 Finanzas.</dt></dl>"
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("es", "cartel") == 0


def test_filter_fr_refnec():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += '<span><sup><i><b>Référence nécessaire</b></i></sup></span><span id="refnec"></span>'
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_obsolete_tpl():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += "<span id='FormattingError'>bouh !</span>"
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0
