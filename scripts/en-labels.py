import re

from scripts_utils import get_content


def process_display(display: str) -> str:
    if "[[" in display:
        display = re.sub(
            r"\[\[(?:w|wikipedia|Wiktionary):[^|]*\|(^\])*",
            "",
            display,
            0,
            re.MULTILINE,
        )
        display = re.sub(r"\[\[[^\|\]]*\|(^\])*", "", display, 0, re.MULTILINE)
        display = display.replace("]]", "")
        display = display.replace("[[w:", "")
        display = display.replace("[[", "")
    return display


def clean_lua_text(text: str) -> str:
    text = text.replace("local ", "")
    text = text.replace("end", "")
    text = text.replace("true", "True")
    text = text.replace("false", "False")
    return text.replace("--", "#")


def process_page(url: str, repl: list[str], stop_line: str) -> dict[str, str]:
    text = get_content(f"{url}?action=raw")
    text = clean_lua_text(text)
    text = text.replace('" .. ', '" + ').replace('" ..\n', '" + ')
    text = text.replace(' .. "', ' + "').replace(' ..\n"', ' + "')

    text = re.sub(r"function\s+(\w+\([\w|\,|\s]+\))", "def \\g<1>:", text)
    text = text.replace("for _, v in ipairs(b) do", "\n    for v in b:\n        ")

    for r in repl:
        text = re.sub(rf"[ \t]+{r}[\s]*=", f'    "{r}":', text)
        if r != "labels":
            text = re.sub(rf"{r}[\s]*=", f'"{r}":', text)

    code = ""
    for line in text.split("\n"):
        if line.strip().startswith(stop_line):
            break
        elif "require" not in line:
            code += line + "\n"

    exec(code, globals())
    results: dict[str, str] = {}

    for k, v in labels.items():  # type: ignore[name-defined] # noqa: F821
        if k == "deprecated label":
            continue
        label_v = v
        label_k = k
        aliases = []
        if isinstance(v, str):
            label_v = labels.get(v, v)  # type: ignore[name-defined] # noqa: F821
            if label_v != v:
                label_k = v
        if isinstance(label_v, str):
            display = label_v
        else:
            display = label_v.get("display", label_k)
            aliases = label_v.get("aliases", [])
        display = process_display(display)
        results[k] = display.replace('"', "'")

        if isinstance(aliases, str):
            aliases = [aliases]
        for a in aliases:
            results[a] = display.replace('"', "'")

    return results


repl = sorted(
    [
        "accent_display",
        "accent_Wikipedia",
        "addl",
        "aliases",
        "alias_of",
        "category",
        "country",
        "labels",
        "def",
        "deprecated",
        "deprecated_aliases",
        "display",
        "form_of_display",
        "from",
        "fulldef",
        "glossary",
        "langs",
        "language",
        "nolink",
        "noreg",
        "omit_preComma",
        "omit_postComma",
        "omit_preSpace",
        "omit_postSpace",
        "othercat",
        "parent",
        "parent_label",
        "plain_categories",
        "pos_categories",
        "prep",
        "region",
        "regional_categories",
        "sense_categories",
        "special_display",
        "the",
        "topical_categories",
        "track",
        "type",
        "verb",
        "Wikidata",
        "wikipedia",
        "Wikipedia",
        "Wiktionary",
    ],
    key=len,
    reverse=True,
)

results: dict[str, str] = {}
urls = [
    ("https://en.wiktionary.org/wiki/Module:labels/data", "return labels"),
    ("https://en.wiktionary.org/wiki/Module:labels/data/lang/en", "################## accent qualifiers"),
    ("https://en.wiktionary.org/wiki/Module:labels/data/regional", "return labels"),
    ("https://en.wiktionary.org/wiki/Module:labels/data/topical", "return"),
]
for url, pattern in urls:
    results |= process_page(url, repl, pattern)
qualifiers = process_page("https://en.wiktionary.org/wiki/Module:labels/data/qualifiers", repl, "return require(")
results |= qualifiers
print("labels = {")
for key, value in sorted(results.items()):
    if len(key) < 62 and len(key):  # if it's too long, it's not useful
        print(f'    "{key}": "{value}",')
print(f"}}  # {len(results):,}")

syntaxes: dict[str, dict[str, bool]] = {}
for k, v in labels.items():  # type: ignore[name-defined] # noqa: F821
    label_v = v
    if isinstance(v, str):
        label_v = labels.get(v)  # type: ignore[name-defined] # noqa: F821
    if not label_v:
        continue
    omit_preComma = label_v.get("omit_preComma")
    omit_postComma = label_v.get("omit_postComma")
    omit_preSpace = label_v.get("omit_preSpace")

    aliases = []
    aliases = label_v.get("aliases", [])

    if omit_postComma or omit_preComma or omit_preSpace:
        for a in aliases:
            syntaxes[a] = {
                "omit_postComma": bool(omit_postComma),
                "omit_preComma": bool(omit_preComma),
                "omit_preSpace": bool(omit_preSpace),
            }
        syntaxes[k] = {
            "omit_postComma": bool(omit_postComma),
            "omit_preComma": bool(omit_preComma),
            "omit_preSpace": bool(omit_preSpace),
        }

print()
print("syntaxes = {")
for key, value in sorted(syntaxes.items()):  # type: ignore[assignment]
    print(f'    "{key}": {{')
    for k, v in value.items():  # type: ignore[attr-defined]
        print(f'        "{k}": {v},')
    print("    },")
print(f"}}  # {len(syntaxes):,}")
