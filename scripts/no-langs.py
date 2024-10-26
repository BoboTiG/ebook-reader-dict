import re

from scripts_utils import get_content, get_soup

ROOT_URL = "https://no.wiktionary.org"
START_URL = f"{ROOT_URL}/wiki/Kategori:Spr%C3%A5kmaler"
NEXTPAGE_TEXT = "neste side"
REGEX_CLEANUP = re.compile(r"\{[^}]+\}").sub


def process_page(page_url: str, languages: dict[str, str]) -> str:
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
            content = get_content(f"{li_url}?action=raw")

            # 1. Use the text until a potential `<noinclude>(...)`
            # 2. Get rid of potential `{{{l|[}}}{{{l|[}}}...{{{l|]]}}}`
            #                     and `{{{{#ifeq:{{{1}}}|{{lc:{{{1}}}}}|språkmal|#if:1}}|{{{1}}}}}`
            # 3. Get rid of potential `[[xxx]]`
            if (
                (content := content.split("<", 1)[0])
                and (content := REGEX_CLEANUP("", content).replace("}", "").split("#", 1)[0])
                and (content := content.replace("|", "").replace("[", "").replace("]", "").strip())
            ):
                languages[key] = content
    return nextpage


next_page_url = START_URL
languages: dict[str, str] = {}

while next_page_url:
    next_page_url = process_page(next_page_url, languages)

print("langs = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(languages):,}")
