import requests
from bs4 import BeautifulSoup


ROOT = "https://fr.wiktionary.org"
START_URL = "https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Mod%C3%A8les_r%C3%A9gionaux_du_Wiktionnaire"
NEXTPAGE_TEXT = "page suivante"
REDIRECT_URL = "https://fr.wiktionary.org/w/index.php?title=Mod%C3%A8le:{}&redirect=no"


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


def process_category_page(url, results, aliases):
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
        region = template_soup.find("span", {"id": ["région"]})
        if not region:
            continue
        results[template_name] = region.text.strip("()")

        # Enventual alias(es)
        redirections = template_soup.find("div", {"class": ["plainlinks"]})
        if redirections:
            # [1:] to get rid of the first link pointing to "Redirections"
            aliases.extend(a.text for a in redirections.find_all("a")[1:])
    return nextpage


next_page_url = START_URL
results = {}
aliases = []

# Fetch models first, and store aliases
while next_page_url:
    next_page_url = process_category_page(next_page_url, results, aliases)

# Fetch aliases
for alias in set(aliases):
    alias_url = REDIRECT_URL.format(alias)
    soup = get_soup(alias_url)
    div = soup.find("div", {"class": ["redirectMsg"]})
    if not div:
        # Deleted or no more valid alias
        continue

    modele = div.find("a")
    if modele:
        modele = modele.text.replace("Modèle:", "")
        results[alias] = modele

print("regions = {")
for t, r in sorted(results.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(results):,}")
