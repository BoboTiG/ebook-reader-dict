"""German language (Deutsch)."""
from typing import Tuple

# Regex to find the pronunciation
pronunciation = r"{{Lautschrift\|([^}]+)}}"

# Regex to find the gender
gender = r",\s+{{([fmnu]+)}}"

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{Sprache|Deutsch}}", "{{sprache|deutsch}}")
etyl_section = ("{{Herkunft}}",)
sections = (
    *etyl_section,
    "{{Bedeutungen}",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = ()

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "Herkunft unbelegt",
    "QS Bedeutungen",
    "QS Herkunft",
    "QS_Herkunft",
    "WP",
)

# Templates that will be completed/replaced using italic style.
# templates_italic = {}

# Templates more complex to manage.
templates_multi = {
    # {{f}}
    "f": "italic('f')",
    # {{L|at||en}}
    "L": "parts[1]",
    # {{n}}
    "n": "italic('n')",
    # {{f}}
    "m": "italic('m')",
    # {{Ü|pl|dzień}}
    "Ü": "italic(parts[-1])",
}

templates_markierung = {
    "abw.": "abwertend",
    "adv.": "adverbial",
    "fachspr.": "fachsprachlich",
    "fam.": "familiär",
    "fDu.": "f Du.",
    "fig.": "figurativ",
    "fPl.": "f Pl.",
    "geh.": "gehoben",
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
    "veraltend": "veraltend",
    "va.": "veraltet",
    "vulg.": "vulgär",
}


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

    """  # noqa
    from ..defaults import last_template_handler as default
    from .template_handlers import render_template, lookup_template
    from ...user_functions import italic

    from .langs import langs

    if lang := langs.get(template[0], ""):
        return f"{lang}{template[1] if len(template) > 1 else ''}"

    if markierung := templates_markierung.get(template[0], ""):
        return italic(f"{markierung}{template[1] if len(template) > 1 else ''}")

    if lookup_template(template[0]):
        return render_template(template)

    return default(template, locale, word=word)


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
