import re

from scripts_utils import get_soup

url = "https://pt.wiktionary.org/w/index.php?title=Predefini%C3%A7%C3%A3o:escopo/n%C3%BAcleo&action=edit"
soup = get_soup(url)
textarea = soup.find("textarea")

text = textarea.text
text = re.sub(r"(<!--.*?-->)", "", text, flags=re.DOTALL)
text = re.sub(r"(\[\[Categoria.*?\]\])", "", text, flags=re.DOTALL)

results = {}
for line in text.split("\n"):
    if line.startswith("|"):
        array = line.split("=")
        words = array[0].split("|")
        result = array[1]
        for word in words:
            if word and word[0] != "#":
                results[word.replace("\u200e", "")] = result

print("escopos = {")
for t, r in sorted(results.items()):
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(results):,}")
