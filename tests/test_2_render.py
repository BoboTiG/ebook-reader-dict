from pathlib import Path
from typing import Callable
from unittest.mock import patch

import pytest

from wikidict import render
from wikidict.stubs import Word, Words


def test_simple() -> None:
    assert render.main("fr") == 0
    assert render.main("fr", workers=0) == 0
    assert render.main("fr", workers=2) == 0


def test_no_json_file() -> None:
    with patch.object(render, "get_latest_json_file", return_value=None):
        assert render.main("fr") == 1


def test_empty_json_file(tmp_path: Path) -> None:
    file = tmp_path / "test.json"
    file.write_text("{}")
    with patch.object(render, "get_latest_json_file", return_value=file):
        with pytest.raises(ValueError):
            render.main("fr")


def test_render_word(page: Callable[[str, str], str]) -> None:
    word = ["π", page("π", "fr")]
    words: Words = {}
    render.render_word(word, words, "fr")
    assert words["π"]


def test_render_word_sv_with_almost_empty_definition(
    page: Callable[[str, str], str]
) -> None:
    word = ["Götet", page("Götet", "sv")]
    words: Words = {}
    render.render_word(word, words, "sv")
    assert words["Götet"]


def test_render_word_with_empty_subdefinition(page: Callable[[str, str], str]) -> None:
    words: Words = {}
    render.render_word(["test", page("tests-definitions", "fr")], words, "fr")
    word: Word = words["test"]

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
