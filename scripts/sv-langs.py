import re

from scripts_utils import get_content

soup = get_content("https://sv.wiktionary.org/wiki/Modul:lang/data?action=raw")
pattern = re.compile(r'data\["([^"]+)"\]\s+=\s+\{.*\s+name\s+=\s+"([^"]+)",')

langs = re.findall(pattern, soup)

# Unknown lang
langs.append(("gmq-bot", "okänt språk"))

print("langs = {")
for key, name in sorted(langs):
    print(f'    "{key}": "{name}",')
print(f"}}  # {len(langs):,}")
