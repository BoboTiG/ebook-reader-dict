"""Convert words from JSON data to eBook format (ZIP)."""
import gzip
import json
import os
from collections import defaultdict
from contextlib import suppress
from datetime import date
from pathlib import Path
from shutil import rmtree
from typing import Dict, List
from zipfile import ZIP_DEFLATED, ZipFile

from marisa_trie import Trie

from .constants import WORD_FORMAT
from .lang import etyl_word, wiktionary
from .stubs import Word, Words
from .utils import format_description, guess_prefix

Groups = Dict[str, Words]


def craft_index(wordlist: List[str], output_dir: Path) -> Path:
    """Generate the special file "words" that is an index of all words."""
    output = output_dir / "words"
    trie = Trie(wordlist)
    trie.save(output)
    return output


def make_groups(words: Words) -> Groups:
    """Group word by prefix for later HTML creation, see save()."""
    groups: Groups = defaultdict(dict)
    for word, data in words.items():
        groups[guess_prefix(word)][word] = data
    return groups


def load(output_dir: Path) -> Words:
    """Load the big JSON file containing all words and their details."""
    raw_data = output_dir / "data.json"
    with raw_data.open(encoding="utf-8") as fh:
        words: Words = json.load(fh)
    print(f">>> Loaded {len(words):,} words from {raw_data}", flush=True)
    return words


def save(groups: Groups, output_dir: Path, locale: str) -> None:
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

        # Add the release description in the comment
        release = format_description(locale, output_dir)
        # Sanitize the comment
        release = release.replace(":arrow_right:", "->")
        release = release.replace(f"[dicthtml-{locale}.zip](", "")
        release = release.replace(")", "")
        release = release.replace("`", '"')
        release = release.replace("<sub>", "")
        release = release.replace("</sub>", "")
        # Actually add the comment
        fh.comment = release.encode()

        # Check the ZIP validity
        assert fh.testzip()

    print(f">>> Generated {dicthtml} ({dicthtml.stat().st_size:,} bytes)", flush=True)


def convert_etymology(etyl_word: str, etymology: str) -> str:
    """Return the HTML code to include for the etymology of a word."""
    return (
        f"<dl><dt><u>{etyl_word}</u></dt><dd>{etymology}</dd></dl>"
        if etyl_word and etymology
        else ""
    )


def convert_genre(genre: str) -> str:
    """Return the HTML code to include for the genre of a word."""
    return f" <i>{genre}.</i>" if genre else ""


def convert_pronunciation(pronunciation: str) -> str:
    """Return the HTML code to include for the etymology of a word."""
    return f" \\{pronunciation}\\" if pronunciation else ""


def save_html(name: str, words: Words, output_dir: Path, locale: str) -> Path:
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
        for word, details in words.items():

            details = Word(*details)
            definitions = ""

            for definition in details.definitions:
                if isinstance(definition, str):
                    definitions += f"<li>{definition}</li>"
                else:
                    definitions += '<ol style="list-style-type:lower-alpha">'
                    definitions += "".join(f"<li>{d}</li>" for d in definition)
                    definitions += "</ol>"

            pronunciation = convert_pronunciation(details.pronunciation)
            genre = convert_genre(details.genre)
            etymology = convert_etymology(etyl_word[locale], details.etymology)

            fh.write(WORD_FORMAT.format(**locals()))

        fh.write("</html>\n")

    # Compress the HTML with gzip
    output = output_dir / f"{name}.html"
    with raw_output.open(mode="rb") as fi, gzip.open(output, mode="wb") as fo:
        fo.writelines(fi)

    return output


def main(locale: str) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale

    # Retrieve all words
    words = load(output_dir)

    # Create groups of words
    groups = make_groups(words)

    # Save to HTML pages and the fial ZIP
    save(groups, output_dir, locale)

    print(">>> Conversion done!", flush=True)
    return 0
