import re

from scripts_utils import get_content

url = "https://el.wiktionary.org/wiki/Module:labels/alias"
lines = get_content(url).splitlines()

aliases = {}

strip_span = re.compile(r"<span[^>]+>([^<]+)</span>", flags=re.MULTILINE).sub
find_key = re.compile(r">\s*alias\[([^\]]+)\]").findall
find_alias = re.compile(r"lab = (.)([^\1]+)\1").findall

for line in lines:
    if '<span class="n">alias</span>' not in line or "&#39;" not in line:
        continue
    line = strip_span(r"\1", line).replace("&#39;", "'").replace("&quot;", '"')
    key = find_key(line)[0][1:-1]
    alias = find_alias(line)[0][1]
    aliases[key] = alias

print("aliases = {")
for key, valias in sorted(aliases.items()):
    print(f'    "{key}": "{valias}",')
print(f"}}  # {len(aliases):,}")
