import re

from scripts_utils import get_soup


def read_all_lines_etym(lines: list[str]) -> dict[str, dict[str, str]]:
    # remove aliases
    lua_code = "\n".join(lines)
    lua_code = re.sub(r"aliases\s*=\s*{([^}]*)}", "", lua_code, count=0, flags=re.MULTILINE | re.DOTALL)
    lines = lua_code.split("\n")

    pattern = re.compile(r"(\w*)\s*=\s*([{|\"].*[}|\"])")
    pattern2 = re.compile(r"(\w*)\s*=\s*{")
    concat = ""
    in_comment = False
    for line in lines:
        line = line.strip()
        if line == "local" or line.startswith("for code, family"):
            break
        if "require" in line:
            continue
        if line.startswith("--[[") or line.startswith("--[=["):
            in_comment = True
            continue
        if in_comment and line.startswith("]]") or line.startswith("]=]--"):
            in_comment = False
            continue
        if in_comment:
            continue
        if line.startswith(("--", "return", "end", "local function")):
            continue
        remove_words = ("nil,", "ancestral_to_parent", "remove_diacritics", "remove_exceptions", "m_langdata")
        if any(word in line for word in remove_words):
            continue
        # deal with "local m = {}"
        if line.startswith("local"):
            line = line.replace("local", "")
            concat += line.strip() + "\n"
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
        elif line.endswith(",") and not line.endswith("],") and not line[:-1] == "}":
            result = f"{line[:-1]} : None,"
        elif not line.endswith('"'):
            result = line

        concat += result + "\n"
    exec(concat, globals())
    return m  # type: ignore[name-defined, no-any-return] # noqa: F821


def read_all_lines_lang(lines: list[str]) -> dict[str, str]:
    code = ""
    m: dict[str, str] = {}
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


def get_content(url: str) -> list[str]:
    soup = get_soup(url)
    content_div = soup.find("div", "mw-parser-output")
    content_div = content_div.find("div", {"class": "mw-highlight"}, recursive=False)
    return str(content_div.text).split("\n")


def process_lang_page(url: str) -> dict[str, str]:
    lines = get_content(url)
    return read_all_lines_lang(lines)


# Etymology languages
lines = get_content("https://en.wiktionary.org/wiki/Module:etymology_languages/data")
mres: dict[str, dict[str, str]] = read_all_lines_etym(lines)
languages = {key: list(val.keys())[0] for key, val in mres.items()}

# Families
lines = get_content("https://en.wiktionary.org/wiki/Module:families/data")
for key, val in read_all_lines_etym(lines).items():
    languages[key] = list(val.keys())[0]

languages |= process_lang_page("https://en.wiktionary.org/wiki/Module:languages/data/2")
languages |= process_lang_page("https://en.wiktionary.org/wiki/Module:languages/data/exceptional")

for letter in "abcdefghijklmnopqrstuvwxyz":
    url = f"https://en.wiktionary.org/wiki/Module:languages/data/3/{letter}"
    languages.update(process_lang_page(url))

print("langs = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(languages):,}")
