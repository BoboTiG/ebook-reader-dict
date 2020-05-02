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

# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_modèles
templates = {
    "absol": "(Absolument)",
    "agri": "(Agriculture)",
    "analogie": "(Par analogie)",
    "antiq": "(Antiquité)",
    "apposition": "(En apposition)",
    "argot internet": "(Argot Internet)",
    "argot typographes": "(Argot des typographes)",
    "argot voleurs": "(Argot des voleurs)",
    "Argadz": "(Argot des Gadz’Arts)",
    "astron": "(Astronomie)",
    "au figuré": "(Figuré)",
    "BE": "(Belgique)",
    "bioch": "(Biochimie)",
    "e": "ème",
    "élec": "(Électricité)",
    "ellipse": "(Par ellipse)",
    "enclit": "(Enclitique)",
    "enfantin": "(Langage enfantin)",
    "euph": "(Par euphémisme)",
    "euphém": "(Par euphémisme)",
    "euphémisme": "(Par euphémisme)",
    "exag": "(Par hyperbole)",
    "exagération": "(Par hyperbole)",
    "épithète": "(Employé comme épithète) ",
    "finan": "(Finance)",
    "FR": "(France)",
    "formel": "(Soutenu)",
    "géom": "(Géométrie)",
    "graphe": "(Théorie des graphes)",
    "hyperb": "(Par hyperbole)",
    "hyperbole": "(Par hyperbole)",
    "idiomatique": "(Figuré)",
    "improprement": "(Usage critiqué)",
    "indén": "(Indénombrable)",
    "info": "(Informatique)",
    "injur": "(Injurieux)",
    "juri": "(Droit)",
    "ling": "(Linguistique)",
    "math": "(Mathématiques)",
    "mélio": "(Mélioratif)",
    "métaph": "(Figuré)",
    "métaphore": "(Figuré)",
    "méton": "(Par métonymie)",
    "métrol": "(Métrologie)",
    "néol": "(Néologisme)",
    "note": "Note :",
    "par ext": "(Par extension)",
    "part": "(En particulier)",
    "partic": "(En particulier)",
    "particulier": "(En particulier)",
    "peu attesté": "/!\\ Ce terme est très peu attesté.",
    "pronl": "(Pronominal)",
    "propre": "(Sens propre)",
    "QC": "(Québec)",
    "réfl": "(Réfléchi)",
    "région": "(Régionalisme)",
    "spéc": "(Spécialement)",
    "unités": "(Métrologie)",
    "usage": "Note d'usage :",
}

# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les/Bandeaux
templates_ignored = (
    "ancre",
    "créer-séparément",
    "désabrévier",
    "ébauche",
    "ébauche-déc",
    "ébauche-déf",
    "ébauche-étym",
    "ébauche-étym-nom-scientifique",
    "ébauche-exe",
    "ébauche-gent",
    "ébauche-pron",
    "ébauche-syn",
    "ébauche-trad",
    "ébauche-trad-exe",
    "ébauche-trans",
    "ébauche2-exe",
    "préciser",
    "refnec",
    "référence nécessaire",
    "réf",
    "trad-exe",
    "trier",
)

templates_multi = {
    # {{emploi|au passif}}
    "emploi": 'f"({capitalize(parts[1])})"',
    # {{forme pronominale|mutiner}}
    "forme pronominale": 'f"{capitalize(tpl)} de {parts[1]}"',
    # {{siècle2|XIX}}
    "siècle2": 'f"{parts[1]}ème"',
    # {{variante de|ranche|fr}}
    "variante de": 'f"{capitalize(tpl)} {parts[1]}"',
    # {{variante ortho de|acupuncture|fr}}
    "variante ortho de": 'f"Variante orthographique de {parts[1]}"',
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
