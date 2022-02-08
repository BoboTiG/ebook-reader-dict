import requests
from bs4 import BeautifulSoup


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


def get_text(url):
    soup = get_soup(url)
    div = soup.find("span", "form-of-definition")
    if not div:
        return ""
    res = div.text.replace(" term", "")
    res = res.replace(" [Term?]", "")
    return res


ROOT = "https://en.wiktionary.org"
url = f'{ROOT}/wiki/Category:Form-of_templates'
soup = get_soup(url)
tables = soup.find_all("table", "wikitable")

columns = ["template", "aliases", "cat", "inflection", "cap", "dot", "from", "pos"]

body = tables[0].find("tbody")
trs = body.find_all("tr")
trs.pop(0)  # remove header
alias_dict = {}
count = 0
print("form_of_templates = {")
for tr in trs:
    tds_html = tr.find_all("td")
    tds = [t.text.strip() for t in tds_html]
    if tds := dict(zip(columns, tds)):
        link = tr.find("a")
        url_template = ROOT + link["href"]
        if text := get_text(url_template):
            print(f'    "{tds["template"]}": {{')
            print(f'        "text": "{text}",')
            print(f'        "dot": {tds["dot"] == "yes"},')
            print("    },")
            count += 1
            for alias in sorted(tds["aliases"].split(",")):
                if alias := alias.strip():
                    print(f'    "{alias}": {{')
                    print(f'        "text": "{text}",')
                    print(f'        "dot": {tds["dot"] == "yes"},')
                    print("    },")
                    count += 1

print(f"}}  # {count:,}")
