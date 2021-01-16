from typing import Tuple, Dict, List
from collections import defaultdict  # noqa
from .langs import langs
from ...user_functions import (
    capitalize,
    concat,
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
    >>> render_etimologia("etimología", ["compuesto", "regio", "monte", "-ano"], defaultdict(str))
    'Compuesto de <i>regio</i>, <i>monte</i> y <i>-ano</i>'
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
    >>> render_etimologia("etimología", ["la", "piscis", "pez"], defaultdict(str))
    'Del latín <i>piscis</i> ("pez")'
    >>> render_etimologia("etimología", ["la", "-aceus"], defaultdict(str, {"alt":"-acĕus"}))
    'Del latín <i>-acĕus</i>'
    >>> render_etimologia("etimología", ["la", "illos"], defaultdict(str, {"diacrítico":"illōs", "sig":"no"}))
    'Del latín <i>illōs</i>'
    >>> render_etimologia("etimología", ["osp", "fasta"], defaultdict(str))
    'Del castellano antiguo <i>fasta</i>'
    >>> render_etimologia("etimología", ["grc", "ἄκανθα", "espina", "grc","πτερύγιον", "aleta"], defaultdict(str, {"tr":"akntha", "tr2": "pterúgion"}))
    'Del griego antiguo <i>ἄκανθα</i> (<i>akntha</i>, "espina") y <i>πτερύγιον</i> (<i>pterúgion</i>, "aleta")'
    >>> render_etimologia("etimología", ["osp", "foja", "", "osp","foia"], defaultdict(str))
    'Del castellano antiguo <i>foja</i> y <i>foia</i>'
    >>> render_etimologia("etimología", ["osp", "foja", "", "la","sed"], defaultdict(str))
    'Del castellano antiguo <i>foja</i> y el latín <i>sed</i>'
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
    >>> render_etimologia("etimología", ["sufijo", "espumar", "ero"], defaultdict(str, {"alt":"espumado", "alt2":"era"}))
    'De <i>espumado</i> y el sufijo <i>-era</i>'
    >>> render_etimologia("etimología", ["prefijo", "a", "contecer"], defaultdict(str))
    'Del prefijo <i>a-</i> y <i>contecer</i>'
    >>> render_etimologia("etimología", ["incierta"], defaultdict(str))
    'Incierta'
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
        phrase += concat(list(map(italic, parts)), ", ", f" {glue} ")
    elif cat == "confijo":
        phrase = f"Del prefijo {italic(parts.pop(0) + '-')}"
        for part in parts[:-1].copy():
            phrase += f", {italic(parts.pop(0))}"
        phrase += f" y el sufijo {italic(suffix + parts[0])}"
    elif cat == "epónimo":
        phrase = "Epónimo"
        if parts:
            phrase += f" {parts[-1]}"
    elif cat == "incierta":
        return "Incierta"
    elif cat == "femenino":
        phrase = (
            f"De {italic(parts[0])} y el sufijo flexivo {italic('-a')} para el femenino"
        )
    elif cat == "fonética":
        phrase = f"Por alteración fonética de {italic(parts[0])}"
    elif cat == "plural":
        plural = "-s" if len(parts) == 1 else parts[-1]
        phrase = f"De {italic(parts[0])} y el sufijo flexivo {italic(plural)}"
    elif cat == "prefijo":
        phrase = f"Del prefijo {italic(parts.pop(0) + '-')}"
        if parts:
            phrase += f" {glue}"
            phrase += f" {italic(parts.pop(0))}"
    elif cat == "pronominal":
        phrase = f"De {italic(parts[0])}, con el pronombre reflexivo átono"
    elif cat == "sufijo":
        sens = data.get("tr", "")
        word = data["alt"] or data["diacrítico"] or (parts[0] if parts else "")
        word2 = (
            data["alt2"] or data["diacrítico2"] or (parts[1] if len(parts) > 1 else "")
        )
        more = f" ({italic(sens)})" if sens else ""
        phrase = f"De {italic(word)}{more} y el sufijo {italic(suffix + word2)}"
    elif cat in langs:
        phrase = f"Del {langs[cat]} {italic(word)}"
        tr = data["tr"] or data["transcripción"]
        local_phrase = []
        if tr:
            local_phrase.append(italic(tr))
        if len(parts) > 1 and parts[1]:
            local_phrase.append(f'"{parts[1]}"')
        if local_phrase:
            phrase += f' ({concat(local_phrase, ", ")})'

        if len(parts) > 3 and parts[2] in langs:
            phrase += " y"
            lang2 = parts[2]
            if lang2 != cat:
                phrase += f" el {langs[lang2]}"
            phrase += f" {italic(parts[3])}"
            tr2 = data["tr2"] or data["transcripción2"]
            local_phrase = []
            if tr2:
                local_phrase.append(italic(tr2))
            if len(parts) > 4 and parts[4]:
                local_phrase.append(f'"{parts[4]}"')
            if local_phrase:
                phrase += f' ({concat(local_phrase, ", ")})'
    else:
        phrase = f"Del {cat} {italic(word)}" if cat else ""
        sens = data["transcripción"]
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
