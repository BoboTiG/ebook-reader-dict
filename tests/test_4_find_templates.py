from unittest.mock import patch

from wikidict import find_templates


def test_simple():
    assert find_templates.main("fr") == 0


def test_no_json_file():
    with patch.object(find_templates, "get_latest_json_file", return_value=None):
        assert find_templates.main("fr") == 1


def test_no_sections():
    words = {"foo": ""}
    find_templates.find_templates(words, "fr")


def test_no_templates():
    code = "\n".join(
        """
== {{langue|conv}} ==
=== {{S|numéral|conv}} ===
'''42'''
""".splitlines()
    ).strip()
    words = {"foo": code}
    find_templates.find_templates(words, "fr")
