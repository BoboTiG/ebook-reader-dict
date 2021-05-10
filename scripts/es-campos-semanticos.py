import requests
from bs4 import BeautifulSoup


START_URL = (
    "https://es.wiktionary.org/wiki/Categor%C3%ADa:Plantillas_de_campo_sem%C3%A1ntico"
)
ROOT_URL = "https://es.wiktionary.org/"
ALIAS_URL = "https://es.wiktionary.org/w/index.php?title=Especial:LoQueEnlazaAqu%C3%AD/{}&hidetrans=1&hidelinks=1"
NEXTPAGE_TEXT = "página siguiente"


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


def process_alias_page(model, template_text, results):
    url = ALIAS_URL.format(model)
    soup = get_soup(url)
    ul = soup.find("ul", {"id": ["mw-whatlinkshere-list"]})
    if not ul:
        return
    for alias in ul.find_all("a", {"class": ["mw-redirect"]}):
        alias = alias.text.replace("Plantilla:", "")
        if alias == "editar":
            continue
        # print(f'    "{alias}": "{template_text}"')
        results[alias] = template_text


def process_cs_page(url, results):
    soup = get_soup(url)

    nextpage = ""
    nextpage_div = soup.find(id="mw-pages")
    last_link = nextpage_div.find_all("a")[-1]
    if NEXTPAGE_TEXT == last_link.text:
        nextpage = ROOT_URL + last_link.get("href")
    # print(nextpage)

    divs_category = soup.find_all("div", {"class": "mw-category-group"})
    for divs_category in divs_category:
        lis = divs_category.find_all("li")
        for li in lis:
            template_link = li.find("a")
            template_url = ROOT_URL + template_link.get("href")
            template_name = template_link.text.split(":")[1]
            template_soup = get_soup(template_url)
            template_text_div = template_soup.find("div", {"class": "mw-parser-output"})
            template_text = template_text_div.find("p").text.strip()
            if template_text[-1] == ".":
                template_text = template_text[:-1]
            results[template_name] = template_text
            # print(f'"{template_name}": "{template_text}"')
            process_alias_page(template_link.text, template_text, results)

    return nextpage


results = {}
next_page_url = START_URL
while next_page_url:
    next_page_url = process_cs_page(next_page_url, results)


print("campos_semanticos = {")
for t, r in sorted(results.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(results):,}")
