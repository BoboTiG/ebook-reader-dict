import re

from scripts_utils import get_soup

url = "https://el.wiktionary.org/wiki/Module:labels/data"
lines = get_soup(url).find("div", "mw-highlight-lines").text.splitlines()
labels: dict[str, str | bool] = {}
remove_trailing_comma = re.compile(r"},\s*#?.*$").sub

code = ""
for line in lines:
    line = line.strip()
    if line.startswith("["):
        line = line.replace("--", "#")
        line = line.replace("true", "True")
        line = line.replace("false", "False")
        line = remove_trailing_comma("}", line)

        sline = line.split("=")
        outline = f"labels{sline[0]} = "
        outline2 = " : ".join([lab.strip() for lab in sline[1:]])
        outline2 = re.sub(r"\s*([\w]+)\s*:", r'"\g<1>" :', outline2)
        code += f"{outline}{outline2}\n"
exec(code, globals())
print("labels = {")
for k, v in labels.items():
    print(f'    "{k}": {{')
    for k, v in v.items():  # type: ignore
        if k in ["link", "linkshow"]:
            print(f'        "{k}": "{v}",')
    print("    },")
print(f"}}  # {len(labels)}")
