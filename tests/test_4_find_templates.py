from unittest.mock import patch

from wikidict import find_templates


def test_simple() -> None:
    assert find_templates.main("fr") == 0


def test_no_json_file() -> None:
    with patch.object(find_templates, "get_latest_json_file", return_value=None):
        assert find_templates.main("fr") == 1


def test_no_sections() -> None:
    words = {"foo": ""}
    find_templates.find_templates(words, "fr")


def test_no_templates() -> None:
    code = "\n".join(
        """
== {{langue|conv}} ==
=== {{S|numéral|conv}} ===
'''42'''
""".splitlines()
    ).strip()
    words = {"foo": code}
    find_templates.find_templates(words, "fr")
