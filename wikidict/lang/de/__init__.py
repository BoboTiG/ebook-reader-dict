"""German language (Deutsch)."""
import re
from typing import List, Pattern, Tuple

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{Sprache|Deutsch}}", "{{sprache|deutsch}}")
etyl_section = ("{{Herkunft}}",)
sections = (
    *etyl_section,
    "{{Aussprache}",
    "{{Bedeutungen}",
    "{{Grundformverweis ",
    "{{Alte Schreibweise|",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = ()

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "Herkunft unbelegt",
    "QS Bedeutungen",
    "QS_Bedeutungen",
    "QS Herkunft",
    "QS_Herkunft",
)

# Templates more complex to manage.
templates_multi = {
    # {{f}}
    "f": "italic('f')",
    # {{fm}}
    "fm": "italic('f, m')",
    # {{fn}}
    "fn": "italic('f, n')",
    # {{L|at||en}}
    "L": "parts[1]",
    # {{lang|fr|-ose}}
    "lang": "parts[-1]",
    # {{m}}
    "m": "italic('m')",
    # {{mf}}
    "mf": "italic('m, f')",
    # {{n}}
    "n": "italic('n')",
    # {{noredlink|diminutiv}}
    "noredlink": "parts[-1]",
    # {{Polytonisch|(το)}}
    "Polytonisch": "parts[-1]",
    # {{Ü|pl|dzień}}
    "Ü": "italic(parts[-1])",
    # {{vgl.}}
    "vgl.": "italic('vergleiche:')",
    # {{W|Datenkompression|Datenkompressionen}}
    "W": "parts[-1]",
    "WP": "parts[-1]",
}

templates_other = {
    "Gen.": "Genitiv:",
    "Pl.": "Plural:",
    "Pl.1": "Plural 1:",
    "Pl.2": "Plural 2:",
    "Pl.3": "Plural 3:",
    "Pl.4": "Plural 4:",
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

<sub>Letzte Aktualisierung: {creation_date}.</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_genders(
    code: str,
    pattern: Pattern[str] = re.compile(r",\s+{{([fmnu]+)}}"),
) -> List[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("=== {{Wortart|Abkürzung|Deutsch}}, {{mf}}, {{Wortart|Substantiv|Deutsch}} ===")
    ['mf']
    """
    return pattern.findall(code)


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(r"{Lautschrift\|([^}]+)}"),
) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations(":{{IPA}} {{Lautschrift|ˈʁɪndɐˌsteːk}}")
    ['[ˈʁɪndɐˌsteːk]']
    >>> find_pronunciations(":{{IPA}} {{Lautschrift|ˈʁɪndɐˌsteːk}}, {{Lautschrift|ˈʁɪndɐˌʃteːk}}, {{Lautschrift|ˈʁɪndɐˌsteɪ̯k}}")
    ['[ˈʁɪndɐˌsteːk]', '[ˈʁɪndɐˌʃteːk]', '[ˈʁɪndɐˌsteɪ̯k]']
    """  # noqa
    return [f"[{p}]" for p in matches] if (matches := pattern.findall(code)) else []


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

    >>> last_template_handler(["default"], "de")
    '<i>(Default)</i>'
    >>> last_template_handler(["fr."], "de")
    'französisch'
    >>> last_template_handler(["fr.", ":"], "de")
    'französisch:'
    >>> last_template_handler(["fr"], "de")
    'Französisch'
    """  # noqa
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
        return render_template(template)

    # note: this should be used for variants only
    if template[0].startswith(
        (
            "Grundformverweis ",
            "Alte Schreibweise",
        )
    ):
        return template[1]

    return default(template, locale, word=word)
