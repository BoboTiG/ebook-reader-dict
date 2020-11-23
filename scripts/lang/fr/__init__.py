"""French language."""
from typing import Tuple
from .domain_templates import domain_templates

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
    "?",
    "ancre",
    "créer-séparément",
    "désabrévier",
    "Import",
    "lien web",
    "Modèle",
    "Ouvrage",
    "ouvrage",
    "plans d’eau",
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
    "vérifier",
)

# Modèles qui seront remplacés par du texte italique.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les
templates_italic = {
    **domain_templates,
    "abréviation": "Abréviation",
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
    "BE": "Belgique",
    "bdd": "Bases de données",
    "bioch": "Biochimie",
    "biol": "Biologie",
    "b-m-cour": "Beaucoup moins courant",
    "botan": "Botanique",
    "bot.": "Botanique",
    "CA": "Canada",
    "CH": "Suisse",
    "CI": "Côte d’Ivoire",
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
    "cycl": "Cyclisme",
    "dermatol": "Dermatologie",
    "dérision": "Par dérision",
    "désuet": "Désuet",
    "détroit": "Géographie",
    "didact": "Didactique",
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
    "énergie": "Industrie de l’énergie",
    "épithète": "Employé comme épithète",
    "familier": "Familier",
    "FR": "France",
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
    "intrans": "Intransitif",
    "iron": "Ironique",
    "jardi": "Jardinage",
    "juri": "Droit",
    "jurisprudence": "Droit",
    "just": "Justice",
    "ling": "Linguistique",
    "litt": "Littéraire",
    "logi": "Logique",
    "légis": "Droit",
    "maçon": "Maçonnerie",
    "maladie": "Nosologie",
    "manège": "Équitation",
    "marque": "Marque commerciale",
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
    "nom-coll": "Nom collectif",
    "nucl": "Nucléaire",
    "numis": "Numismatique",
    "néol": "Néologisme",
    "néologisme": "Néologisme",
    "oenol": "Œnologie",
    "opti": "Optique",
    "ornithol": "Ornithologie",
    "ortho1990": "Orthographe rectifiée de 1990",
    "par analogie": "Par analogie",
    "POO": "Programmation orientée objet",
    "p us": "Peu usité",
    "paléogr": "Paléographie",
    "par ext": "Par extension",
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
    "pl-rare": "Plus rare",
    "plais": "Par plaisanterie",
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
    "QC": "Québec",
    "RDC": "Congo-Kinshasa",
    "RDCongo": "Congo-Kinshasa",
    "reli": "Religion",
    "régional": "Régionalisme",
    "réseaux": "Réseaux informatiques",
    "sci-fi": "Science-fiction",
    "scol": "Éducation",
    "scolaire": "Éducation",
    "sexe": "Sexualité",
    "sigle": "Sigle",
    "sociol": "Sociologie",
    "sout": "Soutenu",
    "spéc": "Spécialement",
    "spécialement": "Spécialement",
    "spécifiquement": "Spécifiquement",
    "stat": "Statistiques",
    "sylv": "Sylviculture",
    "TAAF": "Vocabulaire des TAAF",
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
    "typo": "Typographie",
    "typog": "Typographie",
    "télé": "Audiovisuel",
    "US": "États-Unis",
    "USA": "États-Unis",
    "vieilli": "Vieilli",
    "vieux": "Vieilli",
    "vélo": "Cyclisme",
    "verlan": "Verlan",
    "vête": "Habillement",
    "volley": "Volley-ball",
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
    "cf": "f\"→ voir{' ' + concat([italic(p) for p in parts[1:] if '=' not in p], ', ', ' et ') if len(parts) > 1 else ''}\"",  # noqa
    # {{circa|1150}}
    "circa": "term('c. ' + parts[1])",
    # {{créatures|fr|mythologiques}
    "créatures": "term('Mythologie')",
    # {{couleur|#B0F2B6}}
    "couleur": "color(parts[1])",
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
    # XIV{{exp|e}}
    "exp": "superscript(parts[1] if len(parts) > 1 else 'e')",
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
    # {{graphie|u}}
    "graphie": 'f"‹&nbsp;{parts[1]}&nbsp;›"',
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
    # {{lexique|philosophie|fr}}
    # {{lexique|philosophie|sport|fr}}
    "lexique": "term(', '.join(capitalize(p) for p in parts[1:-1]))",
    # {{localités|fr|d’Espagne}}
    "localités": "term('Géographie')",
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
    # {{provinces|fr|d’Espagne}}
    "provinces": "term('Géographie')",
    # {{RFC|5322}}
    "RFC": "sentence(parts)",
    # {{région}}
    # {{région|Lorraine et Dauphiné}}
    "région": "term(capitalize(parts[1] if len(parts) > 1 else 'régionalisme'))",
    "régionalisme": "term(capitalize(parts[1] if len(parts) > 1 else 'régionalisme'))",
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
    "trad-": "parts[2]",
    # {{unité|92|%}}
    "unité": "concat(parts[1:], sep=' ')",
    # {{Unité|60|cm}}
    "Unité": "concat(parts[1:], sep=' ')",
    # {{variante de|ranche|fr}}
    "variante de": "sentence(parts)",
    "Variante de": "sentence(parts)",
    # {{variante ortho de|acupuncture|fr}}
    "Variante ortho de": 'f"Variante orthographique de {parts[1]}"',
    "variante ortho de": 'f"Variante orthographique de {parts[1]}"',
    "variante orthographique de": 'f"Variante orthographique de {parts[1]}"',
    # {{W|Jacques Brandenberger}}
    "W": "parts[-1] if parts else ''",
    # {{wd|Q30092597|Frederick H. Pough}}
    "wd": "parts[2] if len(parts) == 3 else ''",
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


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["acronyme", "fr"], "fr")
        '<i>(Acronyme)</i>'
        >>> last_template_handler(["acronyme", "en", "de=light-emitting diode", "m=oui"], "fr")
        'Acronyme de <i>light-emitting diode</i>'
        >>> last_template_handler(["acronyme", "en", "de=light-emitting diode"], "fr")
        'acronyme de <i>light-emitting diode</i>'
        >>> last_template_handler(["acronyme", "en", "fr", "de=light-emitting diode", "texte=Light-Emitting Diode", "m=1"], "fr")
        'Acronyme de <i>Light-Emitting Diode</i>'

        >>> last_template_handler(["argot", "fr"], "fr")
        '<i>(Argot)</i>'
        >>> last_template_handler(["argot", "fr", "militaire"], "fr")
        '<i>(Argot militaire)</i>'
        >>> last_template_handler(["argot", "fr", "spéc=militaire"], "fr")
        '<i>(Argot militaire)</i>'

        >>> last_template_handler(["agglutination", "m=1"], "fr")
        'Agglutination'
        >>> last_template_handler(["agglutination", "fr", "de=harbin", "texte=l'harbin", "m=1"], "fr")
        "Agglutination de <i>l'harbin</i>"

        >>> last_template_handler(["calque", "la", "fr"], "fr")
        'latin'
        >>> last_template_handler(["calque", "en", "fr", "mot=to date", "sens=à ce jour"], "fr")
        'anglais <i>to date</i> («&nbsp;à ce jour&nbsp;»)'
        >>> last_template_handler(["calque", "sa", "fr", "mot=वज्रयान", "tr=vajrayāna", "sens=véhicule du diamant"], "fr")
        'sanskrit वज्रयान, <i>vajrayāna</i> («&nbsp;véhicule du diamant&nbsp;»)'

        >>> last_template_handler(["cit_réf", "Dictionnaire quelconque", "2007"], "fr")
        '<i>Dictionnaire quelconque</i>, 2007'
        >>> last_template_handler(["cit_réf", "titre=Dictionnaire quelconque", "date=2007"], "fr")
        '<i>Dictionnaire quelconque</i>, 2007'
        >>> last_template_handler(["cit_réf", "Dictionnaire quelconque", "date=2007"], "fr")
        '<i>Dictionnaire quelconque</i>, 2007'
        >>> last_template_handler(["cit_réf", "Dictionnaire quelconque", "2007", "Certain auteur"], "fr")
        'Certain auteur, <i>Dictionnaire quelconque</i>, 2007'
        >>> last_template_handler(["cit_réf", "Dictionnaire quelconque", "2007", "Certain auteur", "Certain article"], "fr")
        '«&nbsp;Certain article&nbsp;», dans Certain auteur, <i>Dictionnaire quelconque</i>, 2007'
        >>> last_template_handler(["cit_réf", "titre=Dictionnaire quelconque", "2007", "auteur=Certain auteur", "article=Certain article"], "fr")
        '«&nbsp;Certain article&nbsp;», dans Certain auteur, <i>Dictionnaire quelconque</i>, 2007'
        >>> last_template_handler(["cit_réf", "Nephilologus", "1934", "auteur_article=Marius", "article=Certain article", "pages=pp. 241-259"], "fr")
        'Marius, «&nbsp;Certain article&nbsp;», dans <i>Nephilologus</i>, 1934, pp. 241-259'

        >>> last_template_handler(["composé de", "longus", "aevum", "lang=la"], "fr")
        'composé de <i>longus</i> et de <i>aevum</i>'
        >>> last_template_handler(["composé de", "longus", "aevum", "lang=la", "f=1"], "fr")
        'composée de <i>longus</i> et de <i>aevum</i>'
        >>> last_template_handler(["composé de", "longus", "sens1=long", "aevum", "sens2=temps", "lang=la", "m=1"], "fr")
        'Composé de <i>longus</i> («&nbsp;long&nbsp;») et de <i>aevum</i> («&nbsp;temps&nbsp;»)'
        >>> last_template_handler(["composé de", "longus", "aevum", "sens=long temps", "lang=la"], "fr")
        'composé de <i>longus</i> et de <i>aevum</i>, littéralement «&nbsp;long temps&nbsp;»'
        >>> last_template_handler(["composé de", "δῆμος", "tr1=dêmos", "sens1=peuple", "ἀγωγός", "tr2=agōgós", "sens2=guide", "sens=celui qui guide le peuple", "lang=grc", "m=1"], "fr")
        'Composé de δῆμος, <i>dêmos</i> («&nbsp;peuple&nbsp;») et de ἀγωγός, <i>agōgós</i> («&nbsp;guide&nbsp;»), littéralement «&nbsp;celui qui guide le peuple&nbsp;»'
        >>> last_template_handler(["composé de", "aux", "mains", "de", "m=1"], "fr")
        'Composé de <i>aux</i>, <i>mains</i> et de <i>de</i>'
        >>> last_template_handler(["composé de", "anti-", "quark", "lang=en"], "fr")
        'dérivé de <i>quark</i> avec le préfixe <i>anti-</i>'
        >>> last_template_handler(["composé de", "anti-", "quark", "sens=quarks au rebut"], "fr")
        'dérivé de <i>quark</i> avec le préfixe <i>anti-</i>, littéralement «&nbsp;quarks au rebut&nbsp;»'
        >>> last_template_handler(["composé de", "anti-", "quark", "lang=en", "m=1", "f=1"], "fr")
        'Dérivée de <i>quark</i> avec le préfixe <i>anti-</i>'
        >>> last_template_handler(["composé de", "clear", "-ly", "lang=en", "m=1"], "fr")
        'Dérivé de <i>clear</i> avec le suffixe <i>-ly</i>'
        >>> last_template_handler(["composé de", "느낌", "tr1=neukkim", "sens1=sensation", "표", "tr2=-pyo", "sens2=symbole", "lang=ko", "m=1"], "fr")
        'Dérivé de 느낌, <i>neukkim</i> («&nbsp;sensation&nbsp;») avec le suffixe 표, <i>-pyo</i> («&nbsp;symbole&nbsp;»)'

        >>> last_template_handler(["date", ""], "fr")
        '<i>(Date à préciser)</i>'
        >>> last_template_handler(["date", "?"], "fr")
        '<i>(Date à préciser)</i>'
        >>> last_template_handler(["date"], "fr")
        '<i>(Date à préciser)</i>'
        >>> last_template_handler(["date", "1957"], "fr")
        '<i>(1957)</i>'
        >>> last_template_handler(["date", "1957"], "fr")
        '<i>(1957)</i>'
        >>> last_template_handler(["date", "vers l'an V"], "fr")
        "<i>(Vers l'an V)</i>"

        >>> last_template_handler(["dénominal"], "fr")
        'dénominal'
        >>> last_template_handler(["dénominal", "de=psychoanalyze", "m=1"], "fr")
        'Dénominal de <i>psychoanalyze</i>'

        >>> last_template_handler(["déverbal"], "fr")
        'déverbal'
        >>> last_template_handler(["déverbal", "de=peko", "lang=eo", "m=0"], "fr")
        'déverbal de <i>peko</i>'
        >>> last_template_handler(["déverbal", "de=accueillir", "m=1"], "fr")
        'Déverbal de <i>accueillir</i>'
        >>> last_template_handler(["déverbal sans suffixe", "de=réserver", "m=1"], "fr")
        'Déverbal sans suffixe de <i>réserver</i>'

        >>> last_template_handler(["équiv-pour", "un homme", "maître"], "fr")
        '<i>(pour un homme on dit</i>&nbsp: maître<i>)</i>'
        >>> last_template_handler(["équiv-pour", "le mâle", "lion"], "fr")
        '<i>(pour le mâle on dit</i>&nbsp: lion<i>)</i>'
        >>> last_template_handler(["équiv-pour", "une femme", "autrice", "auteure", "auteuse"], "fr")
        '<i>(pour une femme on peut dire</i>&nbsp: autrice, auteure, auteuse<i>)</i>'
        >>> last_template_handler(["équiv-pour", "une femme", "texte=certains disent", "professeure", "professeuse", "professoresse", "professrice"], "fr")
        '<i>(pour une femme certains disent</i>&nbsp: professeure, professeuse, professoresse, professrice<i>)</i>'

        >>> last_template_handler(["étyl", "grc", "fr"], "fr")
        'grec ancien'
        >>> last_template_handler(["étyl", "la", "fr", "dithyrambicus"], "fr")
        'latin <i>dithyrambicus</i>'
        >>> last_template_handler(["étyl", "no", "fr", "mot=ski"], "fr")
        'norvégien <i>ski</i>'
        >>> last_template_handler(["étyl", "la", "fr", "mot=invito", "type=verb"], "fr")
        'latin <i>invito</i>'
        >>> last_template_handler(["étyl", "grc", "fr", "mot=λόγος", "tr=lógos", "type=nom", "sens=étude"], "fr")
        'grec ancien λόγος, <i>lógos</i> («&nbsp;étude&nbsp;»)'
        >>> last_template_handler(["étyl", "grc", "fr", "λόγος", "lógos", "étude", "type=nom", "lien=1"], "fr")
        'grec ancien λόγος, <i>lógos</i> («&nbsp;étude&nbsp;»)'
        >>> last_template_handler(["étyl", "la", "fr", "mot=jugulum", "sens=endroit où le cou se joint aux épaules = la gorge"], "fr")  # noqa
        'latin <i>jugulum</i> («&nbsp;endroit où le cou se joint aux épaules = la gorge&nbsp;»)'
        >>> last_template_handler(["étyl", "la", "fr", "mot=subgrunda", "tr", "sens=même sens"], "fr")
        'latin <i>subgrunda</i> («&nbsp;même sens&nbsp;»)'
        >>> last_template_handler(["étyl", "grc", "fr", "mot="], "fr")
        'grec ancien'
        >>> last_template_handler(['étyl', 'grc', 'mot=ὑπόθεσις', 'tr=hupóthesis', 'sens=action de mettre dessous', 'nocat=1'], "fr")
        'grec ancien ὑπόθεσις, <i>hupóthesis</i> («&nbsp;action de mettre dessous&nbsp;»)'
        >>> last_template_handler(["étyl", "grc", "fr", "tr=leipein", "sens=abandonner"], "fr")
        'grec ancien <i>leipein</i> («&nbsp;abandonner&nbsp;»)'
        >>> last_template_handler(["étyl", "1=grc", "2=es", "mot=νακτός", "tr=naktós", "sens=dense"], "fr")
        'grec ancien νακτός, <i>naktós</i> («&nbsp;dense&nbsp;»)'
        >>> last_template_handler(["étyl", "proto-indo-européen", "fr"], "fr")
        'indo-européen commun'

        >>> last_template_handler(["étylp", "la", "fr", "mot=Ladon"], "fr")
        'latin <i>Ladon</i>'

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

        >>> last_template_handler(["la-verb", "amō", "amare", "amāre", "amavi", "amāvi", "amatum", "amātum"], "fr")
        '<b>amō</b>, <i>infinitif</i> : amāre, <i>parfait</i> : amāvi, <i>supin</i> : amātum'
        >>> last_template_handler(["la-verb", "vŏlo", "velle", "velle", "volui", "vŏlŭi", "2ps=vis", "2ps2=vīs", "pattern=irrégulier"], "fr")
        '<b>vŏlo</b>, vīs, <i>infinitif</i> : velle, <i>parfait</i> : vŏlŭi <i>(irrégulier)</i>'
        >>> last_template_handler(["la-verb", "horrĕo", "horrere", "horrēre", "horrui", "horrŭi", "pattern=sans passif"], "fr")
        '<b>horrĕo</b>, <i>infinitif</i> : horrēre, <i>parfait</i> : horrŭi <i>(sans passif)</i>'
        >>> last_template_handler(["la-verb", "sum", "es", "esse", "esse", "fui", "fui", "futurus", "futurus", "2ps=es", "2ps2=es", "pattern=irrégulier", "44=participe futur"], "fr")
        '<b>sum</b>, es, <i>infinitif</i> : esse, <i>parfait</i> : fui, <i>participe futur</i> : futurus <i>(irrégulier)</i>'

        >>> last_template_handler(["l", "dies Lunae", "la"], "fr")
        'dies Lunae'
        >>> last_template_handler(["lien", "渦", "zh-Hans"], "fr")
        '渦'
        >>> last_template_handler(["lien", "フランス", "ja", "sens=France"], "fr")
        'フランス («&nbsp;France&nbsp;»)'
        >>> last_template_handler(["lien", "フランス", "ja", "tr=Furansu", "sens=France"], "fr")
        'フランス, <i>Furansu</i> («&nbsp;France&nbsp;»)'
        >>> last_template_handler(["lien", "camara", "sens=voute, plafond vouté", "la"], "fr")
        'camara («&nbsp;voute, plafond vouté&nbsp;»)'

        >>> last_template_handler(["phon", "tɛs.tjɔ̃"], "fr")
        '<b>[tɛs.tjɔ̃]</b>'
        >>> last_template_handler(["phon", "na.t͡ʃe", "fr"], "fr")
        '<b>[na.t͡ʃe]</b>'

        >>> last_template_handler(["polytonique", "μηρóς", "mêrós", "cuisse"], "fr")
        'μηρóς, <i>mêrós</i> («&nbsp;cuisse&nbsp;»)'
        >>> last_template_handler(["polytonique", "φόβος", "phóbos", "sens=effroi, peur"], "fr")
        'φόβος, <i>phóbos</i> («&nbsp;effroi, peur&nbsp;»)'
        >>> last_template_handler(["Polytonique", "नामन्", "nā́man"], "fr")
        'नामन्, <i>nā́man</i>'
        >>> last_template_handler(["Polytonique", "هند", "hend", "Inde"], "fr")
        'هند, <i>hend</i> («&nbsp;Inde&nbsp;»)'

        >>> last_template_handler(["recons", "maruos"], "fr")
        '*<i>maruos</i>'
        >>> last_template_handler(["recons", "maruos", "gaul"], "fr")
        '*<i>maruos</i>'
        >>> last_template_handler(["recons", "maruos", "gaul", "sens=mort"], "fr")
        '*<i>maruos</i> («&nbsp;mort&nbsp;»)'
        >>> last_template_handler(["recons", "lang-mot-vedette=fr", "sporo", "sc=Latn"], "fr")
        '*<i>sporo</i>'
        >>> last_template_handler(["recons", "lang-mot-vedette=fr"], "fr")
        '*'

        >>> last_template_handler(["siècle"], "fr")
        '<i>(Siècle à préciser)</i>'
        >>> last_template_handler(["siècle", "?"], "fr")
        '<i>(Siècle à préciser)</i>'
        >>> last_template_handler(["siècle", ""], "fr")
        '<i>(Siècle à préciser)</i>'
        >>> last_template_handler(["siècle", "XVIII"], "fr")
        '<i>(XVIII<sup>e</sup> siècle)</i>'
        >>> last_template_handler(["siècle", "XVIII"], "fr")
        '<i>(XVIII<sup>e</sup> siècle)</i>'
        >>> last_template_handler(["siècle", "XVIII", "XIX"], "fr")
        '<i>(XVIII<sup>e</sup> siècle - XIX<sup>e</sup> siècle)</i>'

        >>> last_template_handler(["Suisse", "fr", "précision=Fribourg, Valais, Vaud"], "fr")
        '<i>(Suisse : Fribourg, Valais, Vaud)</i>'
        >>> last_template_handler(["Suisse", "it"], "fr")
        '<i>(Suisse)</i>'

        >>> last_template_handler(["supplétion", "aller"], "fr")
        'Cette forme dénote une supplétion car son étymologie est distincte de celle de <i>aller</i>'
        >>> last_template_handler(["supplétion", "un", "mot=oui"], "fr")
        'Ce mot dénote une supplétion car son étymologie est distincte de celle de <i>un</i>'
        >>> last_template_handler(["supplétion", "better", "best", "lang=en", "mot=oui"], "fr")
        'Ce mot dénote une supplétion car son étymologie est distincte de celles de <i>better</i> et de <i>best</i>'
        >>> last_template_handler(["supplétion", "am", "are", "was", "lang=en", "mot=oui"], "fr")
        'Ce mot dénote une supplétion car son étymologie est distincte de celles de <i>am</i>, de <i>are</i> et de <i>was</i>'

        >>> last_template_handler(["syncope", "fr", "m=1"], "fr")
        'Syncope'
        >>> last_template_handler(["syncope", "fr", "de=ne voilà-t-il pas"], "fr")
        'syncope de <i>ne voilà-t-il pas</i>'
        >>> last_template_handler(["parataxe", "fr", "de=administrateur", "de2=réseau"], "fr")
        'parataxe de <i>administrateur</i> et de <i>réseau</i>'
        >>> last_template_handler(["déglutination", "fr", "de=agriote", "texte=l’agriote", "m=1"], "fr")
        'Déglutination de <i>l’agriote</i>'

        >>> last_template_handler(["univerbation", "m=1", "fr", "de=gens", "de2=armes"], "fr")
        'Univerbation de <i>gens</i> et de <i>armes</i>'
        >>> last_template_handler(["univerbation", "m=1", "fr", "de=gens", "texte=les gens", "de2=armes", "texte2=les armes"], "fr")
        'Univerbation de <i>les gens</i> et de <i>les armes</i>'

        >>> last_template_handler(["zh-lien", "人", "rén"], "fr")
        '人 (<i>rén</i>)'
        >>> last_template_handler(["zh-lien", "马", "mǎ", "馬"], "fr")
        '马 (馬, <i>mǎ</i>)'
        >>> last_template_handler(["zh-lien", "骨", "gǔ", "骨"], "fr")
        '骨 (骨, <i>gǔ</i>)'

        >>> last_template_handler(["LienRouge", "fr=Comité", "trad=United Nations", "texte=COPUOS"], "fr")
        '<i>COPUOS</i>'
        >>> last_template_handler(["LienRouge", "Comité", "trad=Ausschuss", "texte=COPUOS"], "fr")
        '<i>COPUOS</i>'
        >>> last_template_handler(["LienRouge", "fr=Comité", "trad=United Nations"], "fr")
        '<i>Comité</i>'
        >>> last_template_handler(["LienRouge", "Comité", "trad=Ausschuss"], "fr")
        '<i>Comité</i>'
        >>> last_template_handler(["LienRouge", "fr=Comité"], "fr")
        '<i>Comité</i>'
        >>> last_template_handler(["LienRouge", "Comité"], "fr")
        '<i>Comité</i>'
        >>> last_template_handler(["LienRouge", "trad=United Nations"], "fr")
        '<i>United Nations</i>'

    """
    from .langs import langs
    from ..defaults import last_template_handler as default
    from ...user_functions import (
        capitalize,
        century,
        extract_keywords_from,
        italic,
        strong,
        term,
    )

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "acronyme":
        if not data["texte"] and not data["de"]:
            return italic("(Acronyme)")
        phrase = "Acronyme" if data["m"] in ("1", "oui") else "acronyme"
        return f"{phrase} de {italic(data['texte'] or data['de'])}"

    if tpl == "argot":
        phrase = "Argot"
        if data["spéc"]:
            phrase += f" {data['spéc']}"
        elif len(parts) == 2:
            phrase += f" {parts[1]}"
        return term(phrase)

    if tpl in (
        "agglutination",
        "déglutination",
        "dénominal",
        "déverbal",
        "déverbal sans suffixe",
        "parataxe",
        "reverlanisation",
        "syncope",
        "univerbation",
    ):
        phrase = tpl
        if data["m"] == "1":
            phrase = capitalize(phrase)

        if data["de"]:
            phrase += " de "
            if data["nolien"] != "1" and data["texte"]:
                phrase += italic(data["texte"])
            else:
                phrase += italic(data["de"])

        if tpl in ("univerbation", "parataxe") and data["de2"]:
            phrase += " et de "
            if data["nolien"] != "1" and data["texte2"]:
                phrase += italic(data["texte2"])
            else:
                phrase += italic(data["de2"])

        return phrase

    if tpl in ("cit_réf", "cit réf"):
        i = 0
        if data["titre"]:
            phrase = italic(data["titre"])
        else:
            phrase = italic(parts[i])
            i += 1
        phrase += ", "
        if data["date"]:
            phrase += data["date"]
        elif i < len(parts):
            phrase += parts[i]
            i += 1
        if data["auteur"]:
            phrase = data["auteur"] + ", " + phrase
        elif i < len(parts):
            phrase = parts[i] + ", " + phrase
            i += 1
        if data["article"]:
            phrase = f"«&nbsp;{data['article']}&nbsp;», dans {phrase}"
        elif i < len(parts):
            phrase = f"«&nbsp;{parts[i]}&nbsp;», dans {phrase}"
            i += 1
        phrase += f", {data['pages']}" if data["pages"] else ""
        phrase = (
            f"{data['auteur_article']}, {phrase}" if data["auteur_article"] else phrase
        )
        return phrase

    if tpl in ("composé de", "composé_de"):
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
                    phrase += f" («&nbsp;{data[idx]}&nbsp;»)"

                phrase += (
                    " avec le "
                    if number == len(parts) - 1
                    else ", "
                    if multiple and number <= len(part)
                    else ""
                )

            if "sens" in data:
                phrase += f", littéralement «&nbsp;{data['sens']}&nbsp;»"

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
                phrase += f" («&nbsp;{data[idx]}&nbsp;»)"

            phrase += (
                " et de "
                if number == len(parts) - 1
                else ", "
                if multiple and number <= len(part)
                else ""
            )

        if "sens" in data:
            phrase += f", littéralement «&nbsp;{data['sens']}&nbsp;»"

        return phrase

    if tpl == "date":
        date = parts[-1] if parts and parts[-1] not in ("", "?") else "Date à préciser"
        return term(capitalize(date))

    if tpl == "équiv-pour":
        phrase = f"(pour {parts.pop(0)} "
        phrase += data.get("texte", "on dit" if len(parts) == 1 else "on peut dire")
        return f"{italic(phrase)}&nbsp: {', '.join(parts)}{italic(')')}"

    if tpl in ("étyl", "étylp", "calque"):
        # The lang name
        phrase = langs[data["1"] or parts.pop(0)]

        for part in parts:
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
            phrase += f" («&nbsp;{data['sens']}&nbsp;»)"

        return phrase

    if tpl in ("forme reconstruite", "recons"):
        phrase = italic(parts.pop(0)) if parts else ""
        if data["sens"]:
            phrase += f" («&nbsp;{data['sens']}&nbsp;»)"
        return f"*{phrase}"

    if tpl == "fr-verbe-flexion":
        return data.get("1", parts[0] if parts else "")

    if tpl == "la-verb":
        phrase = strong(parts[0]) + ","
        if data["2ps"]:
            phrase += f" {data.get('2ps2', data['2ps'])},"
        phrase += f" {italic('infinitif')} : {parts[2]}"
        if parts[3] != "-":
            phrase += f", {italic('parfait')} : {parts[4]}"
        if data["44"]:
            phrase += f", {italic(data['44'])} : {parts[6]}"
        elif len(parts) > 5:
            phrase += f", {italic('supin')} : {parts[6]}"
        if data["pattern"]:
            phrase += " " + italic(f"({data['pattern']})")
        return phrase

    if tpl in ("lien", "l"):
        phrase = parts.pop(0)
        if data["tr"]:
            phrase += f", {italic(data['tr'])}"
        if data["sens"]:
            phrase += f" («&nbsp;{data['sens']}&nbsp;»)"
        return phrase

    if tpl == "LienRouge":
        if data["texte"]:
            return italic(data["texte"])
        if data["fr"]:
            return italic(data["fr"])
        if parts:
            return italic(parts[0])
        if data["trad"]:
            return italic(data["trad"])

    if tpl == "phon":
        return strong(f"[{parts[0]}]")

    if tpl.lower() == "polytonique":
        phrase = parts.pop(0)
        if data["tr"] or parts:
            phrase += f", {italic(data['tr'] or parts.pop(0))}"
        if data["sens"] or parts:
            phrase += f" («&nbsp;{data['sens'] or parts.pop(0)}&nbsp;»)"
        return phrase

    if tpl == "siècle":
        parts = [
            part for part in parts if part.strip() and part not in ("lang=fr", "?")
        ]
        phrase = century(parts, "siècle") if parts else "Siècle à préciser"
        return term(phrase)

    if tpl == "Suisse":
        if data["précision"]:
            return term(f"Suisse : {data['précision']}")
        else:
            return term("Suisse")

    if tpl == "supplétion":
        if data["mot"]:
            phrase = "Ce mot dénote une supplétion car son étymologie est distincte de "
        else:
            phrase = (
                "Cette forme dénote une supplétion car son étymologie est distincte de "
            )
        if len(parts) > 1:
            phrase += "celles de "
            phrase += ", de ".join(f"{italic(p)}" for p in parts[:-1])
            phrase += f" et de {italic(parts[-1])}"
        else:
            phrase += f"celle de {italic(parts[0])}"
        return phrase

    if tpl == "zh-lien":
        simple = parts.pop(0)
        pinyin = italic(parts.pop(0))
        traditional = parts[0] if parts else ""
        if not traditional:
            return f"{simple} ({pinyin})"
        return f"{simple} ({traditional}, {pinyin})"

    # This is a country in the current locale
    if tpl in langs:
        return langs[tpl]

    return default(template, locale, word=word)


# Contenu de la release sur GitHub :
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr
release_description = """\
Nombre de mots : {words_count}
Export Wiktionnaire : {dump_date}

Installation :

1. Copier le fichier [dicthtml-{locale}.zip <sup>:floppy_disk:</sup>]({url}) dans le dossier `.kobo/custom-dict/` de la liseuse.
2. **Redémarrer** la liseuse.

<sub>Mis à jour le {creation_date}</sub>
"""  # noqa

# Le nom du dictionnaire qui sera affiché en-dessous de chaque définition
wiktionary = "Wiktionnaire (ɔ) {year}"
