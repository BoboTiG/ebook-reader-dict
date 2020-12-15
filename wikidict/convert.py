import gzip
import json
import os
from collections import defaultdict
from contextlib import suppress
from datetime import date
from pathlib import Path
from shutil import rmtree
from typing import Dict, List, Type
from zipfile import ZIP_DEFLATED, ZipFile

from marisa_trie import Trie

from scripts.constants import WORD_FORMAT
from scripts.lang import wiktionary
from scripts.stubs import Word, Words
from scripts.utils import (
    convert_etymology,
    convert_genre,
    convert_pronunciation,
    format_description,
    guess_prefix,
)

Groups = Dict[str, Words]
Variants = Dict[str, List[str]]


class BaseFormat:

    __slots__ = {"locale", "output_dir", "words", "variants"}

    def __init__(
        self, locale: str, output_dir: Path, words: Words, variants: Variants
    ) -> None:
        self.locale = locale
        self.output_dir = output_dir
        self.words = words
        self.variants = variants

    def process(self) -> None:
        raise NotImplementedError()

    def save(self) -> None:
        raise NotImplementedError()


class KoboBaseFormat(BaseFormat):
    def create_definitions(self, details: Word) -> str:
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
                        definitions += '<ol style="list-style-type:lower-roman">'
                        definitions += "".join(f"<li>{d}</li>" for d in subdef)
                        definitions += "</ol>"
                definitions += "</ol>"
        return definitions


class KoboFormat(KoboBaseFormat):
    def process(self) -> None:
        self.groups = self.make_groups(self.words)
        self.save()

    def create_install(self, locale: str, output_dir: Path) -> Path:
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

    def craft_index(self, wordlist: List[str], output_dir: Path) -> Path:
        """Generate the special file "words" that is an index of all words."""
        output = output_dir / "words"
        trie = Trie(wordlist)
        trie.save(output)
        return output

    def make_groups(self, words: Words) -> Groups:
        """Group word by prefix for later HTML creation, see save()."""
        groups: Groups = defaultdict(dict)
        for word, data in words.items():
            groups[guess_prefix(word)][word] = data
        return groups

    def save(self) -> None:
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
            rmtree(self.output_dir / "tmp")
        (self.output_dir / "tmp").mkdir()

        # Files to add to the final archive
        to_compress = []

        # First, create individual HTML files
        wordlist: List[str] = []
        print(">>> Generating HTML files ", end="", flush=True)
        for prefix, words in self.groups.items():
            to_compress.append(self.save_html(prefix, words, self.output_dir / "tmp"))
            wordlist.extend(words.keys())
            print(".", end="", flush=True)
        print(f" [{len(self.groups.keys()):,}]", flush=True)

        # Then create the special "words" file
        to_compress.append(self.craft_index(wordlist, self.output_dir / "tmp"))

        # Add unrelated files, just for history
        to_compress.append(self.create_install(self.locale, self.output_dir))
        to_compress.append(self.output_dir / "words.count")
        to_compress.append(self.output_dir / "words.snapshot")

        # Pretty print the source
        source = wiktionary[self.locale].format(year=date.today().year)

        # Finally, create the ZIP
        dicthtml = self.output_dir / f"dicthtml-{self.locale}.zip"
        with ZipFile(dicthtml, mode="w", compression=ZIP_DEFLATED) as fh:
            fh.comment = bytes(source, "utf-8")
            for file in to_compress:
                fh.write(file, arcname=file.name)

            # Check the ZIP validity
            # testzip() returns the name of the first corrupt file, or None
            assert fh.testzip() is None, fh.testzip()

        print(
            f">>> Generated {dicthtml} ({dicthtml.stat().st_size:,} bytes)", flush=True
        )

    def save_html(
        self,
        name: str,
        words: Words,
        output_dir: Path,
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
                            root_details = self.words.get(variant, "")
                            if root_details:
                                found_different_prefix = True
                                break
                    variants_words = {}
                    # if we found one variant, then list them all
                    if found_different_prefix:
                        for variant in word_details.variants:
                            root_details = self.words.get(variant, "")
                            if root_details:
                                variants_words[variant] = Word(*root_details)
                    if word.endswith("s"):  # crude detection of plural
                        singular = word[:-1]
                        maybe_noun = self.words.get(
                            singular, ""
                        )  # do we have the singular?
                        # make sure we are not redirecting to a verb (je mange, tu manges)
                        # verb form is also a singular noun
                        if maybe_noun and not Word(*maybe_noun).variants:
                            variants_words[singular] = Word(*maybe_noun)
                            for variant in word_details.variants:
                                maybe_verb = self.words.get(variant, "")
                                if maybe_verb:
                                    variants_words[variant] = Word(*maybe_verb)
                    if variants_words:
                        current_words = variants_words

                # write to file
                for current_word, details in current_words.items():
                    details = Word(*details)
                    if not details.definitions:
                        continue
                    definitions = self.create_definitions(details)

                    pronunciation = convert_pronunciation(details.pronunciations)
                    genre = convert_genre(details.genre)
                    etymology = convert_etymology(details.etymology)

                    var = ""
                    if self.variants[word]:
                        var = "<var>"
                        for v in self.variants[word]:
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


class DFFormat(KoboBaseFormat):
    def process(self) -> None:
        self.save()

    def save(self) -> None:
        name = f"dict-{self.locale}-{self.locale}"
        raw_output = self.output_dir / f"{name}.df"
        with raw_output.open(mode="w", encoding="utf-8") as fh:
            for word, details in self.words.items():
                details = Word(*details)
                if not details.definitions:
                    continue
                definitions = self.create_definitions(details)

                pronunciation = convert_pronunciation(details.pronunciations)
                genre = convert_genre(details.genre)
                etymology = convert_etymology(details.etymology)
                fh.write(f"@ {word}\n")
                if pronunciation or genre:
                    fh.write(f": {pronunciation.strip()} {genre}\n")
                for v in self.variants[word]:
                    fh.write(f"& {v}\n")
                fh.write(f"<html>{etymology}\n")
                fh.write(f"<ol>{definitions}</ol>\n\n")
        print(f">>> Generated {name}.df ({raw_output.stat().st_size:,} bytes)", flush=True)


def get_latest_json_file(locale: str, output_dir: Path) -> str:
    """Get the name of the last data-*.json file."""
    files = list(output_dir.glob("data-*.json"))
    return str(sorted(files)[-1]) if files else ""


def get_formaters() -> List[Type[BaseFormat]]:
    return [KoboFormat, DFFormat]


def run_formatter(
    cls: Type[BaseFormat],
    locale: str,
    output_dir: Path,
    words: Words,
    variants: Variants,
) -> None:
    formater = cls(locale, output_dir, words, variants)
    formater.process()


def load(filename: str) -> Words:
    """Load the big JSON file containing all words and their details."""
    print(f">>> Loading {filename} ...")
    input_file = Path(filename)
    with input_file.open(encoding="utf-8") as fh:
        words: Words = json.load(fh)
    print(f">>> Loaded {len(words):,} words from {input_file}", flush=True)
    return words


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


def main(locale: str) -> int:
    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    filename = get_latest_json_file(locale, output_dir)

    # Get all words from the database
    words: Words = load(filename)
    variants: Variants = make_variants(words)

    # Get all registered formats
    formaters = get_formaters()

    # And distribute the workload
    from multiprocessing import Pool
    from functools import partial

    with Pool(len(formaters)) as pool:
        pool.map(
            partial(
                run_formatter,
                locale=locale,
                output_dir=output_dir,
                words=words,
                variants=variants,
            ),
            formaters,
        )
    return 0
