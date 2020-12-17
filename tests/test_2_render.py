from unittest.mock import patch

import pytest

from wikidict import render


def test_simple():
    assert render.main("fr") == 0


def test_no_json_file():
    with patch.object(render, "get_latest_json_file", return_value=None):
        assert render.main("fr") == 1


def test_empty_json_file(tmp_path):
    file = tmp_path / "test.json"
    file.write_text("{}")
    with patch.object(render, "get_latest_json_file", return_value=file):
        with pytest.raises(ValueError):
            render.main("fr")


def test_render_word(page):
    word = ["π", page("π", "fr")]
    words = {}
    render.render_word(word, words, "fr")
    assert words["π"]
