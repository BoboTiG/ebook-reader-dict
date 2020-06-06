"""Catalan language."""

# Regex to find the pronunciation
pronunciation = r"{ca-pron\|(?:or=)?/([^/\|]+)"

# Regex to find the genre
genre = r"{ca-\w+\|([fm]+)"

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
section_patterns = (r"\#",)
section_level = 2
head_sections = ("{-ca-}", "{-mul-}")
sections = (
    "Abreviatura",
    "Acrònim",
    "Adjectiu",
    "Adverbi",
    "Article",
    "Contracció",
    "Infix",
    "Interjecció",
    "Lletra",
    "Nom",
    "Numeral",
    "Prefix",
    "Preposició",
    "Pronom",
    "Sigles",
    "Sufix",
    "Símbol",
    "Verb",
)

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = (
    # Ignore conjuged verbs
    "ca-forma-conj",
    # Proper nouns
    "cognom",
    "prenom",
    # Ignore genres
    "forma-f",
    # Ignore plurals
    "forma-p",
)

# But some words need to be kept even if they would have been skipped by definitions_to_ignore
words_to_keep = tuple()  # type: ignore

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "manquen accepcions",
    "sense accepcions",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "alguerès-verb": "alguerès",
    "arcaic": "arcaisme",
    "fruits": "botànica",
    "plantes": "botànica",
    "valencià-verb": "valencià",
}

# Templates more complex to manage.
templates_multi = {
    # {{color|#E01010}}
    "color": "color(parts[1])",
    # {{e|la|lupus}}
    "e": "parts[2]",
    # {{forma-|abreujada|ca|bicicleta}}
    "forma-": "f\"{italic('forma ' + parts[1] + ' de')} {strong(parts[-1])}\"",
    # {{forma-a|ca|Beget}}
    "forma-a": "f\"{italic('forma alternativa de')} {strong(parts[2])}\"",
    # {{forma-pron|ca|estimar}}
    "forma-pron": "f\"{italic('forma pronominal de')} {strong(parts[2])}\"",
    # {{IPAchar|[θ]}}
    "IPAchar": "parts[-1]",
    # {{marca|ca|fruits}}
    # {{marca|ca|interrogatiu|condicional}}
    "marca": "term(lookup_italic(concat(parts, sep=', ', indexes=[2, 3, 4, 5], skip='_'), 'ca'))",
    # {{marca-nocat|ca|balear}}
    # {{marca-nocat|ca|occidental|balear}}
    "marca-nocat": "term(lookup_italic(concat(parts, sep=', ', indexes=[2, 3, 4, 5]), 'ca'))",
    # {{q|tenir bona planta}}
    "q": "term(parts[-1])",
    # {{terme|it|come}}
    "terme": "parts[-1]",
}

# Templates that will be completed/replaced using custom style.
templates_other = {
    "m": "m.",
}

# A warning will be printed when a template contains superfuous spaces,
# except for those listed bellow:
templates_warning_skip = tuple()  # type: ignore

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ca
release_description = """\
:warning: Contributors needed for that locale.

Words count: {words_count}
Wiktionary dump: {dump_date}

:arrow_right: Download: [dicthtml-{locale}.zip]({url})

---

Installation:

1. Copy the `dicthtml-{locale}.zip` file into the `.kobo/dict/` folder of the reader.
2. Restart the reader.

---

Caractéristics :

- Only definitions are included: there is no quote nor ethymology.
- 1-character words are not included.
- Proper nouns are not included.
- Conjuged verbs are not included.

<sub>Updated on {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Viccionari (ɔ) {year}"
