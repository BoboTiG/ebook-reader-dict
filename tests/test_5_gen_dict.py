import pytest

from wikidict import gen_dict


@pytest.mark.parametrize(
    "locale, words, format",
    [
        ("fr", "logiciel", "kobo"),
        ("fr", "base,logiciel", "kobo"),
        ("fr", "logiciel", "stardict"),
    ],
)
def test_gen_dict(locale, words, format, tmp_path):
    res = gen_dict.main(locale, words, tmp_path, format=format)
    assert res == 0
