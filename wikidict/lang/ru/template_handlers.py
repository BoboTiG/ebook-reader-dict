from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from ...user_functions import extract_keywords_from
from .. import defaults
from .langs_short import langs_short


def get_etymology(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """For etymology content, need to run code to get text from other wiktionary page."""
    # Fetching that endpoint for 1.3+ million of words is not a solution, skipping for now.
    return ""
    if not parts or not (etyl := parts[0].split("|")[0]):
        return ""
    url = f"https://ru.wiktionary.org/wiki/Шаблон:{tpl}:{etyl}"
    page = requests.get(url).content
    soup = BeautifulSoup(page, features="html.parser")
    content = soup.find("div", class_="mw-parser-output")
    return str(content.getText())


def get_definition(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    return str(data["определение"] + data["примеры"])


def get_note(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    return f"({parts[0]})"


def render_lang(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_lang("lang", ["de", "Fahne", "знамя", "знамя2", "знамя3"], defaultdict(str, {"зачин": "зачин", "add": "add,", "add2": "add2", "comment": "comment"}))
    'зачин нем. Fahne add, add2 «знамя, знамя2, знамя3» (comment)'
    >>> render_lang("lang", ["de", "Fahne", "знамя"], defaultdict(str, {"скр": "1"}))
    'Fahne «знамя»'
    >>> render_lang("lang", ["ru", "зна́мя"], defaultdict(str, {}))
    'русск. зна́мя'
    """
    lang_short = langs_short.get(parts.pop(0), "")
    text = f"{data['зачин']}"
    if data["скр"] != "1":
        text += f" {lang_short}"
    text += f" {parts.pop(0)}"
    if add := data["add"]:
        text += f" {add}"
    if add := data["add2"]:
        text += f" {add}"
    if parts:
        text += f" «{', '.join(parts)}»"
    if comment := data["comment"]:
        text += f" ({comment})"
    return text.strip()


def render_кавычки(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_кавычки("кавычки", ["en", "love"], defaultdict(str))
    '“love”'
    """
    match parts[0]:
        case "da":
            return f"»{parts[1]}«"
        case "de":
            return f"„{parts[1]}“"
        case "el":
            return f"“{parts[1]}„"
        case "en":
            return f"“{parts[1]}”"
        case "es" | "ru" | "sr":
            return f"«{parts[1]}»"
        case "fi":
            return f"”{parts[1]}”"
        case "fr":
            return f"«&nbsp;{parts[1]}&nbsp;»"
        case "ja" | "zh":
            return f"「{parts[1]}」"
        case "pl":
            return f"„{parts[1]}”"
        case "sv":
            return f"’{parts[1]}’"

    return f'"{parts[1]}"'


template_mapping = {
    "lang": render_lang,
    "w": defaults.render_wikilink,
    "W": defaults.render_wikilink,
    "этимология": get_etymology,
    "значение": get_definition,
    "помета": get_note,
    "кавычки": render_кавычки,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
