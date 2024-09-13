from scripts_utils import get_soup

ROOT = "https://fr.wiktionary.org"
START_URL = "https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Mod%C3%A8les_de_th%C3%A9matique"
NEXTPAGE_TEXT = "page suivante"
ALIAS_URL = "https://fr.wiktionary.org/w/index.php?title=Sp%C3%A9cial:Pages_li%C3%A9es/Mod%C3%A8le:{}&limit=10&hidetrans=1&hidelinks=1"  # noqa


def process_category_page(url: str, results: dict[str, str]) -> str:
    soup = get_soup(url)

    nextpage = ""
    nextpage_div = soup.find(id="mw-pages")
    last_link = nextpage_div.find_all("a")[-1]
    if NEXTPAGE_TEXT == last_link.text:
        nextpage = ROOT + last_link.get("href")

    content_div = soup.find("div", "mw-category-generated")
    lis = content_div.find_all("li")
    for li in lis:
        template_url = ROOT + li.find("a").get("href")
        template_name = li.text.split(":")[1]
        template_soup = get_soup(template_url)
        parser_output = template_soup.find("span", {"class": ["term", "texte"]})
        rendering = parser_output.text
        if template_name and rendering:
            results[template_name] = rendering.strip("()")

    return nextpage


def process_alias_page(key: str, value: str, results: dict[str, str]) -> None:
    url = ALIAS_URL.format(key)
    soup = get_soup(url)
    ul = soup.find("ul", {"id": ["mw-whatlinkshere-list"]})
    if not ul:
        return
    for alias in ul.find_all("a", {"class": ["mw-redirect"]}):
        alias = alias.text.replace("Modèle:", "")
        if alias == "modifier":
            continue
        results[alias] = value


next_page_url = START_URL
results: dict[str, str] = {}

while next_page_url:
    next_page_url = process_category_page(next_page_url, results)

# Fetch aliases
for key, value in list(results.items()):
    process_alias_page(key, value, results)

print("domain_templates = {")
for t, r in sorted(results.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(results):,}")
