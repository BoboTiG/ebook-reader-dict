import re
from io import StringIO
import xml.etree.ElementTree as ET

import requests

url = "https://raw.githubusercontent.com/unicode-org/cldr/master/common/main/ca.xml"
with requests.get(url) as req:
    req.raise_for_status()
    buf = StringIO(initial_value=req.text)
    tree = ET.parse(buf)
    root = tree.getroot()

languages = {}
for lang in root.iter("language"):
    iso = lang.get("type")
    name = lang.text
    languages[iso] = name

url = "https://ca.wiktionary.org/wiki/M%C3%B2dul:llengua/taula"
with requests.get(url) as req:
    req.raise_for_status()
    lines = req.text

# Strips the newline character
pattern = re.compile(r'.*"s2">"([^"]+)"')
count = 0
iso = name = ""
for line in lines:
    line = line.strip()
    if line.startswith('<span class="n">c</span>'):
        m = pattern.match(line)
        iso = m.group(1)
    elif line.startswith('<span class="n">nom'):
        m = pattern.match(line)
        name = m.group(1)
        if iso:
            languages[iso] = name

print("langs = {")
for iso, lang in sorted(languages.items()):
    print(f'    "{iso}": "{lang}",')
print(f"}}  # {len(languages):,}")
