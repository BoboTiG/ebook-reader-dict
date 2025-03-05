"""Convert rendered data to working dictionaries."""

import bz2
import gc
import gzip
import hashlib
import json
import logging
import os
import re
import shutil
from collections import defaultdict
from collections.abc import Generator
from datetime import date
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from jinja2 import Template
from marisa_trie import Trie
from pyglossary.glossary_v2 import ConvertArgs, Glossary

from .constants import ASSET_CHECKSUM_ALGO, GH_REPOS, NO_ETYMOLOGY_SUFFIX
from .lang import wiktionary
from .stubs import Groups, Variants, Word, Words
from .utils import (
    convert_gender,
    convert_pronunciation,
    format_description,
    guess_prefix,
)

# Kobo-related dictionaries
WORD_TPL_KOBO = Template(
    """\
<w>
    <p>
        <a name="{{ word }}"/><b>{{ current_word }}</b>{{ pronunciation }}{{ gender }}
        <br/>
        <br/>
        <ol>
            {% for definition in definitions %}
                {% if definition is string %}
                    <li>{{ definition }}</li>
                {% else %}
                    <ol style="list-style-type:lower-alpha">
                        {% for sub_def in definition %}
                            {% if sub_def is string %}
                                <li>{{ sub_def }}</li>
                            {% else %}
                                <ol style="list-style-type:lower-roman">
                                    {% for sub_sub_def in sub_def %}
                                        <li>{{ sub_sub_def }}</li>
                                    {% endfor %}
                                </ol>
                            {% endif %}
                        {% endfor %}
                    </ol>
                {% endif %}
            {% endfor %}
        </ol>
        {% if etymologies %}
            {% for etymology in etymologies %}
                {% if etymology is string %}
                    <p>{{ etymology }}</p>
                {% else %}
                    <ol>
                        {% for sub_etymology in etymology %}
                            <li>{{ sub_etymology }}</li>
                        {% endfor %}
                    </ol>
                {% endif %}
            {% endfor %}
            <br/>
        {% endif %}
    </p>
    {% if variants %}
        {{ variants }}
    {% endif %}
</w>
"""
)

# DictFile-related dictionaries
WORD_TPL_DICTFILE = Template(
    """\
@ {{ word }}
{%- if pronunciation or gender %}
: {{ pronunciation }} {{ gender }}
{%- endif %}
{%- for variant in variants %}
& {{ variant }}
{%- endfor %}
<html><ol>
    {%- for definition in definitions -%}
        {%- if definition is string -%}
            <li>{{ definition }}</li>
        {%- else -%}
            <ol style="list-style-type:lower-alpha">
                {%- for sub_def in definition -%}
                    {%- if sub_def is string -%}
                        <li>{{ sub_def }}</li>
                    {%- else -%}
                        <ol style="list-style-type:lower-roman">
                            {%- for sub_sub_def in sub_def -%}
                                <li>{{ sub_sub_def }}</li>
                            {%- endfor -%}
                        </ol>
                    {%- endif -%}
                {%- endfor -%}
            </ol>
        {%- endif -%}
    {%- endfor -%}
</ol>
{%- if etymologies -%}
    {%- for etymology in etymologies -%}
        {%- if etymology is string -%}
            <p>{{ etymology }}</p>
        {%- else -%}
            <ol>
                {%- for sub_etymology in etymology -%}
                    <li>{{ sub_etymology }}</li>
                {%- endfor -%}
            </ol>
        {%- endif -%}
    {%- endfor -%}
    <br/>
{%- endif -%}</html>
"""
)

# Mobi
COVER_FILE = Path(__file__).parent.parent / "cover.png"
KINDLEGEN_FILE = Path.home() / ".local" / "bin" / "kindlegen"

log = logging.getLogger(__name__)


class BaseFormat:
    """Base class for all dictionaries."""

    __slots__ = {
        "locale",
        "output_dir",
        "snapshot",
        "words",
        "variants",
        "include_etymology",
    }

    def __init__(
        self,
        locale: str,
        output_dir: Path,
        words: Words,
        variants: Variants,
        snapshot: str,
        *,
        include_etymology: bool = True,
    ) -> None:
        self.locale = locale
        self.output_dir = output_dir
        self.words = words
        self.variants = variants
        self.snapshot = snapshot
        self.include_etymology = include_etymology

    def dictionary_file(self, output_file: str) -> Path:
        file = self.output_dir / output_file.format(locale=self.locale)
        if not self.include_etymology:
            file = file.with_stem(f"{file.stem}{NO_ETYMOLOGY_SUFFIX}")
        return file

    def handle_word(self, word: str, details: Word, **kwargs: Any) -> Generator[str]:  # pragma: nocover
        raise NotImplementedError()

    def process(self) -> None:  # pragma: nocover
        raise NotImplementedError()

    @staticmethod
    def render_word(template: Template, **kwargs: Any) -> str:
        return "".join(line.strip() for line in template.render(**kwargs).splitlines()) + "\n"

    @staticmethod
    def compute_checksum(file: Path) -> None:
        checksum = hashlib.new(ASSET_CHECKSUM_ALGO, file.read_bytes()).hexdigest()
        checksum_file = file.with_suffix(f"{file.suffix}.{ASSET_CHECKSUM_ALGO}")
        checksum_file.write_text(f"{checksum} {file.name}")
        log.info("Crafted %s (%s)", checksum_file.name, checksum)

    def summary(self, file: Path) -> None:
        log.info("Generated %s (%s bytes)", file.name, f"{file.stat().st_size:,}")
        self.compute_checksum(file)


class KoboFormat(BaseFormat):
    """Save the data into Kobo-specific ZIP file."""

    output_file = "dicthtml-{locale}-{locale}.zip"

    def process(self) -> None:
        self.groups = self.make_groups(self.words)
        self.save()

    @staticmethod
    def create_install(locale: str, output_dir: Path) -> Path:
        """Generate the INSTALL.txt file."""
        release = format_description(locale, output_dir)

        # Sanitization
        release = release.replace(":arrow_right:", "->")
        # With etymology
        release = release.replace(f" (dict-{locale}-{locale}.mobi)", "")
        release = release.replace(f" (dict-{locale}-{locale}.zip)", "")
        release = release.replace(f" (dict-{locale}-{locale}.df.bz2)", "")
        release = release.replace(f" (dicthtml-{locale}-{locale}.zip)", "")
        release = release.replace(f" (dictorg-{locale}-{locale}.zip)", "")
        # Without etymology
        release = release.replace(f" (dict-{locale}-{locale}{NO_ETYMOLOGY_SUFFIX}.mobi)", "")
        release = release.replace(f" (dict-{locale}-{locale}{NO_ETYMOLOGY_SUFFIX}.zip)", "")
        release = release.replace(f" (dict-{locale}-{locale}{NO_ETYMOLOGY_SUFFIX}.df.bz2)", "")
        release = release.replace(f" (dicthtml-{locale}-{locale}{NO_ETYMOLOGY_SUFFIX}.zip)", "")
        release = release.replace(f" (dictorg-{locale}-{locale}{NO_ETYMOLOGY_SUFFIX}.zip)", "")
        release = release.replace("`", '"')
        release = release.replace("<sub>", "")
        release = release.replace("</sub>", "")

        file = output_dir / "INSTALL.txt"
        file.write_text(release)
        return file

    @staticmethod
    def craft_index(wordlist: list[str], output_dir: Path) -> Path:
        """Generate the special file "words" that is an index of all words."""
        output = output_dir / "words"
        trie = Trie(wordlist)
        trie.save(output)
        return output

    @staticmethod
    def make_groups(words: Words) -> Groups:
        """Group word by prefix."""
        groups: Groups = defaultdict(dict)
        for word, details in words.items():
            groups[guess_prefix(word)][word] = details
        return groups

    def handle_word(self, word: str, details: Word, **kwargs: Any) -> Generator[str]:
        name: str = kwargs["name"]
        words: Words = kwargs["words"]
        current_words: Words = {word: details}

        # use variant definitions for a word if one variant prefix is different
        # "suis" listed with the definitions of "être" and "suivre"
        if details.variants:
            found_different_prefix = False
            for variant in details.variants:
                if guess_prefix(variant) != name:
                    if root_details := self.words.get(variant):
                        found_different_prefix = True
                        break
            variants_words = {}
            # if we found one variant, then list them all
            if found_different_prefix:
                for variant in details.variants:
                    if root_details := self.words.get(variant):
                        variants_words[variant] = root_details
            if word.endswith("s"):  # crude detection of plural
                singular = word[:-1]
                maybe_noun = self.words.get(singular)  # do we have the singular?
                # make sure we are not redirecting to a verb (je mange, tu manges)
                # verb form is also a singular noun
                if isinstance(maybe_noun, Word) and not maybe_noun.variants:
                    variants_words[singular] = maybe_noun
                    for variant in details.variants:
                        if maybe_verb := self.words.get(variant):
                            variants_words[variant] = maybe_verb
            if variants_words:
                current_words = variants_words

        # write to file
        for current_word, current_details in current_words.items():
            if not current_details.definitions:
                continue

            variants = ""
            if word_variants := self.variants.get(word, []):
                # add variants of empty* variant, only 1 redirection...
                # gastada* -> gastado* -> gastar --> (gastada, gastado) -> gastar
                for v in word_variants.copy():
                    wv: Word = words.get(v, Word.empty())
                    if wv and not wv.definitions:
                        for vv in self.variants.get(v, []):
                            word_variants.append(vv)
                word_variants.sort(key=lambda s: (len(s), s))
                variants = "<var>"
                for v in word_variants:
                    # no variant with different prefix
                    v = v.lower().strip()
                    if guess_prefix(v) == name:
                        variants += f'<variant name="{v}"/>'
                variants += "</var>"
            # no empty var tag
            if len(variants) < 15:
                variants = ""

            yield self.render_word(
                WORD_TPL_KOBO,
                word=word,
                current_word=current_word,
                definitions=current_details.definitions,
                pronunciation=convert_pronunciation(current_details.pronunciations),
                gender=convert_gender(current_details.genders),
                etymologies=current_details.etymology if self.include_etymology else [],
                variants=variants,
            )

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
        tmp_dir = self.output_dir / "tmp"
        shutil.rmtree(tmp_dir, ignore_errors=True)
        tmp_dir.mkdir()

        # Files to add to the final archive
        to_compress = []

        # First, create individual HTML files
        wordlist: list[str] = []
        for prefix, words in self.groups.items():
            to_compress.append(self.save_html(prefix, words, tmp_dir))
            wordlist.extend(words.keys())

        # Then create the special "words" file
        to_compress.append(self.craft_index(wordlist, tmp_dir))

        # Add unrelated files, just for history
        words_count = self.output_dir / "words.count"
        words_snapshot = self.output_dir / "words.snapshot"
        words_count.write_text(str(len(wordlist)))
        words_snapshot.write_text(self.snapshot)
        to_compress.extend(
            (
                words_count,
                words_snapshot,
                self.create_install(self.locale, self.output_dir),
            )
        )

        # Pretty print the source
        source = wiktionary[self.locale].format(year=date.today().year)

        # Finally, create the ZIP
        final_file = self.dictionary_file(self.output_file)
        with ZipFile(final_file, mode="w", compression=ZIP_DEFLATED) as fh:
            fh.comment = bytes(source, "utf-8")
            for file in to_compress:
                fh.write(file, arcname=file.name)

            # Check the ZIP validity
            # testzip() returns the name of the first corrupt file, or None
            assert fh.testzip() is None, fh.testzip()

        self.summary(final_file)

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
        """

        # Save to uncompressed HTML
        raw_output = output_dir / f"{name}.raw.html"
        with raw_output.open(mode="w", encoding="utf-8") as fh:
            for word, details in words.items():
                fh.writelines(self.handle_word(word, details, name=name, words=words))

        # Compress the HTML with gzip
        output = output_dir / f"{name}.html"
        with raw_output.open(mode="rb") as fi, gzip.open(output, mode="wb") as fo:
            fo.writelines(fi)

        return output


class DictFileFormat(BaseFormat):
    """Save the data into a *.df* DictFile."""

    output_file = "dict-{locale}-{locale}.df"

    def handle_word(self, word: str, details: Word, **kwargs: Any) -> Generator[str]:
        if details.definitions:
            yield self.render_word(
                WORD_TPL_DICTFILE,
                word=word,
                definitions=details.definitions,
                pronunciation=convert_pronunciation(details.pronunciations),
                gender=convert_gender(details.genders),
                etymologies=details.etymology if self.include_etymology else [],
                variants=self.variants.get(word, []),
            )

    def process(self) -> None:
        file = self.dictionary_file(self.output_file)
        with file.open(mode="w", encoding="utf-8") as fh:
            for word, details in self.words.items():
                fh.writelines(self.handle_word(word, details))

        self.summary(file)

    @staticmethod
    def render_word(template: Template, **kwargs: Any) -> str:
        return template.render(**kwargs) + "\n\n"


class ConverterFromDictFile(DictFileFormat):
    target_format = ""
    target_suffix = ""
    final_file = ""
    glossary_options: dict[str, str | bool] = {}

    def _patch_gc(self) -> None:
        """Bypass performances issues when calling PyGlossary from Python."""

        def noop_gc_collect() -> None:  # pragma: nocover
            pass

        gc.collect = noop_gc_collect  # type: ignore[assignment]

    def _cleanup(self) -> None:
        shutil.rmtree(self.output_dir_tmp, ignore_errors=True)

    @property
    def output_dir_tmp(self) -> Path:
        return self.output_dir / self.target_format

    def _convert(self) -> None:
        """Convert the DictFile to the target format."""
        Glossary.init()
        glos = Glossary()
        glos.config = {"cleanup": False}  # Prevent deleting temporary SQLite files

        glos.setInfo("description", wiktionary[self.locale].format(year=date.today().year))
        glos.setInfo("title", f"Wiktionary {self.locale.upper()}-{self.locale.upper()}")
        glos.setInfo("website", GH_REPOS)
        glos.setInfo("date", f"{self.snapshot[:4]}-{self.snapshot[4:6]}-{self.snapshot[6:8]}")

        self.output_dir_tmp.mkdir()
        glos.convert(
            ConvertArgs(
                inputFilename=str(self.dictionary_file(DictFileFormat.output_file)),
                outputFilename=str(self.output_dir_tmp / f"dict-data.{self.target_suffix}"),
                writeOptions=self.glossary_options,
                sqlite=True,
            )
        )

    def _compress(self) -> Path:
        final_file = self.dictionary_file(self.final_file)
        with ZipFile(final_file, mode="w", compression=ZIP_DEFLATED) as fh:
            for file in self.output_dir_tmp.glob("dict-data.*"):
                fh.write(file, arcname=file.name)

            for entry in self.output_dir.glob("res/*"):
                fh.write(entry, arcname=f"res/{entry.name}")

            # Check the ZIP validity
            # testzip() returns the name of the first corrupt file, or None
            assert fh.testzip() is None, fh.testzip()

        return final_file

    def process(self) -> None:
        self._cleanup()
        self._patch_gc()
        self._convert()
        final_file = self._compress()
        self.summary(final_file)


class BZ2DictFileFormat(BaseFormat):
    def process(self) -> None:
        df_file = self.dictionary_file(DictFileFormat.output_file)
        bz2_file = df_file.with_suffix(".df.bz2")
        bz2_file.write_bytes(bz2.compress(df_file.read_bytes()))
        return self.summary(bz2_file)


class DictOrgFormat(ConverterFromDictFile):
    """Save the data into a DICT.org file."""

    target_format = "dict.org"
    target_suffix = "index"
    final_file = "dictorg-{locale}-{locale}.zip"
    glossary_options = {"dictzip": True, "install": False}


class MobiFormat(ConverterFromDictFile):
    """Save the data into a Mobi file.

    Incompatibility issues:

    1) No support for several HTML tags, they will be ignored:

        Warning(inputpreprocessor):W29007: Rejected unknown tag: <bdi>

    2) No support for the <math> HTML tag, the HTML code adapted to be purged to prevent a hard failure:

        Error(htmlprocessor):E32001: Error occured while parsing content. HTML tag that is not supported by Kindle readers found in source  math

    3) Most locales are not properly supported:

        Warning(index build):W15008: language not supported. Using default phonetics for spellchecker: english.

    4) The Esperanto (EO) locale is not recognized at all:

        Warning(prcgen):W14024: Unrecognized language code in dc:Language metadata field.
        Error(prcgen):E23006: Language not recognized in metadata. The dc:Language field is mandatory. Aborting.

    """

    # TODO: images support
    # Warning(prcgen):W14010: media file not found /.../mobi/dict-data.mobi/OEBPS/db28a816.gif

    target_format = "mobi"
    target_suffix = "mobi"
    final_file = "dict-{locale}-{locale}.mobi"
    glossary_options = {"cover_path": str(COVER_FILE), "keep": True, "kindlegen_path": str(KINDLEGEN_FILE)}

    def _cleanup(self) -> None:
        """Alter the .df file content to remove unsupported HTML tags."""
        super()._cleanup()

        file = self.dictionary_file(DictFileFormat.output_file)
        content_old = file.read_text()
        content_new = re.sub(r"(<math>.+</math>)", "", content_old)
        if content_old != content_new:
            file.write_text(content_new)

    def _compress(self) -> Path:
        """For now, we just move the final file to its expected location."""
        src = self.output_dir_tmp / f"dict-data.{self.target_suffix}" / "OEBPS" / f"content.{self.target_suffix}"
        return src.rename(self.dictionary_file(self.final_file))

    def process(self) -> None:
        """Filter out unrecognized locales."""
        if self.locale == "eo":
            log.warning(
                "Esperanto is not a recognized language on Kindle, therefore it is not possible to create such a dictionary."
            )
        else:
            super().process()


class StarDictFormat(ConverterFromDictFile):
    """Save the data into a StarDict file."""

    target_format = "stardict"
    target_suffix = "ifo"
    final_file = "dict-{locale}-{locale}.zip"
    glossary_options = {"dictzip": True}


def get_primary_formaters() -> list[type[BaseFormat]]:
    return [KoboFormat, DictFileFormat]


def get_secondary_formaters() -> list[type[BaseFormat]]:
    """Formaters that require files generated by `get_primary_formaters()`."""
    return [BZ2DictFileFormat, DictOrgFormat, StarDictFormat]


def get_tertiary_formaters() -> list[type[BaseFormat]]:
    """Formaters that require files generated by `get_primary_formaters()` but will likely mess with them."""
    return [MobiFormat]


def run_formatter(
    cls: type[BaseFormat],
    locale: str,
    output_dir: Path,
    words: Words,
    variants: Variants,
    snapshot: str,
    *,
    include_etymology: bool = True,
) -> None:
    formater = cls(
        locale,
        output_dir,
        words,
        variants,
        snapshot,
        include_etymology=include_etymology,
    )
    formater.process()


def load(file: Path) -> Words:
    """Load the big JSON file containing all words and their details."""
    log.info("Loading %s ...", file)
    with file.open(encoding="utf-8") as fh:
        words: Words = {key: Word(*values) for key, values in json.load(fh).items()}
    log.info("Loaded %s words from %s", f"{len(words):,}", file)
    return words


def make_variants(words: Words) -> Variants:
    """Group word by variant."""
    variants: Variants = defaultdict(list)
    for word, details in words.items():
        # Variant must be normalized by trimming whitespace and lowercasing it.
        for variant in details.variants:
            if variant:
                variants[variant].append(word)
    return variants


def get_latest_json_file(output_dir: Path) -> Path | None:
    """Get the name of the last data-*.json file."""
    files = list(output_dir.glob("data-*.json"))
    return sorted(files)[-1] if files else None


def distribute_workload(
    formaters: list[type[BaseFormat]],
    output_dir: Path,
    file: Path,
    locale: str,
    words: Words,
    variants: Variants,
    *,
    include_etymology: bool = True,
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
                include_etymology=include_etymology,
            ),
            formaters,
        )


def main(locale: str) -> int:
    """Entry point."""
    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    file = get_latest_json_file(output_dir)
    if not file:
        log.error("No dump found. Run with --render first ... ")
        return 1

    # Get all words from the database
    words: Words = load(file)
    variants: Variants = make_variants(words)

    # And run formaters, distributing the workload
    args = (output_dir, file, locale, words, variants)

    distribute_workload(get_primary_formaters(), *args)
    distribute_workload(get_secondary_formaters(), *args)
    distribute_workload(get_tertiary_formaters(), *args)

    distribute_workload(get_primary_formaters(), *args, include_etymology=False)
    distribute_workload(get_secondary_formaters(), *args, include_etymology=False)
    distribute_workload(get_tertiary_formaters(), *args, include_etymology=False)

    return 0
