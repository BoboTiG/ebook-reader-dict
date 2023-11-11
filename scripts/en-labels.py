import re
from typing import Dict, Tuple

from scripts_utils import get_soup


def process_display(display: str) -> str:
    if "[[" in display:
        display = re.sub(
            r"\[\[(?:w|wikipedia|Wiktionary):[^|]*\|(^\])*",
            "",
            display,
            0,
            re.MULTILINE,
        )
        display = re.sub(r"\[\[[^\|\]]*\|(^\])*", "", display, 0, re.MULTILINE)
        display = display.replace("]]", "")
        display = display.replace("[[w:", "")
        display = display.replace("[[", "")
    return display


def clean_lua_text(text: str) -> str:
    text = text.replace("local ", "")
    text = text.replace("end", "")
    text = text.replace("true", "True")
    text = text.replace("false", "False")
    text = text.replace("--", "#")
    return text


def dialect_handler(text: str) -> Dict[str, str]:
    lines = text.split("\n")
    line1 = lines[0]
    match = re.search(r'"([^"]*)"', line1)
    if match:
        href = match.group(1)
        dialect_url = f"https://en.wiktionary.org/wiki/{href}"
        soup = get_soup(dialect_url)
        div = soup.find("div", {"class": "mw-highlight-lines"})
        text_dialect = div.text
        text_dialect = clean_lua_text(text_dialect)
        code = ""
        for line in text_dialect.split("\n"):
            if line.strip().startswith("aliases = "):
                break
            else:
                code += line + "\n"
        text_dialect = code
        text_dialect = text_dialect.replace('["', '"')
        text_dialect = text_dialect.replace('"] =', '" :')
        text_dialect = text_dialect.replace('"}', '"]')
        for r in ["alts", "link", "plain_categories"]:
            text_dialect = re.sub(
                rf"[ \t]+{r}[\s]*= ", f'            "{r}":', text_dialect
            )
        text_dialect = text_dialect.replace('{"', '["')
        exec(text_dialect, globals())
        results: Dict[str, str] = {}
        for k, v in labels.items():  # type: ignore # noqa
            results[k] = k
            for alt in v.get("alts", []):
                results[alt] = k
        return results
    else:
        return {}


def process_page(
    url: str,
    repl: Tuple[str, ...],
    stop_line: str,
    var_name: str,
    print_result: bool = True,
) -> Dict[str, str]:
    soup = get_soup(url)
    div = soup.find("div", {"class": "mw-highlight-lines"})
    text = div.text
    if text.startswith("local data = require"):
        return dialect_handler(text)
    text = text.replace("local ", "")
    text = text.replace("end", "")
    text = text.replace("true", "True")
    text = text.replace("false", "False")
    text = text.replace("--", "#")

    text = re.sub(r"function\s+(\w+\([\w|\,|\s]+\))", "def \\g<1>:", text)
    text = text.replace("for _, v in ipairs(b) do", "\n    for v in b:\n        ")

    for r in repl:
        text = re.sub(rf"[ \t]+{r}[\s]*=", f'    "{r}":', text)
        if r != "labels":
            text = re.sub(rf"{r}[\s]*=", f'"{r}":', text)

    code = ""
    for line in text.split("\n"):
        if line.strip().startswith(stop_line):
            break
        elif "require" not in line:
            code += line + "\n"

    exec(code, globals())
    results: Dict[str, str] = {}

    for k, v in labels.items():  # type: ignore # noqa
        if k == "deprecated label":
            continue
        label_v = v
        label_k = k
        aliases = []
        if isinstance(v, str):
            label_v = labels.get(v, v)  # type: ignore # noqa
            if label_v != v:
                label_k = v
        if isinstance(label_v, str):
            display = label_v
        else:
            display = label_v.get("display", label_k)
            aliases = label_v.get("aliases", [])
        display = process_display(display)
        results[k] = display

        if isinstance(aliases, str):
            aliases = [aliases]
        for a in aliases:
            results[a] = display

    if print_result:
        print(f"{var_name} = {{")
        for key, value in sorted(results.items()):
            print(f'    "{key}": "{value}",')
        print(f"}}  # {len(results):,}")
    return results


url = "https://en.wiktionary.org/wiki/Module:labels/data"
repl = (
    "deprecated_aliases",
    "special_display",
    "aliases",
    "alias_of",
    "category",
    "labels",
    "deprecated",
    "display",
    "glossary",
    "language",
    "omit_preComma",
    "omit_postComma",
    "omit_preSpace",
    "plain_categories",
    "pos_categories",
    "regional_categories",
    "sense_categories",
    "topical_categories",
    "track",
    "wikipedia",
    "Wikipedia",
    "Wiktionary",
)
stop_line = "return labels"
var_name = "labels"
results_data: Dict[str, str] = {}
results_data |= process_page(url, repl, stop_line, "", print_result=False)

url = "https://en.wiktionary.org/wiki/Module:labels/data/qualifiers"
stop_line = "return require("
results_data |= process_page(url, repl, stop_line, "", print_result=False)
print(f"{var_name} = {{")
for key, value in sorted(results_data.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(results_data):,}")

syntaxes: Dict[str, Dict[str, bool]] = {}
for k, v in labels.items():  # type: ignore # noqa
    label_v = v
    if isinstance(v, str):
        label_v = labels.get(v)  # type: ignore # noqa
    if not label_v:
        continue
    omit_preComma = label_v.get("omit_preComma")
    omit_postComma = label_v.get("omit_postComma")
    omit_preSpace = label_v.get("omit_preSpace")

    aliases = []
    aliases = label_v.get("aliases", [])

    if omit_postComma or omit_preComma or omit_preSpace:
        for a in aliases:
            syntaxes[a] = {
                "omit_postComma": bool(omit_postComma),
                "omit_preComma": bool(omit_preComma),
                "omit_preSpace": bool(omit_preSpace),
            }
        syntaxes[k] = {
            "omit_postComma": bool(omit_postComma),
            "omit_preComma": bool(omit_preComma),
            "omit_preSpace": bool(omit_preSpace),
        }

print()
print("label_syntaxes = {")
for key, value in sorted(syntaxes.items()):  # type: ignore
    print(f'    "{key}": {{')
    for k, v in value.items():  # type: ignore
        print(f'        "{k}": {v},')
    print("    },")
print(f"}}  # {len(syntaxes):,}")

print()

url = "https://en.wiktionary.org/wiki/Module:labels/data/topical"
stop_line = "return"
var_name = "labels_topical"
process_page(url, repl, stop_line, var_name)

print()

url = "https://en.wiktionary.org/wiki/Module:labels/data/regional"
stop_line = "return labels"
var_name = "labels_regional"
process_page(url, repl, stop_line, var_name)

print()

# labels_subvarieties
root_url = "https://en.wiktionary.org"
url = "https://en.wiktionary.org/wiki/Special:PrefixIndex/Module:labels/data/lang/"

soup = get_soup(url)
div = soup.find("div", {"class": "mw-prefixindex-body"})
lis = div.findAll("li")
results: Dict[str, str] = {}
for li in lis:
    if not li.text.endswith("documentation"):
        href = li.find("a")["href"]
        page_url = root_url + href
        stop_line = "return"
        var_name = "labels_subvarieties"
        results |= process_page(page_url, repl, stop_line, var_name, print_result=False)

print(f"{var_name} = {{")
for key, value in sorted(results.items()):
    if len(key) < 62:  # if it's too long, it's not useful
        print(f'    "{key}": "{value}",')
print(f"}}  # {len(results):,}")
