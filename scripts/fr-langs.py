import re

from scripts_utils import get_soup


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
l['bas latin'] = { 'nom': 'bas latin' }  # 2020-07-19
l['deu'] = { 'nom': 'allemand' }  # 2020-05-19
l['ell'] = { 'nom': 'grec' }  # 2020-05-19
l['eus'] = { 'nom': 'basque' }  # 2020-05-19
l['gallo-roman'] = { 'nom': 'gallo-roman' }  # 2021-01-24
l['ind'] = { 'nom': 'indonésien' }  # 2020-05-19
l['latin archaïque'] = { 'nom': 'latin archaïque' }  # 2021-01-24
l['latin classique'] = { 'nom': 'latin classique' }  # 2020-07-19
l['latin contemporain'] = { 'nom': 'latin contemporain' }  # 2021-01-24
l['latin ecclésiastique'] = { 'nom': 'latin ecclésiastique' }  # 2020-07-20
l['latin humaniste'] = { 'nom': 'latin humaniste' }  # 2021-01-24
l['latin impérial'] = { 'nom': 'latin impérial' }  # 2020-07-20
l['latin médiéval'] = { 'nom': 'latin médiéval' }  # 2020-07-20
l['latin populaire'] = { 'nom': 'latin populaire' }  # 2020-07-20
l['lat pop'] = { 'nom': 'latin populaire' }  # 2020-11-03
l['latin tardif'] = { 'nom': 'latin tardif' }  # 2020-07-20
l['latin vulgaire'] = { 'nom': 'latin vulgaire' }  # 2020-07-20
l['latin néolatin'] = { 'nom': 'latin néolatin' }  # 2021-01-24
# Fin langues oubliées
"""


soup = get_soup("https://fr.wiktionary.org/wiki/Module:langues/data")
code = soup.find("pre", {"class": "mw-code"}).text.replace("--", "#").replace("true", "True").split("\n")

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
    print(f'    "{key}": "{value["nom"]}",')
print(f"}}  # {len(l):,}")  # type: ignore[name-defined] # noqa: F821
