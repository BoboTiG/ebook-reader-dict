from scripts_utils import get_content

text = get_content("https://eo.wiktionary.org/w/index.php?title=%C5%9Cablono:tbldialektoj&action=raw")
text = text.split("############################################################")[1].strip()

dialects = {}
for line in text.splitlines():
    if not line or not line.startswith("[["):
        continue
    line = line.split(",", 1)[0]
    line = line.replace("[[", "").replace("]]", "")
    key, value = line.split(" ", 1)
    dialects[key.strip()] = value.split("|", 1)[0].strip()

print("dialects = {")
for key, value in sorted(dialects.items()):
    print(f'    "{key}": {value!r},')
print(f"}}  # {len(dialects):,}")
