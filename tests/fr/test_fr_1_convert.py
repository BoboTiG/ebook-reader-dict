import os
from unittest.mock import patch
from zipfile import ZipFile

import pytest

os.environ["WIKI_LOCALE"] = "fr"

# Must be imported after *WIKI_LOCALE* is set
from scripts import constants as C  # noqa
from scripts import convert  # noqa
from scripts.lang import size_min  # noqa


def test_main(data):
    """Test the JSON -> HTML conversion."""

    # Start the whole process

    # Patch the minimum dict size
    with patch.dict(size_min, {"fr": 1024}):
        assert convert.main() == 0

    # This must fail as the dict generated in tests is way too small
    with pytest.raises(ValueError):
        assert convert.main() == 0

    # Check for the final ZIP file
    dicthtml = C.SNAPSHOT / f"dicthtml-fr.zip"
    assert dicthtml.is_file()

    # Check the ZIP content
    with ZipFile(dicthtml) as fh:
        expected = [
            "de.html",
            "sl.html",
            "ac.html",
            "au.html",
            "ba.html",
            "co.html",
            "em.html",
            "en.html",
            "gr.html",
            "ic.html",
            "mo.html",
            "mu.html",
            "na.html",
            "pi.html",
            "pr.html",
            "ra.html",
            "sa.html",
            "si.html",
            "ép.html",
            "œc.html",
            "words",
            "words.count",
            "words.snapshot",
        ]
        assert fh.namelist() == expected
