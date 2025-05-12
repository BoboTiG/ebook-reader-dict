from collections import defaultdict

from ...user_functions import (
    concat,
    extract_keywords_from,
    italic,
)
from .langs import langs


def render_avledet(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_avledet("avledet", ["gml", "no", "abbedie"], defaultdict(str))
    'middelnedertysk <i>abbedie</i>'
    >>> render_avledet("avledet", ["middelalderlatin", "no", "abbatia"], defaultdict(str))
    'middelalderlatin <i>abbatia</i>'
    >>> render_avledet("avledet", ["la", "no", "approbatio", "", "godkjennelse"], defaultdict(str))
    'latin <i>approbatio</i> («godkjennelse»)'
    >>> render_avledet("avledet", ["la", "no", "Februarius", "Februārius"], defaultdict(str))
    'latin <i>Februārius</i>'
    >>> render_avledet("avledet", ["grc", "no", "σχηματικός", "", "som hører til månefaser"], defaultdict(str, {"tr":"skhematikos"}))
    'gammelgresk σχηματικός (<i>skhematikos</i>, «som hører til månefaser»)'
    """
    in_parenthesis = []
    if tr := data["tr"]:
        in_parenthesis.append(italic(tr))
    if len(parts) > 4:
        in_parenthesis.append(f"«{parts[4]}»")

    phrase = f"{langs.get(parts[0], parts[0])} "
    trad = parts[3] if len(parts) > 3 and parts[3] else parts[2]
    phrase += trad if tr else italic(trad)
    if in_parenthesis:
        phrase += f" ({', '.join(in_parenthesis)})"
    return phrase


def render_lant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_lant("lånt", ["en", "no", "latte"], defaultdict(str))
    'engelsk <i>latte</i>'
    >>> render_lant("lånt", ["it", "no", "caffè", "", "kaffe"], defaultdict(str))
    'italiensk <i>caffè</i> («kaffe»)'
    >>> render_lant("overslån", ["en", "no", "quality of life"], defaultdict(str))
    'engelsk <i>quality of life</i>'
    >>> render_lant("overslån", ["en", "no", "virgin oil", "virgin", "oil"], {"t1": "jomfru", "t2": "olje"})
    'engelsk <i>virgin oil</i>, <i>virgin</i> («jomfru») + <i>oil</i> («olje»)'
    """
    phrase = f"{langs[parts[0]]} {italic(parts[2])}"
    if rest := parts[3:]:
        if not rest[0]:
            phrase += f" («{rest[1]}»)"
        else:
            phrase += ", "
            for idx, part in enumerate(rest, 1):
                phrase += italic(part)
                if trad := data[f"t{idx}"]:
                    phrase += f" («{trad}»)"
                if part != parts[-1]:
                    phrase += " + "

    return phrase


def render_sammensetning(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_sammensetning("sammensetning", ["bonde", "vett"], defaultdict(str))
    '<i>bonde</i> + <i>vett</i>'
    >>> render_sammensetning("sammensetning", ["arv", "-e-", "-løs"], defaultdict(str))
    '<i>arv</i> + <i>-e-</i> + <i>-løs</i>'
    >>> render_sammensetning("sammensetning", ["Achter", "Bahn"], {"tr1": "åtter", "tr2": "bane"})
    '<i>Achter</i> («åtter») + <i>Bahn</i> («bane»)'
    """
    phrase_parts = []
    for i, part in enumerate(parts, start=1):
        trindex = f"tr{i}"
        tr = data[trindex]
        phrase_parts.append(f"{italic(part)}" + (f" («{tr}»)" if tr else ""))
    return concat(phrase_parts, " + ")


def render_term(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_term("term", ["ord"], defaultdict(str))
    '<i>ord</i>'
    >>> render_term("term", ["verbo", "verbō"], defaultdict(str))
    '<i>verbō</i>'
    >>> render_term("term", ["verbo", "verbō", "for ordet"], defaultdict(str))
    '<i>verbō</i> («for ordet»)'
    >>> render_term("term", ["ord", "", "taleenhet"], defaultdict(str))
    '<i>ord</i> («taleenhet»)'
    >>> render_term("term", ["λόγος"], defaultdict(str, {"sc": "Grek", "tr": "lógos"}))
    'λόγος (<i>lógos</i>)'
    >>> render_term("term", ["λόγος", "", "ord"], defaultdict(str, {"sc": "Grek", "tr": "lógos"}))
    'λόγος (<i>lógos</i>, «ord»)'
    >>> render_term("term", ["mot"], defaultdict(str, {"språk": "fr"}))
    '<i>mot</i>'
    >>> render_term("term", ["ord#Verb", "word"], defaultdict(str))
    '<i>word</i>'
    """
    phrase = ""
    term = parts[1] if len(parts) > 1 else ""
    term = term or parts[0]
    phrase = term if data["sc"] else italic(term)

    meaning = parts[2] if len(parts) > 2 else ""
    meaning = f"«{meaning}»" if meaning else ""

    tr = data["tr"]
    tr = italic(tr) if tr else ""

    end_phrase = concat([tr, meaning], ", ")

    phrase += f" ({end_phrase})" if end_phrase else ""

    return phrase


def render_ursprak(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_ursprak("proto", ["indoeuropeisk", "klek-", "", "kleg-", "å rope/skrike"], defaultdict(str))
    'urindoeuropeisk *klek-, *kleg- («å rope/skrike»)'
    >>> render_ursprak("urspråk", ["indoeuropeisk", "rei-", "stripete, flekkete"], defaultdict(str))
    'urindoeuropeisk *rei- («stripete, flekkete»)'
    """
    lang = parts.pop(0)
    phrase = data["tittel"] or f"ur{lang}"
    while parts:
        term = parts.pop(0)
        meaning = parts.pop(0) if parts else ""
        phrase += f" *{term}" if term else ""
        phrase += f" («{meaning}»)" if meaning else ""
        if parts:
            phrase += ","

    return phrase


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_variant("bøyingsform", ["no", "verb", "uttrykke"], defaultdict(str))
    'uttrykke'
    >>> render_variant("no-adj-bøyningsform", ["b", "vis"], defaultdict(str, {"nb": "ja", "nrm": "ja", "nn": "ja"}))
    'vis'
    """
    return parts[-1]


template_mapping = {
    "avledet": render_avledet,
    "lånt": render_lant,
    "overslån": render_lant,
    "proto": render_ursprak,
    "sammensetning": render_sammensetning,
    "Sammensatt": render_sammensetning,
    "term": render_term,
    "urspråk": render_ursprak,
    #
    # Variants
    #
    "__variant__bøyingsform": render_variant,
    "__variant__no-adj-bøyningsform": render_variant,
    "__variant__no-sub-bøyningsform": render_variant,
    "__variant__no-verb-bøyningsform": render_variant,
    "__variant__no-verbform av": render_variant,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
