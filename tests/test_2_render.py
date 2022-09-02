from unittest.mock import patch

import pytest

from wikidict import render


def test_simple():
    assert render.main("fr") == 0
    assert render.main("fr", workers=0) == 0
    assert render.main("fr", workers=2) == 0


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


def test_render_word_sv_with_almost_empty_definition(page):
    word = ["Götet", page("Götet", "sv")]
    words = {}
    render.render_word(word, words, "sv")
    assert words["Götet"]


def test_render_word_with_empty_subdefinition(page):
    word = ["test", page("tests-definitions", "fr")]
    words = {}
    render.render_word(word, words, "fr")
    word = words["test"]

    defs = word.definitions
    assert len(defs) == 2
    assert isinstance(defs[0], str)
    assert isinstance(defs[1], tuple)

    subdefs = defs[1]
    assert len(subdefs) == 2
    assert isinstance(subdefs[0], str)
    assert isinstance(subdefs[1], tuple)

    subsubdefs = subdefs[1]
    assert len(subsubdefs) == 1
    assert isinstance(subsubdefs[0], str)
    assert subsubdefs[0]
