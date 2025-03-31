"""German language (Deutsch)."""

import re

from ...user_functions import unique

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{sprache|deutsch}}", "{{sprache|international}}")
etyl_section = ("{{herkunft}}",)
sections = (
    *etyl_section,
    "{{alte schreibweise|",
    "{{aussprache}",
    "{{bedeutungen}",
    "{{grundformverweis ",
    "{{wortart|symbol|international}",
)

# Variants
variant_titles = (
    "{{grundformverweis ",
    "{{alte schreibweise|",
)
variant_templates = (
    "{{Grundformverweis ",
    "{{Alte Schreibweise|",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "Absatz",
    "Anker",
    "Audio",
    "Benutzer",
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
    "MZ": "f'[{parts[1]}] {concat(parts[2:], \"<br/>\")}'",
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
    # {{small|−6}}
    "small": "small(parts[1])",
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
### 🌟 Um regelmäßig aktualisiert werden zu können, benötigt dieses Projekt Unterstützung; [hier klicken](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) um zu spenden. 🌟

<br/>


Anzahl Worte: {words_count}
Wiktionary-Dump vom: {dump_date}

Vollständige version:
{download_links_full}

Version ohne etymologien:
{download_links_noetym}

<sub>Letzte Aktualisierung: {creation_date}.</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_genders(
    code: str,
    *,
    pattern: re.Pattern[str] = re.compile(r",\s+{{([fmnu]+)}}"),
) -> list[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("=== {{Wortart|Abkürzung|Deutsch}}, {{mf}}, {{Wortart|Substantiv|Deutsch}} ===")
    ['mf']
    """
    return unique(pattern.findall(code))


def find_pronunciations(code: str, locale: str) -> list[str]:
    """
    >>> find_pronunciations("", "de")
    []
    >>> find_pronunciations(":{{IPA}} {{Lautschrift|ˈʁɪndɐˌsteːk}}", "de")
    ['[ˈʁɪndɐˌsteːk]']
    >>> find_pronunciations(":{{IPA}} {{Lautschrift|ˈʁɪndɐˌsteːk}}, {{Lautschrift|ˈʁɪndɐˌʃteːk}}, {{Lautschrift|ˈʁɪndɐˌsteɪ̯k}}", "de")
    ['[ˈʁɪndɐˌsteːk]', '[ˈʁɪndɐˌʃteːk]', '[ˈʁɪndɐˌsteɪ̯k]']
    """
    pattern = re.compile(r"{Lautschrift\|([^}]+)}")
    return [f"[{p}]" for p in unique(pattern.findall(code))]


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    missed_templates: list[tuple[str, str]] | None = None,
) -> str:
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

    >>> last_template_handler(["Grundformverweis Konj", "tragen"], "de")
    'tragen'
    >>> last_template_handler(["Grundformverweis Dekl", "Abschnitt=Substantiv, m", "Maser"], "de")
    'Maser'
    >>> last_template_handler(["Grundformverweis Partizipform", "Verb=abbrühen", "Partizip=abgebrüht"], "de")
    'abbrühen'
    >>> last_template_handler(["Grundformverweis Konj", "1=bereiten", "Abschnitt=Verb.2C_unregelm.C3.A4.C3.9Fig"], "de")
    'bereiten'
    >>> last_template_handler(["Grundformverweis Dekl", "safe#safe_(Deutsch)", "safe"], "de")
    'safe'
    """
    from ...user_functions import extract_keywords_from, italic
    from ..defaults import last_template_handler as default
    from .lang_adjs import lang_adjs
    from .langs import langs
    from .template_handlers import lookup_template, render_template

    if lookup_template(template[0]):
        return render_template(word, template)

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if lang_adj := lang_adjs.get(tpl):
        return f"{lang_adj}{parts[0] if parts else ''}"

    if lang := langs.get(tpl):
        return lang

    if markierung := templates_markierung.get(tpl):
        return italic(f"{markierung}{parts[0] if parts else ''}")

    # note: this should be used for variants only
    if tpl.startswith(("Grundformverweis ", "Alte Schreibweise")):
        variant = data["1"] or data["Verb"] or parts[0]
        return variant.split("#", 1)[0]

    return default(template, locale, word=word, missed_templates=missed_templates)
