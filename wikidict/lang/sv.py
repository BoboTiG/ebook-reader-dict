"""Swedish language."""
from typing import Tuple

# Regex to find the pronunciation
pronunciation = r"{uttal\|sv\|(?:[^\|]+\|)?ipa=([^}]+)}"

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
# https://sv.wiktionary.org/wiki/Wiktionary:Stilguide#Ordklassrubriken
head_sections = ("==Svenska==", "svenska")
sections = (
    "Adjektiv",
    "Adverb",
    "Affix",
    "Artikel",
    "Efterled",
    "Förkortning",
    "Förled",
    "Interjektion",
    "Konjunktion",
    "Possessivt pronomen",
    "Postposition",
    "Prefix",
    "Preposition",
    "Pronomen",
    "Substantiv",
    "Suffix",
    "Verbpartikel",
)

# Templates to ignore: the text will be deleted.
templates_ignored = ("citat",)

# Templates more complex to manage.
templates_multi = {
    # {{avledning|sv|mälta|ordform=prespart}}
    "avledning": "f\"{italic('presensparticip av')} {parts[2]}\"",
    # {{böjning|sv|subst|boll}}
    "böjning": "italic('böjningsform av') + ' ' + parts[-1]",
    # {{led|sv|f|gata}}
    "led": "italic(('förled' if parts[2] == 'f' else 'efterled') + ' tillhörigt ordet') + ' ' + parts[-1]",
    # {{ö|en|test}}
    "ö": 'f"ger: {parts[-1]}"',
    # {{ö+|en|test}}
    "ö+": "f\"ger: {parts[-1]} {superscript('(' + parts[1] + ')')}\"",
    # {{ö-inte|en|test}}
    "ö-inte": "f\"ger: {strong('inte')} {italic(strike(parts[-1]))}\"",
    # {{tagg|historia}}
    # {{tagg|kat=nedsättande|text=något nedsättande}}
    "tagg": "term(tag(parts[1:]))",
    # {{uttal|sv|ipa=mɪn}}
    "uttal": "f\"{strong('uttal:')} /{parts[-1].lstrip('ipa=')}/\"",
}


_gammalstavning = {
    "hv": "genom stavningsreformen 1906 ",
    "dt": "genom stavningsreformen 1906 ",
    "f": "genom stavningsreformen 1906 ",
    "fv": "genom stavningsreformen 1906 ",
    "eä": "genom sjätte upplagan av SAOL (1889) ",
    "gk": "genom sjunde upplagan av SAOL (1900) ",
    "w": "vid övergången från fraktur till antikva ",
    "aa": "genom rättskrivningsreformen 1948 ",
    "dl": "genom rättskrivningsreformen 1948 ",
    "ld": "genom rättskrivningsreformen 1948 ",
    "ss": "genom rättskrivningsreformen 1996 ",
    "ff": "genom rättskrivningsreformen 1996 ",
    "äe": "genom rättskrivningsreformen 1996 ",
    "sär": "genom rättskrivningsreformen 1996 ",
    "auh": "genom rättskrivningsreformen 1996 ",
    "zs": "genom stavningsreformen 1973 ",
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["foo"], "sv")
        '<i>(Foo)</i>'

        >>> last_template_handler(["gammalstavning", "fv", "brev"], "sv")
        '<i>genom stavningsreformen 1906 ersatt av</i> brev'
        >>> last_template_handler(["gammalstavning", "m", "Dalarna"], "sv")
        '<i>ersatt av</i> Dalarna'

    """  # noqa
    from .defaults import last_template_handler as default
    from ..user_functions import italic

    tpl, *parts = template

    if tpl == "gammalstavning":
        cat = _gammalstavning.get(parts[0], "") + "ersatt av"
        return f"{italic(cat)} {parts[-1]}"

    return default(template, locale, word=word)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/sv
release_description = """\
Ord räknas: {words_count}
Dumpa Wiktionary: {dump_date}

Tillgängliga filer:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Uppdaterad på {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"
