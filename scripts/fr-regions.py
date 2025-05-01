import re

from scripts_utils import get_content, get_soup

ROOT = "https://fr.wiktionary.org"
START_URL = "https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Mod%C3%A8les_r%C3%A9gionaux"
NEXTPAGE_TEXT = "page suivante"
ALIAS_URL = "https://fr.wiktionary.org/w/index.php?title=Sp%C3%A9cial:Pages_li%C3%A9es/Mod%C3%A8le:{}&limit=10&hidetrans=1&hidelinks=1"


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
        template_name = li.text
        if ":" in template_name:
            template_name = template_name.split(":")[1]
            template_soup = get_soup(template_url)
            if region := template_soup.find("section", {"id": ["mwAQ"]}).find("i"):
                results[template_name] = region.text.strip("()")
        else:
            process_regions_page(template_url, results)
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


def get_regions_models() -> dict[str, str]:
    regions: dict[str, str] = {}

    # Fetch models first
    next_page_url = START_URL
    while next_page_url:
        next_page_url = process_regions_page(next_page_url, regions)

    # Fetch aliases
    for model, region in list(regions.items()):
        process_alias_page(model, region, regions)

    return regions


def get_regions_data() -> dict[str, str]:
    text = get_content("https://fr.wiktionary.org/wiki/Module:r%C3%A9gions/data?action=raw")
    return {region: region for region in re.findall(r"t\['([^']+)']", text)}


regions = get_regions_data() | get_regions_models()
print("regions = {")
for key, value in sorted(regions.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(regions):,}")
