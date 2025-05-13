from collections import defaultdict

from bs4 import BeautifulSoup

from ... import constants
from ...user_functions import extract_keywords_from, italic, superscript
from .. import defaults
from .langs_short import langs_short


def get_etymology(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """For etymology content, need to run code to get text from other wiktionary page."""
    # Fetching that endpoint for 1.3+ million of words is not a solution, skipping for now.
    return ""
    if not parts or not (etyl := parts[0].split("|")[0]):
        return ""
    url = f"https://ru.wiktionary.org/wiki/Шаблон:{tpl}:{etyl}"
    page = constants.SESSION.get(url).content
    soup = BeautifulSoup(page, features="html.parser")
    content = soup.find("div", class_="mw-parser-output")
    return str(content.getText())


def get_definition(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    return str(data["определение"] + data["примеры"])


def render_сэ(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_сэ("сэ", ["en", "-ing"], defaultdict(str, {"и": "ru"}))
    'англ. -ing'
    >>> render_сэ("сэ", ["fr", "Aramis"], defaultdict(str))
    'франц. Aramis'
    >>> render_сэ("сэ", ["fr"], defaultdict(str))
    'франц.'
    >>> render_сэ("сэ", ["fr", "pépinière", "питомник"], defaultdict(str, {"и": "ru"}))
    'франц. pépinière ‘питомник’'
    >>> render_сэ("сэ", ["", "alarm", "тревога"], defaultdict(str, {"скр": "1"}))
    'alarm ‘тревога’'
    >>> render_сэ("сэ", ["yue", "海鮮"], defaultdict(str, {"т": "hoi<sup>2</sup> sin<sup>1</sup>"}))
    '海鮮 (hoi<sup>2</sup> sin<sup>1</sup>)'
    """
    lang = parts.pop(0)
    texts = []
    if lang and (slang := langs_short.get(lang)):
        texts.append(slang)
    if parts:
        texts.append(parts.pop(0))
    if parts:
        texts.append(f"‘{parts[0]}’")
    if т := data["т"]:
        texts.append(f"({т})")
    return " ".join(texts)


def render_помета(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_помета("помета", ["о действии"], defaultdict(str))
    '<i>о действии</i>'
    """
    return italic(parts[0])


def render_соотн(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_соотн("соотн.", ["Аввакум"], defaultdict(str))
    'связанный, соотносящийся по значению с существительным Аввакум'
    >>> render_соотн("соотн.", ["Аввакум"], defaultdict(str, {"свойств": "1"}))
    'связанный, соотносящийся по значению с существительным Аввакум; свойственный, характерный для него'
    >>> render_соотн("соотн.", ["Аввакум"], defaultdict(str, {"свойств": "неё"}))
    'связанный, соотносящийся по значению с существительным Аввакум; свойственный, характерный для неё'
    >>> render_соотн("соотн.", ["Аввакум"], defaultdict(str, {"свойств": "магистрали"}))
    'связанный, соотносящийся по значению с существительным Аввакум; свойственный, характерный для магистрали'
    >>> render_соотн("соотн.", ["идиоматизм", "идиома"], defaultdict(str, {"свойств": "1"}))
    'связанный, соотносящийся по значению с существительным идиоматизм, идиома; свойственный, характерный для него'
    """
    phrase = f"связанный, соотносящийся по значению с существительным {', '.join(parts)}"
    if свойств := data["свойств"]:
        phrase += f"; свойственный, характерный для {'него' if свойств == '1' else свойств}"
    return phrase


def render_lang(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_lang("lang", ["de", "Fahne", "знамя", "знамя2", "знамя3"], defaultdict(str, {"зачин": "зачин", "add": "add,", "add2": "add2", "comment": "comment"}))
    'зачин нем. Fahne add, add2 «знамя, знамя2, знамя3» (comment)'
    >>> render_lang("lang", ["de", "Fahne", "знамя"], defaultdict(str, {"скр": "1"}))
    'Fahne «знамя»'
    >>> render_lang("lang", ["ru", "зна́мя"], defaultdict(str, {}))
    'русск. зна́мя'
    >>> render_lang("lang", ["el"], defaultdict(str, {}))
    'греч.'
    >>> render_lang("lang2", ["la", "instrūmentum", "орудие, инструмент"], defaultdict(str, {"ссылка": "instrumentum"}))
    'лат. instrūmentum «орудие, инструмент»'
    """
    lang_short = langs_short.get(parts.pop(0), "")
    if not parts and not data:
        return lang_short

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


def render_t(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_t("t", ["en", "palace"], defaultdict(str, {}))
    'palace <sup>(en)</sup>'
    >>> render_t("t", ["en", "hall", "m"], defaultdict(str, {}))
    'hall <sup>(en)</sup> <i>M.</i>'
    >>> render_t("t", ["en", "bottle", "f"], defaultdict(str, {}))
    'bottle <sup>(en)</sup> <i>ж.</i>'
    >>> render_t("t", ["ja", "会館"], defaultdict(str, {"tr": "kaikan"}))
    '会館 <sup>(ja)</sup> (kaikan)'
    """
    text = f"{parts[1]} {superscript(f'({parts[0]})')}"
    if len(parts) > 2:
        gender = {"f": "ж", "m": "M"}[parts[2]]
        text += f" {italic(f'{gender}.')}"
    if trans := data["tr"]:
        text += f" ({trans})"
    return text


def render_кавычки(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
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


def render_сравн(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_сравн("сравн.", ["злой"], defaultdict(str))
    '<i>сравн. ст.</i> к прил. злой'
    >>> render_сравн("сравн.", ["злой"], defaultdict(str, {"к": "нареч"}))
    '<i>сравн. ст.</i> к нареч. злой'
    """
    return f"{italic('сравн. ст.')} к {data['к'] or 'прил'}. {parts[0]}"


def render_дат(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_дат("дат", ["18", "ru"], defaultdict(str))
    ''
    >>> render_дат("дат", ["18-2", "ru"], defaultdict(str))
    ''
    >>> render_дат("дат", ["XVIII", "ru"], defaultdict(str))
    ''
    >>> render_дат("дат", ["2024", "ru"], defaultdict(str))
    '2024'
    """
    date = parts[0]
    return date if len(date) == 4 and date.isdigit() else ""


def render_действие(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_действие("действие", ["изгнать, изгонять"], defaultdict(str))
    'действие по значению гл. изгнать, изгонять'
    >>> render_действие("действие", ["изгнать, изгонять", "насильственное удаление откуда-либо"], defaultdict(str))
    'действие по значению гл. изгнать, изгонять; насильственное удаление откуда-либо'
    >>> render_действие("действие", ["изгнать, изгонять", "насильственное удаление откуда-либо"], defaultdict(str, {"состояние": "1"}))
    'действие или состояние по значению гл. изгнать, изгонять; насильственное удаление откуда-либо'
    """
    text = "действие "
    if data["состояние"] == "1":
        text += "или состояние "
    text += f"по значению гл. {parts.pop(0)}"
    if parts:
        text += f"; {parts[0]}"
    return text


def render_морфема(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_морфема("морфема", [], defaultdict(str))
    'при добавлении к разным частям речи образует слова'
    >>> render_морфема("морфема", [], defaultdict(str, {"lang": "ru"}))
    'при добавлении к разным частям речи образует слова'
    >>> render_морфема("морфема", [], defaultdict(str, {"удар": ""}))
    'при добавлении к разным частям речи образует слова'
    >>> render_морфема("морфема", [], defaultdict(str, {"знач": ""}))
    'при добавлении к разным частям речи образует слова'
    >>> render_морфема("морфема", [], defaultdict(str, {"удар": "нет"}))
    'в безударной позиции при добавлении к разным частям речи образует слова'
    >>> render_морфема("морфема", [], defaultdict(str, {"удар": "нет", "часть": "глагольной основе", "образует": "существительные", "знач": "действия, названного мотивирующим глаголом", "lang": "ru"}))
    'в безударной позиции при добавлении к глагольной основе образует существительные со значением действия, названного мотивирующим глаголом'
    """
    text = ""
    if удар := data["удар"]:
        match удар:
            case "нет":
                text = "в безударной позиции "

    text += "при добавлении к"
    text += f" {data['часть'] or 'разным частям речи'}"
    text += f" образует {data['образует'] or 'слова'}"

    if знач := data["знач"]:
        text += f" со значением {знач}"

    return text


def render_отчество(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_отчество("отчество", ["Август", "ж", "ru"], defaultdict(str))
    'женское отчество от имени Август'
    >>> render_отчество("отчество", ["Август", "м", "ru"], defaultdict(str))
    'мужское отчество от имени Август'
    """
    text = "мужское" if parts[1] == "м" else "женское"
    return f"{text} отчество от имени {parts[0]}"


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_variant("прич.", ["зыбить"], defaultdict(str))
    'зыбить'
    >>> render_variant("прич.", ["<small>?</small>"], defaultdict(str))
    ''
    """
    if (variant := parts[0]) == "<small>?</small>":
        variant = ""
    return variant


template_mapping = {
    "lang": render_lang,
    "lang2": render_lang,
    "t": render_t,
    "w": defaults.render_wikilink,
    "W": defaults.render_wikilink,
    "этимология": get_etymology,
    "значение": get_definition,
    "помета": render_помета,
    "кавычки": render_кавычки,
    "сэ": render_сэ,
    "сравн.": render_сравн,
    "соотн.": render_соотн,
    "дат": render_дат,
    "действие": render_действие,
    "морфема": render_морфема,
    "отчество": render_отчество,
    #
    # Variants
    #
    "__variant__прич.": render_variant,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
