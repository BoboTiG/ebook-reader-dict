import os
from pathlib import Path
from typing import Type
from unittest.mock import patch
from zipfile import ZipFile

import pytest

from wikidict import convert
from wikidict.constants import ASSET_CHECKSUM_ALGO
from wikidict.stubs import Word

EXPECTED_INSTALL_TXT_FR = """Nombre de mots : 42
Export Wiktionnaire : 2020-12-17

Fichiers disponibles :

- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-fr.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.df.bz2)

Mis à jour le"""

WORDS = {
    "empty": Word.empty(),
    "foo": Word(["pron"], ["gender"], ["etyl"], ["def 1", ("sdef 1",)], []),
    "foos": Word(["pron"], ["gender"], ["etyl"], ["def 1", ("sdef 1", ("ssdef 1",))], ["baz"]),
    "baz": Word(["pron"], ["gender"], ["etyl"], ["def 1", ("sdef 1",)], ["foobar"]),
    "empty1": Word([], [], [], [], ["foo"]),
    "empty2": Word([], [], [], [], ["empty1"]),
    "Multiple Etymologies": Word(
        ["pron"],
        ["gender"],
        ["etyl 1", ("setyl 1",)],
        ["def 1", ("sdef 1",)],
        [],
    ),
    "Multiple Etymology": Word(
        ["pron0"],
        ["gender0"],
        ["etyl0"],
        ["def 0"],
        ["Multiple Etymologies"],
    ),
    "GIF": Word(
        ["pron"],
        ["gender"],
        ["etyl"],
        [
            '<img style="height:100%;max-height:0.8em;width:auto;vertical-align:bottom"'
            ' src="data:image/gif;base64,R0lGODdhNwAZAIEAAAAAAP///wAAAAAAACwAAAAANwAZAE'
            "AIwwADCAwAAMDAgwgTKlzIUKDBgwUZFnw4cGLDihEvOjSYseFEigQtLhSpsaNGiSdTQgS5kiVG"
            "lwhJeuRoMuHHkDBH1pT4cKdKmSpjUjT50efGnEWTsuxo9KbQnC1TFp051KhNpUid8tR6EijPkC"
            "V3en2J9erLoBjRXl1qVS1amTWn6oSK1WfGpnjDQo1q1Wvbs125PgX5l6zctW1JFgas96/FxYwv"
            'RnQsODHkyXuPDt5aVihYt5pBr9woGrJktmpNfxUYEAA7"/>'
        ],
        ["gif"],
    ),
}


def test_simple() -> None:
    assert convert.main("fr") == 0

    # Check for all dictionaries
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"

    # DictFile
    assert (output_dir / "dict-fr-fr.df").is_file()
    assert (output_dir / f"dict-fr-fr.df.{ASSET_CHECKSUM_ALGO}").is_file()
    assert (output_dir / "dict-fr-fr-noetym.df").is_file()
    assert (output_dir / f"dict-fr-fr-noetym.df.{ASSET_CHECKSUM_ALGO}").is_file()

    # DictFile bz2
    assert (output_dir / "dict-fr-fr.df.bz2").is_file()
    assert (output_dir / f"dict-fr-fr.df.bz2.{ASSET_CHECKSUM_ALGO}").is_file()
    assert (output_dir / "dict-fr-fr-noetym.df.bz2").is_file()
    assert (output_dir / f"dict-fr-fr-noetym.df.bz2.{ASSET_CHECKSUM_ALGO}").is_file()

    # StarDict
    assert (output_dir / "dict-fr-fr.zip").is_file()
    assert (output_dir / f"dict-fr-fr.zip.{ASSET_CHECKSUM_ALGO}").is_file()
    assert (output_dir / "dict-fr-fr-noetym.zip").is_file()
    assert (output_dir / f"dict-fr-fr-noetym.zip.{ASSET_CHECKSUM_ALGO}").is_file()

    # Kobo
    assert (output_dir / "dicthtml-fr-fr-noetym.zip").is_file()
    assert (output_dir / f"dicthtml-fr-fr-noetym.zip.{ASSET_CHECKSUM_ALGO}").is_file()
    dicthtml = output_dir / "dicthtml-fr-fr.zip"
    assert dicthtml.is_file()
    assert (output_dir / f"dicthtml-fr-fr.zip.{ASSET_CHECKSUM_ALGO}").is_file()

    # Check the Kobo ZIP content
    with ZipFile(dicthtml) as fh:
        expected = [
            "11.html",
            "INSTALL.txt",
            "aa.html",
            "ac.html",
            "ba.html",
            "ch.html",
            "co.html",
            "de.html",
            "du.html",
            "ef.html",
            "em.html",
            "en.html",
            "ge.html",
            "gr.html",
            "gè.html",
            "ic.html",
            "ko.html",
            "mi.html",
            "mu.html",
            "na.html",
            "pi.html",
            "pr.html",
            "ra.html",
            "sa.html",
            "si.html",
            "sl.html",
            "su.html",
            "te.html",
            "tu.html",
            "words",
            "words.count",
            "words.snapshot",
            "ép.html",
            "œc.html",
            "πa.html",
        ]
        assert sorted(fh.namelist()) == expected

        # testfile returns the name of the first corrupt file, or None
        errors = fh.testzip()
        assert errors is None

        # Check content of INSTALL.txt
        install_txt = fh.read("INSTALL.txt").decode()
        assert install_txt.startswith(EXPECTED_INSTALL_TXT_FR)


def test_no_json_file() -> None:
    with patch.object(convert, "get_latest_json_file", return_value=None):
        assert convert.main("fr") == 1


@pytest.mark.dependency()
@pytest.mark.parametrize(
    "formatter, filename, include_etymology",
    [
        (convert.DictFileFormat, "dict-fr-fr.df", True),
        (convert.DictFileFormat, "dict-fr-fr-noetym.df", False),
        (convert.KoboFormat, "dicthtml-fr-fr.zip", True),
        (convert.KoboFormat, "dicthtml-fr-fr-noetym.zip", False),
    ],
)
def test_generate_primary_dict(formatter: Type[convert.BaseFormat], filename: str, include_etymology: bool) -> None:
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    variants = convert.make_variants(WORDS)
    convert.run_formatter(
        formatter,
        "fr",
        output_dir,
        WORDS,
        variants,
        "20201218",
        include_etymology=include_etymology,
    )

    assert (output_dir / filename).is_file()


@pytest.mark.parametrize(
    "formatter, filename, include_etymology",
    [
        (convert.StarDictFormat, "dict-fr-fr.zip", True),
        (convert.StarDictFormat, "dict-fr-fr-noetym.zip", False),
        (convert.BZ2DictFileFormat, "dict-fr-fr.df.bz2", True),
        (convert.BZ2DictFileFormat, "dict-fr-fr-noetym.df.bz2", False),
    ],
)
@pytest.mark.dependency(
    depends=[
        "test_generate_primary_dict[DictFileFormat-dict-fr-fr.df]",
        "test_generate_primary_dict[DictFileFormat-dict-fr-fr-noetym.df]",
    ]
)
def test_generate_secondary_dict(formatter: Type[convert.BaseFormat], filename: str, include_etymology: bool) -> None:
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    convert.run_formatter(
        formatter,
        "fr",
        output_dir,
        {},
        {},
        "20201218",
        include_etymology=include_etymology,
    )
    assert (output_dir / filename).is_file()


FORMATTED_WORD_KOBO = """\
<w><p><a name="Multiple Etymologies"/><b>Multiple Etymologies</b> pron <i>gender</i>.<br/><br/><ol><li>def 1</li><ol style="list-style-type:lower-alpha"><li>sdef 1</li></ol></ol><br/><p>etyl 1</p><ol><li>setyl 1</li></ol></p><var><variant name="multiple etymology"/></var></w>
"""  # noqa
FORMATTED_WORD_KOBO_NO_ETYMOLOGY = """\
<w><p><a name="Multiple Etymologies"/><b>Multiple Etymologies</b> pron <i>gender</i>.<br/><br/><ol><li>def 1</li><ol style="list-style-type:lower-alpha"><li>sdef 1</li></ol></ol></p><var><variant name="multiple etymology"/></var></w>
"""  # noqa
FORMATTED_WORD_DICTFILE = """\
@ Multiple Etymologies
:  pron  <i>gender</i>.
& Multiple Etymology
<html><ol><li>def 1</li><ol style="list-style-type:lower-alpha"><li>sdef 1</li></ol></ol><br/><p>etyl 1</p><ol><li>setyl 1</li></ol></html>\


"""  # noqa
FORMATTED_WORD_DICTFILE_NO_ETYMOLOGY = """\
@ Multiple Etymologies
:  pron  <i>gender</i>.
& Multiple Etymology
<html><ol><li>def 1</li><ol style="list-style-type:lower-alpha"><li>sdef 1</li></ol></ol></html>\


"""  # noqa


@pytest.mark.parametrize(
    "formatter, include_etymology, expected",
    [
        (convert.KoboFormat, True, FORMATTED_WORD_KOBO),
        (convert.KoboFormat, False, FORMATTED_WORD_KOBO_NO_ETYMOLOGY),
        (convert.DictFileFormat, True, FORMATTED_WORD_DICTFILE),
        (convert.DictFileFormat, False, FORMATTED_WORD_DICTFILE_NO_ETYMOLOGY),
    ],
)
def test_word_rendering(
    formatter: Type[convert.BaseFormat],
    include_etymology: bool,
    expected: str,
) -> None:
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    cls = formatter(
        "fr",
        output_dir,
        WORDS,
        convert.make_variants(WORDS),
        "20221212",
        include_etymology=include_etymology,
    )

    kwargs = {"name": "mu", "words": WORDS} if isinstance(cls, convert.KoboFormat) else {}
    content = next(cls.handle_word("Multiple Etymologies", WORDS["Multiple Etymologies"], **kwargs))
    assert content == expected
