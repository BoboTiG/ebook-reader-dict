"""Render templates from raw data."""

from __future__ import annotations

import json
import logging
import multiprocessing
import os
import re
from collections import defaultdict
from contextlib import suppress
from datetime import timedelta
from functools import partial
from itertools import chain
from pathlib import Path
from time import monotonic
from typing import TYPE_CHECKING, cast

import wikitextparser as wtp
import wikitextparser._spans

from . import lang, utils
from .namespaces import namespaces
from .stubs import Word
from .user_functions import unique

if TYPE_CHECKING:
    from collections.abc import Callable

    from .stubs import Definitions, SubDefinitions, Words


# As stated in wikitextparser._spans.parse_pm_pf_tl():
#   If the byte_array passed to parse_to_spans contains n WikiLinks, then
#   this function will be called n + 1 times. One time for the whole byte_array
#   and n times for each of the n WikiLinks.
#
# We do not care about links, let's speed-up the all process by skipping the n times call.
# Doing that is a ~30% optimization.
wikitextparser._spans.WIKILINK_PARAM_FINDITER = lambda *_: ()


Sections = dict[str, list[wtp.Section]]

# To list all unhandled sections:
#    DEBUG_SECTIONS=1 python -m wikidict LOCALE --render | sort -u >out.log
#
# To make words using a given section to fail:
#    DEBUG_SECTIONS="SECTION" python -m wikidict LOCALE --render
# Example with the RO dict, and the "{{unități}}" section:
#    DEBUG_SECTIONS="{{unități}}" python -m wikidict ro --render
DEBUG_SECTIONS = os.environ.get("DEBUG_SECTIONS", "0")

# To list all unhandled words:
#    DEBUG_EMPTY_WORDS=1 python -m wikidict LOCALE --render >out.log 2>&1
DEBUG_EMPTY_WORDS = "DEBUG_EMPTY_WORDS" in os.environ

log = logging.getLogger(__name__)


def find_definitions(
    word: str,
    parsed_sections: Sections,
    lang_src: str,
    lang_dst: str,
    *,
    missed_templates: list[tuple[str, str]] | None = None,
) -> list[Definitions]:
    """Find all definitions, without eventual subtext."""
    definitions = list(
        chain.from_iterable(
            find_section_definitions(word, section, lang_src, lang_dst, missed_templates=missed_templates)
            for sections in parsed_sections.values()
            for section in sections
        )
    )
    if not definitions:
        return []

    # Remove duplicates
    seen = set()
    return [d for d in definitions if not (d in seen or seen.add(d))]  # type: ignore[func-returns-value]


def es_replace_defs_list_with_numbered_lists(
    lst: wtp.WikiList,
    *,
    regex_item: re.Pattern[str] = re.compile(
        r"(^|\\n);\d+[ |:]+",
        flags=re.MULTILINE,
    ),
    regex_subitem: re.Pattern[str] = re.compile(
        r"(^|\\n):;\s*[a-z]:+\s+",
        flags=re.MULTILINE,
    ),
) -> str:
    """
    ES uses definition lists, not well supported by the parser...
    replace them by numbered lists.
    """
    res = regex_item.sub(r"\1# ", lst.string)
    return regex_subitem.sub(r"\1## ", res)


def find_section_definitions(
    word: str,
    section: wtp.Section,
    lang_src: str,
    lang_dst: str,
    *,
    missed_templates: list[tuple[str, str]] | None = None,
) -> list[Definitions]:
    """Find definitions from the given *section*, with eventual sub-definitions."""
    definitions: list[Definitions] = []

    if lang_src == "es":
        if section.title.strip().lower().startswith(("forma adjetiva", "forma verbal")):
            return definitions
        if lists := section.get_lists(pattern="[:;]"):
            section.contents = "".join(es_replace_defs_list_with_numbered_lists(lst) for lst in lists)

    if lists := section.get_lists(pattern=lang.section_patterns[lang_dst]):
        for a_list in lists:
            for idx, code in enumerate(a_list.items):
                # Ignore some patterns
                if any(ignore_me in code.lower() for ignore_me in lang.definitions_to_ignore[lang_dst]):
                    continue

                # Transform and clean the Wikicode
                definition = utils.process_templates(word, code, lang_dst, missed_templates=missed_templates)

                # Skip empty definitions
                if not definition:
                    continue

                # Keep the definition ...
                definitions.append(definition)

                # ... And its eventual sub-definitions
                subdefinitions: list[SubDefinitions] = []
                for sublist in a_list.sublists(i=idx, pattern=lang.sublist_patterns[lang_dst]):
                    for idx2, subcode in enumerate(sublist.items):
                        subdefinition = utils.process_templates(
                            word, subcode, lang_dst, missed_templates=missed_templates
                        )
                        if not subdefinition:
                            continue

                        subdefinitions.append(subdefinition)
                        subsubdefinitions: list[str] = []
                        for subsublist in sublist.sublists(i=idx2, pattern=lang.sublist_patterns[lang_dst]):
                            for subsubcode in subsublist.items:
                                if subsubdefinition := utils.process_templates(
                                    word,
                                    subsubcode,
                                    lang_dst,
                                    missed_templates=missed_templates,
                                ):
                                    subsubdefinitions.append(subsubdefinition)
                        if subsubdefinitions:
                            subdefinitions.append(tuple(subsubdefinitions))
                if subdefinitions:
                    definitions.append(tuple(subdefinitions))

    return definitions


def find_etymology(
    word: str,
    lang_src: str,
    lang_dst: str,
    parsed_section: wtp.Section,
    *,
    missed_templates: list[tuple[str, str]] | None = None,
) -> list[Definitions]:
    """Find the etymology."""

    def get_items(patterns: tuple[str, ...], *, skip: tuple[str, ...] | None = None) -> list[str]:
        items: list[str]
        try:
            items = parsed_section.get_lists(pattern=patterns)[0].items
        except IndexError:
            items = [parsed_section.contents]
        else:
            if skip:
                items = [item for item in items if not item.lstrip().lower().startswith(skip)]
        return items

    match lang_src:
        case "da":
            items = get_items(("#", ":"))
        case "de":
            items = get_items((":",))
        case "el":
            items = get_items((": ", "#"))
        case "en":
            items = get_items(("",), skip=("===etymology", "{{pie root"))
        case "eo":
            items = get_items((":",))
        case "es":
            items = get_items((r";\d",), skip=("=== etimología",))
        case "fr" | "fro":
            definitions: list[Definitions] = []
            tables = parsed_section.tables
            tableindex = 0
            for section in parsed_section.get_lists():
                for idx, section_item in enumerate(section.items):
                    if any(ignore_me in section_item.lower() for ignore_me in lang.definitions_to_ignore[lang_dst]):
                        continue
                    if section_item == ' {| class="wikitable"':
                        phrase = utils.table2html(word, lang_dst, tables[tableindex])
                        definitions.append(phrase)
                        tableindex += 1
                    else:
                        definitions.append(
                            utils.process_templates(word, section_item, lang_dst, missed_templates=missed_templates)
                        )
                        subdefinitions: list[SubDefinitions] = []
                        for sublist in section.sublists(i=idx):
                            subdefinitions.extend(
                                utils.process_templates(word, subcode, lang_dst, missed_templates=missed_templates)
                                for subcode in sublist.items
                            )
                        if subdefinitions:
                            definitions.append(tuple(subdefinitions))
            return definitions
        case "it":
            items = get_items(("",), skip=("=== {{etim",))
        case "no":
            items = get_items(("#", ":", r"\*"))
        case "pt":
            items = get_items((r"[:]", r"\*"))
        case "ro":
            items = get_items(("",), skip=("=== {{etimologie",))
        case "sv":
            items = re.findall(r"{{etymologi\|(.+)}}\s", parsed_section.contents)
        case _:
            items = [parsed_section.contents]

    return [
        etyl
        for item in items
        if (etyl := utils.process_templates(word, item, lang_dst, missed_templates=missed_templates)) and len(etyl) > 1
    ]


def _find_genders(top_sections: list[wtp.Section], lang_src: str, lang_dst: str) -> list[str]:
    """Find the genders."""
    func: Callable[[str, str], list[str]] = lang.find_genders[lang_src]
    for top_section in top_sections:
        if result := func(top_section.contents, lang_dst):
            return result
    return []


def _find_pronunciations(top_sections: list[wtp.Section], lang_src: str, lang_dst: str) -> list[str]:
    """Find pronunciations."""
    results = []
    func = lang.find_pronunciations[lang_src]
    for top_section in top_sections:
        if result := func(top_section.contents, lang_dst):
            results.extend(result)
    return sorted(unique(results))


def find_all_sections(
    code: str, lang_src: str, lang_dst: str
) -> tuple[list[wtp.Section], list[tuple[str, wtp.Section]]]:
    """Find all sections holding definitions."""
    parsed = wtp.parse(code)
    all_sections = []
    level = lang.section_level[lang_dst]

    # Add fake section for etymology if in the leading part
    if lang_src == "ca":
        etyl_data = etyl_data_section = leading_lines = ""
        etyl_l_sections = lang.etyl_section[lang_dst]

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
            all_sections.append(
                (
                    etyl_data_section,
                    wtp.Section(f"=== {etyl_data_section} ===\n{etyl_data}"),
                )
            )

    def section_title(title: str) -> str:
        if lang_src == "de":
            title = title.split("(")[-1].strip(" )")
        return title.replace(" ", "").lower().strip() if title else ""

    # Get interesting top sections
    top_sections = [
        section
        for section in parsed.get_sections(level=level)
        if section_title(section.title).startswith(lang.head_sections[lang_dst])
    ]

    # Get _all_ sections without any filtering
    all_sections.extend(
        (section.title.strip(), section)
        for top_section in top_sections
        for sublevel in lang.section_sublevels[lang_dst]
        for section in top_section.get_sections(include_subsections=False, level=sublevel)
    )

    return top_sections, all_sections


def find_sections(code: str, lang_src: str, lang_dst: str) -> tuple[list[wtp.Section], Sections]:
    """Find the correct section(s) holding the current locale definition(s)."""
    ret = defaultdict(list)
    wanted = lang.sections[lang_dst]
    top_sections, all_sections = find_all_sections(code, lang_src, lang_dst)
    for title, section in all_sections:
        title = title.lower()
        # Filter on interesting sections
        if title.startswith(wanted):
            ret[title].append(section)
        elif DEBUG_SECTIONS == "1":
            print(f"Title section rejected: {title!r}", flush=True)
        elif DEBUG_SECTIONS == title:
            assert 0  # Break the rendering to report the word as an error and be able to look into it
    return top_sections, ret


def add_potential_variant(
    word: str,
    tpl: str,
    locale: str,
    variants: list[str],
    *,
    repl: Callable[[str, str], str] = re.compile(r"(</?[^>]+>)").sub,
) -> None:
    """
    Ensure a variant identical to the word is not taken into account:
    >>> variants_lst = []
    >>> add_potential_variant("19e", "{{fr-rég|diz.nœ.vjɛm|s=19{{e}}|p=19{{e|es}}}}", "fr", variants_lst)
    >>> variants_lst
    []

    Ensure HTML tags are stripped from variants:
    >>> variants_lst = []
    >>> add_potential_variant("19es", "{{fr-rég|diz.nœ.vjɛm|s=19{{e}}|p=19{{e|es}}}}", "fr", variants_lst)
    >>> variants_lst
    ['19e']
    """
    if (variant := utils.process_templates(word, tpl, locale)) and (variant_cleaned := repl("", variant)) != word:
        # Example of false positive we try to prevent in the condition:
        #    [DE] word="Halles (Saale)" variant="Halle (Saale)"
        #    [EN] word="401(k)s"        variant="401(k)"
        if (
            any(char in variant_cleaned for char in "<>|={}")
            or any(char in variant_cleaned for char in "()")
            and all(char not in word for char in "()")
        ):
            log.warning(f"Potential variant issue: {variant=} → {variant_cleaned=} for {word=}")
        variants.append(variant_cleaned)


def adjust_wikicode(code: str, locale: str) -> str:
    r"""Sometimes we need to adapt the Wikicode.

    >>> adjust_wikicode("[[Fichier:Blason ville fr Petit-Bersac 24.svg|vignette|120px|'''Base''' d’or ''(sens héraldique)'']][[something|else]]", "fr")
    '[[something|else]]'
    >>> adjust_wikicode("[[File:Sarcoscypha_coccinea,_Salles-la-Source_(Matthieu_Gauvain).JPG|vignette|Pézize écarlate]][[something|else]]", "en")
    '[[something|else]]'
    >>> adjust_wikicode("[[File:1864 Guernesey 8 Doubles.jpg|thumb|Pièce de 8 doubles (île de [[Guernesey]], 1864).]][[something|else]]", "en")
    '[[something|else]]'
    >>> adjust_wikicode("[[fil:ISO 7010 E002 new.svg|thumb|right|160px|piktogram nødudgang]][[something|else]]", "da")
    '[[something|else]]'
    >>> adjust_wikicode("[[Catégorie:Localités d’Afrique du Sud en français]][[something|else]]", "fr")
    '[[something|else]]'
    >>> adjust_wikicode("[[Archivo:Striped_Woodpecker.jpg|thumb|[1] macho.]][[something|else]]", "es")
    '[[something|else]]'
    >>> adjust_wikicode("[[Archivo:Mezquita de Córdoba - Celosía 006.JPG|thumb|[1]]][[something|else]]", "es")
    '[[something|else]]'
    >>> adjust_wikicode("[[Archivo:Diagrama bicicleta.svg|400px|miniaturadeimagen|'''Partes de una bicicleta:'''<br>\n[[asiento]] o [[sillín]], [[cuadro]]{{-sub|8}}, [[potencia]], [[puño]]{{-sub|4}}, [[cuerno]], [[manubrio]], [[telescopio]], [[horquilla]], [[amortiguador]], [[frenos]], [[tijera]], [[rueda]], [[rayos]], [[buje]], [[llanta]], [[cubierta]], [[válvula]], [[pedal]], [[viela]], [[cambio]], [[plato]]{{-sub|5}} o [[estrella]], [[piñón]], [[cadena]], [[tija]], [[tubo de asiento]], [[vaina]].]]\n\n[[something|else]]", "es")
    '\n\n[[something|else]]'
    >>> adjust_wikicode("[[File:Karwats.jpg|thumb|A scourge ''(noun {{senseno|en|whip}})'' [[exhibit#Verb|exhibited]] in a [[museum#Noun|museum]].]][[something|else]]", "en")
    '[[something|else]]'
    >>> adjust_wikicode("[[w:Burattino|Burattino]]", "it")
    '[[Burattino|Burattino]]'
    >>> adjust_wikicode("[[en:propedeutici]]", "it")
    ''

    >>> adjust_wikicode("<!-- {{sco}} -->", "fr")
    ''
    >>> adjust_wikicode("<!--<i>sco</i> -->", "fr")
    ''
    >>> adjust_wikicode("<!--\nsco\n-->", "it")
    ''
    """

    # Namespaces (moved from `utils.clean()` to be able to filter on multiple lines)
    # [[File:...|...]] → ''
    all_namespaces = set()
    for namespace in namespaces[locale] + namespaces["en"]:
        all_namespaces.add(namespace)
        all_namespaces.add(namespace.lower())
    pattern = "|".join(iter(all_namespaces))
    code = re.sub(
        # Courtesy of Casimir et Hippolyte & Wiktor Stribiżew from https://stackoverflow.com/q/79006887/1117028
        rf"""
        # Match [[
        \[\[

        # Namespace followed by :
        (?:{pattern}):

        # Match any chars other than [ and ], or any ] that is not immediately followed with another ], or a [
        # that is not immediately followed with [ or one or more digits + ]
        [^][]*(?:](?!])[^][]*|\[(?!\[|\d+\])[^][]*)*

        # Match zero or more occurrences of either [+digit(s)+], or strings between [[ and ]] and then any chars
        # other than [ and ], or any ] that is not immediately followed with another ], or a [ that is not immediately
        # followed with [ or one or more digits + ]
        (?:(?:\[\d+\]|\[\[[^][]*(?:](?!])[^][]*|\[(?!\[)[^][]*)*\]\])[^][]*(?:](?!])[^][]*|\[(?!\[|\d+\])[^][]*)*)*

        # Match ]]
        ]]
        """,
        "",
        code,
        flags=re.VERBOSE,
    )

    # HTML comments (multiline supported)
    # <!-- foo --> → ''
    code = re.sub(r"(?=<!--)([\s\S]*?-->)", "", code)

    # {{!}} → "|"
    # code = code.replace("{{!}}", "|")

    func: Callable[[str, str], str] = lang.adjust_wikicode[locale]
    return func(code, locale)


def parse_word(
    word: str,
    code: str,
    locale: str,
    *,
    force: bool = False,
    missed_templates: list[tuple[str, str]] | None = None,
) -> Word:
    """Parse *code* Wikicode to find word details.
    *force* can be set to True to force the pronunciation and gender guessing.
    It is disabled by default to speed-up the overall process, but enabled when
    called from `get_word.get_and_parse_word()`.
    """
    lang_src, lang_dst = utils.guess_locales(locale, use_log=False, uniformize=True)

    code = adjust_wikicode(code, lang_dst)
    top_sections, parsed_sections = find_sections(code, lang_src, lang_dst)
    prons = []
    genders = []
    etymology = []
    variants: list[str] = []

    # Etymology
    if lang_src == "sv":
        for top in top_sections:
            etymology.extend(find_etymology(word, lang_src, lang_dst, top, missed_templates=missed_templates))
    elif parsed_sections:
        for section in lang.etyl_section[lang_dst]:
            # if not parsed_sections:
            #     break
            for etyl_data in parsed_sections.pop(section, []):
                etymology.extend(find_etymology(word, lang_src, lang_dst, etyl_data, missed_templates=missed_templates))

    # Definitions
    if parsed_sections:
        definitions = find_definitions(word, parsed_sections, lang_src, lang_dst, missed_templates=missed_templates)
    elif lang_src in {"no", "pt"}:
        # Some words have no head sections but only a list of definitions at the root of the "top" section
        marker = {
            "no": "===",
            "pt": "==",
        }[lang_src]
        for top in top_sections:
            contents = top.contents
            top.contents = contents[: contents.find(marker)]
        definitions = find_definitions(word, {"top": top_sections}, lang_src, lang_dst)
    else:
        definitions = []

    if definitions or force:
        prons = _find_pronunciations(top_sections, lang_src, lang_dst)
        genders = _find_genders(top_sections, lang_src, lang_dst)

    # Variants
    if parsed_sections and (interesting_titles := lang.variant_titles[lang_dst]):
        interesting_templates = lang.variant_templates[lang_dst]
        for title, parsed_section in parsed_sections.items():
            if not title.startswith(interesting_titles):
                continue
            for parsed in parsed_section:
                for tpl in parsed.templates:
                    tpl = str(tpl)
                    if tpl.startswith(interesting_templates):
                        add_potential_variant(word, tpl, lang_dst, variants)
        if variants:
            variants = sorted(set(variants))

    return Word(prons, genders, etymology, definitions, variants)


def load(file: Path) -> dict[str, str]:
    """Load the JSON file containing all words and their details."""
    with file.open(encoding="utf-8") as fh:
        words: dict[str, str] = json.load(fh)
    log.info("Loaded %s words from %s", f"{len(words):,}", file)
    return words


def render_word(
    w: list[str],
    words: Words,
    locale: str,
    *,
    missed_templates: list[tuple[str, str]] | None = None,
) -> Word | None:
    word, code = w
    try:
        details = parse_word(word, code, locale, missed_templates=missed_templates)
    except KeyboardInterrupt:
        pass
    except Exception:
        log.exception("ERROR with %r", word)
    else:
        if details.etymology or details.definitions or details.variants:
            words[word] = details
            return details

    if DEBUG_EMPTY_WORDS:
        print(f"Empty {word = }", flush=True)

    return None


def render(in_words: dict[str, str], locale: str, workers: int) -> Words:
    manager = multiprocessing.Manager()
    results: Words = cast(dict[str, Word], manager.dict())
    missed_templates: list[tuple[str, str]] = cast(list[tuple[str, str]], manager.list())

    with suppress(KeyboardInterrupt), multiprocessing.Pool(processes=workers) as pool:
        pool.map(
            partial(render_word, words=results, locale=locale, missed_templates=missed_templates),
            in_words.items(),
        )

    utils.check_for_missing_templates(list(missed_templates))

    return results.copy()


def save(output: Path, words: Words) -> None:
    """Persist data."""
    with output.open(mode="w", encoding="utf-8") as fh:
        json.dump(words, fh, indent=4, sort_keys=True)
    log.info("Saved %s words into %s", f"{len(words):,}", output)


def get_latest_json_file(source_dir: Path, locale: str) -> Path | None:
    """Get the name of the last data_wikicode-*.json file."""
    files = list(source_dir.glob(f"data_wikicode-{locale}-{'[0-9]' * 8}.json"))
    return sorted(files)[-1] if files else None


def get_source_dir(locale: str) -> Path:
    return Path(os.getenv("CWD", "")) / "data" / locale


def get_output_file(source_dir: Path, lang_src: str, lang_dst: str, snapshot: str) -> Path:
    return source_dir.parent / lang_dst / f"data-{lang_src}-{snapshot}.json"


def main(locale: str, *, workers: int = multiprocessing.cpu_count()) -> int:
    """Entry point."""

    start = monotonic()
    lang_src, lang_dst = utils.guess_locales(locale)

    source_dir = get_source_dir(lang_dst)
    if not (input_file := get_latest_json_file(source_dir, lang_src)):
        log.error("No dump found. Run with --parse first ... ")
        return 1

    log.info("Loading %s ...", input_file)
    in_words: dict[str, str] = load(input_file)

    workers = workers or multiprocessing.cpu_count()
    words = render(in_words, locale, workers)
    if not words:
        raise ValueError("Empty dictionary?!")

    output = get_output_file(source_dir, lang_src, lang_dst, input_file.stem.split("-")[-1])
    save(output, words)

    log.info("Render done in %s!", timedelta(seconds=monotonic() - start))
    return 0
