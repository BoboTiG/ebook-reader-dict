"""Convert rendered data to working dictionaries."""

from __future__ import annotations

import bz2
import gc
import gzip
import hashlib
import json
import logging
import multiprocessing
import os
import shutil
from collections import defaultdict
from datetime import date
from functools import partial
from pathlib import Path
from time import monotonic
from typing import TYPE_CHECKING
from zipfile import ZIP_DEFLATED, ZipFile

from jinja2 import Template
from marisa_trie import Trie
from pyglossary.glossary_v2 import ConvertArgs, Glossary

from . import constants
from .lang import wiktionary
from .stubs import Word
from .user_functions import flatten
from .utils import (
    convert_gender,
    convert_pronunciation,
    format_description,
    guess_prefix,
)

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any

    from .stubs import Groups, Variants, Words

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
        <var>
        {%- for variant in variants -%}
            <variant name="{{ variant }}"/>
        {%- endfor -%}
        </var>
    {% endif %}
</w>
"""
)

# DictFile-related dictionaries
# Source: https://pgaskin.net/dictutil/dictgen/#dictfile-format
# Source: https://github.com/hunspell/hunspell/blob/ecc6dbb52025bdf3a766429988e64190d912765f/man/hunspell.1#L93-L139 (for later, in case of issues with other sub-formats)
WORD_TPL_DICTFILE = Template(
    """\
@ {{ word }}
{%- if current_word or pronunciation or gender %}
:
    {%- if current_word %} <b>{{ current_word }}</b>{%- endif -%}
    {%- if pronunciation -%}{{ pronunciation }}{%- endif %}
    {%- if gender -%}{{ gender }}{%- endif -%}
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

    template = Template("")  # To be set by subclasses

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
        self.words = words.copy()
        self.variants = variants.copy()
        self.snapshot = snapshot
        self.include_etymology = include_etymology

        logging.basicConfig(level=logging.INFO)
        log.info(
            "[%s] Starting the conversion with %s words, and %s variants ...",
            type(self).__name__,
            f"{len(words):,}",
            f"{len(variants):,}",
        )

    def dictionary_file(self, output_file: str) -> Path:
        return self.output_dir / output_file.format(
            self.locale, "" if self.include_etymology else constants.NO_ETYMOLOGY_SUFFIX
        )

    def handle_word(self, word: str, words: Words) -> Generator[str]:
        details = words[word]
        current_words = {word: details}
        word_group_prefix = guess_prefix(word)

        if details.variants and any(guess_prefix(variant) != word_group_prefix for variant in details.variants):
            # [***] Variants are more like typos, or misses, and so devices expect word & variants to start with same letters, at least.
            # An example in FR, where "suis" (verb flexion) is a variant of both "ếtre" & "suivre": "suis" & "être" are quite differents.
            # As a workaround, we yield as many words as there are variants but under the word "suis": at the end, we will have 3 words:
            #   - "suis" with the content "suis" (itself)
            #   - "suis" with the content "être"
            #   - "suis" with the content "suivre"
            for variant in details.variants:
                if root := self.words.get(variant):
                    current_words[variant] = root

        for current_word, current_details in sorted(current_words.items()):
            if not current_details.definitions:
                continue

            if variants := self.variants.get(current_word, []):
                # Add variants of empty* variant, only 1 redirection:
                #   [ES] gastada* -> gastado* -> gastar --> (gastada, gastado) -> gastar
                # Note: the process works backward: from gastar up to gastado up to gastada.
                for variant in variants.copy():
                    if (wv := words.get(variant)) and not wv.definitions:
                        variants.extend(self.variants.get(variant, []))

                # Filter out variants:
                #   - variants being identical to the word (it happens when altering `current_words`, cf [***])
                #   - with a different prefix that their word
                current_word_group_prefix = guess_prefix(current_word)
                variants = [
                    variant
                    for variant in variants
                    if variant != word and guess_prefix(variant) == current_word_group_prefix
                ]

                if isinstance(self, KoboFormat):
                    # Variant must be normalized by trimming whitespace and lowercasing it
                    variants = [variant.lower().strip() for variant in variants]

            yield self.render_word(
                self.template,
                word=word,
                current_word=(current_word if isinstance(self, KoboFormat) or current_word != word else ""),
                definitions=current_details.definitions,
                pronunciation=convert_pronunciation(current_details.pronunciations),
                gender=convert_gender(current_details.genders),
                etymologies=current_details.etymology if self.include_etymology else [],
                variants=sorted(variants, key=lambda s: (len(s), s)),
            )

    def process(self) -> None:  # pragma: nocover
        raise NotImplementedError()

    @staticmethod
    def render_word(template: Template, **kwargs: Any) -> str:
        return "".join(line.strip() for line in template.render(**kwargs).splitlines()) + "\n"

    def compute_checksum(self, file: Path) -> None:
        checksum = hashlib.new(constants.ASSET_CHECKSUM_ALGO, file.read_bytes()).hexdigest()
        checksum_file = file.with_suffix(f"{file.suffix}.{constants.ASSET_CHECKSUM_ALGO}")
        checksum_file.write_text(f"{checksum} {file.name}")
        log.info("[%s] Crafted %s (%s)", type(self).__name__, checksum_file.name, checksum)

    def summary(self, file: Path) -> None:
        log.info("[%s] Generated %s (%s bytes)", type(self).__name__, file.name, f"{file.stat().st_size:,}")
        self.compute_checksum(file)


class KoboFormat(BaseFormat):
    """Save the data into Kobo-specific ZIP file."""

    output_file = "dicthtml-{0}-{0}{1}.zip"
    template = WORD_TPL_KOBO

    def process(self) -> None:
        self.groups = self.make_groups(self.words)
        self.save()

    @staticmethod
    def sanitize(locale: str, content: str) -> str:
        """Sanitize the INSTALL.txt file content."""
        content = content.replace(":arrow_right:", "->")
        content = content.replace("`", '"')
        content = content.replace("<sub>", "")
        content = content.replace("</sub>", "")

        for etym_suffix in {"", constants.NO_ETYMOLOGY_SUFFIX}:
            content = content.replace(f" (dict-{locale}-{locale}{etym_suffix}.mobi.zip)", "")
            content = content.replace(f" (dict-{locale}-{locale}{etym_suffix}.zip)", "")
            content = content.replace(f" (dict-{locale}-{locale}{etym_suffix}.df.bz2)", "")
            content = content.replace(f" (dicthtml-{locale}-{locale}{etym_suffix}.zip)", "")
            content = content.replace(f" (dictorg-{locale}-{locale}{etym_suffix}.zip)", "")

        return content

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

    def save(self) -> None:  # sourcery skip: extract-method
        """
        Format of resulting dicthtml-LOCALE-LOCALE.zip:

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
        to_compress: list[Path] = []

        # First, create individual HTML files
        wordlist: list[str] = []
        for prefix, words in self.groups.items():
            to_compress.append(self.save_html(prefix, words, tmp_dir))
            wordlist.extend(words.keys())

        # Then create the special "words" file
        to_compress.append(self.craft_index(wordlist, tmp_dir))

        # Finally, create the ZIP
        final_file = self.dictionary_file(self.output_file)
        with ZipFile(final_file, mode="w", compression=ZIP_DEFLATED) as fh:
            # The ZIP's comment will serve as the dictionary signature
            fh.comment = bytes(wiktionary[self.locale].format(year=date.today().year), "utf-8")

            # Unrelated files, just for history
            fh.writestr(
                constants.ZIP_INSTALL,
                self.sanitize(self.locale, format_description(self.locale, len(self.words), self.snapshot)),
            )
            fh.writestr(constants.ZIP_WORDS_COUNT, str(len(self.words)))
            fh.writestr(constants.ZIP_WORDS_SNAPSHOT, self.snapshot)

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
            for word in words:
                fh.writelines(self.handle_word(word, words))

        # Compress the HTML with gzip
        output = output_dir / f"{name}.html"
        with raw_output.open(mode="rb") as fi, gzip.open(output, mode="wb") as fo:
            fo.writelines(fi)

        return output


class DictFileFormat(BaseFormat):
    """Save the data into a *.df* DictFile."""

    output_file = "dict-{0}-{0}{1}.df"
    template = WORD_TPL_DICTFILE

    def process(self) -> None:
        file = self.dictionary_file(self.output_file)
        with file.open(mode="w", encoding="utf-8") as fh:
            for word in self.words:
                fh.writelines(self.handle_word(word, self.words))

        self.summary(file)

    @staticmethod
    def render_word(template: Template, **kwargs: Any) -> str:
        return template.render(**kwargs) + "\n\n"


class DictFileFormatForMobi(DictFileFormat):
    """Save the data into a *.df* DictFile."""

    output_file = f"altered-{DictFileFormat.output_file}"


class ConverterFromDictFile(DictFileFormat):
    target_format = ""
    target_suffix = ""
    final_file = ""  # {0} = locale, {1} etymology-free suffix
    zip_glob_files = "dict-data.*"
    dictfile_format_cls = DictFileFormat
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
        glos.setInfo("website", constants.GH_REPOS)
        glos.setInfo("date", f"{self.snapshot[:4]}-{self.snapshot[4:6]}-{self.snapshot[6:8]}")

        self.output_dir_tmp.mkdir()

        # Workaround for Esperanto (EO) not being supported by kindlegen
        if isinstance(self, MobiFormat) and self.locale == "eo":
            # According to https://higherlanguage.com/languages-similar-to-esperanto/,
            # French seems the most similar lang that is available on kindlegen, so French it is.
            glos.sourceLangName = "French"
            glos.targetLangName = "French"

        glos.convert(
            ConvertArgs(
                inputFilename=str(self.dictionary_file(self.dictfile_format_cls.output_file)),
                outputFilename=str(self.output_dir_tmp / f"dict-data.{self.target_suffix}"),
                writeOptions=self.glossary_options,
                sqlite=True,
            )
        )

    def _compress(self) -> Path:
        final_file = self.dictionary_file(self.final_file)
        with ZipFile(final_file, mode="w", compression=ZIP_DEFLATED) as fh:
            for file in self.output_dir_tmp.glob(self.zip_glob_files):
                fh.write(file, arcname=file.name)

            for entry in (self.output_dir / self.target_format).glob("res/*"):
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
    final_file = "dictorg-{0}-{0}{1}.zip"
    glossary_options = {"dictzip": True, "install": False}


class MobiFormat(ConverterFromDictFile):
    """Save the data into a Mobi file.

    Incompatibility issues:

    1) No support for multiple HTML tags, they will be ignored:

        Warning(inputpreprocessor):W29007: Rejected unknown tag: <bdi>

    2) Most locales are not fully supported:

        Warning(index build):W15008: language not supported. Using default phonetics for spellchecker: english.

    3) Greek (EL), and Russian (RU), locales might be incorrectly displayed:

        Error(core):E1008: Failed conversion to unicode. The resulting string may contain wrong characters.

    4) Embedded GIF/SVG codes are extracted to their own files, but it's not clear where they are located, so there are no images for now:

        Warning(prcgen):W14010: media file not found /.../mobi/dict-data.mobi/OEBPS/XXX.gif

    """

    target_format = "mobi"
    target_suffix = "mobi"
    final_file = "dict-{0}-{0}{1}.mobi.zip"
    zip_glob_files = ""  # Will be set in `_compress()`
    dictfile_format_cls = DictFileFormatForMobi
    glossary_options = {"cover_path": str(COVER_FILE), "keep": True, "kindlegen_path": str(KINDLEGEN_FILE)}

    def _compress(self) -> Path:
        # Move the relevant file at the top-level data folder, and rename it for more accuracy
        src = self.output_dir_tmp / f"dict-data.{self.target_suffix}" / "OEBPS" / f"content.{self.target_suffix}"
        file = src.rename(self.dictionary_file(self.final_file.removesuffix(".zip")))
        self.zip_glob_files = f"../{file.name}"
        return super()._compress()


class StarDictFormat(ConverterFromDictFile):
    """Save the data into a StarDict file."""

    target_format = "stardict"
    target_suffix = "ifo"
    final_file = "dict-{0}-{0}{1}.zip"
    glossary_options = {"dictzip": True}


def get_primary_formatters() -> list[type[BaseFormat]]:
    return [KoboFormat, DictFileFormat]


def get_secondary_formatters() -> list[type[BaseFormat]]:
    """Formatters that require files generated by `get_primary_formatters()`."""
    return [BZ2DictFileFormat, DictOrgFormat, StarDictFormat]


def run_mobi_formatter(
    output_dir: Path,
    file: Path,
    locale: str,
    words: Words,
    variants: Variants,
    *,
    include_etymology: bool = True,
) -> None:
    """Mobi formatter.

    For multiple languages, we need to delete words if the total number of unique unicode characters is greater than 256.
    To do this, we delete words using the least-used characters until we meet this condition.
    """

    if locale in {"en", "fr", "fro"}:

        def all_chars(word: str, details: Word) -> set[str]:
            chars = set(word)
            if definitions := details.definitions:
                if isinstance(definitions, str):
                    chars.update(definitions)
                elif isinstance(definitions, tuple):
                    chars.update(flatten(definitions))
            if etymology := details.etymology:
                if isinstance(etymology, str):
                    chars.update(etymology)
                elif isinstance(etymology, tuple):
                    chars.update(flatten(etymology))
            return chars

        stats = defaultdict(list)
        for word, details in words.items():
            for char in all_chars(word, details):
                stats[char].append(word)

        if len(stats) > 256:
            new_words = words.copy()
            threshold = 1
            while len(stats) > 256:
                log.info(
                    "[Mobi] Removing words with unique characters count at %d (total is %d)", threshold, len(stats)
                )
                for char, related_words in sorted(stats.copy().items(), key=lambda v: (char, len(v[1]))):
                    if len(related_words) == threshold:
                        for w in related_words:
                            new_words.pop(w, None)
                        stats.pop(char)
                    if len(stats) <= 256:
                        break
                threshold += 1

            log.info(
                "[Mobi] Removed %s words from .mobi (total words count is %s, unique characters count is %d)",
                f"{len(words) - len(new_words):,}",
                f"{len(new_words):,}",
                len(stats),
            )
            words = new_words
            variants = make_variants(words)

    args = (locale, output_dir, words, variants, file.stem.split("-")[1])
    run_formatter(DictFileFormatForMobi, *args, include_etymology=include_etymology)
    run_formatter(MobiFormat, *args, include_etymology=include_etymology)


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
    formatter = cls(
        locale,
        output_dir,
        words,
        variants,
        snapshot,
        include_etymology=include_etymology,
    )
    formatter.process()


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
        for variant in details.variants:
            variants[variant].append(word)
    return variants


def get_latest_json_file(output_dir: Path) -> Path | None:
    """Get the name of the last data-*.json file."""
    files = list(output_dir.glob("data-*.json"))
    return sorted(files)[-1] if files else None


def distribute_workload(
    formatters: list[type[BaseFormat]],
    output_dir: Path,
    file: Path,
    locale: str,
    words: Words,
    variants: Variants,
    *,
    include_etymology: bool = True,
) -> None:
    """Run formatters in parallel."""
    with multiprocessing.Pool(len(formatters)) as pool:
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
            formatters,
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

    # And run formatters, distributing the workload
    args = (output_dir, file, locale, words, variants)

    # Force not using `fork()` on GNU/Linux to prevent deadlocks on "slow" machines (see issue #2333)
    multiprocessing.set_start_method("spawn", force=True)

    start = monotonic()
    for include_etymology in [False, True]:
        distribute_workload(get_primary_formatters(), *args, include_etymology=include_etymology)
        distribute_workload(get_secondary_formatters(), *args, include_etymology=include_etymology)
        run_mobi_formatter(*args, include_etymology=include_etymology)

    log.info("Convert done in %d sec!", monotonic() - start)
    return 0
