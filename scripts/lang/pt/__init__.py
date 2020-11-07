"""Portuguese language."""
from typing import Tuple

# Regex to find the pronunciation
pronunciation = r"{AFI\|\[([^\]]+)\]}"

# Regex to find the genre
genre = r"{([fm]+)}"

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
section_patterns = (r"\#", r"\*")
section_level = 1
section_sublevels = (2,)
head_sections = ("{{-pt-}}",)
etyl_section = ["{{etimologia|pt}}", "Etimologia"]
sections = (
    "Abreviatura",
    "Acrônimo",
    "Adjetivo",
    "Advérbio",
    "Antepositivo",
    "Artigo",
    "Contração",
    *etyl_section,
    "Interjeição",
    "Numeral",
    "Prefixo",
    "Preposição",
    "Pronome",
    "Sigla",
    "Substantivo",
    "Sufixo",
    "Verbo",
)

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = ("peçodef",)

# Templates to ignore: the text will be deleted.
templates_ignored = ("cont",)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "antigo": "arcaico",
    "Calão": "obsceno",
    "coloquialismo": "coloquial",
    "Coloquialismo": "coloquial",
    "Crustáceo": "Zoologia",
    "Figurado": "figurado",
    "Flor": "Botânica",
    "Informal": "coloquial",
    "Planta": "Botânica",
    "Popular": "coloquial",
    "réptil": "Zoologia",
}

# Templates more complex to manage.
templates_multi = {
    # {{escopo|Pecuária}}
    # {{escopo|pt|estrangeirismo}}
    # {{escopo|pt|coloquial|brasil}}
    "escopo": "term(lookup_italic(concat(parts, sep=' e ', indexes=[2, 3, 4, 5], skip='_'), 'pt') or parts[1])",
    # {{escopo2|Informática}}
    # {{escopo2|Brasil|governo}}
    "escopo2": "term(parts[1])",
    # {{escopoCat|Náutica|pt}}
    "escopoCat": "term(parts[1])",
    # {{escopoCatLang|Verbo auxiliar|pt}}
    "escopoCatLang": "term(parts[1])",
    # {{escopoUso|Portugal|pt}}
    "escopoUso": "term(lookup_italic(parts[1], 'pt'))",
    # {{fem|heliostático}}
    "fem": 'f"feminino de {strong(parts[1])}"',
    # {{l|pt|usar|usar}}",
    "l": "parts[-1]",
    # {{l.s.|uso}}
    "l.s.": "parts[-1]",
    # {{link preto|ciconiforme}}
    "link preto": "parts[-1]",
    # {{ll|publicar}}
    "ll": "parts[-1]",
    # {{mq|palavra}}
    # {{mq|word|en}}
    "mq": 'f"o mesmo que {strong(parts[1]) if len(parts) == 2 else italic(parts[1])}"',
    # {{varort|tenu-|pt}}
    "varort": 'f"variante ortográfica de {strong(parts[1])}"',
}


def last_template_handler(template: Tuple[str, ...], locale: str) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["etimo", "pt", "canem"], "pt")
        '<i>canem</i>'
        >>> last_template_handler(["etimo", "la", "canis", "sign=cão"], "pt")
        '<i>canis</i> (“cão”)'
        >>> last_template_handler(["etimo", "la", "duos", "(duōs)"], "pt")
        '<i>duos</i> (duōs)'

        >>> last_template_handler(["etm", "la", "pt"], "pt")
        'latim'

        >>> last_template_handler(["llietimo", "en", "anaconda"], "pt")
        'Do inglês <i>anaconda</i>.'
        >>> last_template_handler(["llietimo", "la", "myrmecophaga", "pt"], "pt")
        'Do latim <i>myrmecophaga</i>.'
        >>> last_template_handler(["llietimo", "la", "caprunu", "pt", "", "cabra"], "pt")
        'Do latim <i>caprunu</i> "cabra".'
        >>> last_template_handler(["llietimo", "en", "storm", "sv", "trad=tempestade"], "pt")
        'Do inglês <i>storm</i> "tempestade".'
        >>> last_template_handler(["llietimo", "ru", "ко́шка", "ja", "kóška", "gato"], "pt")
        'Do russo <i>ко́шка</i> (<i>kóška</i>) "gato".'
        >>> last_template_handler(["llietimo", "ru", "ко́шка", "ja", "transcr=kóška", "trad=gato", "ponto="], "pt")
        'Do russo <i>ко́шка</i> (<i>kóška</i>) "gato".'
        >>> last_template_handler(["llietimo", "ru", "ко́шка", "ja", "kóška", "gato", "ponto=não"], "pt")
        'Do russo <i>ко́шка</i> (<i>kóška</i>) "gato"'
        >>> last_template_handler(["llietimo", "tpn", "ïsa'ub", "pt", "formiga mestra"], "pt")
        "Do tupi <i>ïsa'ub</i> (<i>formiga mestra</i>)."

        >>> last_template_handler(["unknown", "test"], "pt")
        '<i>(Unknown)</i>'
    """
    from .langs import langs
    from ..defaults import last_template_handler as default
    from ...user_functions import clean_parts, italic

    tpl = template[0]
    parts = list(template[1:])

    # Handle {{etimo}} template
    if tpl == "etimo":
        phrase = italic(parts[1])
        if len(parts) == 3:
            word = parts[2]
            if word.startswith("sign="):
                word = word.split("=", 1)[1]
                phrase += f" (“{word}”)"
            else:
                phrase += f" {word}"
        return phrase

    # Handle {{etm}} template
    if tpl == "etm":
        return langs[parts[0]]

    # Handle {{llietimo}} template
    if tpl == "llietimo":
        data = clean_parts(parts)
        src, word, *rest = parts
        phrase = f"Do {langs[src]} {italic(word)}"

        if "transcr" in data:
            transcr = data["transcr"]
            phrase += f" ({italic(transcr)})"

        if "trad" in data:
            trad = data["trad"]
            phrase += f' "{trad}"'

        if rest:
            rest.pop(0)  # Remove the destination language
            if rest:
                transcr = rest.pop(0)
                if transcr:
                    phrase += f" ({italic(transcr)})"
                if rest:
                    phrase += f' "{rest.pop(0)}"'

        if data.get("ponto", "") != "não":
            phrase += "."

        return phrase

    return default(template, locale)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/pt
release_description = """\
As palavras contam: {words_count}
Exportação Wikcionário: {dump_date}

Instalação:

1. Copiar o ficheiro [dicthtml-{locale}.zip <sup>:floppy_disk:</sup>]({url}) para a pasta `.kobo/dict/` do leitor.
2. **Reiniciar** o leitor.

<sub>Actualizado em {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wikcionário (ɔ) {year}"
