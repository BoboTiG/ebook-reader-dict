import re
from typing import Set

from scripts_utils import get_soup


def lua_to_python(text: str) -> str:
    in_comment = False
    script = ""
    regex = r"(\w+)\s*=\s*"
    subst = '"\\1": '
    for line in text.split("\n"):
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
        if original_line.startswith("return"):
            continue
        if line.startswith(("--")):
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
        if "--" in line:
            line = line.split("--")[0].strip()
        script += line
    return script


url = "https://ca.wiktionary.org/wiki/M%C3%B2dul:llengua/taula"
soup = get_soup(url)

textarea = soup.find(class_="mw-highlight-lines")

script = lua_to_python(textarea.text)
print(script)
exec(script)
trans_modules = {}
for k, v in c.items():  # type: ignore # noqa
    if "trans_module" in v:
        trans_modules[k] = v["trans_module"]
        print(k)
        print(v["trans_module"])

trans_functions: Set[str] = set()
for v in trans_modules.values():
    url_trans = f"https://ca.wiktionary.org/wiki/M%C3%B2dul:{v}"
    soup = get_soup(url_trans)
    textarea = soup.find(class_="mw-highlight-lines")
    print(textarea.text)
    print(lua_to_python(textarea.text))
    exit()
