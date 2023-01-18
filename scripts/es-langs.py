import re

from scripts_utils import get_content, get_soup

url = "https://es.wiktionary.org/wiki/Ap%C3%A9ndice:C%C3%B3digos_de_idioma"
content = get_content(url)

pattern = r"<tr>\s+<td>([^<]+)</td>\s+<td>([^<]+)\s+</td></tr>"
matches = re.findall(pattern, content)

langs = dict(matches)
print("langs = {")
for t, r in sorted(langs.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(langs):,}")

print()

url = "https://es.wiktionary.org/w/index.php?title=Plantilla:normalizar_nombre&action=edit"

soup = get_soup(url)

textarea = soup.find(id="wpTextbox1")
code = textarea.text
lines = code.split("\n")
keep_lines = []
lang_to_normalize = {}
for line in lines:
    if line.startswith("|") and "#" not in line:
        equal = line[1:].split(" = ")
        if len(equal) > 1:
            keep_lines.append(equal[0].strip())
            for kline in keep_lines:
                la = equal[1].strip()
                if "|" in la and la.startswith("{{"):
                    la = la[2:].split("|")[0]
                    la = langs[la]
                lang_to_normalize[kline] = la
            keep_lines = []
        else:
            keep_lines.append(line[1:].strip())

print("lang_to_normalize = {")
for t, r in sorted(lang_to_normalize.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(lang_to_normalize):,}")
