import re

from scripts_utils import get_soup


def clean_wiki(text: str) -> str:
    text = re.sub(r"\[\[([^||:\]]+)\]\]", "\\1", text)  # [[a]] -> a
    text = re.sub(r"\[\[[^|]+\|(.+?(?=\]\]))\]\]", "\\1", text)  # [[a|b]] -> b
    return text


url = "https://de.wiktionary.org/w/index.php?title=Vorlage:K/Abk&action=edit"
soup = get_soup(url)

textarea = soup.find(id="wpTextbox1")

text = textarea.text.split("#default=")[0]
results = {}
for line in text.split("\n"):
    if not line.startswith("|"):
        continue
    line = clean_wiki(line)
    keys = []
    value = ""
    sArray = line.split("|")
    for s in sArray:
        s = s.strip()
        if "=" in s:
            sSplit = s.split("=")
            keys.append(sSplit[0].strip())
            value = sSplit[1].strip()
        elif s:
            keys.append(s)
    for key in keys:
        results[key] = value

print("abk = {")
for t, r in sorted(results.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(results):,}")
