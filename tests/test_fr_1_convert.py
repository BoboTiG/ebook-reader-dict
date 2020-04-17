import os
from pathlib import Path

os.environ["WIKI_LOCALE"] = "fr"


def test_main(data):
    """Test the JSON -> HTML conversion."""
    from convert import main

    # Start the whole process
    main()

    # Check for individual HTML files
    data_dir = Path(os.environ["CWD"]) / "data" / "fr""
    for group in ("br", "ce"):
        assert (data_dir / "tmp" / f"{group}.raw.html").is_file()
        assert (data_dir / "tmp" / f"{group}.html").is_file()

    # Check for the special "words" file
    assert (data_dir / "tmp" / "words").is_file()

    # Check for the final ZIP file
    assert (data_dir / f"dicthtml-fr.zip").is_file()
