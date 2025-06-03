import re

from scripts_utils import get_content

code = get_content("https://el.wiktionary.org/wiki/Module:topos/kind?action=raw")
in_comment = False
script_first_pass = ""
regex = r"(\w+)\s*=\s*"
subst = '"\\1": '

for line in code.split("\n"):
    original_line = line

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
    if not original_line.startswith("\t"):
        script_first_pass += "\n"
    if line == "kind = {}":
        script_first_pass += line
        continue

    line = line.replace("true", "True")
    line = re.sub(regex, subst, line, count=0, flags=re.MULTILINE)
    if "--" in line:
        line = line.split("-- ", 1)[0]
    script_first_pass += line

# Sanitize entries on 2 lines with comment
script = ""
for line in script_first_pass.splitlines():
    if "--" in line:
        line = line.split("--", 1)[0]
    script += f"{line}\n"

exec(script)

cleaned_kinds = {
    key: {
        "word": values.get("word", ""),  # noqa: F821
        "word_pl": values.get("word_pl", ""),  # noqa: F821
    }
    for key, values in kind.items()  # type: ignore[name-defined] # noqa: F821
}

print("kind: dict[str, dict[str, str]] = {")
for key, value in sorted(cleaned_kinds.items()):
    print(f'    "{key}": {value},')
print(f"}}  # {len(cleaned_kinds):,}")
