from collections import defaultdict  # noqa
from typing import Dict, List, Tuple

from ...user_functions import (
    concat,
    extract_keywords_from,
    italic,
)
from .langs import langs


def render_lant(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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


def render_term(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
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
    term = ""
    phrase = ""
    if len(parts) > 1:
        term = parts[1]
    term = term or parts[0]
    phrase = term if data["sc"] else italic(term)

    meaning = parts[2] if len(parts) > 2 else ""
    meaning = f"«{meaning}»" if meaning else ""

    tr = data["tr"]
    tr = italic(tr) if tr else ""

    end_phrase = concat([tr, meaning], ", ")

    phrase += f" ({end_phrase})" if end_phrase else ""

    return phrase


template_mapping = {
    "term": render_term,
    "lånt": render_lant,
    "overslån": render_lant,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
