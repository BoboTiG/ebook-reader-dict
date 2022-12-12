import re
from typing import Dict, List

from scripts_utils import get_soup


def read_all_lines_etym(lines: List[str]) -> Dict[str, Dict[str, str]]:
    pattern = re.compile(r"(\w*)\s*=\s*([{|\"].*[}|\"])")
    pattern2 = re.compile(r"(\w*)\s*=\s*{")

    m: Dict[str, Dict[str, str]] = {}  # noqa
    concat = ""
    in_comment = False
    for line in lines:
        line = line.strip()
        if line.startswith("--[[") or line.startswith("--[=["):
            in_comment = True
            continue
        if in_comment and line.startswith("]]") or line.startswith("]=]--"):
            in_comment = False
            continue
        if in_comment:
            continue
        if line.startswith(("--", "return", "local")):
            continue
        remove_words = ("wikidata_item", "ancestral_to_parent")
        if any(word in line for word in remove_words):
            continue
        matches = pattern.findall(line)
        matches2 = pattern2.findall(line)
        if matches:
            result = '"' + matches[0][0].strip() + '": ' + matches[0][1] + ","
        elif matches2 and matches2[0]:
            result = '"' + matches2[0].strip() + '" : {' + line[line.index("{") + 1 :]
        else:
            result = line

        if "--" in result:
            result = result.split("--")[0]

        concat += result + "\n"

    exec(concat)
    return m


def read_all_lines_lang(lines: List[str]) -> Dict[str, str]:
    code = ""
    m: Dict[str, str] = {}
    pattern = re.compile(r"m\[\"(.*)\"\]\s+=\s+{")
    for line in lines:
        if code:
            line = line.split("--")[0]
            line = line.strip().strip(",").strip('"')
            m[code] = line
            code = ""
        if match := pattern.match(line):
            code = match[1]
    return m


def get_content(url: str) -> List[str]:
    soup = get_soup(url)
    content_div = soup.find("div", "mw-parser-output")
    content_div = content_div.findChild(
        "div", {"class": "mw-highlight"}, recursive=False
    )
    return str(content_div.text).split("\n")


def process_lang_page(url: str) -> Dict[str, str]:
    lines = get_content(url)
    return read_all_lines_lang(lines)


# Etymology languages
lines = get_content("https://en.wiktionary.org/wiki/Module:etymology_languages/data")
m: Dict[str, Dict[str, str]] = read_all_lines_etym(lines)
languages = {key: val["canonicalName"] for key, val in m.items()}

# Families
lines = get_content("https://en.wiktionary.org/wiki/Module:families/data")
for key, val in read_all_lines_etym(lines).items():
    languages[key] = val["canonicalName"]

languages |= process_lang_page("https://en.wiktionary.org/wiki/Module:languages/data2")
languages |= process_lang_page("https://en.wiktionary.org/wiki/Module:languages/datax")

for letter in "abcdefghijklmnopqrstuvwxyz":
    url = f"https://en.wiktionary.org/wiki/Module:languages/data3/{letter}"
    languages.update(process_lang_page(url))

print("langs = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(languages):,}")
