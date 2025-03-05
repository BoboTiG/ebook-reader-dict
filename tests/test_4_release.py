import os
from pathlib import Path
from typing import Any

import pytest

from wikidict import release

EXPECTED_INSTALL_TXT_FR = """Nombre de mots : 123 456 789
Export Wiktionnaire : 2020-02-20

Version complète :
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dictorg-fr-fr.zip) (dictorg-fr-fr.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.df.bz2) (dict-fr-fr.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.mobi) (dict-fr-fr.mobi)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-fr.zip) (dicthtml-fr-fr.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.zip) (dict-fr-fr.zip)

Version sans étymologies :
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dictorg-fr-fr-noetym.zip) (dictorg-fr-fr-noetym.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr-noetym.df.bz2) (dict-fr-fr-noetym.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr-noetym.mobi) (dict-fr-fr-noetym.mobi)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-fr-noetym.zip) (dicthtml-fr-fr-noetym.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr-noetym.zip) (dict-fr-fr-noetym.zip)

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
