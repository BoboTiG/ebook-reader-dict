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
    assert (output_dir / "dict-fr.df").is_file()
    dicthtml = output_dir / "dicthtml-fr.zip"
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


@pytest.mark.parametrize(
    "formatter, filename",
    [(convert.DFFormat, "dict-fr.df"), (convert.KoboFormat, "dicthtml-fr.zip")],
)
def test_generate_dict(formatter, filename):
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
    }
    variants = defaultdict(str)
    variants["foo"] = ["foobar"]
    convert.run_formatter(formatter, "fr", output_dir, words, variants, "20201218")

    assert (output_dir / filename).is_file()
