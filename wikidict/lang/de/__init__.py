"""German language (Deutsch)."""

import re

from ...user_functions import uniq

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{Sprache|Deutsch}}", "{{sprache|deutsch}}", "{{Sprache|International}}", "{{sprache|international}}")
etyl_section = ("{{Herkunft}}",)
sections = (
    *etyl_section,
    "{{Alte Schreibweise|",
    "{{Aussprache}",
    "{{Bedeutungen}",
    "{{Grundformverweis ",
    "{{Wortart|Symbol|International}",
)

# Variants
variant_titles = (
    "{{Grundformverweis ",
    "{{Alte Schreibweise|",
)
variant_templates = (
    "{{Grundformverweis ",
    "{{Alte Schreibweise|",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "Anker",
    "Audio",
    "Bpur",
    "Fremdsprachige Beispiele",
    "GBS",
    "Herkunft fehlt",
    "Herkunft unbelegt",
    "Hintergrundfarbe",
    "Hörbeispiele",
    "IA",
    "IPA",
    "Lautschrift",
    "Lit-Pfeifer",
    "QS Bedeutung",
    "QS Bedeutungen",
    "QS_Bedeutungen",
    "QS Herkunft",
    "QS_Herkunft",
    "Ref-Adelung",
    "Ref-Bibel",
    "Ref-Duden",
    "Ref-DWDS",
    "Ref-Georges",
    "Ref-LSJ",
    "Ref-Pape",
    "Ref-Pfeifer",
    "Ref-wissen.de",
    "Wikipedia",
)

# More complex templates that will be completed/replaced using custom style.
templates_multi = {
    # {{Akkusativ}}
    "Akkusativ": "f'mit {italic(\"Akkusativ\")}'",
    # {{CH&LI}}
    "CH&LI": "italic('Schweiz und Liechtenstein:')",
    # {{Color|Rot|Schrift}}
    "Color": "parts[-1]",
    # {{f}}
    "f": "italic('f')",
    # {{Farbe|Rot|Schrift}}
    "Farbe": "parts[-1]",
    # {{fm}}
    "fm": "italic('f, m')",
    # {{fn}}
    "fn": "italic('f, n')",
    # {{gM}}
    # {{gM|r}}
    "gM": "f'(männliche{parts[1] if len(parts) == 2 else \"\"})'",
    # {{Hebräische Schrift|תּכלית}}
    "Hebräische Schrift": "parts[-1]",
    # {{IPA-Text|māʔ}}
    "IPA-Text": "parts[1]",
    # {{Kontamination|<Präfix>|<Wort 1>|<Suffix>|<Wort 2>}}
    "Kontamination": "f'Kontamination, zusammengesetzt aus „{parts[1]}-“ (von {parts[2]}) und „-{parts[3]}“ (von {parts[4]})'",
    # {{Koptisch|{{Ü|cop|ⲉⲙⲟⲩ}}}}
    "Koptisch": "parts[-1]",
    # {{L|at||en}}
    "L": "parts[1]",
    # {{lang|fr|-ose}}
    "lang": "parts[-1]",
    # {{linkFr|adieu}}
    "linkFr": "parts[-1]",
    # {{linkFra|adieu}}
    "linkFra": "parts[-1]",
    # {{linkLa|adieu}}
    "linkLa": "parts[-1]",
    # {{linkLat|adieu}}
    "linkLat": "parts[-1]",
    # {{m}}
    "m": "italic('m')",
    # {{mf}}
    "mf": "italic('m, f')",
    # {{MZ|1|2|3|4|5|6|7|8|9|10|11}}
    "MZ": "f'[{parts[1]}] {concat(parts[2:], sep=\"<br/>\")}'",
    # {{n}}
    "n": "italic('n')",
    # {{nf}}
    "nf": "italic('n, f')",
    # {{noredlink|diminutiv}}
    "noredlink": "parts[-1]",
    # {{Plainlink|1=http://de.wikipedia.org/wiki/Ludwig_XIV.|2=Ludwig XIV.}}
    "Plainlink": "parts[-1].removeprefix('2=')",
    # {{Polytonisch|(το)}}
    "Polytonisch": "parts[-1]",
    # {{Ref-behindthename|Alan}}
    "Ref-behindthename": "f'behindthename.com „{word}“'",
    "Ref-Grimm": "f'Jacob Grimm, Wilhelm Grimm: Deutsches Wörterbuch. 16 Bände in 32 Teilbänden. Leipzig 1854–1961 „{word}“'",
    # {{Ü|pl|dzień}}
    "Ü": "parts[-1]",
    # {{Unicode|kɔ}}
    "Unicode": "parts[-1]",
    # {{vergleiche}}
    "vergleiche": "italic('vergleiche:')",
    # {{vgl.}}
    "vgl.": "italic('vergleiche:')",
    # {{W|Datenkompression|Datenkompressionen}}
    "W": "parts[-1]",
    "WP": "parts[-1]",
}

# Templates that will be completed/replaced using custom style.
templates_other = {
    "(R)": "®",
    "DMG": "'DMG:'",
    "Gen.": "Genitiv:",
    "İA": "'İA:'",
    "ISO 9": "ISO 9:",
    "NNBSP": "&nbsp;",
    "Part.": "Partizip II: ",
    "Pl.": "Plural:",
    "Pl.1": "Plural 1:",
    "Pl.2": "Plural 2:",
    "Pl.3": "Plural 3:",
    "Pl.4": "Plural 4:",
    "Prät.": "Präteritum: ",
}

templates_markierung = {
    "abw.": "abwertend",
    "adv.": "adverbial",
    "Dativ": "mit Dativ",
    "fachspr.": "fachsprachlich",
    "fam.": "familiär",
    "fDu.": "f Du.",
    "fig.": "figurativ",
    "fPl.": "f Pl.",
    "geh.": "gehoben",
    "Genitiv": "mit Genitiv",
    "hist.": "historisch",
    "indekl.": "indeklinabel",
    "intrans.": "intransitiv",
    "kPl.": "kein Plural",
    "kSg.": "kein Singular",
    "kSt.": "keine Steigerung",
    "landsch.": "landschaftlich",
    "mPl.": "m Pl.",
    "mDu.": "m Du.",
    "meton.": "metonymisch",
    "nPl.": "n Pl.",
    "refl.": "reflexiv",
    "reg.": "regional",
    "scherzh.": "scherzhaft",
    "trans.": "transitiv",
    "uPl.": "u Pl.",
    "ugs.": "umgangssprachlich",
    "unreg.": "unregelmäßig",
    "übertr.": "übertragen",
    "vatd.": "veraltend",
    "veraltend": "veraltend",
    "va.": "veraltet",
    "veraltet": "veraltet",
    "vul.": "vulgär",
    "vulg.": "vulgär",
}


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/de
release_description = """\
Anzahl Worte: {words_count}
Wiktionary-Dump vom: {dump_date}

Verfügbare Wörterbuch-Formate:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)
- [DICT.org]({url_dictorgfile}) (dictorg-{locale}-{locale}.zip)

<sub>Letzte Aktualisierung: {creation_date}.</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_genders(
    code: str,
    pattern: re.Pattern[str] = re.compile(r",\s+{{([fmnu]+)}}"),
) -> list[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("=== {{Wortart|Abkürzung|Deutsch}}, {{mf}}, {{Wortart|Substantiv|Deutsch}} ===")
    ['mf']
    """
    return uniq(pattern.findall(code))


def find_pronunciations(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"{Lautschrift\|([^}]+)}"),
) -> list[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations(":{{IPA}} {{Lautschrift|ˈʁɪndɐˌsteːk}}")
    ['[ˈʁɪndɐˌsteːk]']
    >>> find_pronunciations(":{{IPA}} {{Lautschrift|ˈʁɪndɐˌsteːk}}, {{Lautschrift|ˈʁɪndɐˌʃteːk}}, {{Lautschrift|ˈʁɪndɐˌsteɪ̯k}}")
    ['[ˈʁɪndɐˌsteːk]', '[ˈʁɪndɐˌʃteːk]', '[ˈʁɪndɐˌsteɪ̯k]']
    """
    return [f"[{p}]" for p in uniq(pattern.findall(code))]


def last_template_handler(template: tuple[str, ...], locale: str, word: str = "") -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

    >>> last_template_handler(["default"], "de")
    '##opendoublecurly##default##closedoublecurly##'
    >>> last_template_handler(["fr."], "de")
    'französisch'
    >>> last_template_handler(["fr.", ":"], "de")
    'französisch:'
    >>> last_template_handler(["fr"], "de")
    'Französisch'
    """
    from ...user_functions import italic
    from ..defaults import last_template_handler as default
    from .lang_adjs import lang_adjs
    from .langs import langs
    from .template_handlers import lookup_template, render_template

    if lang_adj := lang_adjs.get(template[0], ""):
        return f"{lang_adj}{template[1] if len(template) > 1 else ''}"

    if lang := langs.get(template[0], ""):
        return lang

    if markierung := templates_markierung.get(template[0], ""):
        return italic(f"{markierung}{template[1] if len(template) > 1 else ''}")

    if lookup_template(template[0]):
        return render_template(word, template)

    # note: this should be used for variants only
    if template[0].startswith(
        (
            "Grundformverweis ",
            "Alte Schreibweise",
        )
    ):
        return template[1]

    return default(template, locale, word=word)
