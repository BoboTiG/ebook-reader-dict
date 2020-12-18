"""Swedish language."""

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

# Templates more complex to manage.
templates_multi = {
    # {{avledning|sv|mälta|ordform=prespart}}
    "avledning": "f\"{italic('presensparticip av')} {parts[2]}\"",
    # {{tagg|historia}}
    # {{tagg|kat=nedsättande|text=något nedsättande}}
    "tagg": "term(tag(parts[1:]))",
    # {{uttal|sv|ipa=mɪn}}
    "uttal": "f\"{strong('uttal:')} /{parts[-1].lstrip('ipa=')}/\"",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/sv
release_description = """\
Ord räknas: {words_count}
Dumpa Wiktionary: {dump_date}

Installation:

1. Kopiera filen [dicthtml-{locale}.zip <sup>:floppy_disk:</sup>]({url}) till läsaren `.kobo/custom-dict/` mappen på läsaren.
2. **Starta** om läsaren.

<sub>Uppdaterad på {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"
