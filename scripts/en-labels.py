from scripts_utils import get_soup
import re


def process_display(display):
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


def process_page(url, repl, stop_line, var_name, print_result=True):
    soup = get_soup(url)
    div = soup.find("div", {"class": "mw-highlight-lines"})
    text = div.text

    text = text.replace("local ", "")
    text = text.replace("end", "")
    text = text.replace("true", "True")
    text = text.replace("false", "False")
    text = text.replace("--", "#")

    text = re.sub(r"function\s+(\w+\([\w|\,]+\))", "def \\g<1>:", text)
    text = text.replace("for _,v in ipairs(y) do", "for v in y:")

    for r in repl:
        text = re.sub(rf"[ \t]+{r}[\s]*=", f'    "{r}":', text)

    code = ""
    for line in text.split("\n"):
        if line.strip().startswith(stop_line):
            break
        elif "require" not in line:
            code += line + "\n"

    exec(code, globals())
    results = {}

    for k, v in labels.items():  # noqa
        label_v = v
        label_k = k
        if isinstance(v, str):
            label_v = labels.get(v, v)  # noqa
            if label_v != v:
                label_k = v
        if isinstance(label_v, str):
            display = label_v
        else:
            display = label_v.get("display", label_k)
        display = process_display(display)
        if display != k and "deprecated label" not in display:
            results[k] = display
    if print_result:
        print(f"{var_name} = {{")
        for key, value in sorted(results.items()):
            print(f'    "{key}": "{value}",')
        print(f"}}  # {len(results):,}")
    return results


url = "https://en.wiktionary.org/wiki/Module:labels/data"
repl = (
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
    "special_display",
    "topical_categories",
    "track",
    "wikipedia",
    "Wikipedia",
)
stop_line = "# Regional labels"
var_name = "labels"
process_page(url, repl, stop_line, var_name)

syntaxes = {}
for k, v in labels.items():  # noqa
    label_v = v
    if isinstance(v, str):
        label_v = labels.get(v)  # noqa
    if not label_v:
        continue
    omit_preComma = label_v.get("omit_preComma")
    omit_postComma = label_v.get("omit_postComma")
    omit_preSpace = label_v.get("omit_preSpace")
    if omit_postComma or omit_preComma or omit_preSpace:
        syntaxes[k] = {
            "omit_postComma": bool(omit_postComma),
            "omit_preComma": bool(omit_preComma),
            "omit_preSpace": bool(omit_preSpace),
        }

print()
print("label_syntaxes = {")
for key, value in sorted(syntaxes.items()):
    print(f'    "{key}": {{')
    for k, v in value.items():
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
results = {}
for li in lis:
    if not li.text.endswith("documentation"):
        href = li.find("a")["href"]
        page_url = root_url + href
        stop_line = "return"
        var_name = "labels_subvarieties"
        results |= process_page(page_url, repl, stop_line, var_name, print_result=False)

print(f"{var_name} = {{")
for key, value in sorted(results.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(results):,}")
