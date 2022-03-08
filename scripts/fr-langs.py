import re
from scripts_utils import get_url_content

url = "https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_des_langues"
content = get_url_content(url)

pattern = r"<td><span [^>]+>([^<]+)</span></td>\s+<td [^>]+><a [^>]+>([^<]+)</a></td>"
matches = re.findall(pattern, content)
print("langs = {")
for iso, lang in sorted(matches):
    print(f'    "{iso}": "{lang}",')
print(f"}}  # {len(matches):,}")
