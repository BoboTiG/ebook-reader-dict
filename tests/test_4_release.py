import os
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import pytest

from wikidict import constants, release

EXPECTED_INSTALL_TXT_FR = """### 🌟 Afin d'être régulièrement mis à jour, ce projet a besoin de soutien ; [cliquez ici](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) pour faire un don. 🌟

<br/>


Nombre de mots : 123 456 789
Export Wiktionnaire : 2020-02-20

Version complète :
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dictorg-fr-fr.zip) (dictorg-fr-fr.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.df.bz2) (dict-fr-fr.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.mobi.zip) (dict-fr-fr.mobi.zip)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-fr.zip) (dicthtml-fr-fr.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.zip) (dict-fr-fr.zip)

Version sans étymologies :
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dictorg-fr-fr-noetym.zip) (dictorg-fr-fr-noetym.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr-noetym.df.bz2) (dict-fr-fr-noetym.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr-noetym.mobi.zip) (dict-fr-fr-noetym.mobi.zip)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-fr-noetym.zip) (dicthtml-fr-fr-noetym.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr-noetym.zip) (dict-fr-fr-noetym.zip)

<sub>Mis à jour le """


def test_main(capsys: pytest.CaptureFixture[Any]) -> None:
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    with ZipFile(output_dir / "dicthtml-fr-fr.zip", mode="w") as fh:
        fh.writestr(constants.ZIP_WORDS_COUNT, "123456789")
        fh.writestr(constants.ZIP_WORDS_SNAPSHOT, "20200220")

    assert release.main("fr") == 0

    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out.startswith(EXPECTED_INSTALL_TXT_FR)
