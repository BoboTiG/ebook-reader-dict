import re
from typing import Dict

from scripts_utils import get_soup, get_url_content

ROOT = "https://fr.wiktionary.org"
START_URL = "https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Mod%C3%A8les_de_racine_en_arabe_du_Wiktionnaire"
NEXTPAGE_TEXT = "page suivante"
RACINE_URL = "https://fr.wiktionary.org/wiki/Mod%C3%A8le:{}?action=raw"
STRIP_COMMENT = re.compile(r"<!-- \(\w+\)[^\-]+-->").sub


def process_category_page(url: str, results: Dict[str, str]) -> str:
    soup = get_soup(url)

    nextpage = ""
    nextpage_div = soup.find(id="mw-pages")
    last_link = nextpage_div.find_all("a")[-1]
    if NEXTPAGE_TEXT == last_link.text:
        nextpage = ROOT + last_link.get("href")

    content_div = soup.find("div", "mw-category-generated")
    for li in content_div.find_all("li"):
        tpl_title = li.find("a").get("title")
        if " " in tpl_title or "/" in tpl_title or "ar-racine" in tpl_title:
            continue

        process_root(tpl_title.removeprefix("Modèle:"), results)

    return nextpage


def process_root(tpl: str, results: Dict[str, str]) -> None:
    url = RACINE_URL.format(tpl)
    data = get_url_content(url)

    for line in data.splitlines():
        if not line.startswith("| ar-"):
            continue

        racine, text = line[1:].split("=")
        text = STRIP_COMMENT("", text.strip())
        results[racine.strip()] = text.strip()


next_page_url = START_URL
results: Dict[str, str] = {}

while next_page_url:
    next_page_url = process_category_page(next_page_url, results)

print("racines_arabes = {")
for k, v in sorted(results.items()):
    print(f'    "{k}": "{v}",')
print(f"}}  # {len(results):,}")
