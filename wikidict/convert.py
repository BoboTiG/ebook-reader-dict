"""Convert rendered data to working dictionaries."""
import gzip
import json
import os
from collections import defaultdict
from contextlib import suppress
from datetime import date
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from shutil import rmtree
from typing import Dict, List, Optional, Type
from zipfile import ZIP_DEFLATED, ZipFile

from marisa_trie import Trie

from .constants import WORD_FORMAT
from .lang import wiktionary
from .stubs import Definitions, Word, Words
from .utils import (
    convert_gender,
    convert_pronunciation,
    format_description,
    guess_prefix,
)

Groups = Dict[str, Words]
Variants = Dict[str, List[str]]


class BaseFormat:
    """Base class for all dictionaries."""

    __slots__ = {"locale", "output_dir", "snapshot", "words", "variants"}

    def __init__(
        self,
        locale: str,
        output_dir: Path,
        words: Words,
        variants: Variants,
        snapshot: str,
    ) -> None:
        self.locale = locale
        self.output_dir = output_dir
        self.words = words
        self.variants = variants
        self.snapshot = snapshot

    def process(self) -> None:  # pragma: nocover
        raise NotImplementedError()

    @staticmethod
    def summary(file: Path) -> None:
        print(f">>> Generated {file.name} ({file.stat().st_size:,} bytes)", flush=True)


class KoboBaseFormat(BaseFormat):
    """Base class for Kobo-related dictionaries."""

    @staticmethod
    def create_etymology(etymologies: List[Definitions]) -> str:
        """Return the HTML code to include for the etymology of a word."""
        result = ""
        if etymologies:
            for etymology in etymologies:
                if isinstance(etymology, str):
                    result += f"<p>{etymology}</p>"
                else:
                    result += "<ol>"
                    for sub_etymology in etymology:
                        result += f"<li>{sub_etymology}</li>"
                    result += "</ol>"
            result += "</br>"
        return result

    @staticmethod
    def create_definitions(details: Word) -> str:
        """Return the HTML code to include for the definitions of a word."""
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
    """Save the data into Kobo-specific ZIP file."""

    def process(self) -> None:
        self.groups = self.make_groups(self.words)
        self.save()

    @staticmethod
    def create_install(locale: str, output_dir: Path) -> Path:
        """Generate the INSTALL.txt file."""
        release = format_description(locale, output_dir)

        # Sanitization
        release = release.replace(":arrow_right:", "->")
        release = release.replace(f"[dicthtml-{locale}-{locale}.zip](", "")
        release = release.replace(")", "")
        release = release.replace("`", '"')
        release = release.replace("<sub>", "")
        release = release.replace("</sub>", "")

        file = output_dir / "INSTALL.txt"
        file.write_text(release)
        return file

    @staticmethod
    def craft_index(wordlist: List[str], output_dir: Path) -> Path:
        """Generate the special file "words" that is an index of all words."""
        output = output_dir / "words"
        trie = Trie(wordlist)
        trie.save(output)
        return output

    @staticmethod
    def make_groups(words: Words) -> Groups:
        """Group word by prefix."""
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
        for prefix, words in self.groups.items():
            to_compress.append(self.save_html(prefix, words, self.output_dir / "tmp"))
            wordlist.extend(words.keys())

        # Then create the special "words" file
        to_compress.append(self.craft_index(wordlist, self.output_dir / "tmp"))

        # Add unrelated files, just for history
        words_count = self.output_dir / "words.count"
        words_snapshot = self.output_dir / "words.snapshot"
        words_count.write_text(str(len(wordlist)))
        words_snapshot.write_text(self.snapshot)
        to_compress.append(words_count)
        to_compress.append(words_snapshot)
        to_compress.append(self.create_install(self.locale, self.output_dir))

        # Pretty print the source
        source = wiktionary[self.locale].format(year=date.today().year)

        # Finally, create the ZIP
        dicthtml = self.output_dir / f"dicthtml-{self.locale}-{self.locale}.zip"
        with ZipFile(dicthtml, mode="w", compression=ZIP_DEFLATED) as fh:
            fh.comment = bytes(source, "utf-8")
            for file in to_compress:
                fh.write(file, arcname=file.name)

            # Check the ZIP validity
            # testzip() returns the name of the first corrupt file, or None
            assert fh.testzip() is None, fh.testzip()

        self.summary(dicthtml)

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
                    gender = convert_gender(details.gender)
                    etymology = self.create_etymology(details.etymology)

                    var = ""
                    if self.variants.get(word, []):
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


class DictFileFormat(KoboBaseFormat):
    """Save the data into a *.df* DictFile."""

    def process(self) -> None:
        file = self.output_dir / f"dict-{self.locale}-{self.locale}.df"
        with file.open(mode="w", encoding="utf-8") as fh:
            for word, details in self.words.items():
                details = Word(*details)
                if not details.definitions:
                    continue
                definitions = self.create_definitions(details)

                pronunciation = convert_pronunciation(details.pronunciations)
                gender = convert_gender(details.gender)
                etymology = self.create_etymology(details.etymology)
                fh.write(f"@ {word}\n")
                if pronunciation or gender:
                    fh.write(f": {pronunciation.strip()} {gender}\n")
                for v in self.variants[word]:
                    fh.write(f"& {v}\n")
                fh.write(f"<html>{etymology}\n")
                fh.write(f"<ol>{definitions}</ol>\n\n")

        self.summary(file)


class StarDictFormat(DictFileFormat):
    """Save the data into a StarDict file."""

    def _convert(self) -> None:
        """Convert the DictFile to StarDict."""
        from pyglossary import Glossary

        Glossary.init()
        glos = Glossary()

        # Pretty print the source
        source = wiktionary[self.locale].format(year=date.today().year)
        glos.setInfo("description", source)
        glos.setInfo("title", f"Wiktionary {self.locale.upper()}-{self.locale.upper()}")
        glos.convert(
            inputFilename=str(self.output_dir / f"dict-{self.locale}-{self.locale}.df"),
            outputFilename=str(self.output_dir / "dict-data.ifo"),
            writeOptions={"dictzip": False},
            sqlite=False,
        )

    def _cleanup(self) -> None:
        import shutil

        for file in self.output_dir.glob("dict-data.*"):
            file.unlink()
        with suppress(FileNotFoundError):
            shutil.rmtree(self.output_dir / "res")

    def process(self) -> None:
        self._cleanup()
        self._convert()
        final_file = self.output_dir / f"dict-{self.locale}-{self.locale}.zip"
        with ZipFile(final_file, mode="w", compression=ZIP_DEFLATED) as fh:
            for file in self.output_dir.glob("dict-data.*"):
                fh.write(file, arcname=file.name)
            for entry in self.output_dir.glob("res/*"):
                fh.write(entry, arcname=f"res/{entry.name}")

            # Check the ZIP validity
            # testzip() returns the name of the first corrupt file, or None
            assert fh.testzip() is None, fh.testzip()

        self.summary(final_file)


def get_primary_formaters() -> List[Type[BaseFormat]]:
    return [KoboFormat, DictFileFormat]


def get_secundary_formaters() -> List[Type[BaseFormat]]:
    """Formaters that require files generated by `get_primary_formaters()`."""
    return [StarDictFormat]


def run_formatter(
    cls: Type[BaseFormat],
    locale: str,
    output_dir: Path,
    words: Words,
    variants: Variants,
    snapshot: str,
) -> None:
    formater = cls(locale, output_dir, words, variants, snapshot)
    formater.process()


def load(file: Path) -> Words:
    """Load the big JSON file containing all words and their details."""
    print(f">>> Loading {file} ...", flush=True)
    with file.open(encoding="utf-8") as fh:
        words: Words = json.load(fh)
    print(f">>> Loaded {len(words):,} words from {file}", flush=True)
    return words


def make_variants(words: Words) -> Variants:
    """Group word by variant."""
    variants: Variants = defaultdict(list)
    for word, details in words.items():
        details = Word(*details)
        # Variant must be normalized by trimming whitespace and lowercasing it.
        for variant in details.variants:
            if variant:
                variants[variant].append(word)
    return variants


def get_latest_json_file(output_dir: Path) -> Optional[Path]:
    """Get the name of the last data-*.json file."""
    files = list(output_dir.glob("data-*.json"))
    return sorted(files)[-1] if files else None


def distribute_workload(
    formaters: List[Type[BaseFormat]],
    output_dir: Path,
    file: Path,
    locale: str,
    words: Words,
    variants: Variants,
) -> None:
    """Run formaters in parallel."""
    with Pool(len(formaters)) as pool:
        pool.map(
            partial(
                run_formatter,
                locale=locale,
                output_dir=output_dir,
                words=words,
                variants=variants,
                snapshot=file.stem.split("-")[1],
            ),
            formaters,
        )


def main(locale: str) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    file = get_latest_json_file(output_dir)
    if not file:
        print(">>> No dump found. Run with --render first ... ", flush=True)
        return 1

    # Get all words from the database
    words: Words = load(file)
    variants: Variants = make_variants(words)

    # And run formaters, distributing the workload
    args = (output_dir, file, locale, words, variants)
    distribute_workload(get_primary_formaters(), *args)
    distribute_workload(get_secundary_formaters(), *args)
    return 0
