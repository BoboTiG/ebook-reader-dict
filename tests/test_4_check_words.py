from unittest.mock import patch

from wikidict import check_words, check_word, render


def test_errors():
    word_count = 39
    return_value = 42
    with patch.object(check_word, "main", return_value=return_value):
        assert (
            check_words.main("fr", word_count, True, "", "")
            == return_value * word_count
        )


def test_no_json_file():
    with patch.object(render, "get_latest_json_file", return_value=None):
        assert check_words.main("fr", 1, True, "", "") == 1


def test_all(tmp_path):
    file = tmp_path / "test.json"
    file.write_text('{"base":""}')
    with patch.object(render, "get_latest_json_file", return_value=file):
        assert check_words.main("fr", -1, False, "", "") == 0


def test_input(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("base\na")
    assert check_words.main("fr", -1, False, "a", f"{tmp_path}/test.txt") == 0


def test_numeric_offset(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("base\na")
    assert check_words.main("fr", -1, False, "5", f"{tmp_path}/test.txt") == 0


def test_simple():
    with patch.object(check_word, "main", return_value=0):
        assert check_words.main("fr", 1, True, "", "") == 0
