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
from .lang import wiktionary
from .stubs import Word, Words
from .utils import (
    convert_etymology,
    convert_genre,
    convert_pronunciation,
    format_description,
    guess_prefix,
)

Groups = Dict[str, Words]
Variants = Dict[str, List[str]]


def create_install(locale: str, output_dir: Path) -> Path:
    """Generate the INSTALL.txt file."""
    release = format_description(locale, output_dir)

    # Sanitization
    release = release.replace(":arrow_right:", "->")
    release = release.replace(f"[dicthtml-{locale}.zip](", "")
    release = release.replace(")", "")
    release = release.replace("`", '"')
    release = release.replace("<sub>", "")
    release = release.replace("</sub>", "")

    file = output_dir / "INSTALL.txt"
    file.write_text(release)
    return file


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


def make_variants(words: Words) -> Variants:
    """Group word by variant for later HTML creation, see save()."""
    variants: Variants = defaultdict(list)
    for word, details in words.items():
        details = Word(*details)
        # Variant must be normalized by trimming whitespace and lowercasing it.
        for variant in details.variants:
            if variant:
                variants[variant].append(word)

    return variants


def load(output_dir: Path) -> Words:
    """Load the big JSON file containing all words and their details."""
    raw_data = output_dir / "data.json"
    with raw_data.open(encoding="utf-8") as fh:
        words: Words = json.load(fh)
    print(f">>> Loaded {len(words):,} words from {raw_data}", flush=True)
    return words


def save(
    groups: Groups, variants: Variants, all_words: Words, output_dir: Path, locale: str
) -> None:
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
        to_compress.append(
            save_html(prefix, words, variants, all_words, output_dir / "tmp", locale)
        )
        wordlist.extend(words.keys())
        print(".", end="", flush=True)
    print(f" [{len(groups.keys()):,}]", flush=True)

    # Then create the special "words" file
    to_compress.append(craft_index(wordlist, output_dir / "tmp"))

    # Add unrelated files, just for history
    to_compress.append(create_install(locale, output_dir))
    to_compress.append(output_dir / "words.count")
    to_compress.append(output_dir / "words.snapshot")

    # Pretty print the source
    source = wiktionary[locale].format(year=date.today().year)

    # Finally, create the ZIP
    dicthtml = output_dir / f"dicthtml-{locale}.zip"
    with ZipFile(dicthtml, mode="w", compression=ZIP_DEFLATED) as fh:
        fh.comment = bytes(source, "utf-8")
        for file in to_compress:
            fh.write(file, arcname=file.name)

        # Check the ZIP validity
        # testzip() returns the name of the first corrupt file, or None
        assert fh.testzip() is None, fh.testzip()

    print(f">>> Generated {dicthtml} ({dicthtml.stat().st_size:,} bytes)", flush=True)


def save_html(
    name: str,
    words: Words,
    variants: Variants,
    all_words: Words,
    output_dir: Path,
    locale: str,
) -> Path:
    """Generate individual HTML files.

    Content of the HTML file:

        <html>
            word 1
            word 2
            ...
        </html>

    Syntax of each WORD is define in the *WORD_FORMAT* constant.
    """

    fmt = "".join(line.strip() for line in WORD_FORMAT.splitlines())

    # Save to uncompressed HTML
    raw_output = output_dir / f"{name}.raw.html"
    with raw_output.open(mode="w", encoding="utf-8") as fh:
        for word, word_details in words.items():
            current_words: Words = {}
            word_details = Word(*word_details)
            current_words[word] = word_details

            # use variant definitions for a word if one variant prefix is different
            # "suis" listed with the definitions of "être" and "suivre"
            if word_details.variants:
                found_different_prefix = False
                for variant in word_details.variants:
                    if guess_prefix(variant) != name:
                        root_details = all_words.get(variant, "")
                        if root_details:
                            found_different_prefix = True
                            break
                variants_words = {}
                # if we found one variant, then list them all
                if found_different_prefix:
                    for variant in word_details.variants:
                        root_details = all_words.get(variant, "")
                        if root_details:
                            variants_words[variant] = Word(*root_details)
                if word.endswith("s"):  # crude detection of plural
                    singular = word[:-1]
                    maybe_noun = all_words.get(singular, "")  # do we have the singular?
                    # make sure we are not redirecting to a verb (je mange, tu manges)
                    # verb form is also a singular noun
                    if maybe_noun and not Word(*maybe_noun).variants:
                        variants_words[singular] = Word(*maybe_noun)
                        for variant in word_details.variants:
                            maybe_verb = all_words.get(variant, "")
                            if maybe_verb:
                                variants_words[variant] = Word(*maybe_verb)
                if variants_words:
                    current_words = variants_words

            # write to file
            for current_word, details in current_words.items():
                details = Word(*details)
                if not details.definitions:
                    continue
                definitions = ""
                for definition in details.definitions:
                    if isinstance(definition, str):
                        definitions += f"<li>{definition}</li>"
                    else:
                        definitions += '<ol style="list-style-type:lower-alpha">'
                        for subdef in definition:
                            if isinstance(subdef, str):
                                definitions += f"<li>{subdef}</li>"
                            else:
                                definitions += (
                                    '<ol style="list-style-type:lower-roman">'
                                )
                                definitions += "".join(f"<li>{d}</li>" for d in subdef)
                                definitions += "</ol>"
                        definitions += "</ol>"

                pronunciation = convert_pronunciation(details.pronunciations)
                genre = convert_genre(details.genre)
                etymology = convert_etymology(details.etymology)

                var = ""
                if variants[word]:
                    var = "<var>"
                    for v in variants[word]:
                        # no variant with different prefix
                        v = v.lower().strip()
                        if guess_prefix(v) == name:
                            var += f'<variant name="{v}"/>'
                    var += "</var>"
                # no empty var tag
                if len(var) < 15:
                    var = ""

                fh.write(fmt.format(**locals()))

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

    # Create variant dictionary
    variants = make_variants(words)

    # Save to HTML pages and the final ZIP
    save(groups, variants, words, output_dir, locale)

    print(">>> Conversion done!", flush=True)
    return 0
