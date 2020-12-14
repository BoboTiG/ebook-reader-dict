import os
import re
from .render import get_latest_json_file, load, find_sections, find_all_sections
from typing import Dict, List
from collections import defaultdict
from pathlib import Path


def find_titles(code: str, locale: str) -> List[str]:
    """Find the correct section(s) holding the current locale definition(s)."""
    return [
        section.title.strip()
        for section in find_all_sections(code, locale)
        if section.title
    ]


def find_templates(in_words: Dict[str, str], locale: str) -> None:
    sections = defaultdict(list)
    templates: Dict[str, str] = {}
    for in_word, code in in_words.items():
        for title in find_titles(code, locale):
            sections[title].append(in_word)

        parsed_sections = find_sections(code, locale)
        defs = "\n".join(str(s) for s in parsed_sections.values())
        for template in re.findall(r"({{[^{}]*}})", defs):
            template = template.split("|")[0].lstrip("{").rstrip("}").strip()
            if template not in templates:
                templates[template] = in_word

    with open("sections.txt", "w") as f:
        for title, entries in sorted(sections.items()):
            f.write(f"{title!r} ({len(entries):,})\n")
            if len(entries) < 10:
                # Most likely errors/mispellings
                for entry in entries:
                    f.write(f"    - {entry!r}\n")
            else:
                f.write(f"    - {entries[0]!r}\n")

    if templates:
        with open("templates.txt", "w") as f:
            for template, entry in sorted(templates.items()):
                f.write(f"{entry!r} => {template!r}\n")


def main(locale: str) -> int:
    output_dir = Path(os.getenv("CWD", "")) / "data" / locale
    filename = get_latest_json_file(locale, output_dir)
    if not filename:
        print(">>> No data-XXXXXX.json found. Run with --parse first ... ", flush=True)
        return 1

    print(f">>> Loading {filename} ...")
    in_words: Dict[str, str] = load(filename)

    find_templates(in_words, locale)

    print(">>> Find templates and sections done!", flush=True)
    return 0
