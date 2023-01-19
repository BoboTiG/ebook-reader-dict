from scripts_utils import get_content

url = "https://it.wiktionary.org/w/api.php?action=query&meta=languageinfo&liprop=name&format=json"
content = get_content(url, as_json=True)
langs = content["query"]["languageinfo"]

print("langs = {")
for iso, lang in sorted(langs.items()):
    name = lang["name"]
    print(f'    "{iso}": "{name}",')
print(f"}}  # {len(langs):,}")
