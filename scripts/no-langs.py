from typing import Dict

from scripts_utils import get_soup

ROOT_URL = "https://no.wiktionary.org"
START_URL = f"{ROOT_URL}/wiki/Kategori:Spr%C3%A5kmaler"
NEXTPAGE_TEXT = "neste side"


def process_page(page_url: str, languages: Dict[str, str]) -> str:
    soup = get_soup(page_url)

    nextpage = ""
    nextpage_div = soup.find(id="mw-pages")
    last_link = nextpage_div.find_all("a")[-1]
    if NEXTPAGE_TEXT == last_link.text:
        nextpage = ROOT_URL + last_link.get("href")

    content = soup.find("div", {"id": "mw-pages"})
    lis = content.findAll("li")
    for li in lis:
        link = li.find("a")["href"]
        li_url = ROOT_URL + link
        if ":" in li.text:
            key = li.text.split(":")[1]
            sub_soup = get_soup(li_url)
            content = sub_soup.find("div", {"class": "mw-parser-output"}).find("p", recursive=False)
            if content:
                value = content.text
                languages[key] = value.strip()
    return nextpage


next_page_url = START_URL
languages: Dict[str, str] = {}

while next_page_url:
    next_page_url = process_page(next_page_url, languages)

assert len(languages)
print("langs = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(languages):,}")
