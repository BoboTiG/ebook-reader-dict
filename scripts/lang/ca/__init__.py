"""Catalan language."""

pronunciation = r"{{ca-pron\|(?:or=)?/([^/\|]+)"
genre = r"{{ca-\w+\|([fm]+)"

float_separator = ","
thousands_separator = "."

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

definitions_to_ignore = (
    # Ignore conjuged verbs
    "ca-forma-conj",
    "sense accepcions",
    # Proper nouns
    "cognom",
    "prenom",
    # Ignore genres
    "forma-f",
    # Ignore plurals
    "forma-p",
)
words_to_keep = tuple()  # type: ignore

templates_ignored = tuple()  # type: ignore

templates_other = {
    "m": "m.",
}

templates_italic = {
    "alguerès-verb": "alguerès",
    "arcaic": "arcaisme",
    "fruits": "botànica",
    "plantes": "botànica",
    "valencià-verb": "valencià",
}

templates_multi = {
    # {{color|#E01010}}
    "color": "color(parts[1])",
    # {{e|la|lupus}}
    "e": "parts[2]",
    # {{forma-a|ca|Beget}}
    "forma-a": "f\"{italic('forma alternativa de')} {strong(parts[2])}\"",
    # {{forma-pron|ca|estimar}}
    "forma-pron": "f\"{italic('forma pronominal de')} {strong(parts[2])}\"",
    # {{IPAchar|[θ]}}
    "IPAchar": "parts[-1]",
    # {{marca|ca|fruits}}
    # {{marca|ca|interrogatiu|condicional}}
    "marca": "term(lookup_italic(concat(parts, sep=', ', indexes=[2, 3, 4, 5]), 'ca'))",
    # {{marca-nocat|ca|balear}}
    # {{marca-nocat|ca|occidental|balear}}
    "marca-nocat": "term(lookup_italic(concat(parts, sep=', ', indexes=[2, 3, 4, 5]), 'ca'))",
    # {{q|tenir bona planta}}
    "q": "term(parts[-1])",
    # {{terme|it|come}}
    "terme": "parts[-1]",
}

templates_warning_skip = tuple()  # type: ignore

release_description = """\
Words count: {words_count}
Wiktionary dump: {dump_date}

:arrow_right: Download: [dicthtml-ca.zip]({url})

---

Installation:

1. Copy the `dicthtml-ca.zip` file into the `.kobo/dict/` folder of the reader.
2. Restart the reader.

---

Caractéristics :

- Only definitions are included: there is no quote nor ethymology.
- 1-character words are not included.
- Proper nouns are not included.
- Conjuged verbs are not included.

<sub>Updated on {creation_date}</sub>
"""

wiktionary = "Viccionari (ɔ) {year}"
