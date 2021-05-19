import requests
import re
from bs4 import BeautifulSoup


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


url = "https://en.wiktionary.org/wiki/Module:labels/data/regional"
soup = get_soup(url)
div = soup.find("div", {"class": "mw-highlight-lang-lua"})
text = div.text

text = text.replace("local ", "")
text = text.replace("true", "True")
text = text.replace("--", "#")


text = text.replace("regional_categories =", '"regional_categories":')
text = text.replace("special_display =", '"special_display":')
text = text.replace("display =", '"display":')

text = text.replace("Wikipedia =", '"Wikipedia":')
text = text.replace("plain_categories =", '"plain_categories":')
text = text.replace("language =", '"language":')

code = ""


def process_display(display):
    if "[[" in display:
        display = re.sub(r"\[\[w:[^|]*\|(^\])*", "", display, 0, re.MULTILINE)
        display = display.replace("]]", "")
        display = display.replace("[[w:", "")
        display = display.replace("[[", "")
    return display


stop_line = "# Adds labels"
for line in text.split("\n"):
    if line.startswith(stop_line):
        break
    elif "require" not in line:
        code += line + "\n"

exec(code)
results = {}
for k, v in aliases.items():
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

print("labels_regional = {")
for key, value in sorted(results.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(results):,}")
