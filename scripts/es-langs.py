from scripts_utils import get_soup

url = "https://es.wiktionary.org/wiki/Ap%C3%A9ndice:C%C3%B3digos_de_idioma"
soup = get_soup(url)

langs = {}
tables = soup.find_all("table", {"class": "wikitable"})
for table in tables:
    if table.attrs.get("style"):
        continue
    trs = table.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) > 1:
            langs[tds[0].text.strip()] = tds[1].text.strip()

assert langs
print("langs = {")
for t, r in sorted(langs.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(langs):,}")

print()
