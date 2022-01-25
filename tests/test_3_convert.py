import os
from collections import defaultdict
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

import pytest

from wikidict import convert
from wikidict.stubs import Word


def test_simple(craft_data):
    assert convert.main("fr") == 0

    # Check for all dictionaries
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    assert (output_dir / "dict-fr-fr.df").is_file()  # DictFile
    assert (output_dir / "dict-fr-fr.zip").is_file()  # StarDict
    dicthtml = output_dir / "dicthtml-fr-fr.zip"  # Kobo
    assert dicthtml.is_file()

    # Check the Kobo ZIP content
    with ZipFile(dicthtml) as fh:
        expected = [
            "11.html",
            "INSTALL.txt",
            "aa.html",
            "ac.html",
            "au.html",
            "ba.html",
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


def test_no_json_file():
    with patch.object(convert, "get_latest_json_file", return_value=None):
        assert convert.main("fr") == 1


@pytest.mark.dependency()
@pytest.mark.parametrize(
    "formatter, filename",
    [
        (convert.DictFileFormat, "dict-fr-fr.df"),
        (convert.KoboFormat, "dicthtml-fr-fr.zip"),
    ],
)
def test_generate_primary_dict(formatter, filename):
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    words = {
        "empty": Word("", "", "", [], []),
        "foo": Word("pron", "gender", "etyl", ["def 1", ["sdef 1"]], []),
        "foos": Word(
            "pron", "gender", "etyl", ["def 1", ["sdef 1", ["ssdef 1"]]], ["baz"]
        ),
        "baz": Word("pron", "gender", "etyl", ["def 1", ["sdef 1"]], ["foobar"]),
        "etyls": Word(
            "pron",
            "gender",
            ["etyl 1", ["setyl 1"]],
            ["def 1", ["sdef 1"]],
            ["foobar"],
        ),
        "GIF": Word(
            "pron",
            "gender",
            "etyl",
            [
                '<img style="height:100%;max-height:0.8em;width:auto;vertical-align:bottom"'
                ' src="data:image/gif;base64,R0lGODdhNwAZAIEAAAAAAP///wAAAAAAACwAAAAANwAZAE'
                "AIwwADCAwAAMDAgwgTKlzIUKDBgwUZFnw4cGLDihEvOjSYseFEigQtLhSpsaNGiSdTQgS5kiVG"
                "lwhJeuRoMuHHkDBH1pT4cKdKmSpjUjT50efGnEWTsuxo9KbQnC1TFp051KhNpUid8tR6EijPkC"
                "V3en2J9erLoBjRXl1qVS1amTWn6oSK1WfGpnjDQo1q1Wvbs125PgX5l6zctW1JFgas96/FxYwv"
                'RnQsODHkyXuPDt5aVihYt5pBr9woGrJktmpNfxUYEAA7"/>'
            ],
            ["GIF"],
        ),
    }
    variants = defaultdict(str)
    variants["foo"] = ["foobar"]
    convert.run_formatter(formatter, "fr", output_dir, words, variants, "20201218")

    assert (output_dir / filename).is_file()


@pytest.mark.parametrize(
    "formatter, filename",
    [
        (convert.StarDictFormat, "dict-fr-fr.zip"),
    ],
)
@pytest.mark.dependency(
    depends=["test_generate_primary_dict[DictFileFormat-dict-fr-fr.df]"]
)
def test_generate_secundary_dict(formatter, filename):
    output_dir = Path(os.environ["CWD"]) / "data" / "fr"
    convert.run_formatter(formatter, "fr", output_dir, [], [], "20201218")
    assert (output_dir / filename).is_file()
