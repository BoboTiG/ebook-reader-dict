import re

import requests

url = "https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_des_langues"
with requests.get(url) as req:
    req.raise_for_status()
    content = req.text

pattern = r"<td><span [^>]+>([^<]+)</span></td>\s+<td [^>]+><a [^>]+>([^<]+)</a></td>"
matches = re.findall(pattern, content)
print("langs = {")
for iso, lang in sorted(matches):
    print(f'    "{iso}": "{lang}",')
print(f"}}  # {len(matches):,}")
