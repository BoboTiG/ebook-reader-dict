"""Spanish language."""
from typing import Tuple
from .campos_semanticos import campos_semanticos


# Regex to find the pronunciation
pronunciation = r"fone=([^}\|\s]+)"

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
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
    "forma verbo",
    "marcar sin referencias",
    "participio",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "catafijo",
    "cita requerida",
    "citarequerida",
    "marcar sin referencias",
    "préstamo",
    "sin referencias",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    **campos_semanticos,
    "lunf": "Lunfardismo",
    "rpl": "Río de la Plata",
    "rur": "Rural",
}

# Templates more complex to manage.
templates_multi = {
    # {{adjetivo de sustantivo|el mundo árabe}}
    "adjetivo de sustantivo": '"Que pertenece o concierne " + (f"{parts[2]} " if len(parts) > 2 else "a ") + f"{parts[1]}"',  # noqa
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
    "gentilicio": '"Originario, relativo a, o propio " + ("del" if any("contracción" in part for part in parts) else "de") + f" {parts[1]}"',  # noqa
    # {{gentilicio1|Alemania}}
    "gentilicio1": '"Originario, relativo a, o propio " + ("del" if any("contracción" in part for part in parts) else "de") + f" {parts[1]}"',  # noqa
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
    "sustantivo de verbo": 'f"Acción o efecto de {parts[1]}" + (f" o de {parts[2]}" if len(parts) > 2 else "")',
    # {{-sup|2}}
    "-sup": "superscript(parts[1])",
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
    """
    from itertools import zip_longest
    from ...user_functions import (
        capitalize,
        lookup_italic,
        term,
    )
    from .template_handlers import render_template, lookup_template

    if lookup_template(template[0]):
        return render_template(template)

    parts = [part for part in template[1:] if part.strip()]

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

Archivos disponibles:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Actualizado el {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wikcionario (ɔ) {year}"
