import re
from scripts_utils import get_soup


def read_all_lines_etym(lines):
    pattern = re.compile(r"(\w*)\s*=\s*([{|\"].*[}|\"])")
    pattern2 = re.compile(r"(\w*)\s*=\s*{")

    m = {}  # noqa
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


def read_all_lines_lang(lines):
    code = ""
    m = {}
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


def get_content(url):
    soup = get_soup(url)
    content_div = soup.find("div", "mw-parser-output")
    content_div = content_div.findChild(
        "div", {"class": "mw-highlight"}, recursive=False
    )
    return content_div.text.split("\n")


def process_lang_page(url):
    lines = get_content(url)
    return read_all_lines_lang(lines)


# Etymology languages
url = "https://en.wiktionary.org/wiki/Module:etymology_languages/data"
lines = get_content(url)
m = read_all_lines_etym(lines)
languages = {key: m[key]["canonicalName"] for key in m.keys()}

# Families
url = "https://en.wiktionary.org/wiki/Module:families/data"
lines = get_content(url)
m = read_all_lines_etym(lines)
for key in m.keys():
    languages[key] = m[key]["canonicalName"]

url = "https://en.wiktionary.org/wiki/Module:languages/data2"
m = process_lang_page(url)
languages |= m

url = "https://en.wiktionary.org/wiki/Module:languages/datax"
m = process_lang_page(url)
languages |= m

for letter in "abcdefghijklmnopqrstuvwxyz":
    url = f"https://en.wiktionary.org/wiki/Module:languages/data3/{letter}"
    m = process_lang_page(url)
    languages.update(m)

print("langs = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(languages):,}")
