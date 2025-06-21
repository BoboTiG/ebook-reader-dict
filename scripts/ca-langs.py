import re
import xml.etree.ElementTree as ET
from io import StringIO

from scripts_utils import get_content

url = "https://raw.githubusercontent.com/unicode-org/cldr/master/common/main/ca.xml"
buf = StringIO(initial_value=get_content(url))
tree = ET.parse(buf)
root = tree.getroot()

languages = {}
for lang in root.iter("language"):
    if lang.get("alt"):
        continue
    iso = str(lang.get("type")).lower().replace("_", "-")
    name = lang.text
    languages[iso] = name

url = "https://ca.wiktionary.org/wiki/M%C3%B2dul:llengua/taula?action=raw"
code = get_content(url)
iso = name = ""
groups = []
for line in code.splitlines():
    line = line.strip()
    if line.startswith("c["):
        # c["cbk-zam"] = {
        iso = re.search(r'c\["([^"]+)"\]', line)[1]  # type: ignore[index]
    elif line.startswith("nom ="):
        # nom = "chavacano de Zamboanga"}
        languages[iso] = re.search(r'"([^"]+)"', line)[1]  # type: ignore[index]
    elif line.startswith('type = "grup"'):
        groups.append(iso)

print("langs = {")
for iso, language in sorted(languages.items()):
    print(f'    "{iso}": "{language}",')
print(f"}}  # {len(languages):,}")
print()
print("grups = [")
for iso in groups:
    print(f'    "{iso}",')
print("]")
