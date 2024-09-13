"""DEBUG: find all templates in use."""

import os
import re
from collections import defaultdict
from pathlib import Path

from .lang import sections
from .render import adjust_wikicode, find_all_sections, find_sections, get_latest_json_file, load


def find_titles(code: str, locale: str) -> list[str]:
    """Find the correct section(s) holding the current locale definition(s)."""
    _, all_sections = find_all_sections(code, locale)
    return [title for title, _ in all_sections]


def find_templates(in_words: dict[str, str], locale: str) -> None:
    found_sections = defaultdict(list)
    templates: dict[str, str] = {}
    locale_sections = sections[locale]
    for in_word, code in in_words.items():
        if locale == "da":
            code = adjust_wikicode(code, locale)

        for title in find_titles(code, locale):
            found_sections[title].append(in_word)

        _, parsed_sections = find_sections(code, locale)
        defs = "\n".join(str(s) for s in parsed_sections.values())
        for template in re.findall(r"({{[^{}]*}})", defs):
            if template.startswith(locale_sections):
                continue
            template = template.split("|")[0].lstrip("{").rstrip("}").strip()
            if template not in templates:
                templates[template] = in_word

    if not found_sections:
        print("No sections found.", flush=True)
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
    print(">>> File sections.txt created.", flush=True)

    if templates:
        with open("templates.txt", "w", encoding="utf-8") as f:
            for template, entry in sorted(templates.items()):
                f.write(f"{entry!r} => {template!r}\n")
        print(">>> File templates.txt created.")
    else:
        print("No templates found.", flush=True)


def main(locale: str) -> int:
    """Entry point."""

    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    file = get_latest_json_file(output_dir)
    if not file:
        print(">>> No dump found. Run with --parse first ... ", flush=True)
        return 1

    print(f">>> Loading {file} ...", flush=True)
    in_words: dict[str, str] = load(file)

    print(">>> Working, please be patient ...", flush=True)
    find_templates(in_words, locale)
    return 0
