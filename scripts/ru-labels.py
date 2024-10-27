import re

from scripts_utils import get_content

content = get_content("https://ru.wiktionary.org/wiki/%D0%9C%D0%BE%D0%B4%D1%83%D0%BB%D1%8C:labels/data?action=raw")
key_pattern = re.compile(r"^d\['(.+)'\]").finditer
value_pattern = re.compile(r"] = '(.+)'$").search

labels = {}
for line in content.splitlines():
    if line.startswith("d["):
        key = next(key_pattern(line))[1]
        value = v[1] if (v := value_pattern(line)) else key
        labels[key] = value

print("labels = {")
for key, value in sorted(labels.items()):
    name = value if isinstance(value, str) else key
    print(f'    "{key}": "{name}",')
print(f"}}  # {len(labels):,}")
