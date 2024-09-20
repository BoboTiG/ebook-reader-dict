from collections import defaultdict

from ...user_functions import (
    concat,
    extract_keywords_from,
    italic,
    lookup_italic,
    parenthesis,
    small,
    strong,
    term,
)
from .langs import langs


def render_escopo(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_escopo("escopo", ["Pecuária"], defaultdict(str))
    '<i>(Pecuária)</i>'
    >>> render_escopo("escopo", ["Brasileirismo"], defaultdict(str))
    '<i>(Brasil)</i>'
    >>> render_escopo("escopo", ["pt", "estrangeirismo"], defaultdict(str))
    '<i>(estrangeirismo)</i>'
    >>> render_escopo("escopo", ["pt", "Antropônimo"], defaultdict(str))
    '<i>(Antropônimo)</i>'
    >>> render_escopo("escopo", ["pt", "réptil"], defaultdict(str))
    '<i>(zoologia)</i>'
    >>> render_escopo("escopo", ["gl", "Sexualidade"], defaultdict(str))
    '<i>(Sexualidade)</i>'
    >>> render_escopo("escopo", ["pt", "coloquial", "brasil"], defaultdict(str))
    '<i>(coloquial e Brasil)</i>'
    >>> render_escopo("escopo", ["pt", "Catolicismo", "cristianismo", "cristianismo"], defaultdict(str))
    '<i>(Catolicismo, cristianismo e cristianismo)</i>'
    """
    words = [lookup_italic(p, "pt") for p in parts if p not in langs]
    return term(concat(words, sep=", ", last_sep=" e "))


def render_etimo(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_etimo("etimo", ["la", "myrmecophaga"], defaultdict(str))
    '<i>myrmecophaga</i>'
    >>> render_etimo("etimo", ["grc", "στεγάζω", "(stegházo)"], defaultdict(str))
    '<i>στεγάζω</i> (stegházo)'
    >>> render_etimo("etimo", ["orv", "ꙗзꙑкъ", "(jazykŭ)", "língua"], defaultdict(str))
    '<i>ꙗзꙑкъ</i> (jazykŭ) “língua”'
    >>> render_etimo("etimo", ["orv", "ꙗзꙑкъ"], defaultdict(str, {"transcr": "(jazykŭ)", "trad": "língua"}))
    '<i>ꙗзꙑкъ</i> (jazykŭ) “língua”'
    >>> render_etimo("etimo", ["la", "canis"], defaultdict(str, {"trad": "cão"}))
    '<i>canis</i> “cão”'
    >>> render_etimo("etimo", ["la", "duos", "(duōs)"], defaultdict(str))
    '<i>duos</i> (duōs)'
    >>> render_etimo("etimo", ["grc", "ἄντρον"], defaultdict(str, {"transcr": "ánton", "trad": "caverna"}))
    '<i>ἄντρον</i> ánton “caverna”'
    >>> render_etimo("etimo", ["la", "nomen substantivum", "", "nome autônomo"], defaultdict(str))
    '<i>nomen substantivum</i> “nome autônomo”'
    """
    parts.pop(0)  # Remove the lang
    phrase = italic(parts.pop(0))  # The etimo
    if parts:  # Implicit transcr
        if transcr := parts.pop(0):
            phrase += f" {transcr}"
    if parts:  # Implicit trad
        phrase += f" “{parts.pop(0)}”"
    if transcr := data["transcr"]:
        phrase += f" {transcr}"
    if trad := data["trad"]:
        phrase += f" “{trad}”"
    return phrase


def render_etimo2(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_etimo2("etimo2", ["la", "myrmecophaga", "pt"], defaultdict(str))
    'Do latim <i>myrmecophaga</i>.'
    >>> render_etimo2("etimo2", ["la", "exauctorare"], defaultdict(str))
    'Do latim <i>exauctorare</i>.'
    >>> render_etimo2("llietimo", ["la", "myrmecophaga", "pt"], defaultdict(str))
    'Do latim <i>myrmecophaga</i>.'
    >>> render_etimo2("llietimo", ["en", "storm", "sv"], defaultdict(str, {"trad": "tempestade"}))
    'Do inglês <i>storm</i> “tempestade”.'
    >>> render_etimo2("llietimo", ["ru", "ко́шка", "ja", "kóška", "gato"], defaultdict(str))
    'Do russo <i>ко́шка</i> (<i>kóška</i>) “gato”.'
    >>> render_etimo2("llietimo", ["ru", "ко́шка", "ja"], defaultdict(str, {"transcr": "kóška", "trad": "gato", "ponto": ""}))
    'Do russo <i>ко́шка</i> (<i>kóška</i>) “gato”.'
    >>> render_etimo2("llietimo", ["ru", "ко́шка", "ja", "kóška", "gato"], defaultdict(str, {"ponto": "não"}))
    'Do russo <i>ко́шка</i> (<i>kóška</i>) “gato”'
    >>> render_etimo2("llietimo", ["ru", "ко́шка", "ja", "kóška", "gato"], defaultdict(str, {"ponto": "1"}))
    'Do russo <i>ко́шка</i> (<i>kóška</i>) “gato”'
    >>> render_etimo2("llietimo", ["la", "ardere", "pt"], defaultdict(str, {"4": '"queimar"', "5": "noop"}))
    'Do latim <i>ardere</i> (<i>"queimar"</i>) “noop”.'

    >>> # Note: below example is not expected because we would need to translate Greek to Spanish
    >>> render_etimo2("llietimo", ["grc", "γάτα", "es", "transliteração"], defaultdict(str))
    'Do grego antigo <i>γάτα</i> (<i>transliteração</i>).'
    """
    try:
        src, word, _, *rest = parts
    except ValueError:
        src, word, *rest = parts

    phrase = f"Do {(langs[src].lower())} {italic(word)}"
    if transcr := data["transcr"]:
        phrase += f" ({italic(transcr)})"
    if rest:
        if transcr := rest.pop(0):
            phrase += f" ({italic(transcr)})"
    if trad := data["trad"]:
        phrase += f" “{trad}”"
    if implicit_transcr := data["4"]:
        phrase += f" ({italic(implicit_transcr)})"
    if implicit_trad := data["5"]:
        phrase += f" “{implicit_trad}”"
    if rest:
        phrase += f" “{rest.pop(0)}”"
    if not data.get("ponto", ""):
        phrase += "."
    return phrase


def render_étimo(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_étimo("étimo", ["la", "canem"], defaultdict(str))
    '<i>canem</i>'
    >>> render_étimo("étimo", ["la", "canem", "canum"], defaultdict(str))
    '<i>canum</i>'
    >>> render_étimo("étimo", ["la", "canem", "canum", "canos"], defaultdict(str))
    '<i>canum</i>'
    >>> render_étimo("étimo", ["la", "abūsus"], defaultdict(str, { "sign": "abuso"}))
    '<i>abūsus</i> (“abuso”)'
    >>> render_étimo("étimo", ["grc", "ἄντρον"], defaultdict(str, {"transl": "ánton", "sign": "caverna"}))
    '<i>ἄντρον</i> <i>(ánton)</i> (“caverna”)'
    """
    parts.pop(0)  # Remove the lang
    phrase = italic(parts[1 if len(parts) >= 2 else 0])
    if data["transl"]:
        phrase += " " + italic(f"({data['transl']})")
    if data["sign"]:
        phrase += f" (“{data['sign']}”)"
    return phrase


def render_étimo_junção(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_étimo_junção("étimo junção", ["a-", "canela", "-ar"], defaultdict(str))
    'De <i>a-</i> + <i>canela</i> + <i>-ar</i>.'
    >>> render_étimo_junção("étimo junção", ["a-", "canela", "-ar"], defaultdict(str, {"ponto": "não"}))
    'De <i>a-</i> + <i>canela</i> + <i>-ar</i>'
    >>> render_étimo_junção("étimo junção", ["palavra1", "palavra2", "言葉３"], defaultdict(str, {"r1": "problemát(ico)", "tr2": '"tradução da palavra2"', "tr3": "kotoba3"}))
    'De <i>problemát(ico)</i> + <i>palavra2</i> (<i>"tradução da palavra2"</i>) + <i>言葉３</i> (<i>kotoba3</i>).'
    """
    result: list[str] = []
    for idx, part in enumerate(parts, 1):
        text = italic(data[f"r{idx}"] or part)
        if trans := data[f"tr{idx}"]:
            text += f" ({italic(trans)})"
        result.append(text)
    return f"De {concat(result, sep=' + ')}{'' if data['ponto'] == 'não' else '.'}"


def render_gramática(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_gramática("gramática", ["m", "incont", "c", "comp", "concr"], defaultdict(str))
    '<i>masculino</i>, <i>incontável</i>, <i>comum</i>, <i>composto</i>, <i>concreto</i>'
    >>> render_gramática("gramática", ["?"], defaultdict(str))
    '<small>gênero em falta</small>'
    >>> render_gramática("gramática", ["mp", "card", "pr", "sim", "abstr"], defaultdict(str))
    '<i>masculino plural</i>, <i>cardinal</i>, <i>próprio</i>, <i>simples</i>, <i>abstrato</i>'
    """
    from .gramatica import gramatica_short

    result = []
    for p in parts:
        if full := gramatica_short.get(p, ""):
            if p == "?":
                result.append(small(full))
            else:
                result.append(italic(full))
    return concat(result, ", ")


def render_o_or_a(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_o_or_a("o/a", ["determinad"], defaultdict(str))
    'determinada'
    >>> render_o_or_a("o/a", ["funç", "ões", "ão"], defaultdict(str))
    'funções'
    >>> render_o_or_a("o/a", ["trabalha", "ndo", "r"], defaultdict(str))
    'trabalhando'
    """
    phrase = parts.pop(0)
    phrase += parts[0] if parts else "a"
    return phrase


def render_pbpe_pepb(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_pbpe_pepb("PBPE", ["estafe", "stafe"], defaultdict(str))
    'estafe <sup>(português do Brasil)</sup> ou stafe <sup>(português europeu)</sup>'
    >>> render_pbpe_pepb("PBPE", ["estafe", "stafe"], defaultdict(str, {"inline": "1"}))
    'estafe <sup>(português do Brasil)</sup> ou stafe <sup>(português europeu)</sup>'
    >>> render_pbpe_pepb("PEPB", [], defaultdict(str, {"1": "Autoridade Nacional Palestiniana", "2": "Autoridade Nacional Palestina"}))
    'Autoridade Nacional Palestiniana <sup>(português europeu)</sup> ou Autoridade Nacional Palestina <sup>(português do Brasil)</sup>'
    >>> render_pbpe_pepb("PEPB", ["autocarro", "ônibus"], defaultdict(str))
    'autocarro <sup>(português europeu)</sup> ou ônibus <sup>(português do Brasil)</sup>'
    >>> render_pbpe_pepb("PEPB", ["atómico", "atômico"], defaultdict(str, {"inline": "1"}))
    'atómico/atômico'
    """
    part1 = data["1"] or parts.pop(0)
    part2 = data["2"] or parts.pop(0)
    cmpl1 = "<sup>(português europeu)</sup>"
    cmpl2 = "<sup>(português do Brasil)</sup>"
    if tpl == "PBPE":
        cmpl1, cmpl2 = cmpl2, cmpl1
    elif data["inline"] == "1":
        return f"{part1}/{part2}"
    return f"{part1} {cmpl1} ou {part2} {cmpl2}"


def render_plural(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_plural("p", [], defaultdict(str))
    '<i>plural</i>'
    >>> render_plural("p", ["forma no plural"], defaultdict(str))
    '(<i>plural:</i> <b>forma no plural</b>)'
    >>> render_plural("p", ["plural em letras não romanas", "transliteração"], defaultdict(str))
    '(<i>plural:</i> <b>plural em letras não romanas</b>, <i>transliteração</i>)'
    >>> render_plural("p", ["forma no plural"], defaultdict(str, {"p2": "forma no plural alternativa 1", "p3": "forma no plural alternativa 2"}))
    '(<i>plural:</i> <b>forma no plural</b>, <b>forma no plural alternativa 1</b>, <b>forma no plural alternativa 2</b>)'
    """
    if not parts and not data:
        return italic("plural")
    phrase = f"{italic('plural:')} {strong(parts.pop(0))}"
    if parts:
        phrase += f", {italic(parts.pop(0))}"
    for n in range(2, 4):
        idx = f"p{n}"
        if pn := data[idx]:
            phrase += f", {strong(pn)}"
    return parenthesis(phrase)


def render_plus_info(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_plus_info("+info", [], defaultdict(str, {"data": "1871"}))
    '<small>( <i>Datação</i>: 1871; )</small>'
    >>> render_plus_info("+info", [], defaultdict(str, {"uso": "1871"}))
    '<small>( <i>Uso</i>: 1871 )</small>'
    """
    phrase = italic("Datação" if data["data"] else "Uso")
    phrase += f": {data['data'] or data['uso']}"
    if data["data"]:
        phrase += ";"
    return small(f"( {phrase} )")


def render_trad(tpl: str, parts: list[str], data: defaultdict[str, str], word: str = "") -> str:
    """
    >>> render_trad("trad", ["fr", "surpris"], defaultdict(str))
    'Francês&nbsp;: surpris'
    >>> render_trad("trad", ["de", "Apfelsine", "Orange"], defaultdict(str))
    'Alemão: Apfelsine, Orange'
    >>> render_trad("trad", ["crh", "şorba"], defaultdict(str))
    'Tártaro Da Crimeia: şorba'
    """
    trad = parts.pop(0)
    phrase = langs[trad].title()
    phrase += "&nbsp;: " if trad == "fr" else ": "
    phrase += concat(parts, sep=", ")
    return phrase


template_mapping = {
    "+info": render_plus_info,
    "escopo": render_escopo,
    "etimo": render_etimo,
    "etimo2": render_etimo2,
    "étimo": render_étimo,
    "étimo junção": render_étimo_junção,
    "g": render_gramática,
    "gramática": render_gramática,
    "llietimo": render_etimo2,
    "o/a": render_o_or_a,
    "p": render_plural,
    "PBPE": render_pbpe_pepb,
    "PEPB": render_pbpe_pepb,
    "trad": render_trad,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
