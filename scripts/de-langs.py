import requests
from bs4 import BeautifulSoup


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


root_url = "https://de.wiktionary.org"
start_url = f"{root_url}/wiki/Kategorie:Wiktionary:Sprachadjektive"
soup = get_soup(start_url)

content = soup.find("div", {"class": "mw-category"})
lis = content.findAll("li")
languages = {}
for li in lis:
    link = li.find("a")["href"]
    li_url = root_url + link
    key = li.text.split(":")[1]
    sub_soup = get_soup(li_url)
    content = sub_soup.find("div", {"class": "mw-parser-output"}).find("p")
    value = content.text.strip()
    languages[key] = value

print("langs = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(languages):,}")
