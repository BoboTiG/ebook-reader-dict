import re

from scripts_utils import get_soup

soup = get_soup("https://da.wiktionary.org/wiki/Modul:lang/data").text
pattern = re.compile(r'data\["([^"]+)"\]\s+=\s+\{\s+name\s+=\s+"([^"]+)",')

langs = re.findall(pattern, soup)

# Missing langs
langs.append(("non", "oldnordisk"))

print("langs = {")
for key, name in sorted(langs):
    print(f'    "{key}": "{name}",')
print(f"}}  # {len(langs):,}")
