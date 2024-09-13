from scripts_utils import get_soup

ROOT = "https://fr.wiktionary.org"
START_URL = "https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Mod%C3%A8les_r%C3%A9gionaux"
NEXTPAGE_TEXT = "page suivante"
ALIAS_URL = "https://fr.wiktionary.org/w/index.php?title=Sp%C3%A9cial:Pages_li%C3%A9es/Mod%C3%A8le:{}&limit=10&hidetrans=1&hidelinks=1"  # noqa


def process_regions_page(url: str, results: dict[str, str]) -> str:
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
        if region := template_soup.find("span", {"id": ["région"]}):
            results[template_name] = region.text.strip("()")
    return nextpage


def process_alias_page(model: str, region: str, results: dict[str, str]) -> None:
    url = ALIAS_URL.format(model)
    soup = get_soup(url)
    ul = soup.find("ul", {"id": ["mw-whatlinkshere-list"]})
    if not ul:
        return
    for alias in ul.find_all("a", {"class": ["mw-redirect"]}):
        alias = alias.text.replace("Modèle:", "")
        if alias == "modifier":
            continue
        results[alias] = region


results: dict[str, str] = {}
aliases: list[str] = []

# Fetch models first
next_page_url = START_URL
while next_page_url:
    next_page_url = process_regions_page(next_page_url, results)

# Fetch aliases
for model, region in list(results.items()):
    process_alias_page(model, region, results)

print("regions = {")
for t, r in sorted(results.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(results):,}")
