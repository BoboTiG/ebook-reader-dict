"""French language."""

patterns = (
    "{{S|adjectif|fr}",
    "{{S|adjectif|fr|",
    "{{S|adverbe|fr}",
    "{{S|adverbe|fr|",
    "{{S|adverbe|conv}",
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

size_min = 1024 * 1024 * 30  # 30 MiB

templates = {
    "absol": "(Absolument)",
    "BE": "(Belgique)",
    "bioch": "(Biochimie)",
    "e": "ème",
    "élec": "(Électricité)",
    "finan": "(Finance)",
    "FR": "(France)",
    "géom": "(Géométrie)",
    "juri": "(Droit)",
    "ling": "(Linguistique)",
    "math": "(Mathématiques)",
    "méton": "(Par métonymie)",
    "métrol": "(Métrologie)",
    "néol": "(Néologisme)",
    "note": "Note :",
    "par ext": "(Par extension)",
    "part": "(En particulier)",
    "pronl": "(Pronominal)",
    "QC": "(Québec)",
    "région": "(Régionalisme)",
    "spéc": "(Spécialement)",
}

templates_ignored = ("ébauche-déf", "refnec")

templates_multi = {
    # {{forme pronominale|mutiner}}
    "forme pronominale": "{tpl} de {parts[1]}",
    # {{variante de|ranche|fr}}
    "variante de": "{tpl} {parts[1]}",
}

translations = {
    "release_desc": """Nombre de mots : {words_count}
Export Wiktionnaire : {dump_date}

:arrow_right: Téléchargement : [dicthtml-fr.zip]({url})

---

<sub>Nombre total de téléchargements : {download_count}</sub>
<sub>Date de création du fichier : {creation_date}</sub>
""",
    "thousands_separator": " ",
}
