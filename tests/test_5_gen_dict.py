import os
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest

from wikidict import gen_dict


@pytest.mark.webtest
@pytest.mark.parametrize(
    "locale, words",
    [
        ("fr", "logiciel"),  # Single word
        ("fr", "base,logiciel"),  # Multiple words
        ("fr", "cercle unité"),  # Accentued word + space
        ("fro", "pui"),  # Sublang alone
        ("fr:fr", "logiciel"),  # Sublang falsy
        ("fr:fro", "pui"),  # Sublang
        ("fr:it", "glielo"),  # Another lang
        ("it:fr", "dodo"),  # Another lang
    ],
)
def test_gen_dict(locale: str, words: str, tmp_path: Path) -> None:
    with patch.dict(os.environ, {"CWD": str(tmp_path)}):
        for format in ["dictorg", "kobo", "mobi", "stardict"]:
            assert gen_dict.main(locale, words, str(uuid4()), format=format) == 0
