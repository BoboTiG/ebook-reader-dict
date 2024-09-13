from scripts_utils import get_soup

ROOT = "https://it.wiktionary.org"
START_URL = f"{ROOT}/wiki/Categoria:Template_lingua_testo"
NEXTPAGE_TEXT = "pagina successiva"


def process_page(url: str, results: dict[str, str]) -> str:
    soup = get_soup(url)

    nextpage = ""
    nextpage_div = soup.find(id="mw-pages")
    last_link = nextpage_div.find_all("a")[-1]
    if NEXTPAGE_TEXT == last_link.text:
        nextpage = ROOT + last_link.get("href")

    content_div = soup.find("div", "mw-category-generated")
    lis = content_div.find_all("li")
    for li in lis:
        try:
            tpl_name = li.text.split(":")[1]
        except IndexError:
            continue
        tpl_url = ROOT + li.find("a").get("href")
        tpl_soup = get_soup(tpl_url)
        lang = tpl_soup.find("div", "mw-parser-output").find("a").text
        results[tpl_name] = lang
    return nextpage


results: dict[str, str] = {}

next_page_url = START_URL
while next_page_url:
    next_page_url = process_page(next_page_url, results)

print("langs = {")
for key, value in sorted(results.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(results):,}")
