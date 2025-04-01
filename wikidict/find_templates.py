"""DEBUG: find all templates in use."""

import logging
import os
import re
from collections import defaultdict
from pathlib import Path

from . import lang, render, utils

log = logging.getLogger(__name__)


def find_titles(code: str, lang_src: str, lang_dst: str) -> list[str]:
    """Find the correct section(s) holding the current locale definition(s)."""
    _, all_sections = render.find_all_sections(code, lang_src, lang_dst)
    return [title for title, _ in all_sections]


def find_templates(in_words: dict[str, str], lang_src: str, lang_dst: str) -> None:
    found_sections = defaultdict(list)
    templates: dict[str, str] = {}
    locale_sections = lang.sections[lang_dst]
    for in_word, code in in_words.items():
        if lang_src == "da":
            code = render.adjust_wikicode(code, lang_dst)

        for title in find_titles(code, lang_src, lang_dst):
            found_sections[title].append(in_word)

        _, parsed_sections = render.find_sections(code, lang_src, lang_dst)
        defs = "\n".join(str(s) for s in parsed_sections.values())
        for template in re.findall(r"({{[^{}]*}})", defs):
            if template.startswith(locale_sections):
                continue
            template = template.split("|")[0].lstrip("{").rstrip("}").strip()
            if template not in templates:
                templates[template] = in_word

    if not found_sections:
        log.warning("No sections found.")
        return

    with open("sections.txt", "w", encoding="utf-8") as f:
        for title, entries in sorted(found_sections.items()):
            f.write(f"{title!r} ({len(entries):,})\n")
            if len(entries) < 10:
                # Most likely errors/mispellings
                for entry in entries:
                    f.write(f"    - {entry!r}\n")
            else:
                f.write(f"    - {entries[0]!r}\n")
    log.info("File sections.txt created.")

    if templates:
        with open("templates.txt", "w", encoding="utf-8") as f:
            for template, entry in sorted(templates.items()):
                f.write(f"{entry!r} => {template!r}\n")
        log.info("File templates.txt created.")
    else:
        log.warning("No templates found.")


def main(locale: str) -> int:
    """Entry point."""

    lang_src, lang_dst = utils.guess_locales(locale)

    source_dir = Path(os.getenv("CWD", "")) / "data" / lang_dst
    if not (file := render.get_latest_json_file(source_dir, lang_src)):
        log.error("No dump found. Run with --parse first ... ")
        return 1

    log.info("Loading %s ...", file)
    in_words = render.load(file)

    log.info("Working, please be patient ...")
    find_templates(in_words, lang_src, lang_dst)
    return 0
