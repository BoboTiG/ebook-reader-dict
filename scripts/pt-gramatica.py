from typing import Dict, List

from scripts_utils import get_content

url = "https://pt.wiktionary.org/w/index.php?title=Predefini%C3%A7%C3%A3o:gram%C3%A1tica/core&action=raw"
text = get_content(url)

text = text.replace("{{#ifeq:{{int:Log}}|{{:MediaWiki:Log}}|género|gênero}}", "género")
text = text.replace("{{gramática/core/faltagenero|{{{2|}}}}}", "gênero em falta")
text = "".join(line for line in text.splitlines() if line[0] == "|" and line[1] != " ")
text = text.lstrip("|")

gramaticas: Dict[str, str] = {}
current_abbr: List[str] = []

for p in text.split("|"):
    if "=" in p:
        key, value = p.split("=")
        value = value.strip("'")
        gramaticas[key] = value
        for abbr in current_abbr:
            gramaticas[abbr] = value
        current_abbr.clear()
    else:
        current_abbr.append(p)

print("gramatica_short = {")
for key, value in sorted(gramaticas.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(gramaticas):,}")
