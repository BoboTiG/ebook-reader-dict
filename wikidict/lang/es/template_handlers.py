from typing import Tuple, Dict, List
from collections import defaultdict  # noqa
from .langs import langs
from ...user_functions import (
    capitalize,
    extract_keywords_from,
    italic,
)


def render_variante(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_variante("variante", ["atiesar"], defaultdict(str))
    '<i>Variante de</i> atiesar'
    >>> render_variante("variante", ["diezmo"], defaultdict(str, {"texto":"Variante anticuada de"}))
    '<i>Variante anticuada de</i> diezmo'
    """
    sentence = data["texto"] or "variante de"
    return f"{italic(capitalize(sentence))} {parts[0]}"


def render_etimologia(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_etimologia("etimología", [], defaultdict(str))
    ''
    >>> render_etimologia("etimología", [""], defaultdict(str))
    ''
    >>> render_etimologia("etimología", ["compuesto", "sacar", "punta"], defaultdict(str))
    'Compuesto de <i>sacar</i> y <i>punta</i>'
    >>> render_etimologia("etimología", ["compuesto", "-ónimo", "-iae"], defaultdict(str, {"e":"e"}))
    'Compuesto de <i>-ónimo</i> e <i>-iae</i>'
    >>> render_etimologia("etimología", ["confijo", "anglo", "filo"], defaultdict(str, {"tilde":"sí"}))
    'Del prefijo <i>anglo-</i> y el sufijo <i>-́filo</i>'
    >>> render_etimologia("etimología", ["confijo", "des", "garra", "ar"], defaultdict(str))
    'Del prefijo <i>des-</i>, <i>garra</i> y el sufijo <i>-ar</i>'
    >>> render_etimologia("etimología", ["epónimo"], defaultdict(str))
    'Epónimo'
    >>> render_etimologia("etimología", ["epónimo", "de Adelita, protagonista de un corrido mexicano"], defaultdict(str))
    'Epónimo de Adelita, protagonista de un corrido mexicano'
    >>> render_etimologia("etimología", ["femenino", "topógrafo"], defaultdict(str))
    'De <i>topógrafo</i> y el sufijo flexivo <i>-a</i> para el femenino'
    >>> render_etimologia("etimología", ["fonética", "empeller"], defaultdict(str))
    'Por alteración fonética de <i>empeller</i>'
    >>> render_etimologia("etimología", ["japonés", "片仮名"], defaultdict(str, {"transcripción":"カタカナ, katakana"}))
    'Del japonés <i>片仮名</i> (<i>カタカナ, katakana</i>)'
    >>> render_etimologia("etimología", ["la", "incertus"], defaultdict(str))
    'Del latín <i>incertus</i>'
    >>> render_etimologia("etimología", ["la", "-aceus"], defaultdict(str, {"alt":"-acĕus"}))
    'Del latín <i>-acĕus</i>'
    >>> render_etimologia("etimología", ["la", "illos"], defaultdict(str, {"diacrítico":"illōs", "sig":"no"}))
    'Del latín <i>illōs</i>'
    >>> render_etimologia("etimología", ["osp", "fasta"], defaultdict(str))
    'Del castellano antiguo <i>fasta</i>'
    >>> render_etimologia("etimología", ["plural", "vista"], defaultdict(str))
    'De <i>vista</i> y el sufijo flexivo <i>-s</i>'
    >>> render_etimologia("etimología", ["plural", "vacación", "-es"], defaultdict(str))
    'De <i>vacación</i> y el sufijo flexivo <i>-es</i>'
    >>> render_etimologia("etimología", ["pronominal", "agrupar"], defaultdict(str))
    'De <i>agrupar</i>, con el pronombre reflexivo átono'
    >>> render_etimologia("etimología", ["sánscrito", "गुरू", "maestro"], defaultdict(str, {"transcripción":"gūru"}))
    'Del sánscrito <i>गुरू</i> (<i>gūru</i>, "maestro")'
    >>> render_etimologia("etimología", ["sufijo", "átomo", "ico"], defaultdict(str))
    'De <i>átomo</i> y el sufijo <i>-ico</i>'
    >>> render_etimologia("etimología", ["sufijo", "átomo", "ico"], defaultdict(str))
    'De <i>átomo</i> y el sufijo <i>-ico</i>'
    >>> render_etimologia("etimología", ["sufijo", "ferrojo", "ar"], defaultdict(str, {"tr":"anticuado por cerrojo e influido por fierro"}))
    'De <i>ferrojo</i> (<i>anticuado por cerrojo e influido por fierro</i>) y el sufijo <i>-ar</i>'
    """  # noqa
    if not parts:
        return ""

    glue = data.get("e", "y")
    suffix = "-́" if data.get("tilde", "") == "sí" else "-"
    word = data.get(
        "alt", data.get("diacrítico", parts[1] if len(parts) > 1 else parts[-1])
    )

    cat = parts.pop(0)
    if cat == "compuesto":
        phrase = "Compuesto de "
        phrase += f" {glue} ".join(map(italic, parts))
    elif cat == "confijo":
        phrase = f"Del prefijo {italic(parts.pop(0) + '-')}"
        for part in parts[:-1].copy():
            phrase += f", {italic(parts.pop(0))}"
        phrase += f" y el sufijo {italic(suffix + parts[0])}"
    elif cat == "epónimo":
        phrase = "Epónimo"
        if parts:
            phrase += f" {parts[-1]}"
    elif cat == "femenino":
        phrase = (
            f"De {italic(parts[0])} y el sufijo flexivo {italic('-a')} para el femenino"
        )
    elif cat == "fonética":
        phrase = f"Por alteración fonética de {italic(parts[0])}"
    elif cat == "plural":
        plural = "-s" if len(parts) == 1 else parts[-1]
        phrase = f"De {italic(parts[0])} y el sufijo flexivo {italic(plural)}"
    elif cat == "pronominal":
        phrase = f"De {italic(parts[0])}, con el pronombre reflexivo átono"
    elif cat == "sufijo":
        sens = data.get("tr", "")
        more = f" ({italic(sens)})" if sens else ""
        phrase = f"De {italic(parts[0])}{more} y el sufijo {italic(suffix + parts[1])}"
    elif cat in langs:
        phrase = f"Del {langs[cat]} {italic(word)}"
    else:
        phrase = f"Del {cat} {italic(word)}" if cat else ""
        sens = data.get("transcripción", "")
        if sens or len(parts) > 1:
            phrase += f" ({italic(sens)}"
            if len(parts) > 1:
                phrase += f', "{parts[1]}"'
            phrase += ")"

    return phrase


def render_l_plus(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_l_plus("l+", ["la", "impello", "impellō, impellere"], defaultdict(str, {"glosa":"empujar"}))
    '<i>impellō, impellere</i> ("empujar")'
    >>> render_l_plus("l+", ["grc", "ἀράχνη"], defaultdict(str, {"tr":"aráchnē", "glosa":"araña"}))
    'ἀράχνη (<i>aráchnē</i>, "araña")'
    >>> render_l_plus("l+", ["ar", "حتى"], defaultdict(str, {"tr":"ḥatta"}))
    'حتى (<i>ḥatta</i>)'
    """
    trans = data.get("tr", "")
    glosa = data.get("glosa", "")
    phrase = parts[-1] if trans else italic(parts[-1])
    if trans or glosa:
        phrase += " ("
        if trans:
            phrase += f"{italic(trans)}"
        if glosa:
            if trans:
                phrase += ", "
            phrase += f'"{glosa}"'
        phrase += ")"

    return phrase


template_mapping = {
    "etimología": render_etimologia,
    "l+": render_l_plus,
    "variante": render_variante,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
