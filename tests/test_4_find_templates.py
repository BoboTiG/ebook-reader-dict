from unittest.mock import patch

from wikidict import find_templates


def test_simple():
    assert find_templates.main("fr") == 0


def test_no_json_file():
    with patch.object(find_templates, "get_latest_json_file", return_value=None):
        assert find_templates.main("fr") == 1
