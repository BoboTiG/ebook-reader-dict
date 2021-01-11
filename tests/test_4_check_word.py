from unittest.mock import patch

from wikidict import check_word


def test_simple():
    assert check_word.main("fr", "vendre") == 0


def test_sublist():
    assert check_word.main("fr", "éperon") == 0


def test_error():
    with patch.object(check_word, "contains", return_value=False):
        assert check_word.main("fr", "42") > 0


def test_filter_obsolete_tpl():
    orig = check_word.filter_html

    def new_filter_html(html: str) -> str:
        html += "<span id='FormattingError'>bouh !</span>"
        return orig(html)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0
