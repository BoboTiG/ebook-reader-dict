from scripts_utils import get_soup

ROOT = "https://en.wiktionary.org"


def get_text(url: str) -> str:
    soup = get_soup(url)
    div = soup.find("span", "form-of-definition")
    if not div:
        return ""
    res = str(div.text).replace(" term", "")
    return res.replace(" [Term?]", "")


def print_aliases(template: str, text: str, dot: bool) -> int:
    count = 0
    url_template = f"{ROOT}/wiki/Special:WhatLinksHere?target=Template%3A{template}&namespace=&hidetrans=1&hidelinks=1"
    soup = get_soup(url_template)
    if ul := soup.find("ul", attrs={"id": "mw-whatlinkshere-list"}):
        for li in ul.children:
            alias = li.find("a").text.split(":")[1]
            print(f'    "{alias}": {{')
            print(f'        "text": "{text}",')
            print(f'        "dot": {tds["dot"] == "yes"},')
            print("    },")
            count += 1
    return count


url = f"{ROOT}/wiki/Category:Form-of_templates"
soup = get_soup(url)
tables = soup.find_all("table", "wikitable")

columns = ["template", "aliases", "cat", "inflection", "cap", "dot", "from", "pos"]

body = tables[0].find("tbody")
trs = body.find_all("tr")
trs.pop(0)  # remove header
count = 0
print("form_of_templates = {")
for tr in trs:
    tds_html = tr.find_all("td")
    tds0 = [t.text.strip() for t in tds_html]
    if tds := dict(zip(columns, tds0)):
        link = tr.find("a")
        url_template = ROOT + link["href"]
        if text := get_text(url_template):
            print(f'    "{tds["template"]}": {{')
            print(f'        "text": "{text}",')
            print(f'        "dot": {tds["dot"] == "yes"},')
            print("    },")
            count += 1
            count += print_aliases(tds["template"], text, tds["dot"] == "yes")


print(f"}}  # {count:,}")
