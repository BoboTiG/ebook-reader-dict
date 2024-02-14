from typing import DefaultDict, List, Tuple

import requests
from bs4 import BeautifulSoup

from ...user_functions import extract_keywords_from
from .. import defaults


# for etymology content, need to run code to get text from other wiktionary page
def get_ru_etymology(tpl: str, parts: List[str], data: DefaultDict[str, str]) -> str:
    if not parts[0].split("|")[0]:
        return "?"
    url = f"https://ru.wiktionary.org/wiki/Шаблон:{tpl}:{parts[0].split('|')[0]}"
    page = requests.get(url).content
    soup = BeautifulSoup(page, features="html.parser")
    content = soup.find("div", class_="mw-parser-output")
    return str(content.getText())


def get_ru_example(tpl: str, parts: List[str], data: DefaultDict[str, str]) -> str:
    # if len(parts) > 0:
    #     return ". (Пример: " + parts[0] + ")"
    # elif "текст" in data.keys():
    #     return ". (Пример: " + data["текст"] + ")"
    return ""


def get_ru_definition(tpl: str, parts: List[str], data: DefaultDict[str, str]) -> str:
    return str(data["определение"] + data["примеры"])


def get_ru_note(tpl: str, parts: List[str], data: DefaultDict[str, str]) -> str:
    return f"({parts[0]})"


def get_part0(tpl: str, parts: List[str], data: DefaultDict[str, str]) -> str:
    return str(parts[0])


def get_so(tpl: str, parts: List[str], data: DefaultDict[str, str]) -> str:
    return f"то же, что {list(data.values())[0].strip('|')}"


template_mapping = {
    "t": get_so,  # https://ru.wiktionary.org/wiki/%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD:%3D
    "w": defaults.render_wikilink,
    "W": defaults.render_wikilink,
    "этимология": get_ru_etymology,
    "пример": get_ru_example,
    "значение": get_ru_definition,
    "помета": get_ru_note,
    "выдел": get_part0,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
