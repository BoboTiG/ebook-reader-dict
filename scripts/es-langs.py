import re

import requests

url = "https://es.wiktionary.org/wiki/Ap%C3%A9ndice:C%C3%B3digos_de_idioma"
with requests.get(url) as req:
    req.raise_for_status()
    content = req.text

pattern = r"<tr>\s+<td>([^<]+)</td>\s+<td>([^<]+)\s+</td></tr>"
matches = re.findall(pattern, content)
print("langs = {")
for iso, lang in sorted(matches):
    print(f'    "{iso}": "{lang}",')
print(f"}}  # {len(matches):,}")
