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

url = "https://ca.wiktionary.org/wiki/M%C3%B2dul:llengua/taula"
lines = get_content(url).split("\n")

# Strips the newline character
pattern = re.compile(r'.*"s2">&quot;([^&]+)')
count = 0
iso = name = ""
groups = []
for line in lines:
    line = line.strip()
    if '<span class="n">c</span>' in line:
        m = pattern.match(line)
        if m:
            iso = m[1]
    elif '<span class="n">nom' in line:
        m = pattern.match(line)
        if m:
            name = m[1]
            if iso:
                languages[iso] = name
    elif '<span class="nb">type' in line:
        if "grup" in line:
            groups.append(iso)

print("langs = {")
for iso, lang in sorted(languages.items()):
    print(f'    "{iso}": "{lang}",')
print(f"}}  # {len(languages):,}")
print()
print("grups = [")
for iso in groups:
    print(f'    "{iso}",')
print("]")
