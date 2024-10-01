"""Render templates from raw data."""

import json
import logging
import multiprocessing
import os
import re
from collections import defaultdict
from collections.abc import Callable
from functools import partial
from itertools import chain
from pathlib import Path
from typing import cast

import wikitextparser as wtp
import wikitextparser._spans

from .lang import (
    definitions_to_ignore,
    etyl_section,
    find_genders,
    find_pronunciations,
    head_sections,
    section_level,
    section_patterns,
    section_sublevels,
    sections,
    sublist_patterns,
    variant_templates,
    variant_titles,
)
from .namespaces import namespaces
from .stubs import Definitions, SubDefinitions, Word, Words
from .user_functions import uniq
from .utils import process_templates, table2html

# As stated in wikitextparser._spans.parse_pm_pf_tl():
#   If the byte_array passed to parse_to_spans contains n WikiLinks, then
#   this function will be called n + 1 times. One time for the whole byte_array
#   and n times for each of the n WikiLinks.
#
# We do not care about links, let's speed-up the all process by skipping the n times call.
# Doing that is a ~30% optimization.
wikitextparser._spans.WIKILINK_PARAM_FINDITER = lambda *_: ()


Sections = dict[str, list[wtp.Section]]

# Multiprocessing shared globals, init in render() see #1054
MANAGER = ""
LOCK = multiprocessing.Lock()
MISSING_TPL_SEEN: list[str] = []

log = logging.getLogger(__name__)


def find_definitions(word: str, parsed_sections: Sections, locale: str) -> list[Definitions]:
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
    return [d for d in definitions if not (d in seen or seen.add(d))]  # type: ignore[func-returns-value]


def es_replace_defs_list_with_numbered_lists(
    lst: wtp.WikiList,
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


def find_section_definitions(word: str, section: wtp.Section, locale: str) -> list[Definitions]:
    """Find definitions from the given *section*, with eventual sub-definitions."""
    definitions: list[Definitions] = []

    # do not look for definitions in french verb form section
    if locale == "fr" and section.title.strip().startswith("{{S|verbe|fr|flexion"):
        return definitions

    if locale == "es":
        if section.title.strip().startswith(("Forma adjetiva", "Forma verbal")):
            return definitions
        if lists := section.get_lists(pattern="[:;]"):
            section.contents = "".join(es_replace_defs_list_with_numbered_lists(lst) for lst in lists)

    if lists := section.get_lists(pattern=section_patterns[locale]):
        for a_list in lists:
            for idx, code in enumerate(a_list.items):
                # Ignore some patterns
                if any(ignore_me in code.lower() for ignore_me in definitions_to_ignore[locale]):
                    continue

                # Transform and clean the Wikicode
                definition = process_templates(word, code, locale)

                # Skip empty definitions
                if not definition:
                    continue

                # Keep the definition ...
                definitions.append(definition)

                # ... And its eventual sub-definitions
                subdefinitions: list[SubDefinitions] = []
                for sublist in a_list.sublists(i=idx, pattern=sublist_patterns[locale]):
                    for idx2, subcode in enumerate(sublist.items):
                        subdefinition = process_templates(word, subcode, locale)
                        if not subdefinition:
                            continue

                        subdefinitions.append(subdefinition)
                        subsubdefinitions: list[str] = []
                        for subsublist in sublist.sublists(i=idx2, pattern=sublist_patterns[locale]):
                            for subsubcode in subsublist.items:
                                if subsubdefinition := process_templates(word, subsubcode, locale):
                                    subsubdefinitions.append(subsubdefinition)
                        if subsubdefinitions:
                            subdefinitions.append(tuple(subsubdefinitions))
                if subdefinitions:
                    definitions.append(tuple(subdefinitions))

    return definitions


def find_etymology(word: str, locale: str, parsed_section: wtp.Section) -> list[Definitions]:
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

    items = [parsed_section.contents]
    match locale:
        case "da":
            items = get_items(("#", ":"))
        case "de":
            items = get_items((":",))
        case "el":
            items = get_items((": ",))
        case "en":
            items = get_items(("",), skip=("===etymology", "{{pie root"))
        case "es":
            items = get_items(("",), skip=("=== etimología",))
        case "fr":
            definitions: list[Definitions] = []
            tables = parsed_section.tables
            tableindex = 0
            for section in parsed_section.get_lists():
                for idx, section_item in enumerate(section.items):
                    if any(ignore_me in section_item.lower() for ignore_me in definitions_to_ignore[locale]):
                        continue
                    if section_item == ' {| class="wikitable"':
                        phrase = table2html(word, locale, tables[tableindex])
                        definitions.append(phrase)
                        tableindex += 1
                    else:
                        definitions.append(process_templates(word, section_item, locale))
                        subdefinitions: list[SubDefinitions] = []
                        for sublist in section.sublists(i=idx):
                            subdefinitions.extend(process_templates(word, subcode, locale) for subcode in sublist.items)
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

    return [etyl for item in items if (etyl := process_templates(word, item, locale)) and len(etyl) > 1]


def _find_genders(top_sections: list[wtp.Section], func: Callable[[str], list[str]]) -> list[str]:
    """Find the genders."""
    for top_section in top_sections:
        if result := func(top_section.contents):
            return result
    return []


def _find_pronunciations(top_sections: list[wtp.Section], func: Callable[[str], list[str]]) -> list[str]:
    """Find pronunciations."""
    results = []
    for top_section in top_sections:
        if result := func(top_section.contents):
            results.extend(result)
    return sorted(uniq(results))


def find_all_sections(code: str, locale: str) -> tuple[list[wtp.Section], list[tuple[str, wtp.Section]]]:
    """Find all sections holding definitions."""
    parsed = wtp.parse(code)
    all_sections = []
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
            all_sections.append(
                (
                    etyl_data_section,
                    wtp.Section(f"=== {etyl_data_section} ===\n{etyl_data}"),
                )
            )

    def section_title(title: str) -> str:
        if locale == "de":
            title = title.split("(")[-1].strip(" )")
        return title.replace(" ", "").lower().strip() if title else ""

    # Get interesting top sections
    top_sections = [
        section
        for section in parsed.get_sections(include_subsections=True, level=level)
        if section_title(section.title) in head_sections[locale]
    ]

    # Get _all_ sections without any filtering
    all_sections.extend(
        (section.title.strip(), section)
        for top_section in top_sections
        for sublevel in section_sublevels[locale]
        for section in top_section.get_sections(include_subsections=False, level=sublevel)
    )

    return top_sections, all_sections


def find_sections(code: str, locale: str) -> tuple[list[wtp.Section], Sections]:
    """Find the correct section(s) holding the current locale definition(s)."""
    ret = defaultdict(list)
    wanted = sections[locale]
    top_sections, all_sections = find_all_sections(code, locale)
    for title, section in all_sections:
        # Filter on interesting sections
        if title.startswith(wanted):
            ret[title].append(section)
    return top_sections, ret


def add_potential_variant(word: str, tpl: str, locale: str, variants: list[str]) -> None:
    if (variant := process_templates(word, tpl, locale)) and variant != word:
        variants.append(variant)


def adjust_wikicode(code: str, locale: str) -> str:
    r"""Sometimes we need to adapt the Wikicode.

    >>> adjust_wikicode('{| class="floatright"\n|-\n| {{PIE word|en|h₁eǵʰs}}\n| {{PIE word|en|ḱóm}}\n|}', "en")
    ''
    >>> adjust_wikicode('{| class="floatright"\n|-\n| {{PIE word|en|h₁eǵʰs}}\n| {{PIE word|en|ḱóm}}\n|}{{root|en|ine-pro|*(s)ker-|id=cut|*h₃reǵ-}}', "en")
    '{{root|en|ine-pro|*(s)ker-|id=cut|*h₃reǵ-}}'
    >>> adjust_wikicode("<math>\\frac{|AP|}{|BP|} = \\frac{|AC|}{|BC|}</math>", "en")
    '<math>\\frac{|AP|}{|BP|} = \\frac{|AC|}{|BC|}</math>'

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

    >>> adjust_wikicode("----", "no")
    ''

    >>> adjust_wikicode("<!-- {{sco}} -->", "fr")
    ''
    >>> adjust_wikicode("<!--<i>sco</i> -->", "fr")
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

    # HTML comments
    # <!-- foo --> → ''
    code = re.sub(r"<!--(?:.+-->)?", "", code)

    if locale == "da":
        # {{=da=}} → =={{da}}==
        code = re.sub(r"\{\{=(\w{2})=\}\}", r"=={{\1}}==", code, flags=re.MULTILINE)

    elif locale == "de":
        # {{Bedeutungen}} → === {{Bedeutungen}} ===
        code = re.sub(r"^\{\{(.+)\}\}", r"=== {{\1}} ===", code, flags=re.MULTILINE)

        # Definition lists are not well supported by the parser, replace them by numbered lists
        # Note: using `[ ]*` rather than `\s*` to bypass issues when a section above another one
        #       contains an empty item.
        code = re.sub(r":\[\d+\][ ]*", "# ", code)

        # {{!}} → "|"
        code = code.replace("{{!}}", "|")

    elif locale == "en":
        # Remove tables (cf issue #2073)
        code = re.sub(r"^\{\|.*?\|\}", "", code, flags=re.DOTALL | re.MULTILINE)

    elif locale == "es":
        # {{ES|xxx|núm=n}} → == {{lengua|es}} ==
        code = re.sub(r"^\{\{ES\|.+\}\}", r"== {{lengua|es}} ==", code, flags=re.MULTILINE)

    elif locale == "it":
        if "{{Tabs" not in code:
            # Hack for a fake variants to support more of them
            # `# plurale di [[-ectomia]]`
            code = re.sub(
                r"^(#\s?)+((?:femminile|plurale) [^\[]+)\[\[([^\]]+)\]\]",
                r"\1{{\2|\3}}",
                code,
                flags=re.MULTILINE,
            )

    elif locale == "no":
        code = code.replace("----", "")

    elif locale == "ro":
        locale = "ron"

        # {{-avv-|ANY|ANY}} → === {{avv|ANY|ANY}} ===
        code = re.sub(
            r"^\{\{-(.+)-\|(\w+)\|(\w+)\}\}",
            r"=== {{\1|\2|\3}} ===",
            code,
            flags=re.MULTILINE,
        )

        # Try to convert old Wikicode
        if "==Romanian==" in code:
            # ==Romanian== → == {{limba|ron}} ==
            code = code.replace("==Romanian==", "== {{limba|ron}} ==")

            # ===Adjective=== → === {{Adjective}} ===
            code = re.sub(r"===(\w+)===", r"=== {{\1}} ===", code, flags=re.MULTILINE)

        # ===Verb tranzitiv=== → === {{Verb tranzitiv}} ===
        code = re.sub(r"====([^=]+)====", r"=== {{\1}} ===", code, flags=re.MULTILINE)

        # Hack for a fake variants support because RO doesn't use templates most of the time
        # `#''forma de feminin singular pentru'' [[frumos]].` → `# {{forma de feminin singular pentru|frumos}}`
        code = re.sub(
            r"^(#\s?)'+(forma de [^']+)'+\s*'*\[\[([^\]]+)\]\]'*\.?",
            r"\1{{\2|\3}}",
            code,
            flags=re.MULTILINE,
        )

    if locale in {"it", "ron", "da"}:
        # {{-avv-|it}} → === {{avv}} ===
        code = re.sub(
            rf"^\{{\{{-(.+)-\|{locale}\}}\}}",
            r"=== {{\1}} ===",
            code,
            flags=re.MULTILINE,
        )

        # {{-avv-|ANY}} → === {{avv|ANY}} ===
        code = re.sub(r"^\{\{-(.+)-\|(\w+)\}\}", r"=== {{\1|\2}} ===", code, flags=re.MULTILINE)

        # {{-avv-}} → === {{avv}} ===
        code = re.sub(r"^\{\{-(\w+)-\}\}", r"=== {{\1}} ===", code, flags=re.MULTILINE)

        # {{!}} → "|"
        code = code.replace("{{!}}", "|")

    return code


def parse_word(word: str, code: str, locale: str, force: bool = False) -> Word:
    """Parse *code* Wikicode to find word details.
    *force* can be set to True to force the pronunciation and gender guessing.
    It is disabled by default to speed-up the overall process, but enabled when
    called from get_and_parse_word().
    """
    code = adjust_wikicode(code, locale)
    top_sections, parsed_sections = find_sections(code, locale)
    prons = []
    genders = []
    etymology = []
    variants: list[str] = []

    # Etymology
    for section in etyl_section[locale]:
        if etyl_data := parsed_sections.pop(section, []):
            etymology = find_etymology(word, locale, etyl_data[0])

    definitions = find_definitions(word, parsed_sections, locale)

    if definitions or force:
        prons = _find_pronunciations(top_sections, find_pronunciations[locale])
        genders = _find_genders(top_sections, find_genders[locale])

    # Find potential variants
    if interesting_titles := variant_titles[locale]:
        interesting_templates = variant_templates[locale]
        for title, parsed_section in parsed_sections.items():
            if not title.startswith(interesting_titles):
                continue
            for tpl in parsed_section[0].templates:
                tpl = str(tpl)
                if tpl.startswith(interesting_templates):
                    add_potential_variant(word, tpl, locale, variants)
        if variants:
            variants = sorted(set(variants))

    return Word(prons, genders, etymology, definitions, variants)


def load(file: Path) -> dict[str, str]:
    """Load the JSON file containing all words and their details."""
    with file.open(encoding="utf-8") as fh:
        words: dict[str, str] = json.load(fh)
    log.info("Loaded %s words from %s", f"{len(words):,}", file)
    return words


def render_word(w: list[str], words: Words, locale: str) -> None:
    word, code = w
    try:
        details = parse_word(word, code, locale)
    except Exception:  # pragma: nocover
        log.exception("ERROR with %r", word)
    else:
        if details.definitions or details.variants:
            words[word] = details


def render(in_words: dict[str, str], locale: str, workers: int) -> Words:
    # Skip not interesting words early as the parsing is quite heavy
    sections = head_sections[locale]
    in_words = {word: code for word, code in in_words.items() if any(head_section in code for head_section in sections)}

    MANAGER = multiprocessing.Manager()
    MISSING_TPL_SEEN = MANAGER.list()  # noqa: F841
    results: Words = cast(dict[str, Word], MANAGER.dict())

    with multiprocessing.Pool(processes=workers) as pool:
        pool.map(partial(render_word, words=results, locale=locale), in_words.items())

    return results.copy()


def save(snapshot: str, words: Words, output_dir: Path) -> None:
    """Persist data."""
    raw_data = output_dir / f"data-{snapshot}.json"
    with raw_data.open(mode="w", encoding="utf-8") as fh:
        json.dump(words, fh, indent=4, sort_keys=True)
    log.info("Saved %s words into %s", f"{len(words):,}", raw_data)


def get_latest_json_file(output_dir: Path) -> Path | None:
    """Get the name of the last data_wikicode-*.json file."""
    files = list(output_dir.glob("data_wikicode-*.json"))
    return sorted(files)[-1] if files else None


def main(locale: str, workers: int = multiprocessing.cpu_count()) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    file = get_latest_json_file(output_dir)
    if not file:
        log.error("No dump found. Run with --parse first ... ")
        return 1

    log.info("Loading %s ...", file)
    in_words: dict[str, str] = load(file)

    workers = workers or multiprocessing.cpu_count()
    words = render(in_words, locale, workers)
    if not words:
        raise ValueError("Empty dictionary?!")

    date = file.stem.split("-")[1]
    save(date, words, output_dir)

    log.info("Render done!")
    return 0
