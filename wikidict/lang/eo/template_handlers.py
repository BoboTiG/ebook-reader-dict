from collections import defaultdict

from ...user_functions import concat, extract_keywords_from, italic, small, strong, superscript, term
from .langs import langs
from .tags import tags


def render_deveno3(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_deveno3("deveno3", ["eo", "egy", "Aa"], defaultdict(str, {"sg": "granda"}))
    'la egipta antikva vorto " <b>Aa</b> " <sup>→ egy</sup> (= granda)'
    >>> render_deveno3("deveno3", ["eo", "egy", "Aa"], defaultdict(str, {"sg": "-"}))
    'la egipta antikva vorto " <b>Aa</b> " <sup>→ egy</sup>'
    >>> render_deveno3("deveno3", ["en", "ang", "bridd"], defaultdict(str))
    'la anglosaksa vorto " <b>bridd</b> " <sup>→ ang</sup>'
    """
    parts.pop(0)  # Remove the source lang
    lang = parts.pop(0)
    phrase = f'la {langs[lang]} vorto " {strong(parts.pop(0))} "'
    if lang != "grc":
        phrase += f" {superscript('→ ' + lang)}"
    if (sg := data["sg"]) not in {"", "-"}:
        phrase += f" (= {sg})"
    return phrase


def render_elpropra(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_elpropra("elpropra", ["eo", "P", "Albert Einstein"], defaultdict(str, {"not": "fizikisto"}))
    'la nomo de persono "Albert Einstein" <small>(fizikisto)</small>'
    >>> render_elpropra("elpropra", ["eo", "-", "testo"], defaultdict(str, {"wpl": "-"}))
    'la nomo "testo"'
    >>> render_elpropra("elpropra", ["eo", "P", "Юрий Цолакович Оганесянz"], defaultdict(str, {"wpl": "-", "ts": "Juri Zolakowitsch Oganessia"}))
    'la nomo de persono "Юрий Цолакович Оганесянz" <i>Juri Zolakowitsch Oganessia</i>'
    """
    parts.pop(0)  # Remove the source lang
    phrase = "la nomo "

    match parts.pop(0):
        case "L":
            phrase += "de lando/regno "
        case "M":
            phrase += "de mita estaĵo "
        case "P":
            phrase += "de persono "
        case "R":
            phrase += "de rivero "
        case "T":
            phrase += "de monto "
        case "U":
            phrase += "de urbo "
        case "V":
            phrase += "de provinco "

    phrase += f'"{parts.pop(0)}"'

    if ts := data["ts"]:
        phrase += f" {italic(ts)}"

    if special := data["not"]:
        phrase += f" {small('('+special+')')}"

    return phrase


def render_form(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    Souce: https://eo.wiktionary.org/w/index.php?title=Modulo:meoformo&oldid=1027456
    Date : 2021-12-19 22:43

    >>> render_form("form-eo", [], defaultdict(str), word="ekamus")
    'ekami'
    >>> render_form("form-eo", [], defaultdict(str), word="hispanan")
    'hispana'
    >>> render_form("form-eo", [], defaultdict(str), word="surdaj")
    'surda'
    >>> render_form("form-eo", [], defaultdict(str), word="inexistant")
    'inexistant'
    """
    for suffix, last_char in [
        ("on", "o"),
        ("oj", "o"),
        ("ojn", "o"),
        ("an", "a"),
        ("aj", "a"),
        ("ajn", "a"),
        ("as", "i"),
        ("is", "i"),
        ("os", "i"),
        ("us", "i"),
        ("u", "i"),
    ]:
        if word.endswith(suffix):
            return f"{word.removesuffix(suffix)}{last_char}"
    return word


def render_g(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_g("g", ["nm"], defaultdict(str))
    '<i>neŭtra, vira</i>'
    """
    return {
        "m": italic("vira"),
        "f": italic("ina"),
        "n": italic("neŭtra"),
        "u": italic("komuna"),
        "mf": italic("vira, ina"),
        "nm": italic("neŭtra, vira"),
    }.get(parts[0], parts[0])


def render_hebr(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_hebr("Hebr", ["בַּיִת כְּנֶסֶת"], defaultdict(str, {"d-heb": "bayiṯ k<sup><small>e</small></sup>næsæt", "b": "domo por renkontiĝo"}))
    'בַּיִת כְּנֶסֶת, CHA <i>bayiṯ k<sup><small>e</small></sup>næsæt</i>, „domo por renkontiĝo“'
    >>> render_hebr("Hebr", ["שול"], defaultdict(str, {"d-yid": "shul", "b": "(Religions)"}))
    'שול, YIVO <i>shul</i>, „(Religions)“'
    >>> render_hebr("Hebr", ["אסנוגה"], defaultdict(str, {"d-lad": "esnoga", "b": "Sinagogo, preĝejo"}))
    'אסנוגה, <i>esnoga</i>, „Sinagogo, preĝejo“'
    """
    phrase = parts.pop(0)
    if heb := data["d-heb"]:
        phrase += f", CHA {italic(heb)}"
    elif yid := data["d-yid"]:
        phrase += f", YIVO {italic(yid)}"
    elif lad := data["d-lad"]:
        phrase += f", {italic(lad)}"
    if b := data["b"]:
        phrase += f", „{b}“"
    return phrase


def render_k(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_k("k", ["mul", "astrologio"], defaultdict(str))
    '<i>(astrologio)</i>'
    >>> render_k("k", ["eo", "arkitekturo", "% pri tempo kiel objekto"], defaultdict(str))
    '<i>(arkitekturo; pri tempo kiel objekto)</i>'
    >>> render_k("k", ["eo", "S: % iomete-", "arkitekturo"], defaultdict(str))
    '<i>(iomete arkitekturo)</i>'
    >>> render_k("k", ["eo", "T: ASKI.", "MATSI.", "F: historio", "arkitekturo", "S: % poezia", "S: vulgara", "C: % nepiva", "C: & nepiva"], defaultdict(str))
    '<i>(askia signo; matematika simbolo; historio; arkitekturo; poezia; vulgara; nepiva; nepiva)</i>'
    >>> render_k("k", ["eo", "G: VTR."], defaultdict(str))
    '<i>(transitiva)</i>'
    >>> render_k("k", ["eo", "G: VIT.-", '% kun prepozicio "pri"', "% eĉ-", "VTR.", "C: % celante senvivaĵon aŭ abstraktaĵon"], defaultdict(str))
    '<i>(netransitiva kun prepozicio "pri"; eĉ transitiva; celante senvivaĵon aŭ abstraktaĵon)</i>'
    """
    raw_themes = []
    current_type = ""
    any_is_prefix = False

    for part in parts[1:]:  # Skip the lang
        if ":" in part:
            current_type, part = part.split(":")

        part = part.strip().replace("% ", "").replace("& ", "")

        if is_prefix := part.endswith("-"):
            part = part.removesuffix("-")
            any_is_prefix = True

        match current_type:
            case "":
                pass
            case "C" | "F" | "S":
                part = tags.get(part, part)
            case "G" | "T":
                part = tags.get(part.removesuffix("."), part)
            case _:
                assert 0, f"Unhandled `k` type {current_type!r}"

        if is_prefix:
            part += "-"
        raw_themes.append(part)

    if any_is_prefix:
        # Merge items: when an item ends with a dash, then it must be concat with the next item in the list
        themes = []
        idx = 0
        while idx < len(raw_themes):
            if raw_themes[idx].endswith("-"):
                themes.append(f"{raw_themes[idx].removesuffix('-')} {raw_themes[idx + 1]}")
                idx += 1
            else:
                themes.append(raw_themes[idx])
            idx += 1
    else:
        themes = raw_themes

    return term(concat(themes, sep="; "))


def render_t(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_t("t", ["id", "roti"], defaultdict(str))
    'roti <sup>→ id</sup>'
    >>> render_t("t", ["id", "roti", "nm"], defaultdict(str))
    'roti <sup>→ id</sup> <i>neŭtra, vira</i>'
    >>> render_t("t", ["grc", "ὄνομα", "n"], defaultdict(str, {"ts": "ónuma", "not": "kvin literoj"}))
    'ὄνομα <i>neŭtra</i> <i>ónuma</i> (<small>kvin literoj</small>)'
    >>> render_t("t", ["ja", "脱出する"], defaultdict(str, {"sa": "だっしゅつする", "ts": "dasshutsu suru"}))
    '脱出する <sup>→ ja</sup> aŭ だっしゅつする <sup>→ ja</sup> <i>dasshutsu suru</i>'
    """
    lang = parts.pop(0)
    phrase = parts.pop(0)
    if lang != "grc":
        phrase += f" {superscript('→ ' + lang)}"
    if parts:
        phrase += f" {render_g('g', [parts.pop(0)], defaultdict(), word=word)}"

    if other := data["sa"]:
        phrase += f" aŭ {other} {superscript('→ ' + lang)}"
        if trans := data["ts"]:
            phrase += f" {italic(trans)}"
    else:
        if trans := data["ts"]:
            phrase += f" {italic(trans)}"
        if note := data["not"]:
            phrase += f" ({small(note)})"

    return phrase


template_mapping = {
    "deveno3": render_deveno3,
    "elpropra": render_elpropra,
    "form-eo": render_form,
    "g": render_g,
    "Hebr": render_hebr,
    "k": render_k,
    "t": render_t,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
