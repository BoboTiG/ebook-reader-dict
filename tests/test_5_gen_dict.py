from uuid import uuid4

import pytest

from wikidict import gen_dict


@pytest.mark.parametrize(
    "locale, words",
    [
        ("fr", "logiciel"),  # Single word
        ("fr", "base,logiciel"),  # Multiple words
        ("fr", "cercle unité"),  # Accentued word + space
    ],
)
@pytest.mark.parametrize("format", ["kobo", "stardict"])
def test_gen_dict(locale: str, words: str, format: str) -> None:
    res = gen_dict.main(locale, words, str(uuid4()), format=format)
    assert res == 0
