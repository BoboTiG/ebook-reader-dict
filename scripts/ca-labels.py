import re
from typing import Dict

from scripts_utils import get_content

url = "https://ca.wiktionary.org/w/index.php?title=M%C3%B2dul:etiquetes/dades&action=raw"
text = get_content(url)

text = text.replace("local ", "")
text = text.replace("end", "")
text = text.replace("true", "True")
text = text.replace("false", "False")
text = text.replace("--", "#")
text = text.replace("	alternativa", "alternativa")

repl = (
    "categories_llengua",
    "categories_literal",
    "categories_llegua",
    "omit_preComma",
    "omit_postComma",
    "mostra",
)
for r in repl:
    text = re.sub(rf"[ \t]+{r}[\s]*=", f'    "{r}":', text)

code = ""
for line in text.split("\n"):
    if line.strip().startswith('return {["labels"]'):
        break
    code += line + "\n"

exec(code, globals())


def process_display(display: str) -> str:
    if "[[" in display:
        display = re.sub(r"\[\[[^\|\]]*\|(^\])*", "", display)
        display = display.replace("]]", "")
        display = display.replace("[[", "")
    return display


labels: Dict[str, str] = {}
syntaxes: Dict[str, Dict[str, bool]] = {}

for k, v in etiqueta.items():  # type: ignore # noqa
    if mostra := v.get("mostra"):
        labels[k] = process_display(mostra)
    elif "omit_preComma" in v or "omit_postComma" in v:
        syntaxes[k] = {
            "omit_postComma": bool(v.get("omit_postComma", False)),
            "omit_preComma": bool(v.get("omit_preComma", False)),
        }

for k, v in alternativa.items():  # type: ignore # noqa
    labels[k] = v

for k, v in etiqueta.items():  # type: ignore # noqa
    if "omit_preComma" not in v:
        continue
    syntaxes[k] = {
        "omit_postComma": bool(v.get("omit_postComma", False)),
        "omit_preComma": bool(v.get("omit_preComma", False)),
    }

print("label_syntaxes = {")
for key, value in sorted(syntaxes.items()):
    print(f'    "{key}": {{')
    for k, v in value.items():
        print(f'        "{k}": {v},')
    print("    },")
print(f"}}  # {len(syntaxes):,}")

print()

print("labels = {")
for k, v in sorted(labels.items()):
    print(f'    "{k}": "{v}",')
print(f"}}  # {len(labels):,}")
