from scripts_utils import get_soup

text = get_soup("https://ru.wiktionary.org/wiki/%D0%9C%D0%BE%D0%B4%D1%83%D0%BB%D1%8C:language/data").text
code = ["m: dict[str, str] = {}"]
for line in text[text.find('m["') : text.find("return m")].splitlines():
    if "--" in line:
        line = line.replace("--", "#")

    if "m[" in line:
        if "table.copy(" in line:
            line = line.replace("table.copy(", "").rstrip(")")
        elif '"code"' in line or '"redirect"' in line:
            continue
        else:
            line = line.split("{")[0] + "{"
        code.append(line)
    elif "short =" in line:
        code.append(line.replace("short =", '"short":'))
    elif line.strip() == "}":
        code.append("}")

exec("\n".join(code))

count = 0
print("langs_short: dict[str, str] = {")
for key, value in sorted(m.items()):  # type: ignore[name-defined] # noqa: F821
    if short := value["short"]:
        print(f'    "{key}": "{short}",')
        count += 1
print(f"}}  # {count:,}")
