from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import pytest
from wikitextparser import Section

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


def test_render_word_sv_with_almost_empty_definition(page: Callable[[str, str], str]) -> None:
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


def test_find_section_definitions_and_es_replace_defs_list_with_numbered_lists() -> None:
    section = Section(
        "=== {{sustantivo propio|es|género=femenino}} ===\n"
        ";1 archipiélago de 2&nbsp;000 peñascos.\n"
        ";2 países: país ubicado en el archipiélago anterior.\n"
        ";301 Lingüística:\n"
        ":;a: vocablo que titula un artículo de diccionario.\n\n\n"
        ":;b: artículo de un diccionario, enciclopedia u obra de referencia."
    )
    definitions = render.find_section_definitions("Bahamas", section, "es")
    assert definitions == [
        "archipiélago de 2&nbsp;000 peñascos.",
        "países: país ubicado en el archipiélago anterior.",
        "Lingüística:",
        (
            "vocablo que titula un artículo de diccionario.",
            "artículo de un diccionario, enciclopedia u obra de referencia.",
        ),
    ]


@pytest.mark.parametrize(
    "locale, code, expected",
    [
        (
            "de",
            "{{Bedeutungen}}\n:[1] \n\n{{Herkunft}}\n:[[Abkürzung]] von [[Sturmkanone]]",
            "=== {{Bedeutungen}} ===\n# \n\n=== {{Herkunft}} ===\n:[[Abkürzung]] von [[Sturmkanone]]",
        ),
        (
            "de",
            "{{Bedeutungen}}\n:[1] {{K|Handwerk|Architektur|ft=[[defektives Verb{{!}}defektiv]]}}",
            "=== {{Bedeutungen}} ===\n# {{K|Handwerk|Architektur|ft=[[defektives Verb|defektiv]]}}",
        ),
        (
            "it",
            "== {{-it-}} ==\n{{-agg form-|it}}",
            "== {{-it-}} ==\n=== {{agg form}} ===",
        ),
        (
            "it",
            "== {{-it-}} ==\n{{-agg form-|fr}}",
            "== {{-it-}} ==\n=== {{agg form|fr}} ===",
        ),
        (
            "it",
            "== {{-it-}} ==\n{{-etim-}}\n{{Vd|nero{{!}}nero}}",
            "== {{-it-}} ==\n=== {{etim}} ===\n{{Vd|nero|nero}}",
        ),
    ],
)
def test_adjust_wikicode(locale: str, code: str, expected: str) -> None:
    assert render.adjust_wikicode(code, locale) == expected
