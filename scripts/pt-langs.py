import re
from operator import itemgetter

import requests

url1 = "https://pt.wiktionary.org/wiki/Wikcion%C3%A1rio:Lista_de_l%C3%ADnguas/c%C3%B3digos/A-L"
url2 = "https://pt.wiktionary.org/wiki/Wikcion%C3%A1rio:Lista_de_l%C3%ADnguas/c%C3%B3digos/M-Z"
with requests.get(url1) as req1, requests.get(url2) as req2:
    req1.raise_for_status()
    req2.raise_for_status()
    content = req1.text + req2.text

pattern = r"<li><a[^>]+>([^\<]+)</a>: <a[^>]+>([^\<]+)</a>"
matches = re.findall(pattern, content)
print("langs = {")
for lang, iso in sorted(matches, key=itemgetter(1)):
    print(f'    "{iso}": "{lang}",')
print(f"}}  # {len(matches):,}")
