import os
from zipfile import ZipFile

os.environ["WIKI_LOCALE"] = "fr"

# Must be imported after *WIKI_LOCALE* is set
from scripts import constants as C  # noqa
from scripts import convert  # noqa


def test_main(data):
    """Test the JSON -> HTML conversion."""

    # Start the whole process
    assert convert.main() == 0

    # Check for the final ZIP file
    dicthtml = C.SNAPSHOT / "dicthtml-fr.zip"
    assert dicthtml.is_file()

    # Check the ZIP content
    with ZipFile(dicthtml) as fh:
        expected = [
            "11.html",
            "ac.html",
            "au.html",
            "ba.html",
            "co.html",
            "de.html",
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
            "sl.html",
            "words",
            "words.count",
            "words.snapshot",
            "ép.html",
            "œc.html",
        ]
        assert sorted(fh.namelist()) == expected
