from typing import Tuple, Dict, List

from .. import defaults
from ...user_functions import (
    extract_keywords_from,
)

import requests
from bs4 import BeautifulSoup

# for etymology content, need to run code to get text from other wiktionary page
def get_ru_etymology(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    url = "https://ru.wiktionary.org/wiki/Шаблон:" + tpl + ":" + parts[0].split("|")[0]
    page = requests.get(url).content
    soup = BeautifulSoup(page, features="html.parser")
    content = soup.find("div", class_="mw-parser-output")
    output = content.getText()
    return output


def get_ru_example(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    if len(parts) > 0:
        return ". (Пример: " + parts[0] + ")"
    elif "текст" in data.keys():
        return ". (Пример: " + data["текст"] + ")"
    return ""


template_mapping = {
    "w": defaults.render_wikilink,
    "W": defaults.render_wikilink,
    "этимология": get_ru_etymology,
    "пример": get_ru_example,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
