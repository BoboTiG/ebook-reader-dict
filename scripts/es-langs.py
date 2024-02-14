import re

from scripts_utils import get_content

url = "https://es.wiktionary.org/wiki/Ap%C3%A9ndice:C%C3%B3digos_de_idioma"
content = get_content(url)

pattern = r"<tr>\s+<td>([^<]+)</td>\s+<td>([^<]+)\s+</td></tr>"
matches = re.findall(pattern, content)

langs = dict(matches)
assert langs
print("langs = {")
for t, r in sorted(langs.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(langs):,}")

print()
