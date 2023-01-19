"""Portuguese language."""
import re
from typing import List, Pattern, Tuple

from ...user_functions import uniq
from .escopos import escopos

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
section_patterns = (r"\#", r"\*")
section_level = 1
section_sublevels = (2,)
head_sections = ("{{-pt-}}",)
etyl_section = ("{{etimologia|pt}}", "Etimologia")
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

# Some definitions are not good to keep (plural, gender, ... )
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
    # {{confundir|anacruse}}
    "confundir": "f'{italic(f\"Não confundir com {strong(parts[-1])}\")}'",
    # {{datação|5/4/1810}}
    "datação": "f'[{italic(\"Datação\")}: {parts[-1]}]'",
    # {{escopo2|Informática}}
    # {{escopo2|Brasil|governo}}
    "escopo2": "term(parts[1])",
    # {{escopoCat|Náutica|pt}}
    "escopoCat": "term(lookup_italic(parts[1], 'pt'))",
    # {{escopoCatLang|Verbo auxiliar|pt}}
    "escopoCatLang": "term(lookup_italic(parts[1], 'pt'))",
    # {{escopoClasseMorfo|variação}}
    "escopoClasseMorfo": "small('(' + parts[-1] + ')')",
    # {{escopoObs.|Lê-se <u>formato dois A</u>.}}
    "escopoObs.": "f'{strong(\"Observação\")}: {parts[-1]}'",
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
    # {{link idioma|carro}}
    # {{link idioma|carro|es|vehículo}}
    "link idioma": "parts[3 if len(parts) == 4 else 1]",
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
    # {{politônico|κρατία}}
    "politônico": "parts[-1]",
    # {{r|la|basium|basĭum}}
    "r": "parts[-1]",
    # {{r.l|la|utor|ūtor}}
    "r.l": "parts[-1]",
    # {{varort|tenu-|pt}}
    "varort": 'f"variante ortográfica de {strong(parts[1])}"',
}


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/pt
release_description = """\
As palavras contam: {words_count}
Exportação Wikcionário: {dump_date}

Arquivos disponíveis:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Actualizado em {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wikcionário (ɔ) {year}"


def find_genders(
    code: str,
    pattern: Pattern[str] = re.compile(r"{([fm]+)}"),
) -> List[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("{{oxítona|ca|brum}}, {{mf}}")
    ['mf']
    >>> find_genders("'''COPOM''', {{m}}")
    ['m']
    """
    return uniq(pattern.findall(code))


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(r"{AFI\|(/[^/]+/)"),
) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{AFI|/pɾe.ˈno.me̝/}}")
    ['/pɾe.ˈno.me̝/']
    >>> find_pronunciations("{{AFI|/pɾe.ˈno.me̝/|lang=pt}}")
    ['/pɾe.ˈno.me̝/']
    """
    return uniq(pattern.findall(code))


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

        >>> last_template_handler(["etimo", "la", "myrmecophaga"], "pt")
        '<i>myrmecophaga</i>'
        >>> last_template_handler(["etimo", "grc", "στεγάζω", "(stegházo)"], "pt")
        '<i>στεγάζω</i> (stegházo)'
        >>> last_template_handler(["etimo", "orv", "ꙗзꙑкъ", "(jazykŭ)", "língua"], "pt")
        '<i>ꙗзꙑкъ</i> (jazykŭ) “língua”'
        >>> last_template_handler(["etimo", "orv", "ꙗзꙑкъ", "transcr=(jazykŭ)", "trad=língua"], "pt")
        '<i>ꙗзꙑкъ</i> (jazykŭ) “língua”'
        >>> last_template_handler(["etimo", "la", "canis", "trad=cão"], "pt")
        '<i>canis</i> “cão”'
        >>> last_template_handler(["etimo", "la", "duos", "(duōs)"], "pt")
        '<i>duos</i> (duōs)'
        >>> last_template_handler(["etimo", "grc", "ἄντρον", "transcr=ánton", "trad=caverna"], "pt")
        '<i>ἄντρον</i> (ánton) “caverna”'
        >>> last_template_handler(["etimo", "grc", "ἄντρον", "transl=ánton", "sign=caverna"], "pt")
        '<i>ἄντρον</i> <i>(ánton)</i> (“caverna”)'
        >>> last_template_handler(["etimo", "la", "abūsus", "sign=abuso"], "pt")
        '<i>abūsus</i> (“abuso”)'
        >>> last_template_handler(["etimo", "la", "nomen substantivum", "", "nome autônomo"], "pt")
        '<i>nomen substantivum</i> “nome autônomo”'

        >>> last_template_handler(["étimo", "la", "canem"], "pt")
        '<i>canem</i>'
        >>> last_template_handler(["étimo", "la", "canem", "canum"], "pt")
        '<i>canum</i>'
        >>> last_template_handler(["étimo", "la", "canem", "canum", "canos"], "pt")
        '<i>canum</i>'

        >>> last_template_handler(["etm", "la", "pt"], "pt")
        'latim'

        >>> last_template_handler(["gramática", "m", "incont", "c", "comp", "concr"], "pt")
        '<i>masculino</i>, <i>incontável</i>, <i>comum</i>, <i>composto</i>, <i>concreto</i>'
        >>> last_template_handler(["gramática", "?"], "pt")
        '<small>gênero em falta</small>'
        >>> last_template_handler(["gramática", "mp", "card", "pr", "sim", "abstr"], "pt")
        '<i>masculino plural</i>, <i>cardinal</i>, <i>próprio</i>, <i>simples</i>, <i>abstrato</i>'
        >>> last_template_handler(["gramática", "m", "p", "ord"], "pt")
        '<i>masculino</i>, <i>plural</i>, <i>ordinal</i>'
        >>> last_template_handler(["gramática", "fp", "card"], "pt")
        '<i>feminino plural</i>, <i>cardinal</i>'
        >>> last_template_handler(["gramática", "m", "f", "cont"], "pt")
        '<i>masculino</i>, <i>feminino</i>, <i>contável</i>'
        >>> last_template_handler(["gramática", "m", "f", "p", "int"], "pt")
        '<i>masculino</i>, <i>feminino</i>, <i>plural</i>, <i>interrogativo</i>'
        >>> last_template_handler(["gramática", "mp", "fp", "poss"], "pt")
        '<i>masculino plural</i>, <i>feminino plural</i>, <i>possessivo</i>'
        >>> last_template_handler(["gramática", "n", "d", "trat"], "pt")
        '<i>neutro</i>, <i>dual</i>, <i>de tratamento</i>'

        >>> last_template_handler(["la"], "pt")
        'Latim'

        >>> last_template_handler(["llietimo", "la", "myrmecophaga", "pt"], "pt")
        'Do latim <i>myrmecophaga</i>.'
        >>> # Note: below example is not expected because we would need to translate Greek to Spanish
        >>> last_template_handler(["llietimo", "grc", "γάτα", "es", "transliteração"], "pt")
        'Do grego antigo <i>γάτα</i> (<i>transliteração</i>).'
        >>> last_template_handler(["llietimo", "en", "storm", "sv", "trad=tempestade"], "pt")
        'Do inglês <i>storm</i> “tempestade”.'
        >>> last_template_handler(["llietimo", "ru", "ко́шка", "ja", "kóška", "gato"], "pt")
        'Do russo <i>ко́шка</i> (<i>kóška</i>) “gato”.'
        >>> last_template_handler(["llietimo", "ru", "ко́шка", "ja", "transcr=kóška", "trad=gato", "ponto="], "pt")
        'Do russo <i>ко́шка</i> (<i>kóška</i>) “gato”.'
        >>> last_template_handler(["llietimo", "ru", "ко́шка", "ja", "kóška", "gato", "ponto=não"], "pt")
        'Do russo <i>ко́шка</i> (<i>kóška</i>) “gato”'
        >>> last_template_handler(["llietimo", "ar", "جهاد", "pt", "jihād", "trad=esforço"], "pt")
        'Do árabe <i>جهاد</i> (<i>jihād</i>) “esforço”.'

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
    from ...user_functions import (
        concat,
        extract_keywords_from,
        italic,
        lookup_italic,
        parenthesis,
        small,
        term,
    )
    from ..defaults import last_template_handler as default
    from .gramatica import gramatica_short
    from .langs import langs

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

    if tpl == "etimo":
        src = parts.pop(0)  # Remove the lang
        phrase = italic(parts.pop(0))  # The etimo
        if parts:  # Implicit transcr
            transcr = parts.pop(0)
            phrase += f" {parenthesis(transcr)}" if transcr else ""
        if parts:  # Implicit trad
            phrase += f" “{parts.pop(0)}”"

        if data["transcr"]:
            phrase += f" {parenthesis(data['transcr'])}"
        if data["transl"]:
            phrase += " " + italic(f"({data['transl']})")
        if data["trad"]:
            phrase += f" “{data['trad']}”"
        if data["sign"]:
            phrase += f" (“{data['sign']}”)"

        return phrase

    if tpl == "étimo":
        src = parts.pop(0)  # Remove the lang
        return italic(parts[1 if len(parts) >= 2 else 0])

    if tpl == "etm":
        return langs[parts[0]]

    if tpl in ("g", "gramática"):
        result = []
        for p in parts:
            if full := gramatica_short.get(p, ""):
                if p == "?":
                    result.append(small(full))
                else:
                    result.append(italic(full))
        return concat(result, ", ")

    if tpl == "llietimo":
        src, word, _, *rest = parts
        phrase = f"Do {langs[src]} {italic(word)}"
        if data["transcr"]:
            phrase += f" ({italic(data['transcr'])})"
        if rest:
            if transcr := rest.pop(0):
                phrase += f" ({italic(transcr)})"
        if data["trad"]:
            phrase += f" “{data['trad']}”"
        if rest:
            phrase += f" “{rest.pop(0)}”"
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
