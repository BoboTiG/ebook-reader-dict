"""French language."""

# Titre des sections qui sont intéressantes à analyser.
patterns = (
    "{{S|adjectif|fr}",
    "{{S|adjectif|fr|",
    "{{S|adverbe|fr}",
    "{{S|adverbe|fr|",
    "{{S|adverbe|conv}",
    "{{S|article défini|fr}",
    "{{S|article défini|fr|",
    "{{S|conjonction|fr}",
    "{{S|conjonction|fr|",
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
    # "{{S|pronom interrogatif|fr}",
    # "{{S|pronom interrogatif|fr|",
    # "{{S|pronom personnel|fr}",
    # "{{S|pronom personnel|fr|",
    "{{S|symbole|conv}",
    "{{S|verbe|fr}",
    # Pas besoin des conjugaisons
    # "{{S|verbe|fr|",
)

# Modèle à ignorer : le texte sera supprimé.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les/Bandeaux
templates_ignored = (
    "ancre",
    "créer-séparément",
    "désabrévier",
    "doute",
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
    "réf?",
    "source",
    "trad-exe",
    "trier",
)

# Modèles qui seront remplacés par du texte italique.
# Ex : {{absol}} -> <i>(Absolument)</i>
# Ex : {{absol|fr}} -> <i>(Absolument)</i>
# Ex : {{absol|fr|...}} -> <i>(Absolument)</i>
templates_italic = {
    "absol": "Absolument",
    "adj-indéf-avec-de": "Avec de",
    "admin": "Administration",
    "aéro": "Aéronautique",
    "agri": "Agriculture",
    "analogie": "Par analogie",
    "angl": "Anglicisme",
    "antiq": "Antiquité",
    "apposition": "En apposition",
    "archi": "Architecture",
    "Argadz": "Argot des Gadz’Arts",
    "argot internet": "Argot Internet",
    "argot typographes": "Argot des typographes",
    "argot voleurs": "Argot des voleurs",
    "astron": "Astronomie",
    "auto": "Automobile",
    "automo": "Automobile",
    "antonomase": "Antonomase",
    "au figuré": "Figuré",
    "bdd": "Bases de données",
    "BE": "Belgique",
    "bioch": "Biochimie",
    "biol": "Biologie",
    "ciné": "Cinéma",
    "cuis": "Cuisine",
    "comm": "Commerce",
    "cout": "Couture",
    "didact": "Didactique",
    "élec": "Électricité",
    "ellipse": "Par ellipse",
    "enclit": "Enclitique",
    "enfantin": "Langage enfantin",
    "euph": "Par euphémisme",
    "euphém": "Par euphémisme",
    "euphémisme": "Par euphémisme",
    "exag": "Par hyperbole",
    "exagération": "Par hyperbole",
    "éduc": "Éducation",
    "épithète": "Employé comme épithète",
    "ferro": "Chemin de fer",
    "finan": "Finance",
    "FR": "France",
    "formel": "Soutenu",
    "fortification": "Architecture",
    "géog": "Géographie",
    "géom": "Géométrie",
    "graphe": "Théorie des graphes",
    "hérald": "Héraldique",
    "hist": "Histoire",
    "hyperb": "Par hyperbole",
    "hyperbole": "Par hyperbole",
    "idiomatique": "Figuré",
    "impr": "Imprimerie",
    "improprement": "Usage critiqué",
    "indén": "Indénombrable",
    "indus": "Industrie",
    "info": "Informatique",
    "injur": "Injurieux",
    "intrans": "Intransitif",
    "iron": "Ironique",
    "jardi": "Jardinage",
    "juri": "Droit",
    "jurisprudence": "Droit",
    "ling": "Linguistique",
    "litt": "Littéraire",
    "logi": "Logique",
    "math": "Mathématiques",
    "médecine non conv": "Médecine non conventionnelle",
    "mélio": "Mélioratif",
    "menu": "Menuiserie",
    "métaph": "Figuré",
    "métaphore": "Figuré",
    "météo": "Météorologie",
    "méton": "Par métonymie",
    "métonymie": "Par métonymie",
    "métrol": "Métrologie",
    "mili": "Militaire",
    "musi": "Musique",
    "mythol": "Mythologie",
    "néol": "Néologisme",
    "ornithol": "Ornithologie",
    "par ext": "Par extension",
    "part": "En particulier",
    "partic": "En particulier",
    "particulier": "En particulier",
    "pêch": "Pêche",
    "péj": "Péjoratif",
    "philo": "Philosophie",
    "poés": "Poésie",
    "POO": "Programmation orientée objet",
    "popu": "Populaire",
    "prog": "Programmation informatique",
    "pronl": "Pronominal",
    "propre": "Sens propre",
    "QC": "Québec",
    "reli": "Religion",
    "réfl": "Réfléchi",
    "région": "Régionalisme",
    "scol": "Éducation",
    "sexe": "Sexualité",
    "spéc": "Spécialement",
    "tech": "Technique",
    "technol": "Technologie",
    "télécom": "Télécommunications",
    "tradit": "Orthographe traditionnelle",
    "typo": "Typographie",
    "typog": "Typographie",
    "unités": "Métrologie",
    "vête": "Habillement",
    "vieux": "Vieilli",
    "zool": "Zoologie",
    "zootechnie": "Zoologie",
}

# Modèles un peu plus complexes à gérer, leur prise en charge demande plus de travail.
# Le code de droite sera passer à une fonction qui l'exécutera. Il est possible d'utiliser
# n'importe quelle fonction Python et celles définies dans utils.py.
#
# # Les arguments disponibles sont :
#   - *tpl* (texte) qui contient le nom du modèle.
#   - *parts* (liste de textes) qui contient les autres parties du modèle.
#
# Exemple avec le modèle complet "{{comparatif de|bien|fr|adv}}" :
#   - *tpl* contiendra le texte "comparatif de".
#   - *parts* contiendra la liste ["bien", "fr", "adv"].
#
# L'accès à *tpl* et *parts* permet ensuite de modifier assez aisément le résultat souhaité.
templates_multi = {
    # {{cf|tour d’échelle}}
    # {{cf|lang=fr|faire}}
    "cf": "f\"→ voir {parts[len(parts) - 1] if len(parts) > 1 else ''}\"",
    # {{comparatif de|bien|fr|adv}}
    "comparatif de": 'f"{capitalize(tpl)} {parts[1]}"',
    # {{couleur|#B0F2B6}}
    "couleur": 'f"(Code RGB {parts[1]})"',
    # {{fchim|H|2|O}}
    "fchim": 'f"{format_chimy(parts[1:])}"',
    # {{emploi|au passif}}
    "emploi": 'f"<i>({capitalize(parts[1])})</i>"',
    # {{forme pronominale|mutiner}}
    "forme pronominale": 'f"{capitalize(tpl)} de {parts[1]}"',
    # {{lien|étrange|fr}}
    "lien": "parts[1]",
    # {{nom w pc|Aldous|Huxley}}
    "nom w pc": 'f"{handle_name(parts)}"',
    # {{nombre romain|12}}
    "nombre romain": 'f"{int_to_roman(int(parts[1]))}"',
    # {{pron|plys|fr}}
    "pron": r'f"\\{parts[1]}\\"',
    # {{siècle2|XIX}}
    "siècle2": 'f"{parts[1]}ème"',
    # {{sport|fr}}
    # {{sport|fr|collectifs}}
    "sport": 'f"{handle_sport(tpl, parts)}"',
    # {{term|ne … guère que}}
    "term": 'f"{handle_term(parts[1])}"',
    # {{variante de|ranche|fr}}
    "variante de": 'f"{capitalize(tpl)} {parts[1]}"',
    # {{variante ortho de|acupuncture|fr}}
    "variante ortho de": 'f"Variante orthographique de {parts[1]}"',
}

# Modèles qui seront remplacés par du texte personnalisé.
templates_other = {
    # XIX{{e}}
    "e": "<sup>e</sup>",
    # {{term|au {{f}}}}
    "f": "féminin",
    # Bla bla bla. {{note}} Bla bla bla
    # Bla bla bla. {{note|fr}} Bla bla bla
    "note": "<b>Note :</b>",
    "peu attesté": "/!\\ Ce terme est très peu attesté.",
    # {{p}}
    "p": "<i>pluriel</i>",
    # Bla bla bla. {{usage}} Bla bla bla
    # Bla bla bla. {{usage|fr}} Bla bla bla
    "usage": "<b>Note d'usage :</b>",
}

# Traductions diverses
translations = {
    # Contenu de la release telle qu'elle sera générée sur
    # https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr
    "release_desc": """Nombre de mots : {words_count}
Export Wiktionnaire : {dump_date}

:arrow_right: Téléchargement : [dicthtml-fr.zip]({url})

---

<sub>Nombre total de téléchargements : {download_count}</sub>
<sub>Date de création du fichier : {creation_date}</sub>
""",
    # Séparateur des milliers
    "thousands_separator": " ",
}

# Le nom du dictionnaire qui sera affiché en-dessous de chaque définition
wiktionary = "Wiktionnaire (ɔ) {year}"
