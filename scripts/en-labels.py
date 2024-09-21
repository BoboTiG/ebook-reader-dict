import re

from scripts_utils import get_content, get_soup


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
    return text.replace("--", "#")


def dialect_handler(text: str) -> dict[str, str]:
    lines = text.split("\n")
    line1 = lines[0]
    if not (match := re.search(r'"([^"]*)"', line1)):
        return {}

    soup = get_soup(f"https://en.wiktionary.org/wiki/{match[1]}")
    div = soup.find("div", {"class": "mw-highlight-lines"})
    text_dialect = div.text
    text_dialect = clean_lua_text(text_dialect)
    code = ""
    for line in text_dialect.split("\n"):
        if line.strip().startswith("aliases = "):
            break
        code += line + "\n"

    text_dialect = code
    text_dialect = text_dialect.replace('["', '"')
    text_dialect = text_dialect.replace('"] =', '" :')
    text_dialect = text_dialect.replace('"}', '"]')
    for r in ["alts", "link", "plain_categories"]:
        text_dialect = re.sub(rf"[ \t]+{r}[\s]*= ", f'            "{r}":', text_dialect)
    text_dialect = text_dialect.replace('{"', '["')

    exec(text_dialect, globals())
    results: dict[str, str] = {}
    for k, v in labels.items():  # type: ignore[name-defined] # noqa: F821
        results[k] = k
        for alt in v.get("alts", []):
            results[alt] = k

    return results


def process_page(url: str, repl: list[str], stop_line: str, var_name: str, print_result: bool = True) -> dict[str, str]:
    text = get_content(f"{url}?action=raw")

    if text.startswith("local data = require"):
        return dialect_handler(text)

    text = clean_lua_text(text)
    text = text.replace('" .. ', '" + ').replace('" ..\n', '" + ')
    text = text.replace(' .. "', ' + "').replace(' ..\n"', ' + "')

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
    results: dict[str, str] = {}

    for k, v in labels.items():  # type: ignore[name-defined] # noqa: F821
        if k == "deprecated label":
            continue
        label_v = v
        label_k = k
        aliases = []
        if isinstance(v, str):
            label_v = labels.get(v, v)  # type: ignore[name-defined] # noqa: F821
            if label_v != v:
                label_k = v
        if isinstance(label_v, str):
            display = label_v
        else:
            display = label_v.get("display", label_k)
            aliases = label_v.get("aliases", [])
        display = process_display(display)
        results[k] = display.replace('"', "'")

        if isinstance(aliases, str):
            aliases = [aliases]
        for a in aliases:
            results[a] = display.replace('"', "'")

    if print_result:
        print(f"{var_name} = {{")
        for key, value in sorted(results.items()):
            print(f'    "{key}": "{value}",')
        print(f"}}  # {len(results):,}")
    return results


repl = sorted(
    [
        "accent_display",
        "accent_Wikipedia",
        "addl",
        "aliases",
        "alias_of",
        "category",
        "country",
        "labels",
        "def",
        "deprecated",
        "deprecated_aliases",
        "display",
        "form_of_display",
        "from",
        "fulldef",
        "glossary",
        "langs",
        "language",
        "nolink",
        "noreg",
        "omit_preComma",
        "omit_postComma",
        "omit_preSpace",
        "omit_postSpace",
        "othercat",
        "parent",
        "parent_label",
        "plain_categories",
        "pos_categories",
        "prep",
        "region",
        "regional_categories",
        "sense_categories",
        "special_display",
        "the",
        "topical_categories",
        "track",
        "type",
        "verb",
        "Wikidata",
        "wikipedia",
        "Wikipedia",
        "Wiktionary",
    ],
    key=len,
    reverse=True,
)

results_data: dict[str, str] = process_page(
    "https://en.wiktionary.org/wiki/Module:labels/data",
    repl,
    "return labels",
    "",
    print_result=False,
)
results_data |= process_page(
    "https://en.wiktionary.org/wiki/Module:labels/data/qualifiers",
    repl,
    "return require(",
    "",
    print_result=False,
)
print("labels = {")
for key, value in sorted(results_data.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(results_data):,}")

syntaxes: dict[str, dict[str, bool]] = {}
for k, v in labels.items():  # type: ignore[name-defined] # noqa: F821
    label_v = v
    if isinstance(v, str):
        label_v = labels.get(v)  # type: ignore[name-defined] # noqa: F821
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
for key, value in sorted(syntaxes.items()):  # type: ignore[assignment]
    print(f'    "{key}": {{')
    for k, v in value.items():  # type: ignore[attr-defined]
        print(f'        "{k}": {v},')
    print("    },")
print(f"}}  # {len(syntaxes):,}")

print()

process_page("https://en.wiktionary.org/wiki/Module:labels/data/topical", repl, "return", "labels_topical")
print()

process_page("https://en.wiktionary.org/wiki/Module:labels/data/regional", repl, "return labels", "labels_regional")
print()

# labels_subvarieties
soup = get_soup("https://en.wiktionary.org/wiki/Special:PrefixIndex/Module:labels/data/lang/")
div = soup.find("div", {"class": "mw-prefixindex-body"})
results: dict[str, str] = {}
for li in div.findAll("li"):
    if li.text.endswith("documentation"):
        continue

    if (page_url := f"https://en.wiktionary.org{li.find('a')['href']}").endswith(("example", "/functions")):
        continue

    stop_line = "################## accent qualifiers" if page_url.endswith("/en") else "return"
    results |= process_page(page_url, repl, stop_line, "labels_subvarieties", print_result=False)

print("labels_subvarieties = {")
for key, value in sorted(results.items()):
    if len(key) < 62 and len(key):  # if it's too long, it's not useful
        print(f'    "{key}": "{value}",')
print(f"}}  # {len(results):,}")
