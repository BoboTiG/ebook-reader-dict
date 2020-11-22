"""Spanish language."""
from typing import Tuple

# Regex to find the pronunciation
pronunciation = r"fone=([^}\|\s]+)"

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
section_patterns = (r";\d+[:\s\.]",)  # ;1: ...
sublist_patterns = (r":;\w",)  # :;a: ...
head_sections = ("{{lengua|es}}",)
etyl_section = ["Etimología"]
sections = (
    "Abreviaturas",
    "Adjetivo",
    "{{abreviatura",
    "{{adjetivo",
    "{{adverbio",
    "{{artículo",
    "{{conjunción",
    *etyl_section,
    "{{interjección",
    "{{onomatopeya",
    "{{prefijo",
    "{{preposición",
    "{{pronombre",
    "{{sufijo|",
    "{{sustantivo",
    "{{verbo",
)

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = (
    "antropónimo femenino",
    "antropónimo masculino",
    "apellido",
    "definición imprecisa",
    "definición impropia",
    "f.adj2",
    "f.s.p",
    "forma adjetivo",
    "forma adjetivo 2",
    "forma participio",
    "marcar sin referencias",
    "participio",
)

# Templates to ignore: the text will be deleted.
templates_ignored = ("cita requerida", "citarequerida", "préstamo", "sin referencias")

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "algas": "Ficología",
    "alimentos": "Gastronomía",
    "anfibios": "Zoología",
    "anélidos": "Zoología",
    "animales": "Zoología",
    "artrópodos": "Zoología",
    "arácnidos": "Zootomía",
    "artes": "Arte",
    "árbol": "Botánica",
    "árboles": "Botánica",
    "arbustos": "Botánica",
    "aves": "Zoología",
    "baloncestos": "Baloncesto",
    "bebida": "Gastronomía",
    "bebidas": "Gastronomía",
    "cactos": "Botánica",
    "caza": "Cinegética",
    "Cinematografía": "Cine",
    "ciudades": "Geografía",
    "cereales": "Botánica",
    "condimentos": "Gastronomía",
    "constelaciones": "Astronomía",
    "continentes": "Geografía",
    "crustáceo": "Zoología",
    "crustáceos": "Zoología",
    "cubertería": "Utensilios",
    "deportes": "Deporte",
    "dinosaurios": "Paleontología y Zoología",
    "dioses": "Religión",
    "elementos químico": "Química",
    "elementos químicos": "Química",
    "enfermedad": "Medicina",
    "enfermedades": "Medicina",
    "equinodermos": "Zoología",
    "especias": "Gastronomía",
    "estaciones": "Cronología, Meteorología",
    "Farmacia": "Farmacología",
    "fármacos": "Farmacología",
    "festividades": "Festividad",
    "flores": "Botánica",
    "ficción": "Ficción fantástica",
    "fonética": "Lingüística",
    "fraccionarios": "Fraccionario",
    "frutas": "Botánica, Gastronomía",
    "frutos": "Botánica, frutos",
    "gentilicios": "Gentilicio",
    "glotónimo": "Lingüística",
    "glotónimos": "Lingüística",
    "Hípica": "Equitación",
    "hierbas": "Botánica",
    "hongos": "Micología",
    "huesos": "Anatomía",
    "insectos": "Zoología",
    "instrumentos musicales": "Música [instrumentos]",
    "invertebrados": "Zoología",
    "islas": "Geografía",
    "juegos": "Juego",
    "lagos": "Geografía",
    "lenguas": "Lingüística",
    "lgbt": "LGBT",
    "lunf": "Lunfardismo",
    "mamíferos": "Zoología",
    "mares": "Geografía",
    "Marina": "Náutica",
    "Matemática": "Matemáticas",
    "meses": "Cronología",
    "microbiología": "Biología",
    "minerales": "Mineralogía",
    "moluscos": "Zoología",
    "moneda": "Economía y Numismática",
    "monedas": "Economía y Numismática",
    "Montería": "Cinegética",
    "muebles": "Mobiliario",
    "nemátodos": "Zoología",
    "números": "Matemáticas",
    "países": "Geografía",
    "peces": "Ictiología",
    "perros": "Cinología",
    "pesos y medidas": "Metrología",
    "planetas": "Astronomía",
    "planta": "Botánica",
    "plantas": "Botánica",
    "platelmintos": "Zoología",
    "platos": "Gastronomía",
    "prendas": "Vestimenta",
    "poblaciones": "Geografía",
    "profesiones": "Profesión",
    "provincias": "Geografía",
    "recetas": "Gastronomía",
    "regiones": "Geografía",
    "reptiles": "Zoología",
    "restaurantes": "Comercio",
    "ropa": "Vestimenta",
    "rpl": "Río de la Plata",
    "rur": "Rural",
    "sentimientos": "Humanidades",
    "telas": "Industria",
    "Teologia": "Religión",
    "textiles": "Industria",
    "tiempo": "Medición del tiempo",
    "topónimo": "Geografía",
    "topónimos": "Geografía",
    "tribus urbanas": "Sociedad",
    "vehículos": "Transporte",
    "verduras": "Gastronomía, Botánica",
    "virtudes": "Humanidades",
}

# Templates more complex to manage.
templates_multi = {
    # {{adjetivo de sustantivo|el mundo árabe}}
    "adjetivo de sustantivo": 'f"Que pertenece o concierne a {parts[1]}"',
    # {{contexto|Educación}}
    "contexto": "term(lookup_italic(parts[-1], 'es'))",
    # {{contracción|de|ellas|leng=es}}
    "contracción": "f\"{italic('Contracción de')} {parts[1]} {italic('y')} {parts[2]}\"",
    # {{coord|04|39|N|74|03|O|type:country}}
    "coord": "coord(parts[1:])",
    #  {{diminutivo|historia}}
    "diminutivo": "f\"{italic('Diminutivo de')} {parts[-1]}\"",
    # {{etimología2|de [[hocicar]]}}
    "etimología2": "capitalize(parts[1]) if len(parts) > 1 else ''",
    # {{forma diminutivo|leng=es|cuchara}}
    "forma diminutivo": "f\"{italic('Diminutivo de')} {parts[-1]}\"",
    # {{formatnum:22905}}
    "formatnum": f'number(parts[1], "{float_separator}", "{thousands_separator}")',
    # {{gentilicio|Cataluña}}
    "gentilicio": 'f"Originario, relativo a, o propio de {parts[1]}"',
    # {{gentilicio1|Alemania}}
    "gentilicio1": 'f"Originario, relativo a, o propio de {parts[1]}"',
    # {{gentilicio2|Alemania}}
    "gentilicio2": 'f"Persona originaria de {parts[1]}"',
    # "gentilicio3"
    # {{grafía|psicológico}}
    "grafía": "f\"{italic('Grafía alternativa de')} {strong(parts[1])}\"",
    # {{grafía informal|al tiro}}
    "grafía informal": "f\"{italic('Grafía informal de')} {parts[1]}\"",
    # {{grafía obsoleta|asta}}
    "grafía obsoleta": "f\"{italic('Grafía obsoleta de')} {parts[1]}\"",
    # {{grafía rara|exudar}}
    "grafía rara": "f\"{italic('Grafía poco usada de')} {parts[1]}\"",
    # {{impropia|Utilizado para especificar...}}
    "impropia": "italic(parts[1])",
    # {{l|es|tamo}}
    "l": "parts[-1]",
    # {{nombre científico}}
    "nombre científico": "superscript(tpl)",
    # {{plm}}
    # {{plm|cansado}}
    "plm": "capitalize(parts[1] if len(parts) > 1 else word)",
    # {{redirección suave|protocelta}}
    "redirección suave": "f\"{italic('Véase')} {parts[1]}\"",
    # {{-sub|4}}
    "-sub": "subscript(parts[1])",
    # {{subíndice|5}}
    "subíndice": "subscript(parts[1])",
    # {{sustantivo de adjetivo|abad}}
    # {{sustantivo de adjetivo|abad|abadesa}}
    "sustantivo de adjetivo": 'f"Condición o carácter de {parts[1]}" + (f" o {parts[2]}" if len(parts) > 2 else "")',
    # {{sustantivo de verbo|circular}}
    "sustantivo de verbo": 'f"Acción o efecto de {parts[1]}"',
    # {{-sup|2}}
    "-sup": "superscript(parts[1])",
    # {{superlativo|abundante}}
    "superlativo": "f\"{italic('Superlativo de')} {parts[1]}\"",
    # {{ucf|mujer}}
    "ucf": "capitalize(parts[1])",
    # {{variante obsoleta|hambre}}"
    "variante obsoleta": "f\"{italic('Variante obsoleta de')} {parts[1]}\"",
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["Arqueología"], "es")
        '<i>(Arqueología)</i>'
        >>> last_template_handler(["Anatomía", "y" , "Zootomía"], "es")
        '<i>(Anatomía y Zootomía)</i>'
        >>> last_template_handler(["Angiología", "Endocrinología" , "Fisiología", "Medicina"], "es")
        '<i>(Angiología, Endocrinología, Fisiología, Medicina)</i>'
        >>> last_template_handler(["moluscos", "y" , "alimentos"], "es")
        '<i>(Zoología y Gastronomía)</i>'
        >>> last_template_handler(["cultura", "historia", "y", "lingüística"], "es")
        '<i>(Cultura, Historia y Lingüística)</i>'
        >>> last_template_handler(["Arte", "," , "Arquitectura"], "es")
        '<i>(Arte, Arquitectura)</i>'
        >>> last_template_handler(["Botánica", "leng=es"], "es")
        '<i>(Botánica)</i>'
        >>> last_template_handler(["variante", "atiesar"], "es")
        '<i>Variante de</i> atiesar'
        >>> last_template_handler(["variante", "diezmo", "texto=Variante anticuada de"], "es")
        '<i>Variante anticuada de</i> diezmo'

        >>> last_template_handler(["etimología"], "es")
        ''
        >>> last_template_handler(["etimología", ""], "es")
        ''
        >>> last_template_handler(["etimología", "compuesto", "sacar", "punta"], "es")
        'Compuesto de <i>sacar</i> y <i>punta</i>'
        >>> last_template_handler(["etimología", "compuesto", "-ónimo", "-iae", "e=e"], "es")
        'Compuesto de <i>-ónimo</i> e <i>-iae</i>'
        >>> last_template_handler(["etimología", "confijo", "anglo", "filo", "tilde=sí"], "es")
        'Del prefijo <i>anglo-</i> y el sufijo <i>-́filo</i>'
        >>> last_template_handler(["etimología", "confijo", "des", "garra", "ar"], "es")
        'Del prefijo <i>des-</i>, <i>garra</i> y el sufijo <i>-ar</i>'
        >>> last_template_handler(["etimología", "epónimo"], "es")
        'Epónimo'
        >>> last_template_handler(["etimología", "epónimo", "de Adelita, protagonista de un corrido mexicano"], "es")
        'Epónimo de Adelita, protagonista de un corrido mexicano'
        >>> last_template_handler(["etimología", "femenino", "topógrafo"], "es")
        'De <i>topógrafo</i> y el sufijo flexivo <i>-a</i> para el femenino'
        >>> last_template_handler(["etimología", "fonética", "empeller"], "es")
        'Por alteración fonética de <i>empeller</i>'
        >>> last_template_handler(["etimología", "japonés", "片仮名", "transcripción=カタカナ, katakana"], "es")
        'Del japonés <i>片仮名</i> (<i>カタカナ, katakana</i>)'
        >>> last_template_handler(["etimología", "la", "incertus"], "es")
        'Del latín <i>incertus</i>'
        >>> last_template_handler(["etimología", "la", "-aceus", "alt=-acĕus"], "es")
        'Del latín <i>-acĕus</i>'
        >>> last_template_handler(["etimología", "la", "illos", "diacrítico=illōs", "sig=no"], "es")
        'Del latín <i>illōs</i>'
        >>> last_template_handler(["etimología", "osp", "fasta"], "es")
        'Del castellano antiguo <i>fasta</i>'
        >>> last_template_handler(["etimología", "plural", "vista"], "es")
        'De <i>vista</i> y el sufijo flexivo <i>-s</i>'
        >>> last_template_handler(["etimología", "plural", "vacación", "-es"], "es")
        'De <i>vacación</i> y el sufijo flexivo <i>-es</i>'
        >>> last_template_handler(["etimología", "pronominal", "agrupar"], "es")
        'De <i>agrupar</i>, con el pronombre reflexivo átono'
        >>> last_template_handler(["etimología", "sánscrito", "गुरू", "maestro", "transcripción=gūru"], "es")
        'Del sánscrito <i>गुरू</i> (<i>gūru</i>, "maestro")'
        >>> last_template_handler(["etimología", "sufijo", "átomo", "ico"], "es")
        'De <i>átomo</i> y el sufijo <i>-ico</i>'
        >>> last_template_handler(["etimología", "sufijo", "átomo", "ico"], "es")
        'De <i>átomo</i> y el sufijo <i>-ico</i>'
        >>> last_template_handler(["etimología", "sufijo", "ferrojo", "tr=anticuado por cerrojo e influido por fierro", "ar"], "es")  # noqa
        'De <i>ferrojo</i> (<i>anticuado por cerrojo e influido por fierro</i>) y el sufijo <i>-ar</i>'

        >>> last_template_handler(["l+", "la", "impello", "impellō, impellere", "glosa=empujar"], "es")
        '<i>impellō, impellere</i> ("empujar")'
        >>> last_template_handler(["l+", "grc", "ἀράχνη", "tr=aráchnē", "glosa=araña"], "es")
        'ἀράχνη (<i>aráchnē</i>, "araña")'
        >>> last_template_handler(["l+", "ar", "حتى", "tr=ḥatta"], "es")
        'حتى (<i>ḥatta</i>)'
    """
    from itertools import zip_longest

    from .langs import langs
    from ...user_functions import (
        capitalize,
        extract_keywords_from,
        italic,
        lookup_italic,
        term,
    )

    tpl = template[0]
    parts = [part for part in template[1:] if part.strip()]

    # Handle the {{variante}} template
    if tpl == "variante":
        try:
            sentence = parts[1].split("=")[1]
        except IndexError:
            sentence = "variante de"
        return f"{italic(capitalize(sentence))} {parts[0]}"

    # Handle {{etimología}} template
    if tpl == "etimología":
        data = extract_keywords_from(parts)
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
            phrase = f"De {italic(parts[0])} y el sufijo flexivo {italic('-a')} para el femenino"
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
            phrase = (
                f"De {italic(parts[0])}{more} y el sufijo {italic(suffix + parts[1])}"
            )
        elif cat in langs:
            phrase = f"Del {langs[cat]} {italic(word)}"
        else:
            phrase = f"Del {cat} {italic(word)}"

            sens = data.get("transcripción", "")
            if sens or len(parts) > 1:
                phrase += f" ({italic(sens)}"
                if len(parts) > 1:
                    phrase += f', "{parts[1]}"'
                phrase += ")"

        return phrase

    # Handle the {{l+}} template
    if tpl == "l+":
        data = extract_keywords_from(parts)
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

    res = ""
    for word1, word2 in zip_longest(template, parts):
        # Filter out "leng=" parts
        if "leng=" in word1 or word1 in ("y", ","):
            continue

        res += capitalize(lookup_italic(word1, locale))
        res += " y " if word2 == "y" else ", "

    return term(res.rstrip(", "))


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/es
release_description = """\
Número de palabras: {words_count}
exportación Wikcionario: {dump_date}

Instalacións:

1. Copia el archivo [dicthtml-{locale}.zip <sup>:floppy_disk:</sup>]({url}) en el directorio `.kobo/custom-dict/` del lector.
2. **Reinicie** la luz de lectura.

<sub>Actualizado el {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wikcionario (ɔ) {year}"
