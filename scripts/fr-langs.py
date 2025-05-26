import re

from scripts_utils import get_content


def extract_dict_parts(
    lines: list[str],
    start: str,
    end: str,
    pattern: re.Pattern[str] = re.compile(r"([{,])\s*(\w+)\s*="),
) -> str:
    langs = f"\n{start}\n"
    in_section = False

    for line in lines:
        if not in_section:
            if line.startswith(start):
                in_section = True
            continue
        elif line.startswith(end):
            break

        if line.startswith("#"):
            continue

        langs += re.sub(pattern, r'\1"\2": ', line.strip()) + "\n"

    return f"{langs}{end}\n"


def remove_missing_langs(text: str) -> str:
    """Those langs are part of the dict, but keys are not found. It's likely a Wiki issue."""
    return text.replace("l['vieux néerlandais'] = l['vieux bas francique']\n", "")


def add_missing_langs() -> str:
    """
    Those langs are not yet part of the dict.
    Might be reduced to zero when available on the Wiktionary.
    For the latin ones see https://fr.wiktionary.org/wiki/Module:%C3%A9tymologie#L-120
    """
    return """

# Langues oubliées
l['bas latin'] = { 'name': 'bas latin' }  # 2020-07-19
l['deu'] = { 'name': 'allemand' }  # 2020-05-19
l['ell'] = { 'name': 'grec' }  # 2020-05-19
l['eus'] = { 'name': 'basque' }  # 2020-05-19
l['gallo-roman'] = { 'name': 'gallo-roman' }  # 2021-01-24
l['ind'] = { 'name': 'indonésien' }  # 2020-05-19
l['latin archaïque'] = { 'name': 'latin archaïque' }  # 2021-01-24
l['latin classique'] = { 'name': 'latin classique' }  # 2020-07-19
l['latin contemporain'] = { 'name': 'latin contemporain' }  # 2021-01-24
l['latin ecclésiastique'] = { 'name': 'latin ecclésiastique' }  # 2020-07-20
l['latin humaniste'] = { 'name': 'latin humaniste' }  # 2021-01-24
l['latin impérial'] = { 'name': 'latin impérial' }  # 2020-07-20
l['latin médiéval'] = { 'name': 'latin médiéval' }  # 2020-07-20
l['latin populaire'] = { 'name': 'latin populaire' }  # 2020-07-20
l['lat pop'] = { 'name': 'latin populaire' }  # 2020-11-03
l['latin tardif'] = { 'name': 'latin tardif' }  # 2020-07-20
l['latin vulgaire'] = { 'name': 'latin vulgaire' }  # 2020-07-20
l['latin néolatin'] = { 'name': 'latin néolatin' }  # 2021-01-24
# Fin langues oubliées
"""


code = get_content("https://fr.wiktionary.org/wiki/Module:langues/data?action=raw")
code = code.replace("--", "#").replace("true", "True")
code = re.sub(r"aliasOf\(('[^']+')\)", r"l[\1]", code)
code = code.split("\n")

script = "l = {}\n"
script += extract_dict_parts(code, "# Langues", "# Fin langues")
script += extract_dict_parts(code, "# Redirections de langues", "# Fin redirections de langues")
script += extract_dict_parts(code, "# Proto-langues", "# Fin protolangues")
script += extract_dict_parts(code, "# Redirections de proto-langues", "# Fin redirections de proto-langues")
script = remove_missing_langs(script)
script += add_missing_langs()

exec(script)
print("langs = {")
for key, value in sorted(l.items()):  # type: ignore[name-defined] # noqa: F821
    print(f'    "{key}": "{value["name"]}",')
print(f"}}  # {len(l):,}")  # type: ignore[name-defined] # noqa: F821
