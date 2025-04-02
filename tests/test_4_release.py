from pathlib import Path
from typing import Any
from unittest.mock import patch
from zipfile import ZipFile

import pytest

from wikidict import constants, release, render

EXPECTED_INSTALL_TXT_FR = """### 🌟 Afin d'être régulièrement mis à jour, ce projet a besoin de soutien ; [cliquez ici](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) pour faire un don. 🌟

<br/>


Nombre de mots : 123 456 789
Export Wiktionnaire : 2020-02-20

Version complète :
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dictorg-fr-{0}.zip) (dictorg-fr-{0}.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-{0}.df.bz2) (dict-fr-{0}.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-{0}.mobi.zip) (dict-fr-{0}.mobi.zip)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-{0}.zip) (dicthtml-fr-{0}.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-{0}.zip) (dict-fr-{0}.zip)

Version sans étymologies :
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dictorg-fr-{0}-noetym.zip) (dictorg-fr-{0}-noetym.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-{0}-noetym.df.bz2) (dict-fr-{0}-noetym.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-{0}-noetym.mobi.zip) (dict-fr-{0}-noetym.mobi.zip)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-{0}-noetym.zip) (dicthtml-fr-{0}-noetym.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-{0}-noetym.zip) (dict-fr-{0}-noetym.zip)

<sub>Mis à jour le """

EXPECTED_INSTALL_TXT_IT = """### 🌟 Per poter essere aggiornato regolarmente, questo progetto ha bisogno di sostegno; [cliccare qui](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) per fare una donazione. 🌟

<br/>


Numero di parole: 123 456 789
Export Wiktionary: 2020-02-20

Versione completa:
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dictorg-it-{0}.zip) (dictorg-it-{0}.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dict-it-{0}.df.bz2) (dict-it-{0}.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dict-it-{0}.mobi.zip) (dict-it-{0}.mobi.zip)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dicthtml-it-{0}.zip) (dicthtml-it-{0}.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dict-it-{0}.zip) (dict-it-{0}.zip)

Versione senza etimologia:
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dictorg-it-{0}-noetym.zip) (dictorg-it-{0}-noetym.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dict-it-{0}-noetym.df.bz2) (dict-it-{0}-noetym.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dict-it-{0}-noetym.mobi.zip) (dict-it-{0}-noetym.mobi.zip)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dicthtml-it-{0}-noetym.zip) (dicthtml-it-{0}-noetym.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/it/dict-it-{0}-noetym.zip) (dict-it-{0}-noetym.zip)

<sub>Aggiornato il """


@pytest.mark.parametrize(
    "locale, lang_src, lang_dst",
    [
        ("fr", "fr", "fr"),
        ("fro", "fr", "fro"),
        ("fr:fro", "fr", "fro"),
        ("fr:it", "fr", "it"),
        ("it:fr", "it", "fr"),
    ],
)
def test_main(locale: str, lang_src: str, lang_dst: str, tmp_path: Path, capsys: pytest.CaptureFixture[Any]) -> None:
    with patch.dict("os.environ", {"CWD": str(tmp_path)}):
        source_dir = render.get_source_dir(lang_src, lang_dst)
        assert source_dir == tmp_path / "data" / lang_src / lang_dst

        source_file = release.get_source_file(source_dir, lang_src, lang_dst)
        assert source_file == source_dir / "output" / f"dicthtml-{lang_src}-{lang_dst}.zip"

        source_file.parent.mkdir(parents=True)
        with ZipFile(source_file, mode="w") as fh:
            fh.writestr(constants.ZIP_WORDS_COUNT, "123456789")
            fh.writestr(constants.ZIP_WORDS_SNAPSHOT, "20200220")

        assert release.main(locale) == 0

        captured = capsys.readouterr()
        expected_install = (EXPECTED_INSTALL_TXT_FR if lang_src == "fr" else EXPECTED_INSTALL_TXT_IT).format(lang_dst)
        print(captured.out)
        print()
        print("---")
        print()
        print(expected_install)
        assert captured.out.startswith(expected_install)
