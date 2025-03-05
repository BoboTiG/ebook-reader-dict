from scripts_utils import get_soup

root_url = "https://de.wiktionary.org"
start_url = f"{root_url}/wiki/Kategorie:Wiktionary:Sprachadjektive"
alias_url = "https://de.wiktionary.org/w/index.php?title=Spezial:Linkliste/{}&hidetrans=1&hidelinks=1"
soup = get_soup(start_url)

content = soup.find("div", {"class": "mw-category"})
lis = content.findAll("li")
languages = {}
for li in lis:
    link = li.find("a")["href"]
    li_url = root_url + link
    key = li.text.split(":")[1]
    sub_soup = get_soup(li_url)
    content = sub_soup.find("div", {"class": "mw-parser-output"}).find("p")
    value = content.text.strip()
    languages[key] = value
    a_url = alias_url.format(li.text)
    soup_alias = get_soup(a_url)
    if ul_alias := soup_alias.find("ul", {"id": "mw-whatlinkshere-list"}):
        for alias_li in ul_alias.findAll("li"):
            alias_text = alias_li.find("a").text
            alias_key = alias_text.split(":")[1]
            languages[alias_key] = value


print("lang_adjs = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(languages):,}")
