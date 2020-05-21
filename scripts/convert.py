"""Convert words from JSON data to eBook format (ZIP)."""
import gzip
import json
import os
from collections import defaultdict
from contextlib import suppress
from datetime import date, datetime
from pathlib import Path
from shutil import rmtree
from typing import List
from zipfile import ZIP_DEFLATED, ZipFile

from marisa_trie import Trie

from .constants import GH_REPOS, WORD_FORMAT
from .lang import wiktionary
from . import annotations as T
from .utils import guess_prefix


def craft_index(wordlist: List[str], output_dir: Path) -> Path:
    """Generate the special file "words" that is an index of all words."""
    output = output_dir / "words"
    trie = Trie(wordlist)
    trie.save(output)
    return output


def make_groups(words: T.Words) -> T.Groups:
    """Group word by prefix for later HTML creation, see save()."""
    groups: T.Groups = defaultdict(dict)
    for word, data in words.items():
        groups[guess_prefix(word)][word] = data
    return groups


def load(output_dir: Path) -> T.Words:
    """Load the big JSON file containing all words and their details."""
    raw_data = output_dir / "data.json"
    with raw_data.open(encoding="utf-8") as fh:
        words: T.Words = json.load(fh)
    print(f">>> Loaded {len(words):,} words from {raw_data}", flush=True)
    return words


def save(groups: T.Groups, output_dir: Path, locale: str) -> None:
    """
    Format of resulting dicthtml-LOCALE.zip:

        aa.html
        ab.html
        ..
        words

    Each word must be stored into the file {letter1}{letter2}.html (gzip content).
    """

    # Clean-up before we start
    with suppress(FileNotFoundError):
        rmtree(output_dir / "tmp")
    (output_dir / "tmp").mkdir()

    # Files to add to the final archive
    to_compress = []

    # First, create individual HTML files
    wordlist: List[str] = []
    print(">>> Generating HTML files ", end="", flush=True)
    for prefix, words in groups.items():
        to_compress.append(save_html(prefix, words, output_dir / "tmp", locale))
        wordlist.extend(words.keys())
        print(".", end="", flush=True)
    print(f" [{len(groups.keys()):,}]", flush=True)

    # Then create the special "words" file
    to_compress.append(craft_index(sorted(wordlist), output_dir / "tmp"))

    # Add unrealted files, just for history
    to_compress.append(output_dir / "words.count")
    to_compress.append(output_dir / "words.snapshot")

    # Finally, create the ZIP
    dicthtml = output_dir / f"dicthtml-{locale}.zip"
    with ZipFile(dicthtml, mode="w", compression=ZIP_DEFLATED) as fh:
        for file in to_compress:
            fh.write(file, arcname=file.name)

        # Add the source in the comment
        now = datetime.utcnow().isoformat()
        fh.comment = f"Source: {GH_REPOS}\n{now}".encode()

    print(f">>> Generated {dicthtml} ({dicthtml.stat().st_size:,} bytes)", flush=True)


def save_html(name: str, words: T.Words, output_dir: Path, locale: str) -> Path:
    """Generate individual HTML files.

    Content of the HTML file:

        <html>
            word 1
            word 2
            ...
        </html>

    Syntax of each WORD is define in the *WORD_FORMAT* constant.
    """

    # Prettry print the source
    source = wiktionary[locale].format(year=date.today().year)

    # Save to uncompressed HTML
    raw_output = output_dir / f"{name}.raw.html"
    with raw_output.open(mode="w", encoding="utf-8") as fh:
        for word, (pronunciation, genre, defs) in words.items():
            definitions = "".join(f"<li>{d}</li>" for d in defs)
            if pronunciation:
                pronunciation = f" \\{pronunciation}\\"
            if genre:
                genre = f" <i>{genre}.</i>"

            fh.write(WORD_FORMAT.format(**locals()))

        fh.write("</html>\n")

    # Compress the HTML with gzip
    output = output_dir / f"{name}.html"
    with raw_output.open(mode="rb") as fi, gzip.open(output, mode="wb") as fo:
        fo.writelines(fi)

    return output


def main(locale: str) -> int:
    """Extry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale

    # Retrieve all words
    words = load(output_dir)

    # Create groups of words
    groups = make_groups(words)

    # Save to HTML pages and the fial ZIP
    save(groups, output_dir, locale)

    print(">>> Conversion done!", flush=True)
    return 0
