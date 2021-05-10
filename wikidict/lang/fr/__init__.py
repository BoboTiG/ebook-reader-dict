"""French language."""
from typing import Tuple

from .arabiser import arabiser
from .domain_templates import domain_templates
from .regions import regions

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
#     python -m wikidict fr --find-templates
# Ensuite il faudra purger la liste et il restera les sections ci-dessous.
head_sections = ("{{langue|fr}}", "{{langue|conv}}")
etyl_section = ["{{S|étymologie}}"]
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
    *etyl_section,
    "{{S|interfixe|fr}",
    "{{S|interjection|fr|",
    "{{S|interjection|fr}",
    "{{S|lettre|fr}",
    "{{S|locution-phrase|fr|",
    "{{S|locution-phrase|fr}",
    "{{S|nom commun|fr|",
    "{{S|nom commun|fr}",
    "{{S|nom propre|fr|",
    "{{S|nom propre|fr}",
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
    "{{S|verbe|fr|flexion",
)

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
    "{doute",
    "{ébauche",
    "{ébauche-déc",
    "{ébauche-déf",
    "{ébauche-étym",
    "{ébauche-étym-nom-scientifique",
    "{ébauche-exe",
    "{ébauche-gent",
    "{ébauche-pron",
    "{ébauche-syn",
    "{ébauche-trad",
    "{ébauche-trad-exe",
    "{ébauche-trans",
    "{ébauche2-exe",
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
    "ducaux",  # pluriel irrégulier
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
    "*",
    ",",
    "?",
    "Article",
    "article",
    "Accord des couleurs",
    "ancre",
    "créer-séparément",
    "désabrévier",
    "ébauche-déf",
    "fr-rég",
    "ibid",
    "Import",
    "laé",
    "lien-ancre-étym",
    "lire en ligne",
    "Modèle",
    "Ouvrage",
    "ouvrage",
    "périodique",
    "plans d’eau",
    "préciser",
    "R",
    "RÉF",
    "refnec",
    "réfnéc",
    "réfnec",
    "référence nécessaire",
    "Référence nécessaire",
    "réf",
    "réf?",
    "réf ?",
    "source",
    "source?",
    "trad-exe",
    "trier",
    "vérifier",
    "voir-conj",
)

# Modèles qui seront remplacés par du texte italique.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les
templates_italic = {
    **domain_templates,
    **regions,
    "absol": "Absolument",
    "adj-indéf-avec-de": "Avec de",
    "admin": "Administration",
    "aéro": "Aéronautique",
    "agri": "Agriculture",
    "analogie": "Par analogie",
    "angl": "Anglicisme",
    "anat": "Anatomie",
    "antiq": "Antiquité",
    "apposition": "En apposition",
    "arch": "Archaïsme",
    "archaïque": "Archaïsme",
    "archaïsme": "Archaïsme",
    "archi": "Architecture",
    "Argadz": "Argot des Gadz’Arts",
    "argot internet": "Argot Internet",
    "argot typographes": "Argot des typographes",
    "argot voleurs": "Argot des voleurs",
    "astron": "Astronomie",
    "au figuré": "Figuré",
    "audiovi": "Audiovisuel",
    "auto": "Automobile",
    "automo": "Automobile",
    "avant 1835": "Archaïque, orthographe d’avant 1835",
    "BD": "Bande dessinée",
    "BDD": "Bases de données",
    "bdd": "Bases de données",
    "bioch": "Biochimie",
    "biol": "Biologie",
    "b-m-cour": "Beaucoup moins courant",
    "botan": "Botanique",
    "bot.": "Botanique",
    "cartes": "Cartes à jouer",
    "catholicisme": "Christianisme",
    "chim": "Chimie",
    "chir": "Chirurgie",
    "ciné": "Cinéma",
    "cuis": "Cuisine",
    "comm": "Commerce",
    "composants": "Électronique",
    "compta": "Comptabilité",
    "constr": "Construction",
    "cour": "Courant",
    "cours d'eau": "Géographie",
    "cout": "Couture",
    "critiqué": "Usage critiqué",
    "cycl": "Cyclisme",
    "dermatol": "Dermatologie",
    "déris": "Par dérision",
    "dérision": "Par dérision",
    "désuet": "Désuet",
    "détroit": "Géographie",
    "didact": "Didactique",
    "diplo": "Diplomatie",
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
    "extrêmement_rare": "Extrêmement rare",
    "écolo": "Écologie",
    "écon": "Économie",
    "éduc": "Éducation",
    "énallages": "Énallage",
    "énergie": "Industrie de l’énergie",
    "épithète": "Employé comme épithète",
    "familier": "Familier",
    "ferro": "Chemin de fer",
    "ferroviaire": "Chemin de fer",
    "figure": "Rhétorique",
    "finan": "Finance",
    "finances": "Finance",
    "fonderie": "Métallurgie",
    "formel": "Soutenu",
    "fortification": "Architecture",
    "gastronomie": "Cuisine",
    "généralement": "Généralement",
    "génériquement": "Génériquement",
    "germ": "Germanisme",
    "graphe": "Théorie des graphes",
    "géog": "Géographie",
    "géol": "Géologie",
    "géom": "Géométrie",
    "géoph": "Géophysique",
    "habil": "Habillement",
    "hérald": "Héraldique",
    "hippisme": "Sports hippiques",
    "hist": "Histoire",
    "horlog": "Horlogerie",
    "humour": "Par plaisanterie",
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
    "ironie": "Ironique",
    "jardi": "Jardinage",
    "juri": "Droit",
    "jurisprudence": "Droit",
    "just": "Justice",
    "ling": "Linguistique",
    "litote": "Par litote",
    "litt": "Littéraire",
    "locutions latines": "Latinisme",
    "logi": "Logique",
    "légis": "Droit",
    "m-cour": "Moins courant",
    "maçon": "Maçonnerie",
    "maladie": "Nosologie",
    "manège": "Équitation",
    "marque": "Marque commerciale",
    "marque déposée": "Marque commerciale",
    "math": "Mathématiques",
    "méc": "Mécanique",
    "médecine non conv": "Médecine non conventionnelle",
    "mélio": "Mélioratif",
    "menu": "Menuiserie",
    "mercatique": "Marketing",
    "métrol": "Métrologie",
    "mili": "Militaire",
    "minér": "Minéralogie",
    "musi": "Musique",
    "mythol": "Mythologie",
    "méca": "Mécanique",
    "méde": "Médecine",
    "métal": "Métallurgie",
    "métaph": "Figuré",
    "métaphore": "Figuré",
    "météo": "Météorologie",
    "météorol": "Météorologie",
    "méton": "Par métonymie",
    "métonymie": "Par métonymie",
    "muscle": "Anatomie",
    "neurol": "Neurologie",
    "noms de domaine": "Informatique",
    "nom-coll": "Nom collectif",
    "nom-déposé": "Marque commerciale",
    "nucl": "Nucléaire",
    "numis": "Numismatique",
    "néol": "Néologisme",
    "néologisme": "Néologisme",
    "obsolète": "désuet",
    "oenol": "Œnologie",
    "opti": "Optique",
    "ornithol": "Ornithologie",
    "ortho1990": "orthographe rectifiée de 1990",
    "par analogie": "Par analogie",
    "POO": "Programmation orientée objet",
    "p-us": "Peu usité",
    "p us": "Peu usité",
    "paléogr": "Paléographie",
    "par ext": "Par extension",
    "par plaisanterie": "Par plaisanterie",
    "part": "En particulier",
    "partic": "En particulier",
    "particulier": "En particulier",
    "pathologie": "Nosologie",
    "pâtes": "Cuisine",
    "pêch": "Pêche",
    "péj": "Péjoratif",
    "philo": "Philosophie",
    "photo": "Photographie",
    "phys": "Physique",
    "pl-cour": "Plus courant",
    "pl-rare": "Plus rare",
    "plais": "Par plaisanterie",
    "plaisanterie": "Par plaisanterie",
    "poés": "Poésie",
    "polit": "Politique",
    "popu": "Populaire",
    "presse": "Journalisme",
    "procédure": "Justice",
    "prog": "Programmation informatique",
    "programmation": "Programmation informatique",
    "pronl": "Pronominal",
    "propre": "Sens propre",
    "propriété": "Droit",
    "propulsion": "Propulsion spatiale",
    "prov": "Proverbial",
    "psychia": "Psychiatrie",
    "psychol": "Psychologie",
    "reli": "Religion",
    "réciproque2": "Réciproque",
    "régional": "Régionalisme",
    "réseaux": "Réseaux informatiques",
    "sci-fi": "Science-fiction",
    "scol": "Éducation",
    "scolaire": "Éducation",
    "sexe": "Sexualité",
    "SMS": "Langage SMS",
    "sociol": "Sociologie",
    "sout": "Soutenu",
    "spéc": "Spécialement",
    "spécialement": "Spécialement",
    "spécifiquement": "Spécifiquement",
    "stat": "Statistiques",
    "sylv": "Sylviculture",
    "tech": "Technique",
    "technol": "Technologie",
    "temps": "Chronologie",
    "text": "Textile",
    "théât": "Théâtre",
    "théol": "Théologie",
    "télécom": "Télécommunications",
    "tr-fam": "Très familier",
    "trans": "Transitif",
    "transit": "Transitif",
    "transports": "Transport",
    "tradit": "orthographe traditionnelle",
    "très-rare": "Très rare",
    "très très rare": "Extrêmement rare",
    "typo": "Typographie",
    "typog": "Typographie",
    "télé": "Audiovisuel",
    "vieilli": "Vieilli",
    "vieux": "Vieilli",
    "vélo": "Cyclisme",
    "verlan": "Verlan",
    "vête": "Habillement",
    "volley": "Volley-ball",
    "vulg": "Vulgaire",
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
#   html/wikidict/user_functions.html
templates_multi = {
    # {{1er}}
    # {{1er|mai}}
    "1er": "f\"1{superscript('er')}{'&nbsp;' + parts[1] if len(parts) > 1 else ''}\"",
    # {{Arabe|ن و ق}}
    "Arab": "parts[1] if len(parts) > 1 else 'arabe'",
    "Arabe": "parts[1] if len(parts) > 1 else 'arabe'",
    "Braille": "parts[1]",
    # {{comparatif de|bien|fr|adv}}
    "comparatif de": "sentence(parts)",
    # {{cf}}
    # {{cf|tour d’échelle}}
    # {{cf|lang=fr|triner}}
    "cf": "f\"→ voir{' ' + concat([italic(p) for p in parts[1:] if p and '=' not in p], ', ', ' et ') if len(parts) > 1 else ''}\"",  # noqa
    # {{circa|1150}}
    "circa": "term('c. ' + [p for p in parts if p and '=' not in p][1])",
    # {{Cyrl|Сергей}}
    "Cyrl": "parts[1] if len(parts) > 1 else 'cyrillique'",
    # {{créatures|fr|mythologiques}
    "créatures": "term('Mythologie')",
    # {{couleur|#B0F2B6}}
    "couleur": "parts[1]",
    # {{Deva|[[देव]]|deva|divin}}
    "Deva": "parts[1].strip('[]')",
    # {{déverbal de|haler|fr}}
    "déverbal de": 'f"Déverbal de {italic(parts[1])}"',
    # {{dénominal de|affection|fr}}
    "dénominal de": 'f"Dénominal de {italic(parts[1])}"',
    # {{diminutif|fr|m=1}}
    "diminutif": "'Diminutif' if any(p in ('m=1', 'm=oui') for p in parts) else 'diminutif'",
    # {{fchim|H|2|O}}
    "fchim": "chimy(parts[1:])",
    "formule chimique": "chimy(parts[1:])",
    # XIX{{e}}
    # {{e|-1}}
    "e": "superscript(parts[1] if len(parts) > 1 else 'e')",
    "ex": "superscript(parts[1] if len(parts) > 1 else 'e')",
    # XIX{{ème}}
    "ème": "superscript(parts[1] if len(parts) > 1 else 'e')",
    # {{er}}
    "er": "superscript(parts[1] if len(parts) > 1 else 'er')",
    # {{ère}}
    "ère": "superscript(parts[1] if len(parts) > 1 else 're')",
    # XIV{{exp|e}}
    "exp": "superscript(parts[1] if len(parts) > 1 else 'e')",
    # {{emploi|au passif}}
    "emploi": "term(capitalize(parts[1]))",
    # {{#expr: 2 ^ 30}}
    "#expr": "eval_expr(parts[1])",
    # {{formatnum:-1000000}}
    "formatnum": f'number(parts[1], "{float_separator}", "{thousands_separator}")',
    # {{forme pronominale|mutiner}}
    "forme pronominale": 'f"{capitalize(tpl)} de {parts[1]}"',
    # {{graphie|u}}
    "graphie": 'f"‹&nbsp;{parts[1]}&nbsp;›"',
    # {{Ier}}
    "Ier": "f\"{small_caps('i')}{superscript('er')}\"",
    # {{îles|fr}}
    # {{îles|fr|des Antilles}}
    "îles": "term('Géographie')",
    # {{in|5}}
    "in": "subscript(parts[1])",
    # {{incise|tambour, timbale, etc.|fin}}
    "incise": "f'— {parts[1]} —' if len(parts) == 2 else f'— {parts[1]}'",
    # {{indice|n}}
    "indice": "subscript(parts[1])",
    # {{info lex|boulangerie}}
    # {{info lex|équitation|sport}}
    "info lex": "term(', '.join(capitalize(part) for part in parts[1:]))",
    # {{ISBN|978-1-23-456789-7|2-876-54301-X}}
    "ISBN": "'ISBN ' + concat(parts[1:], sep=', ', last_sep=' et ')",
    # {{lexique|philosophie|fr}}
    # {{lexique|philosophie|sport|fr}}
    "lexique": "term(', '.join(capitalize(p) for p in [a for a in parts if '=' not in a][1:-1]))",
    # {{localités|fr|d’Espagne}}
    "localités": "term('Géographie')",
    # {{mn-lien|далай|dalai|ᠲᠠᠯᠠᠢ}}
    "mn-lien": "f'{parts[1]} (MNS : {italic(parts[2])})'",
    # {{nobr|1 000 000 000 000}}
    "nobr": "re.sub(r'^1=', '', parts[-1].replace(' ', '&nbsp;').replace('!', '|'))",
    # {{nom w pc|Aldous|Huxley}}
    "nom w pc": "person(word, parts[1:])",
    # {{nombre romain|12}}
    "nombre romain": "int_to_roman(int(parts[1]))",
    # {{numéro}}
    "numéro": 'f\'n{superscript("o")}{parts[1] if len(parts) > 1 else ""}\'',
    "n°": 'f\'n{superscript("o")}{parts[1] if len(parts) > 1 else ""}\'',
    # {{o}}
    "o": "superscript('o')",
    # {{petites capitales|Dupont}}
    "petites capitales": "small_caps(parts[1])",
    # {{pc|Dupont}}
    "pc": "small_caps(parts[1])",
    # {{phon|tɛs.tjɔ̃}}
    "phon": "strong(f'[{parts[1]}]')",
    # {{pron|plys|fr}}
    "pron": r'f"\\{parts[1]}\\"',
    # {{pron-API|/j/}}
    "pron-API": "parts[1]",
    # {{provinces|fr|d’Espagne}}
    "provinces": "term('Géographie')",
    # {{RFC|5322}}
    "RFC": "sentence(parts)",
    # {{région}}
    # {{région|Lorraine et Dauphiné}}
    "région": "term(parts[1] if len(parts) > 1 else 'Régionalisme')",
    "régionalisme": "term(parts[1] if len(parts) > 1 else 'Régionalisme')",
    # {{re}}
    "re": "superscript(parts[1] if len(parts) > 1 else 're')",
    # {{registre|traditionnellement}}
    "registre": "italic(f\"({capitalize(parts[1])})\") if len(parts) > 1 else ''",
    # {{smcp|Dupont}}
    "smcp": "small_caps(parts[1])",
    # {{SIC}}
    # {{sic !}}
    "SIC": "f'<sup>[sic : {parts[1]}]</sup>' if len(parts) > 1 else '<sup>[sic]</sup>'",
    "sic !": "f'<sup>[sic : {parts[1]}]</sup>' if len(parts) > 1 else '<sup>[sic]</sup>'",
    # {{sport|fr}}
    # {{sport|fr|collectifs}}
    "sport": "term(capitalize(concat(parts, sep=' ', indexes=[0, 2])))",
    # {{substantivation de|mettre en exergue}}
    "substantivation de": 'f"Substantivation de {italic(parts[1])}"',
    # {{superlatif de|petit|fr}}
    "superlatif de": "sentence(parts)",
    # {{term|ne … guère que}}
    "term": "term(capitalize(parts[1]))",
    # {{terme|Astrophysique}}
    "terme": "term(capitalize(parts[1]))",
    # {{trad+|conv|Sitophilus granarius}}
    "trad+": "parts[2]",
    "trad-": "parts[2]",
    # {{variante de|ranche|fr}}
    "variante de": "sentence(parts)",
    "Variante de": "sentence(parts)",
    # {{wd|Q30092597|Frederick H. Pough}}
    "wd": "parts[2] if len(parts) == 3 else ''",
    # {{wsp|Panthera pardus|''Panthera pardus''}}
    # {{wsp|Brassicaceae}}
    "wsp": "parts[2] if len(parts) > 2 else parts[1]",
    # {{WSP|Panthera leo}}
    "WSP": "italic(parts[1])",
    # 1,23{{x10|9}}
    "x10": "f'×10{superscript(parts[1])}' if len(parts) > 1 else '×10'",
}

# Modèles qui seront remplacés par du texte personnalisé.
templates_other = {
    "!": "!",
    "=": "=",
    "absolu": "<i>absolu</i>",
    "apJC": "apr. J.-C.",
    "attention": "⚠",
    "au singulier uniquement": "<i>au singulier uniquement</i>",
    "au pluriel uniquement": "<i>au pluriel uniquement</i>",
    "avJC": "av. J.-C.",
    "c": "<i>commun</i>",
    "collectif": "<i>collectif</i>",
    "commun": "<i>commun</i>",
    "convention verbe grc": "<b>Note&nbsp;:</b> Par convention, les verbes grecs anciens sont désignés par la 1<sup>re</sup> personne du singulier du présent de l’indicatif actif.",  # noqa
    "dépendant": "<i>dépendant</i>",
    "déterminé": "déterminé",
    "f": "<i>féminin</i>",
    "féminin": "<i>féminin</i>",
    "fm?": "<i>féminin ou masculin (l’usage hésite)</i>",
    "fm ?": "<i>féminin ou masculin (l’usage hésite)</i>",
    "fplur": "<i>féminin pluriel</i>",
    "genre": "Genre à préciser",
    "genre ?": "Genre à préciser",
    "i": "<i>intransitif</i>",
    "impers": "<i>impersonnel</i>",
    "indéterminé": "indéterminé",
    "invar": "<i>invariable</i>",
    "invariable": "<i>invariable</i>",
    "la-note-ij": "(Le ‹&nbsp;j&nbsp;›, absent du latin classique, traduit le ‹&nbsp;i&nbsp;› devant une voyelle dans la tradition scholastique française. Voyez «&nbsp;j en latin&nbsp;».)",  # noqa
    "m": "<i>masculin</i>",
    "masculin": "<i>masculin</i>",
    "majus": "<i>majuscule</i>",
    "masculin et féminin": "<i>masculin et féminin identiques</i>",
    "mf": "<i>masculin et féminin identiques</i>",
    "mf?": "<i>masculin ou féminin (l’usage hésite)</i>",
    "mf ?": "<i>masculin ou féminin (l’usage hésite)</i>",
    "minus": "<i>minuscule</i>",
    "mplur": "<i>masculin pluriel</i>",
    "msing": "<i>masculin singulier</i>",
    "n": "<i>neutre</i>",
    "non standard": "⚠ Il s’agit d’un terme utilisé qui n’est pas d’un usage standard.",
    "nombre ?": "Nombre à préciser",
    "note": "<b>Note&nbsp;:</b>",
    "note-fr-féminin-homme": "<i>Ce mot féminin n’a pas de masculin correspondant, et il peut désigner des hommes.</i>",  # noqa
    "note-fr-masculin-femme": "<i>Ce mot masculin n'a pas de féminin correspondant, et il peut désigner des femmes.</i>",  # noqa
    "note-gentilé": "Ce mot est un gentilé : il désigne les habitants d’un lieu, les personnes qui en sont originaires ou qui le représentent (par exemple, les membres d’une équipe sportive).",  # noqa
    "note-majuscule-taxo": "En biologie, le nom binominal et les autres noms scientifiques (en latin) prennent toujours une majuscule. En français, les naturalistes mettent fréquemment une majuscule aux noms de taxons supérieurs au genre. Un nom vernaculaire ne prend pas de majuscule, mais on peut en mettre une quand on veut expliciter le fait que l’on ne parle pas d’individus, mais que l’on veut parler de l’espèce, du genre, de la famille, de l’ordre, etc.",  # noqa
    "note-majuscule-taxon": "En biologie, le nom binominal et les autres noms scientifiques (en latin) prennent toujours une majuscule. En français, les naturalistes mettent fréquemment une majuscule aux noms de taxons supérieurs au genre. Un nom vernaculaire ne prend pas de majuscule, mais on peut en mettre une quand on veut expliciter le fait que l’on ne parle pas d’individus, mais que l’on veut parler de l’espèce, du genre, de la famille, de l’ordre, etc.",  # noqa
    "peu attesté": "⚠ Ce terme est très peu attesté.",
    "o": "<i>neutre</i>",
    "p": "<i>pluriel</i>",
    "palind": "<i>palindrome</i>",
    "pp": "<i>participe passé</i>",
    "pré": "<i>prétérit</i>",
    "prés": "<i>présent</i>",
    "prnl": "<i>pronominal</i>",
    "s": "<i>singulier</i>",
    "sp": "<i>singulier et pluriel identiques</i>",
    "sp ?": "<i>singulier et pluriel identiques ou différenciés (l’usage hésite)</i>",
    "réfl": "<i>réfléchi</i>",
    "réciproque": "<i>réciproque</i>",
    "t": "<i>transitif</i>",
    "tr-dir": "<i>transitif direct</i>",
    "tr-indir": "<i>transitif indirect</i>",
    "usage": "<b>Note d’usage&nbsp;:</b>",
    "vlatypas-pivot": "v’là-t-i’ pas",
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["Citation/François Béroalde de Verville"], "fr")
        'François Béroalde de Verville'
        >>> last_template_handler(["Citation/Amélie Nothomb/Mercure"], "fr")
        '<i>Mercure</i>'
        >>> last_template_handler(["Citation/Edmond Nivoit/Notions élémentaires sur l’industrie dans le département des Ardennes/1869"], "fr")
        'Edmond Nivoit, <i>Notions élémentaires sur l’industrie dans le département des Ardennes</i>, 1869'
        >>> last_template_handler(["Citation/Edmond Nivoit/Notions élémentaires sur l’industrie dans le département des Ardennes/1869|171"], "fr")
        'Edmond Nivoit, <i>Notions élémentaires sur l’industrie dans le département des Ardennes</i>, 1869, page 171'

        >>> last_template_handler(["code langue", "créole guyanais"], "fr")
        'gcr'
        >>> last_template_handler(["code langue", "foo"], "fr")
        ''

        >>> last_template_handler(["R:TLFi"], "fr", "pedzouille")
        '«&nbsp;pedzouille&nbsp;», dans <i>TLFi, Le Trésor de la langue française informatisé</i>, 1971–1994'
        >>> last_template_handler(["R:TLFi", "pomme"], "fr", "pedzouille")
        '«&nbsp;pomme&nbsp;», dans <i>TLFi, Le Trésor de la langue française informatisé</i>, 1971–1994'

        >>> last_template_handler(["fr-verbe-flexion", "colliger", "ind.i.3s=oui"], "fr")
        'colliger'
        >>> last_template_handler(["fr-verbe-flexion", "grp=3", "couvrir", "ind.i.3s=oui"], "fr")
        'couvrir'
        >>> last_template_handler(["fr-verbe-flexion", "impers=oui", "revenir", "ind.i.3s=oui"], "fr")
        'revenir'
        >>> last_template_handler(["fr-verbe-flexion", "grp=3", "'=oui", "ind.i.1s=oui", "ind.i.2s=oui", "avoir"], "fr")
        'avoir'
        >>> last_template_handler(["fr-verbe-flexion", "grp=3", "1=dire", "imp.p.2p=oui", "ind.p.2p=oui", "ppfp=oui"], "fr")
        'dire'

        >>> last_template_handler(["Légifrance", "base=CPP", "numéro=230-45", "texte=article 230-45"], "fr")
        'article 230-45'
        >>> last_template_handler(["Légifrance", "base=CPP", "numéro=230-45"], "fr")
        ''

        >>> last_template_handler(["ar-mot", "elHasan_"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">الحَسَن</span></span> <small>(elHasan_)</small>'
        >>> last_template_handler(["ar-ab", "maktûbũ"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">مَكْتُوبٌ</span></span>'

        >>> last_template_handler(["nom langue", "gcr"], "fr")
        'créole guyanais'

    """  # noqa
    from .langs import langs
    from ..defaults import last_template_handler as default
    from ...user_functions import (
        chinese,
        extract_keywords_from,
        italic,
        person,
    )
    from .template_handlers import render_template, lookup_template

    if lookup_template(template[0]):
        return render_template(template)

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl.startswith("Citation/"):
        parts = tpl.split("/")[1:]
        author = person(word, parts.pop(0).split(" ", 1))
        book = parts.pop(0) if parts else ""
        date = parts.pop(0) if parts else ""
        if "|" in date:
            date, page = date.split("|")
        else:
            page = ""
        if not date and not book:
            return author
        if not date:
            return italic(book)
        if not page:
            return f"{author}, {italic(book)}, {date}"
        return f"{author}, {italic(book)}, {date}, page {page}"

    if tpl == "code langue":
        lang = parts[0]
        for code, l10n in langs.items():
            if l10n == lang:
                return code
        return ""

    if tpl == "R:TLFi":
        w = parts[0] if parts else word
        return f"«&nbsp;{w}&nbsp;», dans <i>TLFi, Le Trésor de la langue française informatisé</i>, 1971–1994"

    if tpl == "fr-verbe-flexion":
        return data.get("1", parts[0] if parts else "")

    if tpl == "Légifrance":
        return data["texte"]

    if tpl == "nom langue":
        return langs[parts[0]]

    if tpl in ("ar-mot", "ar-terme"):
        return f'<span style="line-height: 0px;"><span style="font-size:larger">{arabiser(parts[0])}</span></span> <small>({parts[0]})</small>'  # noqa
    if tpl == "ar-ab":
        return f'<span style="line-height: 0px;"><span style="font-size:larger">{arabiser(parts[0])}</span></span>'

    if tpl in ("zh-l", "zh-m"):
        return chinese(parts, data, laquo="«&nbsp;", raquo="&nbsp;»")

    # This is a country in the current locale
    if tpl in langs:
        return langs[tpl]

    return default(template, locale, word=word)


# Contenu de la release sur GitHub :
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr
release_description = """\
Nombre de mots : {words_count}
Export Wiktionnaire : {dump_date}

Fichiers disponibles :

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Mis à jour le {creation_date}</sub>
"""  # noqa

# Le nom du dictionnaire qui sera affiché en-dessous de chaque définition
wiktionary = "Wiktionnaire (ɔ) {year}"
