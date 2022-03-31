from typing import Tuple, Dict, List

from .. import defaults
from ...user_functions import (
    extract_keywords_from,
    italic,
)

import requests
from bs4 import BeautifulSoup

#for etymology content, need to run code to get text from other wiktionary page
def get_ru_etymology(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    url = 'https://ru.wiktionary.org/wiki/Шаблон:' + tpl +":"+ parts[0].split("|")[0]
    page = requests.get(url).content
    soup = BeautifulSoup(page, features="html.parser")
    content = soup.find('div', class_='mw-parser-output')
    output = content.getText() 
    return output

def get_ru_example(tpl:str, parts: List[str], data: Dict[str,str]) -> str:
    if len(parts) > 0:
        return ('. (Пример: ' + parts[0] + ')')
    elif 'текст' in data.keys():
        return ('. (Пример: ' + data['текст'] + ')')
    return '' 

def render_wikisource(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_wikisource("ws", ["Les Grenouilles qui demandent un Roi"], defaultdict(str))
    'Les Grenouilles qui demandent un Roi'
    >>> render_wikisource("ws", ["Bible Segond 1910/Livre de Daniel", "Livre de Daniel"], defaultdict(str))
    'Livre de Daniel'
    >>> render_wikisource("ws", ["ADB:Emmerling, Ludwig August", "Ludwig August Emmerling"], defaultdict(str, {"lang":"de"}))
    'Ludwig August Emmerling'
    >>> render_wikisource("ws", ["ADB:Emmerling, Ludwig August"], defaultdict(str, {"lang":"de", "Ludwig August <span style": "'font-variant:small-caps'>Emmerling</span>"}))
    "Ludwig August <span style='font-variant:small-caps'>Emmerling</span>"
    """  # noqa
    phrase = parts[-1]
    if data:
        # Possible imbricated templates: {{ws| {{pc|foo bar}} }}
        potential_phrase = "".join(f"{k}={v}" for k, v in data.items() if k != "lang")
        if potential_phrase:
            phrase = potential_phrase
    return phrase


def render_zh_lien(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_zh_lien("zh-lien", ["人", "rén"], defaultdict(str))
    '人 (<i>rén</i>)'
    >>> render_zh_lien("zh-lien", ["马", "mǎ", "馬"], defaultdict(str))
    '马 (馬, <i>mǎ</i>)'
    >>> render_zh_lien("zh-lien", ["骨", "gǔ", "骨"], defaultdict(str))
    '骨 (骨, <i>gǔ</i>)'
    """
    simple = parts.pop(0)
    pinyin = italic(parts.pop(0))
    traditional = parts[0] if parts else ""
    if not traditional:
        return f"{simple} ({pinyin})"
    return f"{simple} ({traditional}, {pinyin})"


template_mapping = {
    "w": defaults.render_wikilink,
    "W": defaults.render_wikilink,
    "ws": render_wikisource,
    "zh-lien": render_zh_lien,
    "этимология":get_ru_etymology,
    "пример":get_ru_example,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
