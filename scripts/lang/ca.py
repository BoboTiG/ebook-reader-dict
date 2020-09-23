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
head_sections = ("{{-ca-}}", "{{-mul-}}")
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

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ca
release_description = """\
Les paraules compten: {words_count}
Abocador Viccionari: {dump_date}

:arrow_right: Descarregar: [dicthtml-{locale}.zip]({url})

---

Instal·lació:

1. Copieu el fitxer `dicthtml-{locale}.zip` a la carpeta `.kobo/dict/` del lector.
2. Reinicieu el lector.

---

Característiques:

- No hi ha etimologia.
- Els noms propis no s’inclouen.
- No s’inclouen els verbs conjugats.

<sub>Actualitzat el {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Viccionari (ɔ) {year}"
