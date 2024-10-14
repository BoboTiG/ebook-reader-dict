import re

from scripts_utils import get_content

text = get_content("https://ru.wiktionary.org/wiki/%D0%9C%D0%BE%D0%B4%D1%83%D0%BB%D1%8C:languages/data?action=raw")
text = text.replace("local ", "").replace("return langs;", "")

#   ["abq"] = { "abq", "Абазинский" },
#   ["fic-drw"] = { "", "Дроу", "ф", ""  },
text = re.sub(r'  \["([^"]+)"\]\s*=\s*{\s*"[^"]*",\s*"([^"]+)".+', r'    "\1": "\2",', text)

exec(text)

print("langs = {")
for key, name in sorted(langs.items()):  # type: ignore[name-defined] # noqa: F821
    print(f'    "{key}": "{name}",')
print(f"}}  # {len(langs):,}")  # type: ignore[name-defined] # noqa: F821
