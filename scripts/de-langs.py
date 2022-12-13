from typing import Dict

from scripts_utils import get_soup

ROOT_URL = "https://de.wiktionary.org"
START_URL = f"{ROOT_URL}/wiki/Kategorie:Wiktionary:Sprachk%C3%BCrzel"
NEXTPAGE_TEXT = "nächste Seite"

ALIAS_URL = "https://de.wiktionary.org/w/index.php?title=Spezial:Linkliste/{}&hidetrans=1&hidelinks=1"


def process_page(page_url: str, languages: Dict[str, str]) -> str:
    soup = get_soup(page_url)

    nextpage = ""
    nextpage_div = soup.find(id="mw-pages")
    last_link = nextpage_div.find_all("a")[-1]
    if NEXTPAGE_TEXT == last_link.text:
        nextpage = ROOT_URL + last_link.get("href")

    content = soup.find("div", {"class": "mw-category"})
    lis = content.findAll("li")
    for li in lis:
        link = li.find("a")["href"]
        li_url = ROOT_URL + link
        key = li.text.split(":")[1]
        sub_soup = get_soup(li_url)
        content = sub_soup.find("div", {"class": "mw-parser-output"}).find(
            "p", recursive=False
        )
        value = content.text.strip()
        languages[key] = value
        a_url = ALIAS_URL.format(li.text)
        soup_alias = get_soup(a_url)
        if ul_alias := soup_alias.find("ul", {"id": "mw-whatlinkshere-list"}):
            for alias_li in ul_alias.findAll("li"):
                alias_text = alias_li.find("a").text
                alias_key = alias_text.split(":")[1]
                languages[alias_key] = value

    return nextpage


next_page_url = START_URL
languages: Dict[str, str] = {}

while next_page_url:
    next_page_url = process_page(next_page_url, languages)


print("langs = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(languages):,}")
