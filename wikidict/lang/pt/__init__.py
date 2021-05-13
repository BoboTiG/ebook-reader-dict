"""Portuguese language."""
from typing import Tuple

from .escopos import escopos

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
templates_ignored = (
    "cont",
    "FDSP",
    "ligaçãoPalavraWdic",
    "OESP",
    "#seigual",
    "t",
    "trad",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {**escopos}

# Templates more complex to manage.
templates_multi = {
    # {{AFI|/k/|pt}}
    "AFI": "parts[1]",
    # {{barra de cor|#0000FF|#0000FF}}
    "barra de cor": "color(parts[-1])",
    # {{escopo2|Informática}}
    # {{escopo2|Brasil|governo}}
    "escopo2": "term(parts[1])",
    # {{escopoCat|Náutica|pt}}
    "escopoCat": "term(lookup_italic(parts[1], 'pt'))",
    # {{escopoCatLang|Verbo auxiliar|pt}}
    "escopoCatLang": "term(lookup_italic(parts[1], 'pt'))",
    # {{escopoClasseMorfo|variação}}
    "escopoClasseMorfo": "small('(' + parts[-1] + ')')",
    # {{escopoUso|Portugal|pt}}
    "escopoUso": "term(lookup_italic(parts[1], 'pt'))",
    # {{fem|heliostático}}
    "fem": 'f"feminino de {strong(parts[1])}"',
    # {{fl|la|occŭlo}}
    "fl": "parts[-1]",
    # {{l|pt|usar|usar}}",
    "l": "parts[-1]",
    # {{l.o.|jurídico|jurídica}}
    "l.o.": "parts[-1]",
    # {{l.s.|uso}}
    "l.s.": "parts[-1]",
    # {{link opcional|arapytãŋa|tpn}}
    "link opcional": "parts[1]",
    # {{link preto|ciconiforme}}
    "link preto": "parts[-1]",
    # {{ll|publicar}}
    "ll": "parts[-1]",
    # {m|ar|شيشة|tr=šīša}}
    "m": "italic('masculino')",
    # {{mq|palavra}}
    # {{mq|word|en}}
    "mq": 'f"o mesmo que {strong(parts[1]) if len(parts) == 2 else italic(parts[1])}"',
    # {{PE|cu}}
    "PE": "f\"{parts[-1]} {superscript('(português de Portugal)')}\"",
    # {{r|la|basium|basĭum}}
    "r": "parts[-1]",
    # {{r.l|la|utor|ūtor}}
    "r.l": "parts[-1]",
    # {{varort|tenu-|pt}}
    "varort": 'f"variante ortográfica de {strong(parts[1])}"',
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["+info", "data=1871"], "pt")
        '<small>( <i>Datação</i>: 1871; )</small>'

        >>> last_template_handler(["escopo", "Pecuária"], "pt")
        '<i>(Pecuária)</i>'
        >>> last_template_handler(["escopo", "Brasileirismo"], "pt")
        '<i>(Brasileirismo)</i>'
        >>> last_template_handler(["escopo", "pt", "estrangeirismo"], "pt")
        '<i>(estrangeirismo)</i>'
        >>> last_template_handler(["escopo", "pt", "Antropônimo"], "pt")
        '<i>(Antropônimo)</i>'
        >>> last_template_handler(["escopo", "pt", "réptil"], "pt")
        '<i>(Zoologia)</i>'
        >>> last_template_handler(["escopo", "gl", "Sexualidade"], "pt")
        '<i>(Sexualidade)</i>'
        >>> last_template_handler(["escopo", "pt", "coloquial", "brasil"], "pt")
        '<i>(coloquial e Brasil)</i>'
        >>> last_template_handler(["escopo", "pt", "Catolicismo", "cristianismo", "cristianismo"], "pt")
        '<i>(Catolicismo, cristianismo e cristianismo)</i>'

        >>> last_template_handler(["etimo", "la", "canem"], "pt")
        '<i>canem</i> <sup>(la)</sup>'
        >>> last_template_handler(["etimo", "la", "canis", "sign=cão"], "pt")
        '<i>canis</i> (“cão”)'
        >>> last_template_handler(["etimo", "la", "duos", "(duōs)"], "pt")
        '<i>duos</i> (duōs)'
        >>> last_template_handler(["étimo", "grc", "ἄντρον", "transl=ánton", "sign=caverna"], "pt")
        '<i>ἄντρον</i> <i>(ánton)</i> (“caverna”)'

        >>> last_template_handler(["etm", "la", "pt"], "pt")
        'latim'

        >>> last_template_handler(["gramática", "m", "incont", "c", "comp", "concr"], "pt")
        '<i>masculino</i>, <i>incontável</i>, <i>comum</i>, <i>composto</i>, <i>concreto</i>'
        >>> last_template_handler(["gramática", "?"], "pt")
        '<small>gênero em falta</small>'
        >>> last_template_handler(["gramática", "mp", "card", "pr", "sim", "abstr"], "pt")
        '<i>masculino plural</i>, <i>cardinal</i>, <i>próprio</i>, <i>simples</i>, <i>abstrato</i>'
        >>> last_template_handler(["gramática", "m", "p", "ord"], "pt")
        '<i>masculino</i>, <i>pessoal</i>, <i>ordinal</i>'
        >>> last_template_handler(["gramática", "fp", "card"], "pt")
        '<i>feminino plural</i>, <i>cardinal</i>'
        >>> last_template_handler(["gramática", "m", "f", "cont"], "pt")
        '<i>masculino</i>, <i>feminino</i>, <i>contável</i>'
        >>> last_template_handler(["gramática", "m", "f", "p", "int"], "pt")
        '<i>masculino</i>, <i>feminino</i>, <i>pessoal</i>, <i>interrogativo</i>'
        >>> last_template_handler(["gramática", "mp", "fp", "poss"], "pt")
        '<i>masculino plural</i>, <i>feminino plural</i>, <i>possessivo</i>'
        >>> last_template_handler(["gramática", "n", "d", "trat"], "pt")
        '<i>neutro</i>, <i>dativo</i>, <i>de tratamento</i>'

        >>> last_template_handler(["la"], "pt")
        'Latim'

        >>> last_template_handler(["llietimo", "en", "anaconda"], "pt")
        'Do inglês <i>anaconda</i> <sup>(en)</sup>.'
        >>> last_template_handler(["llietimo", "la", "myrmecophaga", "pt"], "pt")
        'Do latim <i>myrmecophaga</i> <sup>(la)</sup>.'
        >>> last_template_handler(["llietimo", "grc", "myrmecophaga", "pt"], "pt")
        'Do grego antigo <i>myrmecophaga</i>.'
        >>> last_template_handler(["llietimo", "la", "caprunu", "pt", "", "cabra"], "pt")
        'Do latim <i>caprunu</i> <sup>(la)</sup> "cabra".'
        >>> last_template_handler(["llietimo", "en", "storm", "sv", "trad=tempestade"], "pt")
        'Do inglês <i>storm</i> <sup>(en)</sup> "tempestade".'
        >>> last_template_handler(["llietimo", "ru", "ко́шка", "ja", "kóška", "gato"], "pt")
        'Do russo <i>ко́шка</i> <sup>(ru)</sup> (<i>kóška</i>) "gato".'
        >>> last_template_handler(["llietimo", "ru", "ко́шка", "ja", "transcr=kóška", "trad=gato", "ponto="], "pt")
        'Do russo <i>ко́шка</i> <sup>(ru)</sup> (<i>kóška</i>) "gato".'
        >>> last_template_handler(["llietimo", "ru", "ко́шка", "ja", "kóška", "gato", "ponto=não"], "pt")
        'Do russo <i>ко́шка</i> <sup>(ru)</sup> (<i>kóška</i>) "gato"'
        >>> last_template_handler(["llietimo", "tpn", "ïsa'ub", "pt", "formiga mestra"], "pt")
        "Do tupi <i>ïsa'ub</i> <sup>(tpn)</sup> (<i>formiga mestra</i>)."

        >>> last_template_handler(["o/a", "determinad"], "pt")
        'determinada'
        >>> last_template_handler(["o/a", "funç", "ões", "ão"], "pt")
        'funções'
        >>> last_template_handler(["o/a", "trabalha", "ndo", "r"], "pt")
        'trabalhando'

        >>> last_template_handler(["PEPB", "1=Autoridade Nacional Palestiniana", "2=Autoridade Nacional Palestina"], "pt")
        'Autoridade Nacional Palestiniana <sup>(português europeu)</sup> ou Autoridade Nacional Palestina <sup>(português do Brasil)</sup>'
        >>> last_template_handler(["PEPB", "autocarro", "ônibus"], "pt")
        'autocarro <sup>(português europeu)</sup> ou ônibus <sup>(português do Brasil)</sup>'
        >>> last_template_handler(["PEPB", "inline=1", "atómico", "atômico"], "pt")
        'atómico/atômico'
        >>> last_template_handler(["PBPE", "estafe", "stafe"], "pt")
        'estafe <sup>(português do Brasil)</sup> ou stafe <sup>(português europeu)</sup>'

        >>> last_template_handler(["unknown", "test"], "pt")
        '<i>(Unknown)</i>'

        >>> last_template_handler(["xlatio", "it", "chimica", "f."], "pt")
        'chimica f.'
    """  # noqa
    from .langs import langs
    from .gramatica import gramatica_short
    from ..defaults import last_template_handler as default
    from ...user_functions import (
        concat,
        extract_keywords_from,
        italic,
        lookup_italic,
        small,
        superscript,
        term,
    )

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "+info":
        phrase = italic("Datação")
        phrase += f": {data['data']};"
        return small(f"( {phrase} )")

    if tpl == "escopo":
        if len(parts) == 1:
            words = parts
        else:
            words = [lookup_italic(p, "pt") for p in parts if p not in langs]
        return term(concat(words, sep=", ", last_sep=" e "))

    if tpl in ("etimo", "étimo"):
        src = parts.pop(0)  # Remove the lang
        phrase = italic(parts.pop(0))
        if not parts and not data:
            phrase += " " + superscript(f"({src})")
        if parts:
            phrase += f" {parts[0]}"
        if data["transl"]:
            phrase += " " + italic(f"({data['transl']})")
        if data["sign"]:
            phrase += f" (“{data['sign']}”)"
        return phrase

    if tpl == "etm":
        return langs[parts[0]]

    if tpl in ("g", "gramática"):
        result = []
        for p in parts:
            full = gramatica_short.get(p, "")
            if full:
                if p == "?":
                    result.append(small(full))
                else:
                    result.append(italic(full))
        return concat(result, ", ")

    if tpl == "llietimo":
        src, word, *rest = parts
        l10n = superscript(f"({src})")
        phrase = f"Do {langs[src]} {italic(word)}"

        l10n_needed = len(rest) != 1 or data
        if rest:
            rest.pop(0)  # Remove the destination language
            l10n_needed = src != "grc"

        if l10n_needed:
            phrase += f" {l10n}"

        if data["transcr"]:
            phrase += f" ({italic(data['transcr'])})"

        if data["trad"]:
            trad = data["trad"]
            phrase += f' "{trad}"'
        if rest:
            transcr = rest.pop(0)
            if transcr:
                phrase += f" ({italic(transcr)})"
        if rest:
            phrase += f' "{rest.pop(0)}"'

        if data.get("ponto", "") != "não":
            phrase += "."

        return phrase

    if tpl == "o/a":
        phrase = parts.pop(0)
        phrase += f"{parts[0]}" if parts else "a"
        return phrase

    if tpl in ("PEPB", "PBPE"):
        part1 = data["1"] or parts.pop(0)
        part2 = data["2"] or parts.pop(0)
        cmpl1 = "<sup>(português europeu)</sup>"
        cmpl2 = "<sup>(português do Brasil)</sup>"
        if tpl == "PBPE":
            cmpl1, cmpl2 = cmpl2, cmpl1
        if data["inline"] == "1":
            return f"{part1}/{part2}"
        return f"{part1} {cmpl1} ou {part2} {cmpl2}"

    if tpl == "xlatio":
        return f"{parts[1]} {parts[2]}"

    # This is a country in the current locale
    if tpl in langs:
        return langs[tpl].capitalize()

    return default(template, locale, word=word)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/pt
release_description = """\
As palavras contam: {words_count}
Exportação Wikcionário: {dump_date}

Arquivos disponíveis:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Actualizado em {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wikcionário (ɔ) {year}"
