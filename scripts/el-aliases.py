import re

from scripts_utils import get_content

code = get_content("https://el.wiktionary.org/wiki/Module:labels/alias?action=raw")
regex = re.compile(r"alias\[([^\]]+)\] = \{ lab = ([^\]]+) \}").findall
aliases = {}

for line in code.splitlines():
    line = line.strip()
    # alias['συνηρημένο επίθετο'] = { lab = 'σνρ επίθετο' }
    if not line.startswith("alias["):
        continue
    alias, label = regex(line)[0]
    aliases[alias[1:-1]] = label[1:-1]

print("aliases = {")
for key, valias in sorted(aliases.items()):
    print(f'    "{key}": "{valias}",')
print(f"}}  # {len(aliases):,}")
