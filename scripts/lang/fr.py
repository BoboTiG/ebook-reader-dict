"""French language."""

patterns = (
    "{{S|adjectif|fr}",
    "{{S|adjectif|fr|",
    "{{S|adverbe|fr}",
    "{{S|adverbe|fr|",
    "{{S|adverbe|conv}",
    "{{S|article défini|fr}",
    "{{S|article défini|fr|",
    "{{S|interjection|fr}",
    "{{S|interjection|fr|",
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
    "absol": "<i>(Absolument)</i>",
    "aéro": "<i>(Aéronautique)</i>",
    "agri": "<i>(Agriculture)</i>",
    "analogie": "<i>(Par analogie)</i>",
    "angl": "<i>(Anglicisme)</i>",
    "antiq": "<i>(Antiquité)</i>",
    "apposition": "<i>(En apposition)</i>",
    "archi": "<i>(Architecture)</i>",
    "admin": "<i>(Administration)</i>",
    "argot internet": "<i>(Argot Internet)</i>",
    "argot typographes": "<i>(Argot des typographes)</i>",
    "argot voleurs": "<i>(Argot des voleurs)</i>",
    "Argadz": "<i>(Argot des Gadz’Arts)</i>",
    "astron": "<i>(Astronomie)</i>",
    "automo": "<i>(Automobile)</i>",
    "au figuré": "<i>(Figuré)</i>",
    "BE": "<i>(Belgique)</i>",
    "bioch": "<i>(Biochimie)</i>",
    "biol": "<i>(Biologie)</i>",
    "ciné": "<i>(Cinéma)</i>",
    "comm": "<i>(Commerce)</i>",
    "e": "<sup>e</sup>",
    "élec": "<i>(Électricité)</i>",
    "ellipse": "<i>(Par ellipse)</i>",
    "enclit": "<i>(Enclitique)</i>",
    "enfantin": "<i>(Langage enfantin)</i>",
    "euph": "<i>(Par euphémisme)</i>",
    "euphém": "<i>(Par euphémisme)</i>",
    "euphémisme": "<i>(Par euphémisme)</i>",
    "exag": "<i>(Par hyperbole)</i>",
    "exagération": "<i>(Par hyperbole)</i>",
    "épithète": "<i>(Employé comme épithète) ",
    "finan": "<i>(Finance)</i>",
    "FR": "<i>(France)</i>",
    "formel": "<i>(Soutenu)</i>",
    "géog": "<i>(Géographie)</i>",
    "géom": "<i>(Géométrie)</i>",
    "graphe": "<i>(Théorie des graphes)</i>",
    "hérald": "<i>(Héraldique)</i>",
    "hist": "<i>(Histoire)</i>",
    "hyperb": "<i>(Par hyperbole)</i>",
    "hyperbole": "<i>(Par hyperbole)</i>",
    "idiomatique": "<i>(Figuré)</i>",
    "impr": "<i>(Imprimerie)</i>",
    "improprement": "<i>(Usage critiqué)</i>",
    "indén": "<i>(Indénombrable)</i>",
    "indus": "<i>(Industrie)</i>",
    "info": "<i>(Informatique)</i>",
    "injur": "<i>(Injurieux)</i>",
    "intrans": "<i>(Intransitif)</i>",
    "juri": "<i>(Droit)</i>",
    "ling": "<i>(Linguistique)</i>",
    "math": "<i>(Mathématiques)</i>",
    "mélio": "<i>(Mélioratif)</i>",
    "métaph": "<i>(Figuré)</i>",
    "métaphore": "<i>(Figuré)</i>",
    "méton": "<i>(Par métonymie)</i>",
    "métrol": "<i>(Métrologie)</i>",
    "mythol": "<i>(Mythologie)</i>",
    "néol": "<i>(Néologisme)</i>",
    "note": "<b>Note :</b>",
    "ornithol": "<i>(Ornithologie)</i>",
    "p": "<i>pluriel</i>",
    "par ext": "<i>(Par extension)</i>",
    "part": "<i>(En particulier)</i>",
    "partic": "<i>(En particulier)</i>",
    "particulier": "<i>(En particulier)</i>",
    "peu attesté": "/!\\ Ce terme est très peu attesté.",
    "péj": "<i>(Péjoratif)</i>",
    "philo": "<i>(Philosophie)</i>",
    "popu": "<i>(Populaire)</i>",
    "prog": "<i>(Programmation informatique)</i>",
    "pronl": "<i>(Pronominal)</i>",
    "propre": "<i>(Sens propre)</i>",
    "QC": "<i>(Québec)</i>",
    "reli": "<i>(Religion)</i>",
    "réfl": "<i>(Réfléchi)</i>",
    "région": "<i>(Régionalisme)</i>",
    "sexe": "<i>(Sexualité)</i>",
    "spéc": "<i>(Spécialement)</i>",
    "télécom": "<i>(Télécommunications)</i>",
    "tradit": "<i>(Orthographe traditionnelle)</i>",
    "typo": "<i>(Typographie)</i>",
    "unités": "<i>(Métrologie)</i>",
    "usage": "<b>Note d'usage :</b>",
}

# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les/Bandeaux
templates_ignored = (
    "ancre",
    "cf",
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
    "R",
    "refnec",
    "réfnéc",
    "réfnec",
    "référence nécessaire",
    "réf",
    "source",
    "trad-exe",
    "trier",
)

templates_multi = {
    # {{adj-indéf-avec-de}}
    "adj-indéf-avec-de": '"<i>(Avec de)</i>"',
    # {{comparatif de|bien|fr|adv}}
    "comparatif de": 'f"{capitalize(tpl)} {parts[1]}"',
    # {{couleur|#B0F2B6}}
    "couleur": 'f"(Code RGB {parts[1]})"',
    # {{emploi|au passif}}
    "emploi": 'f"<i>({capitalize(parts[1])})</i>"',
    # {{forme pronominale|mutiner}}
    "forme pronominale": 'f"{capitalize(tpl)} de {parts[1]}"',
    # {{lien|étrange|fr}}
    "lien": 'f"{parts[1]}"',
    # {{nombre romain|12}}
    "nombre romain": 'f"{int_to_roman(int(parts[1]))}"',
    # {{pron|plys|fr}}
    "pron": r'f"\\{parts[1]}\\"',
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
