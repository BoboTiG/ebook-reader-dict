from scripts_utils import get_content

results: dict[str, str] = {}
text = get_content("https://es.wiktionary.org/wiki/M%C3%B3dulo:contexto/csem?action=raw")
code = text.splitlines()[1:-1]  # Skip "local m = {}" and "return m"

script = "m = {}\n" + "\n".join(code)
exec(script)

print("campos_semanticos = {")
for t, r in sorted(m.items()):  # type: ignore[name-defined] # noqa: F821
    print(f'    "{t}": "{r.pop()}",')
print(f"}}  # {len(m):,}")  # type: ignore[name-defined] # noqa: F821
