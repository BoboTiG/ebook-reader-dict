import re

from scripts_utils import get_soup

url = "https://el.wiktionary.org/wiki/Module:Languages"
soup = get_soup(url)

in_comment = False
script = ""
regex = r"(\w+)\s*=\s*"
subst = '"\\1": '


textarea = soup.find("pre", {"class": "mw-code"})
for line in textarea.text.split("\n"):
    original_line = line

    line = line.strip()
    if line.startswith("--[[") or line.startswith("--[=["):
        in_comment = True
        continue
    if in_comment and line.startswith("]]") or line.startswith("]=]--"):
        in_comment = False
        continue
    if in_comment:
        continue
    if line.startswith(("--", "return")):
        continue
    if not original_line.startswith(" ") and not original_line.startswith("\t"):
        script += "\n"
    if line.startswith("local"):
        line = line.replace("local ", "")
    else:
        line = re.sub(regex, subst, line, 0, re.MULTILINE)
    # line = line.replace("'", '"')
    line = line.replace("false", "False")
    line = line.replace("fals", "False")
    line = line.replace("true", "True")
    if "-- " in line:
        line = line.split("-- ")[0]
    script += line

exec(script)
languages = {
    key: {
        "name": Languages[key].get("name", ""),  # type: ignore[name-defined] # noqa
        "frm": Languages[key].get("frm", ""),  # type: ignore[name-defined] # noqa
        "from": Languages[key].get("from", ""),  # type: ignore[name-defined] # noqa
        "apo": Languages[key].get("apo", ""),  # type: ignore[name-defined] # noqa
        "family": Languages[key].get("family", ""),  # type: ignore[name-defined] # noqa
    }
    for key in Languages.keys()  # type: ignore[name-defined] # noqa
}

# Aliases found in https://el.wiktionary.org/wiki/Module:%CE%B5%CF%84%CF%85%CE%BC%CE%BF%CE%BB%CE%BF%CE%B3%CE%AF%CE%B1#L-182--L-185
languages["αρχ"] = languages["grc"]
languages["ελν"] = languages["grc-koi"]
languages["κοι"] = languages["grc-koi"]
languages["μσν"] = languages["gkm"]

print("langs: dict[str, dict[str, str | bool]] = {")
for key, value in sorted(languages.items()):
    print(f'    "{key}": {value},')
print(f"}}  # {len(languages):,}")
