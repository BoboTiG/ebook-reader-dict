"""Spanish language."""

import re

from ...user_functions import flatten, unique
from .campos_semanticos import campos_semanticos

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{lengua|es}}",)
section_sublevels = (4, 3)
etyl_section = ("etimología", "etimología 1")
sections = (
    *etyl_section,
    "abreviaturas",
    "adjetivo",
    "{{abreviatura",
    "{{adjetivo",
    "{{adverbio",
    "{{artículo",
    "{{conjunción",
    "{{interjección",
    "{{locución",
    "{{onomatopeya",
    "{{prefijo",
    "{{preposición",
    "{{pronombre",
    "{{sufijo|",
    "{{sustantivo",
    "{{verbo",
    #
    # Variants, see render.find_section_definitions()
    #
    "forma adjetiva",
    "forma adjetiva y de participio",
    "forma verbal",
)

# Variants
variant_titles = (
    "forma adjetiva",
    "forma verbal",
)
variant_templates = (
    "{{enclítico",
    "{{infinitivo",
    "{{forma adjetivo",
    "{{forma adjetivo 2",
    "{{forma participio",
    "{{forma pronombre",
    "{{forma verbo",
    "{{f.v",
    "{{gerundio",
    "{{participio",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    *variant_templates,
    "antropónimo femenino",
    "antropónimo masculino",
    "apellido",
    "definición imprecisa",
    "f.adj2",
    "f.s.p",
    "f.v",
    "marcar sin referencias",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "ámbito",
    "ampliable",
    "arcoiris",
    "catafijo",
    "cita requerida",
    "citarequerida",
    "clear",
    "definición",
    "definición imprecisa",
    "dicvis",
    "dicvisdesc",
    "ejemplo",
    "ejemplo requerido",
    "elemento químico",
    "FEN",
    "inflect.es.sust.invariante",
    "mapa",
    "marcar sin referencias",
    "parónimo",
    "picdic",
    "picdiclabel",
    "préstamo",
    "pron-graf",
    "referencia",
    "relacionado",
    "revisar línea",
    "revisión",
    "sin referencias",
    "t",
    "uso",
)

# Templates that will be completed/replaced using italic style.
# use capital letter first, if lower, then see lowercase_italic
templates_italic = {
    "afectado": "Literario",
    "coloquial": "Coloquial",
    "Coloquial": "Coloquial",
    "elevado": "Literario",
    "extranjerismo": "Préstamo no adaptado",
    "figurado": "Figurado",
    "germanía": "Jergal",
    "jergal": "Jergal",
    "jerga": "Jergal",
    "literario": "Literario",
    "lunf": "Lunfardismo",
    "poético": "Literario",
    "rpl": "Río de la Plata",
    "rur": "Rural",
    "rural": "Rural",
    "slang": "Jergal",
    "sociedad": "Sociedad",
}

# Templates more complex to manage.
templates_multi = {
    # {{adjetivo de sustantivo|el mundo árabe}}
    "adjetivo de sustantivo": '"Que pertenece o concierne " + (f"{parts[2]} " if len(parts) > 2 else "a ") + f"{parts[1]}"',
    # {{adjetivo de padecimiento|alergia}}
    "adjetivo de padecimiento": 'f"Que padece o sufre de {parts[1]}" + (f" o {parts[2]} " if len(parts) > 2 else "")',
    # {{año de documentación|1250}}
    "año de documentación": 'f"Uso atestiguado desde {parts[1]}"',
    # {{cognados|tonina}}
    "cognados": "f\"{strong('Cognado:')} {parts[1]}\"",
    # {{color|#DDB88E|espacio=6}}
    "color": "color([p for p in parts if '=' not in p][1] if len(parts) > 1 else '#000000')",
    # {{contexto|Educación}}
    "contexto": "term(lookup_italic(parts[-1], 'es'))",
    # {{coord|04|39|N|74|03|O|type:country}}
    "coord": "coord(parts[1:], locale='es')",
    # {{datación|xv}}
    "datación": 'f"Atestiguado desde el siglo {parts[-1]}"',
    # {{definición impropia|Utilizado para especificar...}}
    "definición impropia": "italic(parts[1])",
    # {{DRAE}}
    "DRAE": 'f"«{word}», <i>Diccionario de la lengua española (2001)</i>, 22.ª ed., Madrid: Real Academia Española, Asociación de Academias de la Lengua Española y Espasa."',
    "DRAE2001": 'f"«{word}», <i>Diccionario de la lengua española (2001)</i>, 22.ª ed., Madrid: Real Academia Española, Asociación de Academias de la Lengua Española y Espasa."',
    # {{etimología2|de [[hocicar]]}}
    "etimología2": "parts[1] if (len(parts) > 1 and parts[1] != '...') else ''",
    # {{impropia|Utilizado para especificar...}}
    "impropia": "italic(parts[1])",
    # {{interjección|es}}
    "interjección": "strong('Interjección')",
    # {{neologismo|feminismo}}
    "neologismo": "strong(concat([capitalize(part) for part in parts], ', '))",
    # {{nombre científico}}
    "nombre científico": "superscript(tpl)",
    # {{plm}}
    # {{plm|cansado}}
    "plm": "capitalize(parts[1] if len(parts) > 1 else word)",
    # {{redirección suave|protocelta}}
    "redirección suave": "f\"{italic('Véase')} {parts[1]}\"",
    # {{-sub|4}}
    "-sub": "subscript(parts[1] if len(parts) > 1 else '{{{1}}}')",
    # {{subíndice|5}}
    "subíndice": "subscript(parts[1])",
    # {{-sup|2}}
    "-sup": "superscript(parts[1])",
    # {{superíndice|2}}
    "superíndice": "superscript(parts[1])",
    # {{trad|la|post meridem}}
    "trad": 'f"{parts[2]}" + superscript(f"({parts[1]})")',
    # {{ucf}}
    # {{ucf|mujer}}
    "ucf": "capitalize(parts[1] if len(parts) > 1 else word)",
    # {{variante anticuada|arsafraga}}
    "variante anticuada": "f\"{italic('Variante anticuada de')} {parts[1]}\"",
    # {{variante informal|cómo estás}}
    "variante informal": "f\"{italic('Variante informal de')} {parts[1]}\"",
    # {{variante obsoleta|hambre}}
    "variante obsoleta": "f\"{italic('Variante obsoleta de')} {parts[1]}\"",
    # {{variante rara|pecuniario}}
    "variante rara": "f\"{italic('Variante rara de')} {parts[1]}\"",
    # {{variante subestándar|-mos}}
    "variante subestándar": "f\"{italic('Variante subestándar de')} {parts[1]}\"",
    # {{versalita|xx}}
    "versalita": "small_caps(parts[1])",
    # {{verde|*exfollare}}
    "verde": "italic(parts[1])",
}

lowercase_italic = ("Rural", "Jergal", "Lunfardismo")

templates_other = {
    "antropónimo ambiguo": "<i>Nombre de pila tanto de mujer como de varón</i>",
    "onomatopeya": "Onomatopeya",
    "sigla": "Sigla",
    "suma de partes": "<i>Se utiliza como la suma de las partes: consulte las entradas de cada término por separado</i>",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/es
release_description = """\
### 🌟 Para que este proyecto pueda actualizarse con regularidad, necesita apoyo; [haga clic aquí](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) para donar. 🌟

<br/>


Número de palabras: {words_count}
exportación Wikcionario: {dump_date}

Versión completa:
{download_links_full}

Versión sin etimología:
{download_links_noetym}

<sub>Actualizado el {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wikcionario (ɔ) {year}"


def find_pronunciations(code: str, locale: str) -> list[str]:
    """
    >>> find_pronunciations("", "es")
    []
    >>> find_pronunciations("{{pron-graf|fone=ˈa.t͡ʃo}}", "es")
    ['[ˈa.t͡ʃo]']
    >>> find_pronunciations("{{pron-graf|pron=seseo|altpron=No seseante|fone=ˈgɾa.θjas|2pron=seseo|alt2pron=Seseante|2fone=ˈgɾa.sjas|audio=Gracias (español).ogg}}", "es")
    ['[ˈgɾa.θjas]', '[ˈgɾa.sjas]']
    >>> find_pronunciations("{{pronunciación|[ ˈrwe.ɰo ]}}", "es")
    ['[ˈrwe.ɰo]']
    >>> find_pronunciations("{{pronunciación|[ los ] o [ lɔʰ ]<ref>[l.htm l.htm] C</ref>}}", "es")
    ['[los]', '[lɔʰ]']
    """
    pattern = re.compile(
        r"{pronunciación\|\[\s*([^}\|\s]+)\s*\](?:.*\[\s*([^}\|\s]+)\s*\])*"
        if "{pronunciación|" in code
        else r"fone=([^}\|\s]+)"
    )
    return [f"[{p}]" for p in unique(flatten(pattern.findall(code)))]


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    missed_templates: list[tuple[str, str]] | None = None,
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["default"], "es")
        '##opendoublecurly##default##closedoublecurly##'

        >>> last_template_handler(["en"], "es")
        'Inglés'

        >>> last_template_handler(["csem", "economía", "numismática"], "es")
        '<i>(Economía, numismática)</i>'
        >>> last_template_handler(["csem", "adjetivo de verbo", "rondar", "ronda"], "es")
        '<i>(Adjetivo de verbo, rondar, ronda)</i>'
        >>> last_template_handler(["csem", "leng=es", "derecho", "deporte"], "es")
        '<i>(Derecho, deporte)</i>'

        >>> last_template_handler(["forma participio", "apropiado", "femenino"], "es")
        'apropiado'
    """
    from ...user_functions import (
        capitalize,
        concat,
        extract_keywords_from,
        italic,
        lookup_italic,
    )
    from .. import defaults
    from .langs import langs
    from .template_handlers import lookup_template, render_template

    if lookup_template(template[0]):
        return render_template(word, template)

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "csem":
        return italic(
            "("
            + capitalize(
                concat(
                    [
                        campos_semanticos.get(part.title()) or campos_semanticos.get(part.lower()) or part
                        for part in parts
                    ],
                    ", ",
                ).lower()
            )
            + ")"
        )

    if lookup_italic(template[0], locale, empty_default=True):
        phrase_a: list[str] = []
        parts.insert(0, tpl)
        added = set()
        append_to_last = False
        for index, part in enumerate(parts, 1):
            if part == ",":
                continue
            elif part in ("y", "e", "o", "u"):
                phrase_a[-1] += f" {part} "
                append_to_last = True
                continue
            else:
                local_phrase = lookup_italic(part, locale)
                if local_phrase not in added:
                    added.add(local_phrase)
                    sindex = str(index) if index > 1 else ""
                    if data[f"nota{sindex}"]:
                        local_phrase += f" ({data[f'nota{sindex}']})"
                else:
                    local_phrase = part
            if index > 1 and local_phrase in lowercase_italic:
                local_phrase = local_phrase.lower()
            if append_to_last:
                phrase_a[-1] += local_phrase
                append_to_last = False
            else:
                phrase_a.append(local_phrase)
        return italic(f"({concat(phrase_a, ', ')})") if phrase_a else ""

    if lang := langs.get(template[0]):
        return capitalize(lang)

    # note: this should be used for variants only
    if tpl in (
        "enclítico",
        "infinitivo",
        "forma adjetivo",
        "forma adjetivo 2",
        "forma participio",
        "forma pronombre",
        "forma verbo",
        "f.v",
        "gerundio",
        "participio",
    ):
        return parts[0]

    return defaults.last_template_handler(template, locale, word=word, missed_templates=missed_templates)


random_word_url = "https://es.wiktionary.org/wiki/Especial:Aleatorio_en_categor%C3%ADa/Espa%C3%B1ol"


def adjust_wikicode(code: str, locale: str) -> str:
    """ """
    # {{ES|xxx|núm=n}} → == {{lengua|es}} ==
    return re.sub(r"^\{\{ES\|.+\}\}", r"== {{lengua|es}} ==", code, flags=re.MULTILINE)
