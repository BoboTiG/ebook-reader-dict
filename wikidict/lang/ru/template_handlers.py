from typing import DefaultDict, List, Tuple

import requests
from bs4 import BeautifulSoup

from ...user_functions import extract_keywords_from
from .. import defaults


# for etymology content, need to run code to get text from other wiktionary page
def get_etymology(tpl: str, parts: List[str], data: DefaultDict[str, str], word: str = "") -> str:
    # Fetching that endpoint for 1.3+ milion of words is not a solution, skipping for now.
    return ""
    if not parts or not (etyl := parts[0].split("|")[0]):
        return ""
    url = f"https://ru.wiktionary.org/wiki/Шаблон:{tpl}:{etyl}"
    page = requests.get(url).content
    soup = BeautifulSoup(page, features="html.parser")
    content = soup.find("div", class_="mw-parser-output")
    return str(content.getText())


def get_example(tpl: str, parts: List[str], data: DefaultDict[str, str], word: str = "") -> str:
    # if len(parts) > 0:
    #     return ". (Пример: " + parts[0] + ")"
    # elif "текст" in data.keys():
    #     return ". (Пример: " + data["текст"] + ")"
    return ""


def get_definition(tpl: str, parts: List[str], data: DefaultDict[str, str], word: str = "") -> str:
    return str(data["определение"] + data["примеры"])


def get_note(tpl: str, parts: List[str], data: DefaultDict[str, str], word: str = "") -> str:
    return f"({parts[0]})"


template_mapping = {
    "w": defaults.render_wikilink,
    "W": defaults.render_wikilink,
    "этимология": get_etymology,
    "пример": get_example,
    "значение": get_definition,
    "помета": get_note,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
