"""French language."""

# Regex pour trouver la prononciation
pronunciation = r"{pron\|([^}\|]+)"

# Regexp pour trouver le genre
genre = r"{([fmsingp]+)}"

# Titre des sections qui sont intéressantes à analyser.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_des_sections_de_types_de_mots
# Pour récupérer la liste complète des sections :
#     DEBUG=1 WIKI_DUMP=20200501 python -m scripts --locale fr --get-only
# Ensuite il faudra purger la liste et il restera les sections ci-dessous.
patterns = (
    "{{S|abréviations}",
    "{{S|adjectif démonstratif|fr|",
    "{{S|adjectif démonstratif|fr}",
    "{{S|adjectif exclamatif|fr|",
    "{{S|adjectif exclamatif|fr}",
    "{{S|adjectif indéfini|fr|",
    "{{S|adjectif indéfini|fr}",
    "{{S|adjectif interrogatif|fr|",
    "{{S|adjectif interrogatif|fr}",
    "{{S|adjectif numéral|fr|",
    "{{S|adjectif numéral|fr}",
    "{{S|adjectif possessif|fr|",
    "{{S|adjectif possessif|fr}",
    "{{S|adjectif relatif|fr}",
    "{{S|adjectif|conv",
    "{{S|adjectif|fr|",
    "{{S|adjectif|fr}",
    "{{S|adj|fr|",
    "{{S|adj|fr}",
    "{{S|adverbe interrogatif|fr}",
    "{{S|adverbe relatif|fr}",
    "{{S|adverbe|conv",
    "{{S|adverbe|fr|",
    "{{S|adverbe|fr}",
    "{{S|article défini|fr|",
    "{{S|article défini|fr}",
    "{{S|article indéfini|fr|",
    "{{S|article indéfini|fr}",
    "{{S|article partitif|fr|",
    "{{S|article partitif|fr}",
    "{{S|conjonction de coordination|fr}",
    "{{S|conjonction|fr|",
    "{{S|conjonction|fr}",
    "{{S|erreur|fr|",
    "{{S|erreur|fr}",
    "{{S|interfixe|fr}",
    "{{S|interjection|fr|",
    "{{S|interjection|fr}",
    "{{S|lettre|fr}",
    "{{S|locution-phrase|fr|",
    "{{S|locution-phrase|fr}",
    "{{S|nom commun|fr|",
    "{{S|nom commun|fr}",
    "{{S|nom scientifique|",
    "{{S|nom|conv",
    "{{S|nom|fr|",
    "{{S|nom|fr}",
    "{{S|numéral|conv",
    "{{S|onomatopée|fr}",
    "{{S|particule|fr}",
    "{{S|postposition|fr}",
    "{{S|pronom démonstratif|fr|",
    "{{S|pronom démonstratif|fr}",
    "{{S|pronom indéfini|fr|",
    "{{S|pronom indéfini|fr}",
    "{{S|pronom interrogatif|fr|",
    "{{S|pronom interrogatif|fr}",
    "{{S|pronom personnel|fr|",
    "{{S|pronom personnel|fr}",
    "{{S|pronom possessif|fr|",
    "{{S|pronom possessif|fr}",
    "{{S|pronom relatif|fr|",
    "{{S|pronom relatif|fr}",
    "{{S|pronom|fr|",
    "{{S|pronom|fr}",
    "{{S|préfixe|conv",
    "{{S|préfixe|fr|",
    "{{S|préfixe|fr}",
    "{{S|prénom|fr|",
    "{{S|prénom|fr}",
    "{{S|préposition|fr|",
    "{{S|préposition|fr}",
    "{{S|substantif|fr}",
    "{{S|suffixe|conv",
    "{{S|suffixe|fr|",
    "{{S|suffixe|fr}",
    "{{S|symbole|conv",
    "{{S|symbole|fr|",
    "{{S|symbole|fr}",
    "{{S|variante typographique|fr|",
    "{{S|variante typographique|fr}",
    "{{S|verbe|fr|loc",
    "{{S|verbe|fr|num",
    "{{S|verbe|fr}",
)

# Séparateur des nombres à virgule
float_separator = ","

# Séparateur des milliers
thousands_separator = " "

# Certaines définitions ne sont pas intéressantes à garder (pluriel, genre, ...)
definitions_to_ignore = (
    "pluriel d",
    "habitante",
    "masculin pluriel d",
    "féminin pluriel",
    "féminin singulier d",
    "masculin et féminin pluriel d",
    "masculin ou féminin pluriel d",
    "pluriel habituel d",
    "pluriel inhabituel d",
)

# Malgré tout, même si une définition est sur le point d'être ignorée (via definitions_to_ignore),
# alors ces mots seront tout de même conservés.
# https://fr.wikipedia.org/wiki/Pluriels_irr%C3%A9guliers_en_fran%C3%A7ais
words_to_keep = (
    "aspiraux",  # pluriel irrégulier
    "aulx",  # pluriel irrégulier
    "baux",  # pluriel irrégulier
    "cieux",  # pluriel irrégulier
    "cris",  # "Cris" aura la priorité sinon
    "coraux",  # pluriel irrégulier
    "émaux",  # pluriel irrégulier
    "fermaux",  # pluriel irrégulier
    "gemmaux",  # pluriel irrégulier
    "soupiraux",  # pluriel irrégulier
    "travaux",  # pluriel irrégulier
    "vantaux",  # pluriel irrégulier
    "ventaux",  # pluriel irrégulier
    "vitraux",  # pluriel irrégulier
    "yeux",  # pluriel irrégulier
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
    "graphie",
    "Import",
    "Modèle",
    "préciser",
    "R",
    "refnec",
    "réfnéc",
    "réfnec",
    "référence nécessaire",
    "réf",
    "réf?",
    "source",
    "source?",
    "trad-exe",
    "trier",
)

# Modèles qui seront remplacés par du texte italique.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les
templates_italic = {
    "abréviation": "Abréviation",
    "absol": "Absolument",
    "adj-indéf-avec-de": "Avec de",
    "admin": "Administration",
    "aéro": "Aéronautique",
    "agri": "Agriculture",
    "agrumes": "Botanique",
    "alcaloïdes": "Chimie",
    "analogie": "Par analogie",
    "angl": "Anglicisme",
    "animaux": "Zoologie",
    "anat": "Anatomie",
    "antiq": "Antiquité",
    "apposition": "En apposition",
    "arbres": "Botanique",
    "arch": "Archaïsme",
    "archaïque": "Archaïsme",
    "archi": "Architecture",
    "Argadz": "Argot des Gadz’Arts",
    "argot internet": "Argot Internet",
    "argot typographes": "Argot des typographes",
    "argot voleurs": "Argot des voleurs",
    "astron": "Astronomie",
    "atomes": "Chimie",
    "au figuré": "Figuré",
    "audiovi": "Audiovisuel",
    "auto": "Automobile",
    "automo": "Automobile",
    "avant 1835": "Archaïque, orthographe d’avant 1835",
    "BD": "Bande dessinée",
    "BDD": "Bases de données",
    "BE": "Belgique",
    "bactéries": "Bactériologie",
    "bateaux": "Navigation",
    "bdd": "Bases de données",
    "bioch": "Biochimie",
    "biol": "Biologie",
    "b-m-cour": "Beaucoup moins courant",
    "boissons": "Boisson",
    "botan": "Botanique",
    "bot.": "Botanique",
    "bovins": "Zoologie",
    "CA": "Canada",
    "CH": "Suisse",
    "CI": "Côte d’Ivoire",
    "canards": "Ornithologie",
    "caprins": "Zoologie",
    "cartes": "Cartes à jouer",
    "catholicisme": "Christianisme",
    "champignons": "Mycologie",
    "chaussures": "Vêtement",
    "chiens": "Zoologie",
    "chim": "Chimie",
    "chir": "Chirurgie",
    "ciné": "Cinéma",
    "cnidaires": "Zoologie",
    "cours d’eau": "Géographie",
    "cuis": "Cuisine",
    "comm": "Commerce",
    "commerces": "Commerce",
    "composants": "Électronique",
    "compta": "Comptabilité",
    "constr": "Construction",
    "coquillages": "Coquillage",
    "cour": "Courant",
    "cout": "Couture",
    "couvre-chefs": "Habillement",
    "cycl": "Cyclisme",
    "cétacés": "Mammalogie",
    "danses": "Danse",
    "dermatol": "Dermatologie",
    "didact": "Didactique",
    "diacritiques": "Grammaire",
    "dinosaures": "Paléontologie",
    "diplo": "Diplomatie",
    "EU": "Europe",
    "élec": "Électricité",
    "ellipse": "Par ellipse",
    "enclit": "Enclitique",
    "enfantin": "Langage enfantin",
    "entomol": "Entomologie",
    "euph": "Par euphémisme",
    "euphém": "Par euphémisme",
    "euphémisme": "Par euphémisme",
    "ex-rare": "Extrêmement rare",
    "exag": "Par hyperbole",
    "exagération": "Par hyperbole",
    "écolo": "Écologie",
    "écon": "Économie",
    "éduc": "Éducation",
    "électoraux": "Systèmes électoraux",
    "éléments": "Chimie",
    "énergie": "Industrie de l’énergie",
    "épithète": "Employé comme épithète",
    "FR": "France",
    "familles de plantes": "Botanique",
    "ferro": "Chemin de fer",
    "ferroviaire": "Chemin de fer",
    "figure": "Rhétorique",
    "figures": "Rhétorique",
    "finan": "Finance",
    "finances": "Finance",
    "fonderie": "Métallurgie",
    "formations musicales": "Musique",
    "formel": "Soutenu",
    "fortification": "Architecture",
    "fromages": "Fromage",
    "fruits": "Botanique",
    "gastronomie": "Cuisine",
    "genres musicaux": "Musique",
    "gentilés": "Géographie",
    "germ": "Germanisme",
    "giraffidés": "Zoologie",
    "grades": "Militaire",
    "graphe": "Théorie des graphes",
    "gâteaux": "Cuisine",
    "géog": "Géographie",
    "géol": "Géologie",
    "géom": "Géométrie",
    "géoph": "Géophysique",
    "habil": "Habillement",
    "hérald": "Héraldique",
    "hippisme": "Sports hippiques",
    "hist": "Histoire",
    "horlog": "Horlogerie",
    "hyperb": "Par hyperbole",
    "hyperbole": "Par hyperbole",
    "IDLMadeleine": "Îles-de-la-Madeleine",
    "idiomatique": "Figuré",
    "impr": "Imprimerie",
    "improprement": "Usage critiqué",
    "indén": "Indénombrable",
    "indus": "Industrie",
    "info": "Informatique",
    "injur": "Injurieux",
    "insectes": "Entomologie",
    "insultes": "Insulte",
    "intrans": "Intransitif",
    "iron": "Ironique",
    "jardi": "Jardinage",
    "juri": "Droit",
    "jurisprudence": "Droit",
    "just": "Justice",
    "langues": "Linguistique",
    "lapins": "Zoologie",
    "lianes": "Botanique",
    "ling": "Linguistique",
    "litt": "Littéraire",
    "logi": "Logique",
    "légis": "Droit",
    "légumes": "Botanique",
    "maçon": "Maçonnerie",
    "maladie": "Nosologie",
    "maladies": "Nosologie",
    "mammifères": "Zoologie",
    "manège": "Équitation",
    "marque": "Marque commerciale",
    "math": "Mathématiques",
    "méc": "Mécanique",
    "médecine non conv": "Médecine non conventionnelle",
    "mélio": "Mélioratif",
    "menu": "Menuiserie",
    "mercatique": "Marketing",
    "métrol": "Métrologie",
    "meubles": "Mobilier",
    "meubles héraldiques": "Héraldique",
    "mili": "Militaire",
    "minér": "Minéralogie",
    "minéraux": "Minéralogie",
    "mollusques": "Malacologie",
    "montagnes": "Géographie",
    "monnaies": "Numismatique",
    "mouches": "Entomologie",
    "muscles": "Anatomie",
    "musi": "Musique",
    "mythol": "Mythologie",
    "méca": "Mécanique",
    "méde": "Médecine",
    "métal": "Métallurgie",
    "métaph": "Figuré",
    "métaphore": "Figuré",
    "métaplasmes": "Linguistique",
    "météo": "Météorologie",
    "météorol": "Météorologie",
    "méton": "Par métonymie",
    "métonymie": "Par métonymie",
    "muscle": "Anatomie",
    "neurol": "Neurologie",
    "nom-coll": "Nom collectif",
    "nuages": "Météorologie",
    "nucl": "Nucléaire",
    "numis": "Numismatique",
    "néol": "Néologisme",
    "oenol": "Œnologie",
    "oiseaux": "Ornithologie",
    "opti": "Optique",
    "ornithol": "Ornithologie",
    "ortho1990": "Orthographe rectifiée de 1990",
    "ovins": "Zoologie",
    "POO": "Programmation orientée objet",
    "p us": "Peu usité",
    "paléogr": "Paléographie",
    "par ext": "Par extension",
    "part": "En particulier",
    "partic": "En particulier",
    "particulier": "En particulier",
    "pathologie": "Nosologie",
    "pâtes": "Cuisine",
    "peupliers": "Botanique",
    "pêch": "Pêche",
    "péj": "Péjoratif",
    "philo": "Philosophie",
    "photo": "Photographie",
    "phys": "Physique",
    "pl-rare": "Plus rare",
    "plais": "Par plaisanterie",
    "planètes": "Astronomie",
    "plantes": "Botanique",
    "pléonasmes": "Pléonasme",
    "poés": "Poésie",
    "poissons": "Ichtyologie",
    "polit": "Politique",
    "pommes": "Botanique",
    "popu": "Populaire",
    "poules": "Élevage",
    "presse": "Journalisme",
    "primates": "Zoologie",
    "procédure": "Justice",
    "prog": "Programmation informatique",
    "programmation": "Programmation informatique",
    "pronl": "Pronominal",
    "propre": "Sens propre",
    "propriété": "Droit",
    "propulsion": "Propulsion spatiale",
    "protéines": "Biochimie",
    "prov": "Proverbial",
    "prunes": "Botanique",
    "préparations": "Cuisine",
    "psychia": "Psychiatrie",
    "psychol": "Psychologie",
    "QC": "Québec",
    "RDC": "Congo-Kinshasa",
    "RDCongo": "Congo-Kinshasa",
    "raies": "Ichtyologie",
    "reli": "Religion",
    "religieux": "Religion",
    "reptiles": "Herpétologie",
    "roches": "Pétrographie",
    "régional": "Régionalisme",
    "réseaux": "Réseaux informatiques",
    "salades": "Cuisine",
    "salles": "Construction",
    "saules": "Botanique",
    "sci-fi": "Science-fiction",
    "scol": "Éducation",
    "scolaire": "Éducation",
    "serpents": "Herpétologie",
    "sexe": "Sexualité",
    "sigle": "Sigle",
    "singes": "Zoologie",
    "sociol": "Sociologie",
    "soldats": "Militaire",
    "sout": "Soutenu",
    "spéc": "Spécialement",
    "sports": "Sport",
    "stat": "Statistiques",
    "substances": "Chimie",
    "sylv": "Sylviculture",
    "TAAF": "Vocabulaire des TAAF",
    "tech": "Technique",
    "technol": "Technologie",
    "temps": "Chronologie",
    "text": "Textile",
    "textiles": "Textile",
    "théât": "Théâtre",
    "théol": "Théologie",
    "thérapies": "Médecine",
    "télécom": "Télécommunications",
    "tortues": "Zoologie",
    "tr-fam": "Très familier",
    "trans": "Transitif",
    "transit": "Transitif",
    "transports": "Transport",
    "tradit": "orthographe traditionnelle",
    "typo": "Typographie",
    "typog": "Typographie",
    "télé": "Audiovisuel",
    "US": "États-Unis",
    "USA": "États-Unis",
    "unités": "Métrologie",
    "usines": "Industrie",
    "vents": "Météorologie",
    "vieux": "Vieilli",
    "vélo": "Cyclisme",
    "vête": "Habillement",
    "vêtements": "Habillement",
    "zool": "Zoologie",
    "zootechnie": "Zoologie",
}

# Modèles un peu plus complexes à gérer, leur prise en charge demande plus de travail.
# Le code de droite sera passer à une fonction qui l'exécutera. Il est possible d'utiliser
# n'importe quelle fonction Python et celles définies dans user_functions.py.
#
# # Les arguments disponibles sont :
#   - *tpl* (texte) qui contient le nom du modèle.
#   - *parts* (liste de textes) qui contient les toutes parties du modèle.
#
# Exemple avec le modèle complet "{{comparatif de|bien|fr|adv}}" :
#   - *tpl* contiendra le texte "comparatif de".
#   - *parts* contiendra la liste ["comparatif de", "bien", "fr", "adv"].
#
# L'accès à *tpl* et *parts* permet ensuite de modifier assez aisément le résultat souhaité.
#
# Un documentation des fonctions disponibles se trouve dans le fichier HTML suivant :
#   html/scripts/user_functions.html
templates_multi = {
    # {{calque|en|fr|mot=at the end of the day|nocat=1}}
    "calque": "etymology(parts)",
    # {{cf|tour d’échelle}}
    # {{cf|lang=fr|faire}}
    "cf": "f\"→ voir {parts[len(parts) - 1] if len(parts) > 1 else ''}\"",
    # {{comparatif de|bien|fr|adv}}
    "comparatif de": "sentence(parts)",
    # {{couleur|#B0F2B6}}
    "couleur": 'f"[RGB {parts[1]}]"',
    # {{date|1850}}
    "date": "term(parts[1])",
    # {{fchim|H|2|O}}
    "fchim": "chimy(parts[1:])",
    # XIX{{e}}
    # {{e|-1}}
    "e": "superscript(parts[1] if len(parts) > 1 else 'e')",
    # {{er}}
    "er": "superscript('er')",
    # {{emploi|au passif}}
    "emploi": "term(parts[1])",
    # {{étyl|la|fro|mot=invito|type=verb}}
    "étyl": "etymology(parts)",
    # {{#expr: 2 ^ 30}}
    "#expr": "eval_expr(parts[1])",
    # {{formatnum:-1000000}}
    "formatnum": f'number(parts[1], "{float_separator}", "{thousands_separator}")',
    # {{forme pronominale|mutiner}}
    "forme pronominale": 'f"{capitalize(tpl)} de {parts[1]}"',
    # {{in|5}}
    "in": "subscript(parts[1])",
    # {{indice|n}}
    "indice": "subscript(parts[1])",
    # {{lien|étrange|fr}}
    "lien": "parts[1]",
    # {{nom w pc|Aldous|Huxley}}
    "nom w pc": "person(parts[1:])",
    # {{nombre romain|12}}
    "nombre romain": "int_to_roman(int(parts[1]))",
    # {{petites capitales|Dupont}}
    "petites capitales": "small_caps(parts[1])",
    # {{pc|Dupont}}
    "pc": "small_caps(parts[1])",
    # {{pron|plys|fr}}
    "pron": r'f"\\{parts[1]}\\"',
    # {{pron-API|/j/}}
    "pron-API": "parts[1]",
    # {{RFC|5322}}
    "RFC": "sentence(parts)",
    # {{région}}
    # {{région|Lorraine et Dauphiné}}
    "région": "term(parts[1] if len(parts) > 1 else 'Régionalisme')",
    # {{siècle|XVI}}
    # {{siècle|XVIII|XIX}}
    "siècle": "term(century(parts, 'siècle'))",
    # {{siècle2|XIX}}
    "siècle2": 'f"{parts[1]}ème"',
    # {{smcp|Dupont}}
    "smcp": "small_caps(parts[1])",
    # {{sport|fr}}
    # {{sport|fr|collectifs}}
    "sport": "term(concat(parts, sep=' ', indexes=[0, 2]))",
    # {{superlatif de|petit|fr}}
    "superlatif de": "sentence(parts)",
    # {{term|ne … guère que}}
    "term": "term(parts[1])",
    # {{terme|Astrophysique}}
    "terme": "term(parts[1])",
    # {{trad+|conv|Sitophilus granarius}}
    "trad+": "parts[2]",
    # {{unité|92|%}}
    "unité": "concat(parts[1:])",
    # {{variante de|ranche|fr}}
    "variante de": "sentence(parts)",
    # {{variante ortho de|acupuncture|fr}}
    "variante ortho de": 'f"Variante orthographique de {parts[1]}"',
    "variante orthographique de": 'f"Variante orthographique de {parts[1]}"',
    # {{wp|Sarcoscypha coccinea}}
    "wp": 'italic(f"{parts[1]} sur l\'encyclopédie Wikipedia")',
    # {{ws|Bible Segond 1910/Livre de Daniel|Livre de Daniel}}
    # {{ws|Les Grenouilles qui demandent un Roi}}
    "ws": "parts[2] if len(parts) > 2 else parts[1]",
    # {{wsp|Panthera pardus|''Panthera pardus''}}
    # {{wsp|Brassicaceae}}
    "wsp": "parts[2] if len(parts) > 2 else parts[1]",
    # {{WSP|Panthera leo}}
    "WSP": "term(parts[1])",
}

# Modèles qui seront remplacés par du texte personnalisé.
templates_other = {
    "absolu": "<i>absolu</i>",
    "antonomase": "antonomase",
    "aphérèse": "<i>aphérèse</i>",
    "apocope": "Apocope",
    "apJC": "apr. J.-C.",
    "au singulier uniquement": "<i>au singulier uniquement</i>",
    "au pluriel uniquement": "<i>au pluriel uniquement</i>",
    "avJC": "av. J.-C.",
    "collectif": "<i>collectif</i>",
    "contraction": "contraction",
    "dépendant": "<i>dépendant</i>",
    "déterminé": "déterminé",
    "f": "<i>féminin</i>",
    "fm": "féminin ou masculin (l’usage hésite)",
    "fplur": "<i>féminin pluriel</i>",
    "genre ?": "Genre à préciser",
    "i": "<i>intransitif</i>",
    "impers": "<i>impersonnel</i>",
    "indéterminé": "indéterminé",
    "invar": "<i>invariable</i>",
    "m": "<i>masculin</i>",
    "majus": "<i>majuscule</i>",
    "mf": "<i>masculin et féminin identiques</i>",
    "mf ?": "<i>masculin ou féminin (l’usage hésite)</i>",
    "minus": "<i>minuscule</i>",
    "mot-valise": "mot-valise",
    "mplur": "<i>masculing pluriel</i>",
    "msing": "<i>masculing singulier</i>",
    "nombre ?": "Nombre à préciser",
    "note": "<b>Note :</b>",
    "peu attesté": "/!\\ Ce terme est très peu attesté.",
    "p": "<i>pluriel</i>",
    "palind": "<i>palindrome</i>",
    "prnl": "<i>pronominal</i>",
    "s": "<i>singulier</i>",
    "sp": "<i>singulier et pluriel identiques</i>",
    "sp ?": "<i>singulier et pluriel identiques ou différenciés (l’usage hésite)</i>",
    "réfl": "<i>réfléchi</i>",
    "réciproque": "<i>réciproque</i>",
    "t": "<i>transitif</i>",
    "tr-dir": "<i>transitif direct</i>",
    "tr-indir": "<i>transitif indirect</i>",
    "usage": "<b>Note d'usage :</b>",
    "WP": "sur l'encyclopédie Wikipedia",
}

# Le parseur affichera un avertissement quand un modèle contient des espaces superflus,
# sauf pour ceux listés ci-dessous :
templates_warning_skip = ("fchim", "graphie", "lien web", "ouvrage", "source")

# Contenu de la release sur GitHub :
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr
release_description = """\
Nombre de mots : {words_count}
Export Wiktionnaire : {dump_date}

:arrow_right: Téléchargement : [dicthtml-fr.zip]({url})

---

Installation :

1. Copier le fichier `dicthtml-fr.zip` dans le dossier `.kobo/dict/` de la liseuse.
2. Redémarrer la liseuse.

---

Caractéristiques :

- Seules les définitions sont incluses : il n'y a ni les citations ni l'éthymologie.
- Les mots comportant moins de 2 caractères ne sont pas inclus.
- Les noms propres ne sont pas inclus.
- Les conjugaisons ne sont pas incluses.

<sub>Mis à jour le {creation_date}</sub>
"""

# Le nom du dictionnaire qui sera affiché en-dessous de chaque définition
wiktionary = "Wiktionnaire (ɔ) {year}"
