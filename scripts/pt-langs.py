import re
from operator import itemgetter

from scripts_utils import get_content

url1 = "https://pt.wiktionary.org/wiki/Wikcion%C3%A1rio:Lista_de_l%C3%ADnguas/c%C3%B3digos/A-L"
url2 = "https://pt.wiktionary.org/wiki/Wikcion%C3%A1rio:Lista_de_l%C3%ADnguas/c%C3%B3digos/M-Z"
content1 = get_content(url1)
content2 = get_content(url2)
content = content1 + content2

pattern = r"<li><a[^>]+>([^\<]+)</a>: <a[^>]+>([^\<]+)</a>"
matches = re.findall(pattern, content)
seen = set()
print("langs = {")
for lang, iso in sorted(matches, key=itemgetter(1)):
    if iso not in seen:
        print(f'    "{iso}": "{lang}",')
        seen.add(iso)
print(f"}}  # {len(seen):,}")
