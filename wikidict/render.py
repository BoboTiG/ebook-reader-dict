"""Render templates from raw data."""
import json
import os
from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import Dict, List, Pattern

from scripts.lang import (
    definitions_to_ignore,
    genre,
    etyl_section,
    head_sections,
    pronunciation,
    section_level,
    section_sublevels,
    section_patterns,
    sections,
    sublist_patterns,
    words_to_keep,
)
from scripts.stubs import Definitions, SubDefinitions, Word, Words
from scripts.utils import clean, process_templates

import wikitextparser as wtp
import wikitextparser._spans

# As stated in wikitextparser._spans.parse_pm_pf_tl():
#   If the byte_array passed to parse_to_spans contains n WikiLinks, then
#   this function will be called n + 1 times. One time for the whole byte_array
#   and n times for each of the n WikiLinks.
#
# We do not care about links, let's speed-up the all process by skipping the n times call.
# Doing that is a ~30% optimization.
wikitextparser._spans.WIKILINK_PARAM_FINDITER = lambda *_: ()


Sections = Dict[str, wtp.Section]


def find_definitions(
    word: str, parsed_sections: Sections, locale: str
) -> List[Definitions]:
    """Find all definitions, without eventual subtext."""
    definitions = list(
        chain.from_iterable(
            find_section_definitions(word, section, locale)
            for sections in parsed_sections.values()
            for section in sections
        )
    )
    if not definitions:
        return []

    # Remove duplicates
    seen = set()
    return [d for d in definitions if not (d in seen or seen.add(d))]  # type: ignore


def find_section_definitions(
    word: str, section: wtp.Section, locale: str
) -> List[Definitions]:
    """Find definitions from the given *section*, with eventual sub-definitions."""
    definitions: List[Definitions] = []

    # do not look for definitions in french verb form section
    if locale == "fr" and section.title.strip().startswith("{{S|verbe|fr|flexion"):
        return definitions

    lists = section.get_lists(pattern=section_patterns[locale])
    if lists:
        for a_list in lists:
            for idx, code in enumerate(a_list.items):
                # Ignore some patterns
                if word not in words_to_keep[locale] and any(
                    ignore_me in code.lower()
                    for ignore_me in definitions_to_ignore[locale]
                ):
                    continue

                # Transform and clean the Wikicode
                definition = process_templates(word, clean(code), locale)
                if not definition:
                    continue

                # Keep the definition ...
                definitions.append(definition)

                # ... And its eventual sub-definitions
                subdefinitions: List[SubDefinitions] = []
                for sublist in a_list.sublists(i=idx, pattern=sublist_patterns[locale]):
                    for idx2, subcode in enumerate(sublist.items):
                        subdefinition = process_templates(word, clean(subcode), locale)
                        subdefinitions.append(subdefinition)
                        subsubdefinitions: List[str] = []
                        for subsublist in sublist.sublists(
                            i=idx2, pattern=sublist_patterns[locale]
                        ):
                            for subsubcode in subsublist.items:
                                subsubdefinitions.append(
                                    process_templates(word, clean(subsubcode), locale)
                                )
                        if subsubdefinitions:
                            subdefinitions.append(tuple(subsubdefinitions))
                if subdefinitions:
                    definitions.append(tuple(subdefinitions))

    return definitions


def find_etymology(word: str, locale: str, parsed_section: wtp.Section) -> str:
    """Find the etymology."""

    etyl: str

    if locale == "ca":
        return process_templates(word, clean(parsed_section.contents), locale)

    elif locale == "en":
        items = [
            item
            for item in parsed_section.get_lists(pattern=("",))[0].items
            if not item.lstrip().startswith(("===Etymology", "{{PIE root"))
        ]
        for item in items:
            etyl = process_templates(word, clean(item), locale)
            if etyl:
                return etyl

    elif locale == "es":
        etyl = parsed_section.get_lists(pattern=("",))[0].items[1]
        return process_templates(word, clean(etyl), locale)

    elif locale == "pt":
        section_title = parsed_section.title.strip()
        if section_title == "{{etimologia|pt}}":
            try:
                etyl = parsed_section.get_lists()[0].items[0]
            except IndexError:
                etyl = parsed_section.get_lists(pattern=("",))[0].items[1]
        else:
            # "Etimologia" title section
            try:
                etyl = parsed_section.get_lists(pattern=("^:",))[0].items[0]
            except IndexError:
                etyl = parsed_section.get_lists(pattern=("",))[0].items[1]
        return process_templates(word, clean(etyl), locale)

    etymologies = chain.from_iterable(
        section.items for section in parsed_section.get_lists()
    )
    for etymology in etymologies:
        if any(
            ignore_me in etymology.lower()
            for ignore_me in definitions_to_ignore[locale]
        ):
            continue
        etyl = process_templates(word, clean(etymology), locale)
        if etyl:
            return etyl
    return ""


def find_genre(code: str, pattern: Pattern[str]) -> str:
    """Find the genre."""
    match = pattern.search(code)
    if not match:
        return ""
    groups = match.groups()
    if not groups:
        return ""
    return groups[0] or ""


def find_pronunciations(code: str, pattern: Pattern[str]) -> List[str]:
    """Find pronunciations."""
    match = pattern.search(code)
    if not match:
        return []

    # There is at least one match, we need to get whole line
    # in order to be able to find multiple pronunciations
    line = code[match.start() : code.find("\n", match.start())]
    return pattern.findall(line)


def find_all_sections(code: str, locale: str) -> List[wtp.Section]:
    """Find all sections holding definitions."""
    parsed = wtp.parse(code)
    sections = []
    level = section_level[locale]

    # Add fake section for etymology if in the leading part
    if locale == "ca":
        etyl_data = etyl_data_section = leading_lines = ""
        etyl_l_sections = etyl_section[locale]

        leading_part = parsed.get_sections(include_subsections=False, level=level)
        if leading_part:
            leading_lines = leading_part[0].contents.split("\n")

        for etyl_l_section in etyl_l_sections:
            for line in leading_lines:
                if line.startswith(etyl_l_section):
                    etyl_data = line
                    etyl_data_section = etyl_l_section
                    break

        if etyl_data:
            sections.append(wtp.Section(f"=== {etyl_data_section} ===\n{etyl_data}"))

    # Filter on interesting sections
    for section in parsed.get_sections(include_subsections=True, level=level):
        title = section.title.replace(" ", "").lower()
        if title not in head_sections[locale]:
            continue

        for sublevel in section_sublevels[locale]:
            sections.extend(
                section.get_sections(include_subsections=False, level=sublevel)
            )

    return sections


def find_sections(code: str, locale: str) -> Sections:
    """Find the correct section(s) holding the current locale definition(s)."""
    ret = defaultdict(list)
    for section in find_all_sections(code, locale):
        title = section.title.strip()
        if not title.startswith(sections[locale]):
            continue
        ret[title].append(section)
    return ret


def parse_word(word: str, code: str, locale: str, force: bool = False) -> Word:
    """Parse *code* Wikicode to find word details.
    *force* can be set to True to force the pronunciation and genre guessing.
    It is disabled by default t spee-up the overall process, but enabled when
    called from get_and_parse_word().
    """
    parsed_sections = find_sections(code, locale)
    prons = []
    nature = ""
    etymology = ""

    # Etymology
    sections = etyl_section[locale]
    if not isinstance(sections, list):
        sections = [sections]  # type: ignore
    for section in sections:
        etyl_data = parsed_sections.pop(section, [])
        if etyl_data:
            etymology = find_etymology(word, locale, etyl_data[0])

    definitions = find_definitions(word, parsed_sections, locale)

    if definitions or force:
        prons = find_pronunciations(code, pronunciation[locale])
        nature = find_genre(code, genre[locale])

    # find if variant and delete unwanted definitions
    variants = []
    if locale == "fr" and not definitions:  # Pure verb form, no definition
        for title, s in parsed_sections.items():
            if title.startswith("{{S|verbe|fr|flexion"):
                for t in s[0].templates:
                    if t.__str__().startswith("{{fr-verbe-flexion"):
                        infinitive = process_templates(word, clean(t.__str__()), locale)
                        variants.append(infinitive)

    return Word(prons, nature, etymology, definitions, variants)


def get_latest_json_file(locale: str, output_dir: Path) -> str:
    """Get the name of the last data_wikicode-*.json file."""
    files = list(output_dir.glob("data_wikicode-*.json"))
    return str(sorted(files)[-1]) if files else ""


def load(filename: str) -> Dict[str, str]:
    """Load the JSON file containing all words and their details."""
    input_file = Path(filename)
    with input_file.open(encoding="utf-8") as fh:
        words: Dict[str, str] = json.load(fh)
    print(f">>> Loaded {len(words):,} words from {input_file}", flush=True)
    return words


def render(in_words: Dict[str, str], locale: str) -> Words:
    words: Words = {}
    sections = head_sections[locale]
    for in_word, code in in_words.items():
        # Skip not interesting words early as the parsing is quite heavy
        if all(head_section not in code for head_section in sections):
            continue

        try:
            details = parse_word(in_word, code, locale)
        except Exception:  # pragma: nocover
            print(f"ERROR with {in_word!r}", flush=True)
        else:
            if details.definitions or details.variants:
                words[in_word] = details
    return words


def save(snapshot: str, words: Words, output_dir: Path) -> None:
    """Persist data."""
    raw_data = output_dir / f"data-{snapshot}.json"
    with raw_data.open(mode="w", encoding="utf-8") as fh:
        json.dump(words, fh, indent=4, sort_keys=True)

    (output_dir / "words.count").write_text(str(len(words)))
    (output_dir / "words.snapshot").write_text(snapshot)

    print(f">>> Saved {len(words):,} words into {raw_data}", flush=True)


def main(locale: str) -> int:
    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    filename = get_latest_json_file(locale, output_dir)
    if not filename:
        print(">>> No dump found. Run with --parse first ... ", flush=True)
        return 1

    print(f">>> Loading {filename} ...")
    in_words: Dict[str, str] = load(filename)
    words = render(in_words, locale)
    if not words:  # pragma: nocover
        raise ValueError("Empty dictionary?!")

    date = filename.split(".")[0].split("-")[1]
    save(date, words, output_dir)

    print(">>> Render done!", flush=True)
    return 0
