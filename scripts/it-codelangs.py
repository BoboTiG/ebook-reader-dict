from scripts_utils import get_content

url = "https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-localenames-full/main/it/languages.json"  # noqa
content = get_content(url, as_json=True)
codelangs = content["main"]["it"]["localeDisplayNames"]["languages"]

print("codelangs = {")
for code, lang in codelangs.items():
    print(f'    "{code}": "{lang}",')
print(f"}}  # {len(codelangs):,}")
