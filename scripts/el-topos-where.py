import re

from scripts_utils import get_content

code = get_content("https://el.wiktionary.org/wiki/Module:topos/where?action=raw")
in_comment = False
script_first_pass = ""
regex = r"(\w+)\s*=\s*"
subst = '"\\1": '

for line in code.split("\n"):
    if not (line := line.strip()):
        continue
    if line.startswith(("--[[", "--[=[")):
        in_comment = True
        continue
    if in_comment and line.startswith(("]]", "]=]--")):
        in_comment = False
        continue
    if in_comment:
        continue
    if line.startswith(("--", "return")):
        continue
    if line == "where = {}":
        script_first_pass += f"{line}\n"
        continue

    line = re.sub(regex, subst, line, count=0, flags=re.MULTILINE)
    if "--" in line:
        line = line.split("-- ", 1)[0].rstrip()
    script_first_pass += line
    if line.endswith("}"):
        script_first_pass += "\n"

# Sanitize entries on 2 lines with comment
script = ""
for line in script_first_pass.splitlines():
    if "--" in line:
        line = line.split("--", 1)[0]
    script += f"{line}\n"

exec(script)


def clean(text: str) -> str:
    """Extracted from `utils.clean()`."""
    # Local links
    text = re.sub(r"\[\[([^||:\]]+)\]\]", "\\1", text)  # [[a]] → a

    # Internal: [[a|b]] → b
    return re.sub(r"\[\[[^|]+\|(.+?(?=\]\]))\]\]", "\\1", text)


cleaned_wheres = {
    key: clean(values["word"])  # noqa: F821
    for key, values in where.items()  # type: ignore[name-defined] # noqa: F821
}

print("where: dict[str, str] = {")
for key, value in sorted(cleaned_wheres.items()):
    print(f'    "{key}": "{value}",')
print(f"}}  # {len(cleaned_wheres):,}")
