import os
from pathlib import Path

os.environ["WIKI_LOCALE"] = "fr"

# Must be imported after *WIKI_LOCALE* is set
import convert  # noqa


def test_main(data):
    """Test the JSON -> HTML conversion."""
    # Start the whole process
    assert convert.main() == 0

    # Check for individual HTML files
    data_dir = Path(os.environ["CWD"]) / "data" / "fr"
    data_tmp = data_dir / "tmp"
    for group in ("ac", "au", "ba", "em", "ic", "l’", "œc", "pi", "qu", "sl", "su"):
        assert (data_tmp / f"{group}.raw.html").is_file()
        assert (data_tmp / f"{group}.html").is_file()

    # Check for the special "words" file
    assert (data_tmp / "words").is_file()

    # Check for the final ZIP file
    assert (data_dir / f"dicthtml-fr.zip").is_file()
