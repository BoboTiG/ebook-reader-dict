"""French language."""

ignored_templates = (
    "(refnec)",
    "spéc",
)

patterns = (
    "{{S|adjectif|fr}",
    "{{S|adjectif|fr|",
    "{{S|adverbe|fr}",
    "{{S|adverbe|fr|",
    "{{S|article défini|fr}",
    "{{S|article défini|fr|",
    # "{{S|lettre|fr}",
    # "{{S|lettre|fr|",
    "{{S|nom|fr}",
    "{{S|nom|fr|",
    # "{{S|nom propre|fr}",
    # "{{S|nom propre|fr|",
    "{{S|numéral|conv}",
    "{{S|préposition|fr}",
    "{{S|préposition|fr|",
    # "{{S|pronom indéfini|fr}",
    # "{{S|pronom indéfini|fr|",
    # "{{S|pronom personnel|fr}",
    # "{{S|pronom personnel|fr|",
    "{{S|symbole|conv}",
    "{{S|verbe|fr}",
    "{{S|verbe|fr|",
)

release_tr = {
    "date": "Date :",
    "download": ":arrow_right: Téléchargement :",
    "thousands_separator": " ",
    "words_count": "Nombre de mots :",
}

size_min = 1024 * 1024 * 30  # 30 MiB
