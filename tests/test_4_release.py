import os
from pathlib import Path
from typing import Any

import pytest

from wikidict import release

EXPECTED_INSTALL_TXT_FR = """Nombre de mots : 123 456 789
Export Wiktionnaire : 2020-02-20

Fichiers disponibles :

- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-fr.zip) (dicthtml-fr-fr.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.zip) (dict-fr-fr.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.df.bz2) (dict-fr-fr.df.bz2)

<sub>Mis à jour le """


def test_main(capsys: pytest.CaptureFixture[Any]) -> None:
    # Start the whole process
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    (output_dir / "words.count").write_text("123456789")
    (output_dir / "words.snapshot").write_text("20200220")

    try:
        assert release.main("fr") == 0
    finally:
        (output_dir / "words.count").unlink()
        (output_dir / "words.snapshot").unlink()

    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out.startswith(EXPECTED_INSTALL_TXT_FR)
