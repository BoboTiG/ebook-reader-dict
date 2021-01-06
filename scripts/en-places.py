import requests
from bs4 import BeautifulSoup


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


url = "https://en.wiktionary.org/wiki/Template:place"
soup = get_soup(url)
tables = soup.find_all("table", "wikitable")

columns = ["placetype", "article", "display", "preposition", "aliases"]
placetypes = {}
print("recognized_placetypes = {")
body = tables[0].find("tbody")
trs = body.find_all("tr")
trs.pop(0)  # remove header
alias_dict = {}
for tr in trs:
    tds = tr.find_all("td")
    tds = [t.text.strip() for t in tds]
    tds = dict(zip(columns, tds))
    if tds:
        placetype = tds.pop("placetype", None)
        aliases = tds.pop("aliases").split(",")
        placetypes[placetype] = tds
        print(f'    "{placetype}": {{')
        for key in tds:
            print(f'        "{key}": "{tds[key]}",')
        print("    },")
        for alias in sorted(aliases):
            alias = alias.strip()
            if alias:
                alias_dict[alias] = placetype
print(f"}}  # {len(trs):,}")

print()

print("placetypes_aliases = {")
for alias, placetype in sorted(alias_dict.items()):
    print(f'    "{alias}": "{placetype}",')
print(f"}}  # {len(alias_dict):,}")

print()

body = tables[2].find("tbody")
trs = body.find_all("tr")
trs.pop(0)  # remove header
print("recognized_qualifiers = {")
for tr in trs:
    tds = tr.find_all("td")
    tds = [t.text.strip() for t in tds]
    print(f'    "{tds[0]}": "{tds[1]}",')
print(f"}}  # {len(trs):,}")

print()

body = tables[1].find("tbody")
trs = body.find_all("tr")
trs.pop(0)  # remove header
count = 0
print("recognized_placenames = {")
for tr in trs:
    tds = tr.find_all("td")
    place = tds[0].text
    article = tds[1].text
    display = tds[2].text
    if display == "(same)":
        display = ""
    if article or display:
        print(f'    "{place}": {{"article": "{article}", "display": "{display}"}},')
        count += 1
print(f"}}  # {count:,}")
