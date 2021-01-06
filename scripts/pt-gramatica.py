import re

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


url = "https://pt.wiktionary.org/w/index.php?title=Predefini%C3%A7%C3%A3o:gram%C3%A1tica/core&action=edit"
soup = get_soup(url)
textarea = soup.find("textarea")

current_abbr = []
count = 0

text = textarea.text
text = text.replace("{{#ifeq:{{int:Log}}|{{:MediaWiki:Log}}|género|gênero}}", "género")
text = text.replace("{{gramática/core/faltagenero|{{{2|}}}}}", "gênero em falta")
text = re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL)

print("gramatica_short = {")
for p in sorted(text.split("|")):
    p = p.strip()
    if p and "<!--" not in p and ("{" not in p) and ("}" not in p):
        if "=" in p:
            sArray = p.split("=")
            name = sArray[1].strip("'")
            print(f'    "{sArray[0]}": "{name}",')
            count += 1
            for abbr in sorted(current_abbr):
                print(f'    "{abbr}": "{name}",')
                count += 1
            current_abbr.clear()
        else:
            current_abbr.append(p)
print(f"}}  # {count:,}")
