import requests
from bs4 import BeautifulSoup


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


def get_text(url):
    soup = get_soup(url)
    div = soup.find("span", "form-of-definition")
    res = div.text.replace(" term", "")
    res = res.replace(" [Term?]", "")
    return res


ROOT = "https://en.wiktionary.org"
url = ROOT + "/wiki/Category:Form-of_templates"
soup = get_soup(url)
tables = soup.find_all("table", "wikitable")

columns = ["template", "aliases", "cat", "inflection", "cap", "dot", "from", "pos"]

body = tables[0].find("tbody")
trs = body.find_all("tr")
trs.pop(0)  # remove header
alias_dict = {}
count = 0
print("form_of_templates = {{")
for tr in trs:
    tds_html = tr.find_all("td")
    tds = [t.text.strip() for t in tds_html]
    tds = dict(zip(columns, tds))
    if tds:
        link = tr.find("a")
        url_template = ROOT + link["href"]
        text = get_text(url_template)
        print(f'    "{tds["template"]}": {{')
        print(f'        "text": "{text}",')
        print(f'        "dot": {True if tds["dot"] == "yes" else False},')
        print("    }},")
        count += 1
        for alias in sorted(tds["aliases"].split(",")):
            alias = alias.strip()
            if alias:
                print(f'    "{alias}": {{')
                print(f'        "text": "{text}",')
                print(f'        "dot": {True if tds["dot"] == "yes" else False},')
                print("    }},")
                count += 1

print(f"}}  # {count:,}")
