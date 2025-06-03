from scripts_utils import get_content

text = get_content("https://eo.wiktionary.org/w/index.php?title=%C5%9Cablono:tbllingvoj&action=raw")
text = text.split("############################################################")[1].strip()

langs = {}
for line in text.splitlines():
    if not line:
        continue
    line = line.split(",", 1)[0]
    line = line.replace("[[", "").replace("]]", "")
    key, value = line.split(" ", 1)
    langs[key.strip()] = value.strip()

print("langs = {")
for key, value in sorted(langs.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(langs):,}")
