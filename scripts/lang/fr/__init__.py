"""French language."""
from typing import Tuple

# Regex pour trouver la prononciation
pronunciation = r"{pron(?:\|lang=fr)?\|([^}\|]+)"

# Regexp pour trouver le genre
genre = r"{([fmsingp]+)(?: \?\|fr)*}"

# Séparateur des nombres à virgule
float_separator = ","

# Séparateur des milliers
thousands_separator = " "

# Titre des sections qui sont intéressantes à analyser.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_des_sections_de_types_de_mots
# Pour récupérer la liste complète des sections :
#     DEBUG=1 WIKI_DUMP=20200501 python -m scripts --locale fr --get-only
# Ensuite il faudra purger la liste et il restera les sections ci-dessous.
head_sections = ("{{langue|fr}}", "{{langue|conv}}")
etyl_section = "{{S|étymologie}}"
sections = (
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
    "{{S|étymologie}",
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

# Mot-clefs permettant de sélectionner la bonne étymologie
etyl_keywords = ("étyl",)

# Certaines définitions ne sont pas intéressantes à garder (pluriel, genre, ...)
definitions_to_ignore = (
    "pluriel d",
    "habitante",
    "masculin pluriel",
    "féminin pluriel",
    "''féminin de''",
    "féminin singulier",
    "masculin et féminin pluriel",
    "masculin ou féminin pluriel",
    "pluriel habituel",
    "pluriel inhabituel",
    "''pluriel''",
    "{exemple|",
    # Modèles spéciaux
    # "doute",
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
    ",",
    "ancre",
    "créer-séparément",
    "désabrévier",
    "graphie",
    "Import",
    "Modèle",
    "préciser",
    "R",
    "RÉF",
    "refnec",
    "réfnéc",
    "réfnec",
    "référence nécessaire",
    "réf",
    "réf?",
    "réf ?",
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
    # {{comparatif de|bien|fr|adv}}
    "comparatif de": "sentence(parts)",
    # {{cf}}
    # {{cf|tour d’échelle}}
    # {{cf|lang=fr|triner}}
    "cf": "f\"→ voir{' ' + italic(parts[1]) if len(parts) > 1 else ''}\"",
    # {{circa|1150}}
    "circa": "term('c. ' + parts[1])",
    # {{couleur|#B0F2B6}}
    "couleur": "color(parts[1])",
    # {{date}}
    # {{date|1850}}
    "date": "term(parts[1] if len(parts) > 1 else 'Date à préciser')",
    # {{fchim|H|2|O}}
    "fchim": "chimy(parts[1:])",
    # XIX{{e}}
    # {{e|-1}}
    "e": "superscript(parts[1] if len(parts) > 1 else 'e')",
    # {{er}}
    "er": "superscript('er')",
    # {{emploi|au passif}}
    "emploi": "term(capitalize(parts[1]))",
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
    # {{info lex|boulangerie}}
    # {{info lex|équitation|sport}}
    "info lex": "term(', '.join(parts[1:]))",
    # {{lexique|philosophie|fr}}
    # {{lexique|philosophie|sport|fr}}
    "lexique": "term(', '.join(capitalize(p) for p in parts[1:-1]))",
    # {{nobr|1 000 000 000 000}}
    "nobr": "re.sub(r'^1=', '', parts[-1].replace(' ', '&nbsp;').replace('!', '|'))",
    # {{nom w pc|Aldous|Huxley}}
    "nom w pc": "person(word, parts[1:])",
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
    "région": "term(capitalize(parts[1] if len(parts) > 1 else 'régionalisme'))",
    # {{siècle2|XIX}}
    "siècle2": 'f"{parts[1]}ème"',
    # {{smcp|Dupont}}
    "smcp": "small_caps(parts[1])",
    # {{sport|fr}}
    # {{sport|fr|collectifs}}
    "sport": "term(capitalize(concat(parts, sep=' ', indexes=[0, 2])))",
    # {{superlatif de|petit|fr}}
    "superlatif de": "sentence(parts)",
    # {{term|ne … guère que}}
    "term": "term(capitalize(parts[1]))",
    # {{terme|Astrophysique}}
    "terme": "term(capitalize(parts[1]))",
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
    "!": "!",
    "=": "=",
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


def last_template_handler(template: Tuple[str, ...], locale: str) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["recons", "maruos"], "fr")
        '*<i>maruos</i>'
        >>> last_template_handler(["recons", "maruos", "gaul"], "fr")
        '*<i>maruos</i>'
        >>> last_template_handler(["recons", "maruos", "gaul", "sens=mort"], "fr")
        '*<i>maruos</i> (« mort »)'
        >>> last_template_handler(["recons", "lang-mot-vedette=fr", "sporo", "sc=Latn"], "fr")
        '*<i>sporo</i>'

        >>> last_template_handler(["polytonique", "μηρóς", "mêrós", "cuisse"], "fr")
        'μηρóς, <i>mêrós</i> (« cuisse »)'
        >>> last_template_handler(["polytonique", "φόβος", "phóbos", "sens=effroi, peur"], "fr")
        'φόβος, <i>phóbos</i> (« effroi, peur »)'

        >>> last_template_handler(["lien", "渦", "zh-Hans"], "fr")
        '渦'
        >>> last_template_handler(["lien", "フランス", "ja", "sens=France"], "fr")
        'フランス (« France »)'
        >>> last_template_handler(["lien", "フランス", "ja", "tr=Furansu", "sens=France"], "fr")
        'フランス, <i>Furansu</i> (« France »)'
        >>> last_template_handler(["lien", "camara", "sens=voute, plafond vouté", "la"], "fr")
        'camara (« voute, plafond vouté »)'

        >>> last_template_handler(["étyl", "grc", "fr"], "fr")
        'grec ancien'
        >>> last_template_handler(["étyl", "la", "fr", "dithyrambicus"], "fr")
        'latin <i>dithyrambicus</i>'
        >>> last_template_handler(["étyl", "no", "fr", "mot=ski"], "fr")
        'norvégien <i>ski</i>'
        >>> last_template_handler(["étyl", "la", "fr", "mot=invito", "type=verb"], "fr")
        'latin <i>invito</i>'
        >>> last_template_handler(["étyl", "grc", "fr", "mot=λόγος", "tr=lógos", "type=nom", "sens=étude"], "fr")
        'grec ancien λόγος, <i>lógos</i> (« étude »)'
        >>> last_template_handler(["étyl", "grc", "fr", "λόγος", "lógos", "étude", "type=nom", "lien=1"], "fr")
        'grec ancien λόγος, <i>lógos</i> (« étude »)'
        >>> last_template_handler(["étyl", "la", "fr", "mot=jugulum", "sens=endroit où le cou se joint aux épaules = la gorge"], "fr")  # noqa
        'latin <i>jugulum</i> (« endroit où le cou se joint aux épaules = la gorge »)'
        >>> last_template_handler(["étyl", "la", "fr", "mot=subgrunda", "tr", "sens=même sens"], "fr")
        'latin <i>subgrunda</i> (« même sens »)'
        >>> last_template_handler(["étyl", "grc", "fr", "mot="], "fr")
        'grec ancien'
        >>> last_template_handler(['étyl', 'grc', 'mot=ὑπόθεσις', 'tr=hupóthesis', 'sens=action de mettre dessous', 'nocat=1'], "fr")
        'grec ancien ὑπόθεσις, <i>hupóthesis</i> (« action de mettre dessous »)'
        >>> last_template_handler(["étyl", "grc", "fr", "tr=leipein", "sens=abandonner"], "fr")
        'grec ancien <i>leipein</i> (« abandonner »)'
        >>> last_template_handler(["étyl", "1=grc", "2=es", "mot=νακτός", "tr=naktós", "sens=dense"], "fr")
        'grec ancien νακτός, <i>naktós</i> (« dense »)'

        >>> last_template_handler(["étylp", "la", "fr", "mot=Ladon"], "fr")
        'latin <i>Ladon</i>'

        >>> last_template_handler(["calque", "la", "fr"], "fr")
        'latin'
        >>> last_template_handler(["calque", "en", "fr", "mot=to date", "sens=à ce jour"], "fr")
        'anglais <i>to date</i> (« à ce jour »)'
        >>> last_template_handler(["calque", "sa", "fr", "mot=वज्रयान", "tr=vajrayāna", "sens=véhicule du diamant"], "fr")
        'sanskrit वज्रयान, <i>vajrayāna</i> (« véhicule du diamant »)'

        >>> last_template_handler(["composé de", "longus", "aevum", "lang=la"], "fr")
        'composé de <i>longus</i> et de <i>aevum</i>'
        >>> last_template_handler(["composé de", "longus", "aevum", "lang=la", "f=1"], "fr")
        'composée de <i>longus</i> et de <i>aevum</i>'
        >>> last_template_handler(["composé de", "longus", "sens1=long", "aevum", "sens2=temps", "lang=la", "m=1"], "fr")
        'Composé de <i>longus</i> (« long ») et de <i>aevum</i> (« temps »)'
        >>> last_template_handler(["composé de", "longus", "aevum", "sens=long temps", "lang=la"], "fr")
        'composé de <i>longus</i> et de <i>aevum</i>, littéralement « long temps »'
        >>> last_template_handler(["composé de", "δῆμος", "tr1=dêmos", "sens1=peuple", "ἀγωγός", "tr2=agōgós", "sens2=guide", "sens=celui qui guide le peuple", "lang=grc", "m=1"], "fr")
        'Composé de δῆμος, <i>dêmos</i> (« peuple ») et de ἀγωγός, <i>agōgós</i> (« guide »), littéralement « celui qui guide le peuple »'
        >>> last_template_handler(["composé de", "anti-", "quark", "lang=en"], "fr")
        'dérivé de <i>quark</i> avec le préfixe <i>anti-</i>'
        >>> last_template_handler(["composé de", "anti-", "quark", "lang=en", "m=1", "f=1"], "fr")
        'Dérivée de <i>quark</i> avec le préfixe <i>anti-</i>'
        >>> last_template_handler(["composé de", "clear", "-ly", "lang=en", "m=1"], "fr")
        'Dérivé de <i>clear</i> avec le suffixe <i>-ly</i>'
        >>> last_template_handler(["composé de", "느낌", "tr1=neukkim", "sens1=sensation", "표", "tr2=-pyo", "sens2=symbole", "lang=ko", "m=1"], "fr")
        'Dérivé de 느낌, <i>neukkim</i> (« sensation ») avec le suffixe 표, <i>-pyo</i> (« symbole »)'

        >>> last_template_handler(["siècle"], "fr")
        '<i>(Siècle à préciser)</i>'
        >>> last_template_handler(["siècle", "lang=fr", "?"], "fr")
        '<i>(Siècle à préciser)</i>'
        >>> last_template_handler(["siècle", "", "lang=fr"], "fr")
        '<i>(Siècle à préciser)</i>'
        >>> last_template_handler(["siècle", "XVIII"], "fr")
        '<i>(XVIII<sup>e</sup> siècle)</i>'
        >>> last_template_handler(["siècle", "lang=fr", "XVIII"], "fr")
        '<i>(XVIII<sup>e</sup> siècle)</i>'
        >>> last_template_handler(["siècle", "XVIII", "XIX"], "fr")
        '<i>(XVIII<sup>e</sup> siècle - XIX<sup>e</sup> siècle)</i>'
    """
    from collections import defaultdict

    from .langs import langs
    from ..defaults import last_template_handler as default
    from ...user_functions import century, italic, term

    tpl = template[0]
    parts = list(template[1:])

    # Handle {{étyl}}, {{étylp}} and {{calque}} templates
    if tpl in ("étyl", "étylp", "calque"):
        parts = [p.replace("1=", "").replace("2=", "") for p in parts]
        kw_parts = [p for p in parts if "=" in p]
        simple_parts = [p for p in parts if "=" not in p]

        # The lang name
        phrase = langs[simple_parts.pop(0)]

        data = {"mot": "", "sens": "", "tr": ""}
        for part in kw_parts:
            key, value = part.split("=", 1)
            data[key] = value

        for part in simple_parts:
            if part in langs:
                continue
            if not data["mot"]:
                data["mot"] = part
            elif not data["tr"]:
                data["tr"] = part
            elif not data["sens"]:
                data["sens"] = part

        if data["tr"]:
            if data["mot"]:
                phrase += f" {data['mot']},"
            phrase += f" {italic(data['tr'])}"
        elif data["mot"]:
            phrase += f" {italic(data['mot'])}"
        if data["sens"]:
            phrase += f" (« {data['sens']} »)"

        return phrase

    # Handle {{composé de}} template
    if tpl == "composé de":
        data = defaultdict(str)
        for part in parts.copy():
            if "=" in part:
                key, value = part.split("=", 1)
                data[key] = value
                parts.pop(parts.index(part))

        is_derived = any(part.startswith("-") or part.endswith("-") for part in parts)
        is_derived |= any(
            part.startswith("-") or part.endswith("-") for part in data.values()
        )

        if is_derived:
            # Dérivé
            phrase = "D" if "m" in data else "d"
            phrase += "érivée de " if "f" in data else "érivé de "

            parts = sorted(parts, key=lambda part: "-" in part)

            multiple = len(parts) > 2
            for number, part in enumerate(parts, 1):
                is_prefix = part.endswith("-") or data.get(f"tr{number}", "").endswith(
                    "-"
                )
                is_suffix = part.startswith("-") or data.get(
                    f"tr{number}", ""
                ).startswith("-")
                phrase += "préfixe " if is_prefix else "suffixe " if is_suffix else ""

                phrase += f"{part}" if f"tr{number}" in data else f"{italic(part)}"
                if f"tr{number}" in data:
                    idx = f"tr{number}"
                    phrase += f", {italic(data[idx])}"
                if f"sens{number}" in data:
                    idx = f"sens{number}"
                    phrase += f" (« {data[idx]} »)"

                phrase += (
                    " avec le "
                    if number == len(parts) - 1
                    else ", "
                    if multiple
                    else ""
                )

            if "sens" in data:
                phrase += f", littéralement « {data['sens']} »"

            return phrase

        # Composé
        phrase = "C" if "m" in data else "c"
        phrase += "omposée de " if "f" in data else "omposé de "

        multiple = len(parts) > 2
        for number, part in enumerate(parts, 1):
            phrase += f"{part}" if f"tr{number}" in data else f"{italic(part)}"
            if f"tr{number}" in data:
                idx = f"tr{number}"
                phrase += f", {italic(data[idx])}"
            if f"sens{number}" in data:
                idx = f"sens{number}"
                phrase += f" (« {data[idx]} »)"

            phrase += (
                " et de " if number == len(parts) - 1 else ", " if multiple else ""
            )

        if "sens" in data:
            phrase += f", littéralement « {data['sens']} »"

        return phrase

    # Handle the {{recons}} template
    if tpl in ("recons", "forme reconstruite"):
        phrase = ""
        extension = ""
        for part in parts:
            if part.startswith("sens="):
                extension = f" (« {part.split('=', 1)[1]} »)"
            elif "=" in part:
                continue
            elif not phrase:
                phrase = italic(part)
        return f"*{phrase}{extension}"

    # Handle the {{polytonique}} template
    if tpl == "polytonique":
        phrase = parts[0]
        if len(parts) > 1:
            phrase += f", {italic(parts[1].replace('tr=', ''))}"
        if len(parts) > 2:
            phrase += f" (« {parts[2].replace('sens=', '')} »)"
        return phrase

    # Handle the {{lien}} template
    if tpl == "lien":
        phrase = parts[0]
        for part in parts[1:]:
            if part.startswith("tr="):
                phrase += f", {italic(part.split('tr=', 1)[1])}"
            elif part.startswith("sens="):
                phrase += f" (« {part.split('sens=', 1)[1]} »)"
        return phrase

    # Handle the {{siècle}} template
    if tpl == "siècle":
        parts = [
            part for part in parts if part.strip() and part not in ("lang=fr", "?")
        ]
        phrase = century(parts, "siècle") if parts else "Siècle à préciser"
        return term(phrase)

    # This is a country in the current locale
    if tpl in langs:
        return langs[tpl]

    return default(template, locale)


# Contenu de la release sur GitHub :
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr
release_description = """\
Nombre de mots : {words_count}
Export Wiktionnaire : {dump_date}

:arrow_right: Téléchargement : [dicthtml-{locale}.zip]({url})

---

Installation :

1. Copier le fichier `dicthtml-{locale}.zip` dans le dossier `.kobo/dict/` de la liseuse.
2. Redémarrer la liseuse.

---

Caractéristiques :

- Les noms propres ne sont pas inclus.
- Les conjugaisons ne sont pas incluses.

<sub>Mis à jour le {creation_date}</sub>
"""

# Le nom du dictionnaire qui sera affiché en-dessous de chaque définition
wiktionary = "Wiktionnaire (ɔ) {year}"
