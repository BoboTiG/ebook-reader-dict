from unittest.mock import patch

from wikidict import check_random_words, check_word, render


def test_errors():
    with patch.object(check_word, "main", return_value=42):
        assert check_random_words.main("fr", 100) == 4200


def test_no_json_file():
    with patch.object(render, "get_latest_json_file", return_value=None):
        assert check_random_words.main("fr", 1) == 1


def test_simple():
    with patch.object(check_word, "main", return_value=0):
        assert check_random_words.main("fr", 1) == 0
