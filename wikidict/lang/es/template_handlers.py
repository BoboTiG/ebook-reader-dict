from typing import Tuple, Dict, List
from collections import defaultdict  # noqa
from .langs import langs, lang_to_normalize
from ...user_functions import (
    capitalize,
    concat,
    extract_keywords_from,
    italic,
    subscript,
)


def normalizar_nombre(to_normalize: str) -> str:
    """
    >>> normalizar_nombre("latin")
    'latín'
    >>> normalizar_nombre("en")
    'inglés'
    >>> normalizar_nombre("")
    ''
    """
    if not to_normalize:
        return ""
    lcfirst_norm = to_normalize[0].lower() + to_normalize[1:]
    return lang_to_normalize.get(lcfirst_norm, langs.get(lcfirst_norm, lcfirst_norm))


def render_adjetivo_de_verbo(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_adjetivo_de_verbo("adjetivo de verbo", ["gorjear", "gorjea"], defaultdict(str))
    'Que gorjea'
    >>> render_adjetivo_de_verbo("adjetivo de verbo", ["gorjear", "gorjea","unificar", "unifica"], defaultdict(str))
    'Que gorjea o que unifica'
    """
    result = ""
    if len(parts) > 1:
        result += f"Que {parts[1]}"
    if len(parts) > 3:
        result += f" o que {parts[3]}"
    return result


def render_aumentativo(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_aumentativo("aumentativo", ["perro"], defaultdict(str))
    '<i>Aumentativo de</i> perro'
    >>> render_aumentativo("aumentativo", ["azada"], defaultdict(str, {"tipo" : "sustantivo"}))
    '<i>Aumentativo del sustantivo</i> azada'
    >>> render_aumentativo("aumentativo", ["perro"], defaultdict(str, {"i": "x", "tipo" : "sustantivo"}))
    '<i>Aumentativo irregular del sustantivo</i> perro'
    """
    start = "Aumentativo "
    if data["irregular"] or data["irreg"] or data["irr"] or data["i"]:
        start += "irregular "
    start += "de"
    if data["tipo"]:
        start += f"l {data['tipo']}"
    phrase = f"{italic(start)}"
    phrase += f" {render_l('l', [data['alt'] or parts[0]], data)}"
    return phrase


def render_adverbio_de_adjetivo(
    tpl: str, parts: List[str], data: Dict[str, str]
) -> str:
    """
    >>> render_adverbio_de_adjetivo("adverbio_de_adjetivo", ["accidental"], defaultdict(str))
    'De un modo accidental'
    >>> render_adverbio_de_adjetivo("adverbio_de_adjetivo", ["completo", "pleno"], defaultdict(str))
    'De un modo completo o pleno'
    >>> render_adverbio_de_adjetivo("adverbio_de_adjetivo", ["completo", "pleno", "total"], defaultdict(str))
    'De un modo completo, pleno o total'
    """
    result = ""
    if parts:
        result += "De un modo "
    result += concat(parts, ", ", " o ")
    return result


def render_adverbio_de_sustantivo(
    tpl: str, parts: List[str], data: Dict[str, str]
) -> str:
    """
    >>> render_adverbio_de_sustantivo("adverbio de sustantivo", ["escabrosidad"], defaultdict(str))
    'Con escabrosidad'
    """
    result = ""
    if parts:
        result += "Con "
    result += concat(parts, ", ", " o ")
    return result


def render_comparativo(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_comparativo("comparativo", ["bueno", "es"], defaultdict(str, {"irr": "s"}))
    '<i>Comparativo irregular de</i> bueno'
    >>> render_comparativo("comparativo", ["bueno", "es"], defaultdict(str, {"tipo": "regular"}))
    '<i>Comparativo regular de</i> bueno'
    """
    word = parts[0] if parts else ""
    start = "Comparativo"
    if data["tipo"]:
        start += f' {data["tipo"]}'
    if data["i"] or data["irr"] or data["irreg"] or data["irregular"]:
        start += " irregular"
    start += " de"
    phrase = f"{italic(start)} "
    phrase += render_l("l", [data["alt"] or word], data)
    return phrase


def render_etim(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_etim("etim", ["la", "folia"], defaultdict(str))
    'del latín <i>folia</i>'
    >>> render_etim("etim", ["grc", "φάσηλος"], defaultdict(str, {"tr": "phásēlos"}))
    'del griego antiguo <i>φάσηλος</i> (<i>phásēlos</i>)'
    >>> render_etim("etim", ["ar", "كنية"], defaultdict(str, {"tr": "kunyah", "glosa":"sobrenombre", "glosa-alt": "sobrenombre honorífico"}))
    'del árabe <i>كنية</i> (<i>kunyah</i>, "sobrenombre honorífico")'
    >>> render_etim("etim", ["grc", "ἱδρώς", "sudor"], defaultdict(str))
    'del griego antiguo <i>ἱδρώς</i> ("sudor")'
    """  # noqa
    result = f"del {normalizar_nombre(parts[0])}"
    lplus = render_l(
        "l+",
        [
            data["diacrítico"] or data["alt"] or (parts[1] if len(parts) > 1 else ""),
        ],
        defaultdict(
            str,
            {
                "glosa": data["glosa"] or (parts[2] if len(parts) > 2 else ""),
                "glosa-alt": data["glosa-alt"],
                "núm": data["núm"] or data["num"],
                "tr": data["tr"] or data["transcripción"],
            },
        ),
    )
    if lplus:
        result += f" {lplus}"
    return result


def render_etimologia(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_etimologia("etimología", [], defaultdict(str))
    ''
    >>> render_etimologia("etimología", [""], defaultdict(str))
    ''
    >>> render_etimologia("etimología", ["apócope", "Natalia"], defaultdict(str))
    'Acortamiento de <i>Natalia</i>'
    >>> render_etimologia("etimología", ["calco", "en", "plastiglomerate"], defaultdict(str, {"por": "por"}))
    'por calco del inglés <i>plastiglomerate</i>'
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
    >>> render_etimologia("etimología", ["confijo", "en", "furia", "ecer"], defaultdict(str, {"tr2":"ira, cólera"}))
    'Del prefijo <i>en-</i>, <i>furia</i> (<i>ira, cólera</i>) y el sufijo <i>-ecer</i>'
    >>> render_etimologia("etimología", ["epónimo"], defaultdict(str))
    'Epónimo'
    >>> render_etimologia("etimología", ["epónimo", "de Adelita, protagonista de un corrido mexicano"], defaultdict(str))
    'Epónimo de Adelita, protagonista de un corrido mexicano'
    >>> render_etimologia("etimología", ["femenino", "topógrafo"], defaultdict(str))
    'De <i>topógrafo</i> y el sufijo flexivo <i>-a</i> para el femenino'
    >>> render_etimologia("etimología", ["femenino", "Jesús", "a"], defaultdict(str))
    'De <i>Jesús</i> y el sufijo flexivo <i>a</i> para el femenino'
    >>> render_etimologia("etimología", ["metátesis", "rigoroso"], defaultdict(str))
    'Por metátesis de <i>rigoroso</i>'
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
    >>> render_etimologia("etimología", ["latin", "villus", "vello"], defaultdict(str))
    'Del latín <i>villus</i> ("vello")'
    >>> render_etimologia("etimología", ["latin", "villus", "vello", ""], defaultdict(str))
    'Del latín <i>villus</i> ("vello")'
    >>> render_etimologia("etimología", ["bajo latín", "capitanus", "principal"], defaultdict(str))
    'Del bajo latín <i>capitanus</i> ("principal")'
    >>> render_etimologia("etimología", ["osp", "fasta"], defaultdict(str))
    'Del castellano antiguo <i>fasta</i>'
    >>> render_etimologia("etimología", ["grc", "ἄκανθα", "espina", "grc","πτερύγιον", "aleta"], defaultdict(str, {"tr":"akntha", "tr2": "pterúgion"}))
    'Del griego antiguo <i>ἄκανθα</i> (<i>akntha</i>, "espina") y <i>πτερύγιον</i> (<i>pterúgion</i>, "aleta")'
    >>> render_etimologia("etimología", ["osp", "foja", "", "osp","foia"], defaultdict(str))
    'Del castellano antiguo <i>foja</i> y <i>foia</i>'
    >>> render_etimologia("etimología", ["osp", "foja", "", "la","sed"], defaultdict(str))
    'Del castellano antiguo <i>foja</i> y el latín <i>sed</i>'
    >>> render_etimologia("etimología", ["rmq", "lumí", "concubina"], defaultdict(str, {"glosa-alt":"concubina, manceba, querida"}))
    'Del caló <i>lumí</i> ("concubina, manceba, querida")'
    >>> render_etimologia("etimología", ["ONOM"], defaultdict(str))
    'Onomatopéyica'
    >>> render_etimologia("etimología", ["plural", "vista"], defaultdict(str))
    'De <i>vista</i> y el sufijo flexivo <i>-s</i>'
    >>> render_etimologia("etimología", ["plural", "vacación", "-es"], defaultdict(str))
    'De <i>vacación</i> y el sufijo flexivo <i>-es</i>'
    >>> render_etimologia("etimología", ["pronominal", "agrupar"], defaultdict(str))
    'De <i>agrupar</i>, con el pronombre reflexivo átono'
    >>> render_etimologia("etimología", ["pronominal", "espinar"], defaultdict(str, {"num": "1"}))
    'De <i>espinar<sub>1</sub></i>, con el pronombre reflexivo átono'
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
    >>> render_etimologia("etimología", ["sufijo", "héroe", "ficar"], defaultdict(str, {"tr2":"en su variante -ificar"}))
    'De <i>héroe</i> y el sufijo <i>-ficar</i> (<i>en su variante -ificar</i>)'
    >>> render_etimologia("etimología", ["sufijo", "bullicio", "ar"], defaultdict(str, {"glosa":"bullicio"}))
    'De <i>bullicio</i> ("bullicio") y el sufijo <i>-ar</i>'
    >>> render_etimologia("etimología", ["prefijo", "a", "contecer"], defaultdict(str))
    'Del prefijo <i>a-</i> y <i>contecer</i>'
    >>> render_etimologia("etimología", ["incierta"], defaultdict(str))
    'Incierta'
    """  # noqa

    def call_l_single_part(part: str, index: int) -> str:
        sindex = str(index) if index > 1 else ""
        return render_l(
            "l+",
            [
                data["diacrítico" + sindex] or data["alt" + sindex] or part,
            ],
            defaultdict(
                str,
                {
                    "glosa": data["glosa" + sindex],
                    "glosa-alt": data["glosa-alt" + sindex],
                    "núm": data["núm" + sindex] or data["num" + sindex],
                    "tr": data["tr" + sindex],
                },
            ),
        )

    if not parts:
        return ""

    glue = data.get("e", "y")
    suffix = "-́" if data.get("tilde", "") in ("sí", "s", "x") else "-"
    word = data.get(
        "alt", data.get("diacrítico", parts[1] if len(parts) > 1 else parts[-1])
    )

    cat = parts.pop(0)
    if cat in (
        "acortamiento",
        "apócope",
        "síncopa",
        "aféresis",
        "abreviación",
        "supresión",
        "acort",
        "ACORT",
    ):
        phrase = "Acortamiento"
        phrase += f" {data['nota']}" if data["nota"] else ""
        phrase += " de "
        phrase += call_l_single_part(parts[0], 1)
    elif cat in ("calco", "CALC"):
        phrase = (data["por"] or "Por") + " calco"
        phrase += f" {data['nota']}" if data["nota"] else ""
        phrase += " del "
        phrase += normalizar_nombre(parts[0])
        phrase += " "
        phrase += render_l(
            "l+",
            [
                data["diacrítico"]
                or data["alt"]
                or (parts[1] if len(parts) > 1 else ""),
            ],
            defaultdict(
                str,
                {
                    "glosa": data["glosa"] or (parts[2] if len(parts) > 2 else ""),
                    "glosa-alt": data["glosa-alt"],
                    "núm": data["núm"] or data["num"],
                    "tr": data["tr"] or data["transcripción"],
                },
            ),
        )

    elif cat in ("compuesto", "compuesta", "COMP"):
        phrase = capitalize(data["otro"] or "compuesto") + " de "
        phrase += concat(
            list(map(call_l_single_part, parts, range(1, len(parts) + 1))),
            ", ",
            f" {glue} ",
        )
    elif cat in ("confijo", "circunfijo", "CIRCUNF", "CONF"):
        texto_prefijo = data.get("texto-prefijo", "prefijo")
        phrase = f"Del {texto_prefijo} "
        part = parts.pop(0)
        phrase += render_l(
            "l+",
            [
                (data["diacrítico"] or data["alt"] or part) + "-",
            ],
            data,
        )
        for index, part in enumerate(parts[:-1], 2):
            localphrase = call_l_single_part(part, index)
            phrase += f", {localphrase}"
        phrase += f" y el sufijo {italic(suffix + parts[-1])}"
    elif cat == "epónimo":
        phrase = "Epónimo"
        if parts:
            phrase += f" {parts[-1]}"
    elif cat in ("incierta", "incierto", "INC"):
        return "Incierta"
    elif cat in ("femenino", "FEM"):
        data["alt"] = data["diacrítico"] or data["alt"] or parts[0]
        phrase1 = render_l("l+", [parts[0]], data)
        phrase2 = parts[1] if len(parts) > 1 else "-a"
        phrase = f"De {phrase1} y el sufijo flexivo {italic(phrase2)} para el femenino"
    elif cat in ("metátesis", "trasposición", "MET"):
        data["alt"] = data["diacrítico"] or data["alt"] or parts[0]
        phrase1 = render_l("l+", [parts[0]], data)
        phrase = f"Por metátesis de {phrase1}"
    elif cat in (
        "fonética",
        "alteración fonética",
        "adición",
        "epéntesis",
        "prótesis",
        "metaplasmo",
    ):
        nota = f" {data['nota']}" if data["nota"] else ""
        phrase = f"Por alteración fonética{nota} de {call_l_single_part(parts[0], 1)}"
    elif cat in ("onomatopeya", "onomatopéyico", "onomatopéyica", "ONOM"):
        phrase = "Onomatopéyica"
    elif cat == "plural":
        plural = "-s" if len(parts) == 1 else parts[-1]
        data["alt"] = data["diacrítico"] or data["alt"] or parts[0]
        phrase1 = render_l("l+", [parts[0]], data)
        phrase = f"De {phrase1} y el sufijo flexivo {italic(plural)}"
    elif cat in ("prefijo", "PREF"):
        texto_prefijo = data.get("texto-prefijo", "prefijo")
        phrase = f"Del {texto_prefijo} "
        part = parts.pop(0)
        phrase += render_l(
            "l+",
            [
                (data["diacrítico"] or data["alt"] or part) + "-",
            ],
            data,
        )
        if parts:
            phrase += f" {glue}"
            phrase += f" {call_l_single_part(parts.pop(0), 2)}"
    elif cat == "pronominal":
        data["alt"] = data["diacrítico"] or data["alt"] or parts[0]
        phrase1 = render_l("l+", [parts[0]], data)
        phrase = f"De {phrase1}, con el pronombre reflexivo átono"
    elif cat in ("sufijo", "SUF"):
        texto_sufijo = data.get("texto-sufijo", "sufijo")
        word = data["diacrítico"] or data["alt"] or (parts[0] if parts else "")
        word2 = (
            data["diacrítico2"] or data["alt2"] or (parts[1] if len(parts) > 1 else "")
        )
        phrase1 = render_l("l+", [word], data)
        phrase2 = render_l(
            "l+",
            [suffix + word2],
            defaultdict(
                str,
                {
                    "glosa": data["glosa2"],
                    "glosa-alt": data["glosa-alt2"],
                    "núm": data["núm2"] or data["num2"],
                    "tr": data["tr2"] or data["transcripción2"],
                },
            ),
        )
        phrase = f"De {phrase1} y el {texto_sufijo} {phrase2}"
    elif parts:
        phrase = f"Del {normalizar_nombre(cat)} " if cat else ""
        parts.insert(0, cat)
        phrase_array = []
        index = 0
        while parts:
            if not parts[0] and len(parts) == 1:
                break
            sindex = str(index + 1) if index != 0 else ""
            local_phrase = ""
            if index > 0:
                if parts[0] != cat:
                    local_phrase = f"el {normalizar_nombre(parts[0])} "
            local_phrase += render_l(
                "l+",
                [
                    data["diacrítico" + sindex]
                    or data["alt" + sindex]
                    or (parts[1] if len(parts) > 1 else ""),
                ],
                defaultdict(
                    str,
                    {
                        "glosa": data["glosa" + sindex]
                        or (parts[2] if (len(parts) > 2 and parts[2] != "-") else ""),
                        "glosa-alt": data["glosa-alt" + sindex],
                        "núm": data["núm" + sindex] or data["num" + sindex],
                        "tr": data["tr" + sindex] or data["transcripción" + sindex],
                    },
                ),
            )
            if local_phrase:
                phrase_array.append(local_phrase)
            for x in range(3):
                if parts:
                    parts.pop(0)
            index = index + 1

        if phrase_array:
            phrase += concat(phrase_array, ", ", f" {glue} ")

    else:
        phrase = ""

    return phrase


def render_forma(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_forma("forma", ["-acho", "Forma del femenino de"], defaultdict(str))
    '<i>Forma del femenino de</i> -acho'
    >>> render_forma("forma sustantivo", ["ala", "plural"], defaultdict(str))
    '<i>Forma del plural de</i> ala'
    """
    start = "forma de"
    if tpl == "forma":
        start = data["texto"] or (parts[1] if len(parts) > 1 else "forma de")
    elif tpl == "forma sustantivo":
        caso = data["caso"] or (parts[1] if len(parts) > 1 else "")
        numero = (
            data["número"] or data["numero"] or (parts[2] if len(parts) > 2 else "")
        )
        genero = (
            data["género"] or data["genero"] or (parts[3] if len(parts) > 3 else "")
        )
        start = f"Forma del {concat([caso, numero, genero], ' ')} de"
    return f"{italic(capitalize(start))} {parts[0]}"


def render_gentilicio2(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_gentilicio2("gentilicio2", ["Alemania"], defaultdict(str))
    'Persona originaria de Alemania'
    >>> render_gentilicio2("gentilicio2", ["pueblo guajiro"], defaultdict(str, {"contracción":"del"}))
    'Persona originaria del pueblo guajiro'
    """
    return f"Persona originaria {data['contracción'] or 'de'} {parts[0]}"


def render_grafia(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_grafia("grafía", ["psicológico"], defaultdict(str))
    '<i>Grafía alternativa de</i> psicológico'
    >>> render_grafia("grafía informal", ["al tiro"], defaultdict(str))
    '<i>Grafía informal de</i> al tiro'
    >>> render_grafia("grafía obsoleta", ["asta"], defaultdict(str))
    '<i>Grafía obsoleta de</i> asta'
    >>> render_grafia("grafía rara", ["exudar"], defaultdict(str))
    '<i>Grafía poco usada de</i> exudar'
    >>> render_grafia("grafía", ["psicológico"], defaultdict(str, {"texto": "Grafía rara de", "texto_pos": "(por ejemplo)"}))
    '<i>Grafía rara de</i> psicológico <i>(por ejemplo)</i>'
    """  # noqa
    if data["texto"]:
        start = data["texto"]
    else:
        start = "Grafía"
        if tpl in ("grafía", "grafia"):
            start += " alternativa "
        elif tpl == "grafía informal":
            start += " informal "
        elif tpl == "grafía obsoleta":
            start += " obsoleta "
        elif tpl == "grafía rara":
            start += " poco usada "
        start += "de"
    phrase = f"{italic(start)} "
    phrase += render_l("l", [data["alt"] or parts[0]], data)
    if data["texto_pos"]:
        phrase += f' {italic(data["texto_pos"])}'
    return phrase


def render_hipocoristico(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_hipocoristico("hipocorístico", ["Antonio"], defaultdict(str))
    '<i>Hipocorístico de</i> Antonio'
    >>> render_hipocoristico("hipocorístico", ["Antoine", "Antonio"], defaultdict(str))
    '<i>Hipocorístico de</i> Antoine, equivalente del español Antonio'
    """
    phrase = f"{italic('Hipocorístico de')} {parts[0]}"
    if len(parts) > 1:
        phrase += f", equivalente del español {parts[1]}"
    return phrase


def render_l(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_l("l+", ["la", "impello", "impellō, impellere"], defaultdict(str, {"glosa":"empujar"}))
    '<i>impellō, impellere</i> ("empujar")'
    >>> render_l("l+", ["grc", "ἀράχνη"], defaultdict(str, {"tr":"aráchnē", "glosa":"araña"}))
    '<i>ἀράχνη</i> (<i>aráchnē</i>, "araña")'
    >>> render_l("l+", ["ar", "حتى"], defaultdict(str, {"tr":"ḥatta"}))
    '<i>حتى</i> (<i>ḥatta</i>)'
    >>> render_l("l+", ["es", "morro"], defaultdict(str, {"num":"2"}))
    '<i>morro<sub>2</sub></i>'
    """
    trans = data["tr"]
    glosa = data["glosa-alt"] or data["glosa"]
    num = data["núm"] or data["num"]
    phrase = parts[-1]
    if num:
        phrase += subscript(num)
    if tpl == "l+":
        phrase = italic(phrase)
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


def render_superlativo(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_superlativo("superlativo", ["abundante"], defaultdict(str))
    '<i>Superlativo de</i> abundante:&nbsp;sumamente abundante'
    >>> render_superlativo("superlativo", ["pobre"], defaultdict(str, {"i":"s"}))
    '<i>Superlativo irregular de</i> pobre:&nbsp;sumamente pobre'
    >>> render_superlativo("superlativo", ["pobre"], defaultdict(str, {"i":"s", "alt":"alt"}))
    '<i>Superlativo irregular de</i> alt:&nbsp;sumamente pobre'
    >>> render_superlativo("superlativo", ["pobre"], defaultdict(str, {"def":"x"}))
    '<i>Superlativo de</i> pobre'
    >>> render_superlativo("superlativo", ["pobre"], defaultdict(str, {"tr":"tr", "glosa":"glosa"}))
    '<i>Superlativo de</i> pobre (<i>tr</i>, "glosa"):&nbsp;sumamente pobre'
    """
    word = parts[0] if parts else ""
    start = "Superlativo"
    if data["i"] or data["irr"] or data["irreg"] or data["irregular"]:
        start += " irregular"
    start += " de"
    phrase = italic(start)
    phrase += f" {data['alt']}" if data["alt"] else f" {word}"
    local_phrase = []
    if data["tr"]:
        local_phrase.append(italic(data["tr"]))
    if data["glosa"]:
        local_phrase.append(f'"{data["glosa"]}"')
    if local_phrase:
        phrase += f' ({concat(local_phrase, ", ")})'
    if not data["def"]:
        phrase += f":&nbsp;sumamente {word}"
    return phrase


def render_variante(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_variante("variante", ["atiesar"], defaultdict(str))
    '<i>Variante de</i> atiesar'
    >>> render_variante("variante", ["diezmo"], defaultdict(str, {"texto":"Variante anticuada de"}))
    '<i>Variante anticuada de</i> diezmo'
    """
    sentence = data["texto"] or "variante de"
    return f"{italic(capitalize(sentence))} {parts[0]}"


template_mapping = {
    "adjetivo de verbo": render_adjetivo_de_verbo,
    "aumentativo": render_aumentativo,
    "adverbio de adjetivo": render_adverbio_de_adjetivo,
    "adverbio de sustantivo": render_adverbio_de_sustantivo,
    "comparativo": render_comparativo,
    "etim": render_etim,
    "etimología": render_etimologia,
    "forma": render_forma,
    "forma sustantivo": render_forma,
    "gentilicio2": render_gentilicio2,
    "grafia": render_grafia,
    "grafía": render_grafia,
    "grafía informal": render_grafia,
    "grafía obsoleta": render_grafia,
    "grafía rara": render_grafia,
    "hipocorístico": render_hipocoristico,
    "l": render_l,
    "l+": render_l,
    "superlativo": render_superlativo,
    "variante": render_variante,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
