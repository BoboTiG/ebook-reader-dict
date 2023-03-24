import re
from typing import Dict, List

from scripts_utils import get_soup


def read_all_lines_etym(lines: List[str]) -> Dict[str, Dict[str, str]]:
    # remove aliases
    lua_code = "\n".join(lines)
    lua_code = re.sub(
        r"aliases\s*=\s*{([^}]*)}", "", lua_code, 0, re.MULTILINE | re.DOTALL
    )
    lines = lua_code.split("\n")

    pattern = re.compile(r"(\w*)\s*=\s*([{|\"].*[}|\"])")
    pattern2 = re.compile(r"(\w*)\s*=\s*{")
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
        if line.startswith(("--", "return")):
            continue
        # deal with the alias_code function
        line = re.sub(r"local function\s+(\w+\([\w|\,|\s]+\))", "def \\g<1>:", line)
        line = line.replace("for _, v in ipairs(b) do", "\n    for v in b:\n       ")
        line = line.replace(" end", "")
        # deal with "local m = {}"
        if line.startswith("local"):
            line = line.replace("local", "")
            concat += line.strip() + "\n"
            continue
        remove_words = ("nil,", "ancestral_to_parent")
        if any(word in line for word in remove_words):
            continue
        if "--" in line:
            line = line.split("--")[0].strip()
        if line == ",":
            continue
        matches = pattern.findall(line)
        matches2 = pattern2.findall(line)
        if matches:
            result = f'"{matches[0][0].strip()}": {matches[0][1]},'
        elif matches2 and matches2[0]:
            result = f'"{matches2[0].strip()}' + '" : {' + line[line.index("{") + 1 :]
        else:
            if line.endswith(",") and not line.endswith("],"):
                result = f"{line[:-1]} : None,"
            elif not line.endswith('"'):
                result = line

        concat += result + "\n"
    exec(concat, globals())
    return m  # type: ignore # noqa


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
mres: Dict[str, Dict[str, str]] = read_all_lines_etym(lines)
languages = {key: list(val.keys())[0] for key, val in mres.items()}

# Families
lines = get_content("https://en.wiktionary.org/wiki/Module:families/data")
for key, val in read_all_lines_etym(lines).items():
    languages[key] = list(val.keys())[0]

languages |= process_lang_page("https://en.wiktionary.org/wiki/Module:languages/data/2")
languages |= process_lang_page(
    "https://en.wiktionary.org/wiki/Module:languages/data/exceptional"
)

for letter in "abcdefghijklmnopqrstuvwxyz":
    url = f"https://en.wiktionary.org/wiki/Module:languages/data/3/{letter}"
    languages.update(process_lang_page(url))

print("langs = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(languages):,}")
