import requests
import re
from bs4 import BeautifulSoup


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


def process_display(display):
    if "[[" in display:
        display = re.sub(
            r"\[\[(?:w|wikipedia|Wiktionary):[^|]*\|(^\])*",
            "",
            display,
            0,
            re.MULTILINE,
        )
        display = display.replace("]]", "")
        display = display.replace("[[w:", "")
        display = display.replace("[[", "")
        display = display.split("|")[-1]
    return display


def process_page(url, repl, stop_line, var_name):
    soup = get_soup(url)
    div = soup.find("div", {"class": "mw-highlight-lines"})
    text = div.text

    text = text.replace("local ", "")
    text = text.replace("true", "True")
    text = text.replace("--", "#")

    for r in repl:
        text = re.sub(fr"{r}[\s]*=", f'"{r}":', text)

    code = ""
    for line in text.split("\n"):
        if line.strip().startswith(stop_line):
            break
        elif "require" not in line:
            code += line + "\n"

    exec(code, globals())
    results = {}
    for k, v in aliases.items():  # noqa
        label_v = labels.get(v)  # noqa
        if label_v:
            display = label_v.get("display", v)  # noqa
            display = process_display(display)
            results[k] = display

    for k, v in labels.items():  # noqa
        display = v.get("display", k)
        display = process_display(display)
        if display != k:
            results[k] = display

    print(f"{var_name} = {{")
    for key, value in sorted(results.items()):
        print(f'    "{key}": "{value}",')
    print(f"}}  # {len(results):,}")


url = "https://en.wiktionary.org/wiki/Module:labels/data/topical"
repl = (
    "topical_categories",
    "display",
    "plain_categories",
)
stop_line = "return"
var_name = "labels_topical"
process_page(url, repl, stop_line, var_name)

print()

url = "https://en.wiktionary.org/wiki/Module:labels/data/regional"
repl = (
    "regional_categories",
    "special_display",
    "display",
    "Wikipedia",
    "plain_categories",
    "language",
)
stop_line = "# Adds labels"
var_name = "labels_regional"
process_page(url, repl, stop_line, var_name)

print()

url = "https://en.wiktionary.org/wiki/Module:labels/data/subvarieties"
repl = (
    "regional_categories",
    "special_display",
    "display",
    "Wikipedia",
    "plain_categories",
    "language",
    "track",
)
stop_line = "if there is a"
var_name = "labels_subvarieties"
process_page(url, repl, stop_line, var_name)

print()
