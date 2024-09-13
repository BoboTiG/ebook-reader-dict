"""French language."""

import re

from ...user_functions import flatten, uniq
from .ar_pronunciation import toIPA
from .arabiser import appliquer, arabiser
from .domain_templates import domain_templates
from .regions import regions

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
etyl_section = ("{{S|étymologie}}",)
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
    "{{S|nom de famille|fr|",
    "{{S|nom de famille|fr}",
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
    "{{S|pronom indéfini|fr}",
    "{{S|pronom indéfini|fr|",
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

# Variantes
variant_titles = (
    "{{S|adjectif|fr}",
    "{{S|adjectif|fr|flexion",
    "{{S|pronom indéfini|fr|flexion",
    "{{S|nom|fr|flexion",
    "{{S|verbe|fr|flexion",
)
variant_templates = (
    "{{fr-accord-",
    "{{fr-rég",
    "{{fr-verbe-flexion",
)

# Certaines définitions ne sont pas intéressantes à garder (pluriel, genre, ...)
definitions_to_ignore = (
    "habitante",
    "masculin pluriel",
    "féminin pluriel",
    "''féminin de''",
    "féminin singulier",
    "masculin et féminin pluriel",
    "masculin ou féminin pluriel",
    "pluriel d",
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
    "couleurN",
    "créer-séparément",
    "désabrévier",
    "ébauche-déf",
    "ébauche-étym",
    "ébauche-exe",
    "exemple",
    "ibid",
    "Import",
    "lire en ligne",
    "Modèle",
    "Ouvrage",
    "ouvrage",
    "périodique",
    "préciser",
    "R",
    "RÉF",
    "réf",
    "source",
    "Source-wikt",
    "trad-exe",
    "trier",
    "vérifier",
    "voir",
    "voir-conj",
)

# Modèles qui seront remplacés par du texte italique.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les
templates_italic = {
    **domain_templates,
    **regions,
    "Afghanistan": "Afghanistan",
    "Rwanda": "Rwanda",
    "absol": "Absolument",
    "absolument": "Absolument",
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
    "au féminin": "Au féminin",
    "au figuré": "Sens figuré",
    "au pluriel": "Au pluriel",
    "au singulier": "Au singulier",
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
    "beaucoup moins courant": "Beaucoup moins courant",
    "beaucoup plus courant": "Beaucoup plus courant",
    "botan": "Botanique",
    "bot.": "Botanique",
    "Bruxelles": "Brusseleer",
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
    "courant": "Courant",
    "cours d'eau": "Géographie",
    "cout": "Couture",
    "critiqué": "Usage critiqué",
    "cycl": "Cyclisme",
    "dermatol": "Dermatologie",
    "déris": "Par dérision",
    "dérision": "Par dérision",
    "désuet": "Désuet",
    "détroit": "Géographie",
    "diaéthique": "Variation diaéthique",
    "didact": "Didactique",
    "diplo": "Diplomatie",
    "élec": "Électricité",
    "en particulier": "En particulier",
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
    "figuré": "Sens figuré",
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
    "idiom": "Idiotisme",
    "idiomatique": "Sens figuré",
    "idiomatisme": "Idiotisme",
    "impersonnel": "Impersonnel",
    "impr": "Imprimerie",
    "improprement": "Usage critiqué",
    "indén": "Indénombrable",
    "indus": "Industrie",
    "info": "Informatique",
    "injur": "Injurieux",
    "injurieux": "Injurieux",
    "intrans": "Intransitif",
    "intransitif": "Intransitif",
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
    "louchébem": "Louchébem",
    "légis": "Droit",
    "m-cour": "Moins courant",
    "moins courant": "Moins courant",
    "maçon": "Maçonnerie",
    "maladie": "Nosologie",
    "manège": "Équitation",
    "marque": "Marque commerciale",
    "marque commerciale": "Marque commerciale",
    "marque déposée": "Marque commerciale",
    "math": "Mathématiques",
    "méc": "Mécanique",
    "médecine non conv": "Médecine non conventionnelle",
    "mélio": "Mélioratif",
    "menu": "Menuiserie",
    "mercatique": "Marketing",
    "métrol": "Métrologie",
    "mili": "Militaire",
    "militant": "Vocabulaire militant",
    "minér": "Minéralogie",
    "musi": "Musique",
    "mythol": "Mythologie",
    "méca": "Mécanique",
    "méde": "Médecine",
    "métal": "Métallurgie",
    "métaph": "Sens figuré",
    "métaphore": "Sens figuré",
    "météo": "Météorologie",
    "météorol": "Météorologie",
    "méton": "Par métonymie",
    "métonymie": "Par métonymie",
    "moderne": "Moderne",
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
    "POO": "Programmation orientée objet",
    "p-us": "Peu usité",
    "p us": "Peu usité",
    "paléogr": "Paléographie",
    "par analogie": "Par analogie",
    "par euphémisme": "Par euphémisme",
    "par ext": "Par extension",
    "par extension": "Par extension",
    "par hyperbole": "Par hyperbole",
    "par litote": "Par litote",
    "par métonymie": "Par métonymie",
    "par plaisanterie": "Par plaisanterie",
    "parler bellifontain": "Parler bellifontain",
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
    "plus courant": "Plus courant",
    "plais": "Par plaisanterie",
    "plaisanterie": "Par plaisanterie",
    "plus rare": "Plus rare",
    "poés": "Poésie",
    "poét": "Poétique",
    "polit": "Politique",
    "popu": "Populaire",
    "presse": "Journalisme",
    "procédure": "Justice",
    "prog": "Programmation informatique",
    "programmation": "Programmation informatique",
    "pronl": "Pronominal",
    "pronominal": "Pronominal",
    "propre": "Sens propre",
    "propriété": "Droit",
    "propulsion": "Propulsion spatiale",
    "prov": "Proverbial",
    "psychia": "Psychiatrie",
    "psychol": "Psychologie",
    "reli": "Religion",
    "réciproque2": "Réciproque",
    "réfléchi": "Réfléchi",
    "réflexif": "Réfléchi",
    "réseaux": "Réseaux informatiques",
    "sci-fi": "Science-fiction",
    "scol": "Éducation",
    "scolaire": "Éducation",
    "sens propre": "Sens propre",
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
    "transitif": "Transitif",
    "transports": "Transport",
    "tradit": "orthographe traditionnelle",
    "très-rare": "Très rare",
    "très très rare": "Extrêmement rare",
    "typo": "Typographie",
    "typog": "Typographie",
    "télé": "Audiovisuel",
    "un os": "Anatomie",
    "un_os": "Anatomie",
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
templates_multi = {
    # {{1|Descendant}}
    "1": "parts[1]",
    # {{1er}}
    # {{1er|mai}}
    "1er": "f\"1{superscript('er')}{'&nbsp;' + parts[1] if len(parts) > 1 else ''}\"",
    # {{1re}}
    # {{1re|fois}}
    "1re": "f\"1{superscript('re')}{'&nbsp;' + parts[1] if len(parts) > 1 else ''}\"",
    # {{Arabe|ن و ق}}
    "Arab": "parts[1] if len(parts) > 1 else 'arabe'",
    "Arabe": "parts[1] if len(parts) > 1 else 'arabe'",
    "Braille": "parts[1]",
    # {{comparatif de|bien|fr|adv}}
    "comparatif de": "sentence(parts)",
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
    # {{#expr: 2 ^ 30}}
    "#expr": "eval_expr(parts[1])",
    # {{formatnum:-1000000}}
    "formatnum": f'number(parts[1], "{float_separator}", "{thousands_separator}")',
    # {{forme pronominale|mutiner}}
    "forme pronominale": 'f"{capitalize(tpl)} de {parts[1]}"',
    # {{fr-accord-comp|aigre|doux|...}
    "fr-accord-comp": 'f"{parts[1]}-{parts[2]}"',
    # {{fr-accord-comp-mf|eau|de-vie|...}
    "fr-accord-comp-mf": 'f"{parts[1]}-{parts[2]}"',
    # {{fr-accord-oux|d|d}}
    "fr-accord-oux": "parts[1] + 'oux'",
    # {{fr-accord-t-avant1835|abondan|a.bɔ̃.dɑ̃}}
    "fr-accord-t-avant1835": "parts[1]",
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
    # {{info lex|équitation|sport|lang=fr}}
    "info lex": "term(', '.join(capitalize(part) for part in parts[1:] if '=' not in part))",
    # {{ISBN|978-1-23-456789-7|2-876-54301-X}}
    "ISBN": "'ISBN ' + concat(parts[1:], sep=', ', last_sep=' et ')",
    # {{Lang-ar||[[نهر ابراهيم]]|100}}
    "Lang-ar": "parts[2]",
    # {{lexique|philosophie|fr}}
    # {{lexique|philosophie|sport|fr}}
    "lexique": "term(', '.join(capitalize(p) for p in [a for a in parts if '=' not in a][1:-1]))",
    # {{localités|fr|d’Espagne}}
    "localités": "term('Géographie')",
    # {{Mme}}
    # {{Mme|de Maintenon}}
    "Mme": "'M' + superscript('me') + (f' {parts[1]}' if len(parts) > 1 else '')",
    # {{nobr|1 000 000 000 000}}
    "nobr": "re.sub(r'^1=', '', parts[-1].replace(' ', '&nbsp;'))",
    # {{nom w pc|Aldous|Huxley}}
    "nom w pc": "person(word, parts[1:])",
    # {{nombre romain|12}}
    "nombre romain": "int_to_roman(int(parts[1]))",
    # {{numéro}}
    "numéro": 'f\'n{superscript("o")}{parts[1] if len(parts) > 1 else ""}\'',
    "n°": 'f\'n{superscript("o")}{parts[1] if len(parts) > 1 else ""}\'',
    # {{o}}
    "o": "superscript('o')",
    # {{Pas clair|...}}
    "Pas clair": 'f\'{underline(parts[1])}{small("&nbsp;")}{superscript(italic(strong("Pas clair")))}\'',
    # {{petites capitales|Dupont}}
    "petites capitales": "small_caps(parts[1])",
    # {{pc|Dupont}}
    "pc": "small_caps(parts[1])",
    # {{phon|tɛs.tjɔ̃}}
    "phon": "strong(f'[{parts[1]}]')",
    # {{phono|bɔg|fr}}
    "phono": "f'/{parts[1]}/'",
    # {{pron|plys|fr}}
    "pron": r'f"\\{parts[1]}\\"',
    # {{pron-API|/j/}}
    "pron-API": "parts[1]",
    # {{pron-recons|plys|fr}}
    "pron-recons": r'f"*\\{parts[1]}\\"',
    # {{provinces|fr|d’Espagne}}
    "provinces": "term('Géographie')",
    # {{R:Littré|anonacée}})
    "R:Littré": "f'«&nbsp;{parts[-1]}&nbsp;», dans <i>Émile Littré, Dictionnaire de la langue française</i>, 1872–1877'",  # noqa
    # {{R:Tosti|Turgeon}})
    "R:Tosti": "f'«&nbsp;{parts[-1]}&nbsp;» dans Jean {small_caps(\"Tosti\")}, <i>Les noms de famille</i>'",
    # {{RFC|5322}}
    "RFC": "sentence(parts)",
    # {{région}}
    # {{région|Lorraine et Dauphiné}}
    "régio": "term(parts[1] if len(parts) > 1 else 'Régionalisme')",
    "région": "term(parts[1] if len(parts) > 1 else 'Régionalisme')",
    "régional": "term(parts[1] if len(parts) > 1 else 'Régionalisme')",
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
    # {{souligner|r}}espiratory
    "souligner": "underline(parts[1])",
    # {{sport|fr}}
    # {{sport|fr|collectifs}}
    "sport": "term(capitalize(concat(parts, sep=' ', indexes=[0, 2])))",
    # {{substantivation de|mettre en exergue}}
    "substantivation de": 'f"Substantivation de {italic(parts[1])}"',
    # {{superlatif de|petit|fr}}
    "superlatif de": "sentence(parts)",
    # {{trad+|conv|Sitophilus granarius}}
    "trad+": "parts[2]",
    "trad-": "parts[2]",
    # {{wd|Q30092597|Frederick H. Pough}}
    "wd": "parts[2] if len(parts) == 3 else ''",
    # {{wsp|Panthera pardus|''Panthera pardus''}}
    # {{wsp|Brassicaceae}}
    "wsp": "parts[2] if len(parts) > 2 else parts[1]",
    # {{WSP|Panthera leo}}
    "WSP": "italic(parts[1]) if len(parts) > 1 else ''",
    # 1,23{{x10|9}}
    "x10": "f'×10{superscript(parts[1])}' if len(parts) > 1 else '×10'",
}

# Modèles qui seront remplacés par du texte personnalisé.
templates_other = {
    "=": "=",
    "'": "’",
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
    "fsing": "<i>féminin singulier</i>",
    "génit": "<i>génitif</i>",
    "genre": "Genre à préciser",
    "genre ?": "Genre à préciser",
    "généralement pluriel": "Ce terme est généralement utilisé au pluriel.",
    "h": "<sup>(h aspiré)</sup>",
    "h aspiré": "<sup>(h aspiré)</sup>",
    "h_aspiré": "<sup>(h aspiré)</sup>",
    "h muet": "<sup>(h muet)</sup>",
    "i": "<i>intransitif</i>",
    "impers": "<i>impersonnel</i>",
    "indéterminé": "indéterminé",
    "invar": "<i>invariable</i>",
    "invariable": "<i>invariable</i>",
    "invisible": "",
    "la-note-ij": "Le ‹&nbsp;j&nbsp;›, absent du latin classique, traduit le ‹&nbsp;i&nbsp;› devant une voyelle dans la tradition scholastique française. Cf. «&nbsp;j en latin&nbsp;».",  # noqa
    "liaison": "‿",
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
    "note-gentilé": "Ce mot est un gentilé. Un gentilé désigne les habitants d’un lieu, les personnes qui en sont originaires ou qui le représentent (par exemple, les membres d’une équipe sportive).",  # noqa
    "note-majuscule-taxo": "En biologie, le genre, premier mot du nom binominal et les autres noms scientifiques (en latin) prennent toujours une majuscule. Par exemple : Homme moderne : <i>Homo sapiens</i>, famille : Hominidae. Quand ils utilisent des noms en français, ainsi que dans d’autres langues, les naturalistes mettent fréquemment une majuscule aux noms de taxons supérieurs à l’espèce (par exemple : <i>les Hominidés</i>, ou <i>les hominidés</i>).",  # noqa
    "note-majuscule-taxon": "En biologie, le genre, premier mot du nom binominal et les autres noms scientifiques (en latin) prennent toujours une majuscule. Par exemple : Homme moderne : <i>Homo sapiens</i>, famille : Hominidae. Quand ils utilisent des noms en français, ainsi que dans d’autres langues, les naturalistes mettent fréquemment une majuscule aux noms de taxons supérieurs à l’espèce (par exemple : <i>les Hominidés</i>, ou <i>les hominidés</i>)",  # noqa
    "peu attesté": "⚠ Ce terme est très peu attesté.",
    "o": "<i>neutre</i>",
    "p": "<i>pluriel</i>",
    "palind": "<i>palindrome</i>",
    "pluriel": "<i>pluriel</i>",
    "pp": "<i>participe passé</i>",
    "pré": "<i>prétérit</i>",
    "prés": "<i>présent</i>",
    "prnl": "<i>pronominal</i>",
    "s": "<i>singulier</i>",
    "sp": "<i>singulier et pluriel identiques</i>",
    "sp ?": "<i>singulier et pluriel identiques ou différenciés (l’usage hésite)</i>",
    "R:Larousse2vol1922": "<i>Larousse universel en 2 volumes</i>, 1922",
    "R:Rivarol": "Antoine de Rivarol, <i>Dictionnaire classique de la langue française</i>, 1827 ",
    "réfl": "<i>réfléchi</i>",
    "réciproque": "<i>réciproque</i>",
    "t": "<i>transitif</i>",
    "tr-dir": "<i>transitif direct</i>",
    "tr-indir": "<i>transitif indirect</i>",
    "uplet/étym": "Tiré de la fin du suffixe <i>-uple</i> qu’on retrouve dans quintuple, sextuple, qui exprime une multiplication, dérivé du latin <i>-plus</i>.",  # noqa
    "usage": "<b>Note d’usage&nbsp;:</b>",
    "vlatypas-pivot": "v’là-t-i’ pas",
}


# Contenu de la release sur GitHub :
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr
release_description = """\
Nombre de mots : {words_count}
Export Wiktionnaire : {dump_date}

Fichiers disponibles :

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Mis à jour le {creation_date}</sub>
"""  # noqa

# Le nom du dictionnaire qui sera affiché en-dessous de chaque définition
wiktionary = "Wiktionnaire (ɔ) {year}"


def find_genders(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"{([fmsingp]+)(?: \?\|fr)*}"),
) -> list[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("'''-eresse''' {{pron|(ə).ʁɛs|fr}} {{f}}")
    ['f']
    >>> find_genders("'''42''' {{msing}}")
    ['msing']
    """
    return uniq(flatten(pattern.findall(code)))


def find_pronunciations(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"{pron(?:\|lang=fr)?\|([^}\|]+)"),
) -> list[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{pron|ɑ|fr}}")
    ['\\\\ɑ\\\\']
    >>> find_pronunciations("{{pron|ɑ|fr}}, {{pron|a|fr}}")
    ['\\\\ɑ\\\\', '\\\\a\\\\']
    """
    if not (match := pattern.search(code)):
        return []

    # There is at least one match, we need to get whole line
    # in order to be able to find multiple pronunciations
    line = code[match.start() : code.find("\n", match.start())]
    return [f"\\{p}\\" for p in uniq(pattern.findall(line))]


def last_template_handler(template: tuple[str, ...], locale: str, word: str = "") -> str:
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

        >>> last_template_handler(["Citation bloc", "Exemple simple."], "fr")
        '<br/>«&nbsp;Exemple simple.&nbsp;»<br/>'

        >>> last_template_handler(["code langue", "créole guyanais"], "fr")
        'gcr'
        >>> last_template_handler(["code langue", "foo"], "fr")
        ''

        >>> last_template_handler(["diminutif", "fr"], "fr")
        '<i>(diminutif)</i>'
        >>> last_template_handler(["diminutif", "fr", "m=1"], "fr")
        '<i>(Diminutif)</i>'
        >>> last_template_handler(["diminutif", "fr", "de=balle"], "fr")
        'diminutif de <i>balle</i>'

        >>> last_template_handler(["ellipse"], "fr")
        '<i>(Par ellipse)</i>'
        >>> last_template_handler(["ellipse", "de=piston racleur"], "fr")
        '<i>(Ellipse de</i> piston racleur<i>)</i>'

        >>> last_template_handler(["emploi", "au passif"], "fr")
        '<i>(Au passif)</i>'
        >>> last_template_handler(["emploi", "lang=fr", "au passif"], "fr")
        '<i>(Au passif)</i>'
        >>> last_template_handler(["emploi", "au passif", "fr"], "fr")
        '<i>(Au passif)</i>'

        >>> last_template_handler(["fr-accord-ain", "a.me.ʁi.k"], "fr", word="américain")
        'américain'
        >>> last_template_handler(["fr-accord-eau", "cham", "ʃa.m", "inv=de Bactriane", "pinv=.də.bak.tʁi.jan"], "fr")
        'chameau de Bactriane'
        >>> last_template_handler(["fr-accord-el", "ɔp.sjɔ.n", "ms=optionnel"], "fr")
        'optionnel'
        >>> last_template_handler(["fr-accord-en", "bu.le.", "ms=booléen"], "fr")
        'booléen'
        >>> last_template_handler(["fr-accord-er", "bouch", "bu.ʃ", "ms=boucher"], "fr")
        'boucher'
        >>> last_template_handler(["fr-accord-et", "kɔ.k", "ms=coquet"], "fr")
        'coquet'
        >>> last_template_handler(["fr-accord-eux", "malheur", "ma.lœ.ʁ"], "fr")
        'malheureux'
        >>> last_template_handler(["fr-accord-f", "putati", "py.ta.ti"], "fr")
        'putatif'
        >>> last_template_handler(["fr-accord-in", "ma.lw", "deux_n=1"], "fr", word="mallouinnes")
        'mallouin'
        >>> last_template_handler(["fr-accord-in", "ma.lw", "deux_n=1"], "fr", word="mallouins")
        'mallouin'
        >>> last_template_handler(["fr-accord-in", "ma.lw", "deux_n=1"], "fr", word="mallouinne")
        'mallouin'
        >>> last_template_handler(["fr-accord-ind", "m=chacun", "pm=ʃa.kœ̃", "pf=ʃa.kyn"], "fr", word="chacune")
        'chacun'
        >>> last_template_handler(["fr-accord-mf-al", "anim", "a.ni.m"], "fr")
        'animal'
        >>> last_template_handler(["fr-accord-oin", "pron=sɑ̃.ta.lw"], "fr", word="santaloines")
        'santaloine'
        >>> last_template_handler(["fr-accord-rég", "ka.ʁɔt"], "fr", word="aïeuls")
        'aïeul'
        >>> last_template_handler(["fr-accord-rég", "a.ta.ʃe də pʁɛs", "ms=attaché", "inv=de presse"], "fr")
        'attaché de presse'
        >>> last_template_handler(["fr-rég", "ka.ʁɔt"], "fr", word="carottes")
        'carotte'
        >>> last_template_handler(["fr-rég", "ʁy", "s=ru"], "fr")
        'ru'
        >>> last_template_handler(["fr-rég", "ɔm d‿a.fɛʁ", "s=homme", "inv=d’affaires"], "fr", word="hommes d’affaires")
        'homme d’affaires'
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

        >>> last_template_handler(["R:TLFi"], "fr", "pedzouille")
        '«&nbsp;pedzouille&nbsp;», dans <i>TLFi, Le Trésor de la langue française informatisé</i>, 1971–1994'
        >>> last_template_handler(["R:TLFi", "pomme"], "fr", "pedzouille")
        '«&nbsp;pomme&nbsp;», dans <i>TLFi, Le Trésor de la langue française informatisé</i>, 1971–1994'
        >>> last_template_handler(["R:DAF6", "pomme"], "fr", "pedzouille")
        '«&nbsp;pomme&nbsp;», dans <i>Dictionnaire de l’Académie française, sixième édition</i>, 1832-1835'

        >>> last_template_handler(["Légifrance", "base=CPP", "numéro=230-45", "texte=article 230-45"], "fr")
        'article 230-45'
        >>> last_template_handler(["Légifrance", "base=CPP", "numéro=230-45"], "fr")
        ''

        >>> last_template_handler(["ar-ab", "lubné"], "fr")
        'لُبْنَى'

        >>> last_template_handler(["ar-cf", "ar-*i*â*ũ", "ar-ktb"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">كِتَابٌ</span></span> <small>(kitâbũ)</small> («&nbsp;livre, écriture ; pièce écrite&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*â*i*ũ", "ar-kfr", "ici=incroyant"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">كَافِرٌ</span></span> <small>(kâfirũ)</small> (ici, «&nbsp;incroyant&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*u**ânũ", "ar-qr'"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">قُرْآنٌ</span></span> <small>(qur\\\'ânũ)</small> («&nbsp;lecture&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*a*a*@ũ", "ar-qSb"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">قَصَبَةٌ</span></span> <small>(qaSab@ũ)</small> («&nbsp;forteresse&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*u*ay*ũ", "ar-zlj"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">زُلَيْجٌ</span></span> <small>(zulayjũ)</small> («&nbsp;carreau de faïence&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*a*i*iy²ũ", "ar-3lw"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">عَلِيٌّ</span></span> <small>(3aliy²ũ)</small> («&nbsp;supérieur, Ali&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*u*a*ũ", "ar-3mr"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">عُمَرٌ</span></span> <small>(3umarũ)</small> («&nbsp;prospérité&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*u**@ũ", "ar-sWr"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">سُورَةٌ</span></span> <small>(sûr@ũ)</small> («&nbsp;rang, sourate&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*â*i*ũ", "ar-qDy"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">قَاضٍ</span></span> <small>(qâDĩ)</small> («&nbsp;exécuteur, juge&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*a**ânu", "ar-3mr"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">عَمْرَانُ</span></span> <small>(3amrânu)</small> («&nbsp;Amran&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*a**@ũ", "ar-zhr"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">زَهْرَةٌ</span></span> <small>(zahr@ũ)</small> («&nbsp;fleur ; beauté&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*a*â*ũ", "ar-'Vn"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">أَذَانٌ</span></span> <small>(\\\'aVânũ)</small> («&nbsp;adhan, appel à la prière&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*i*â*ũ", "ar-rwD"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">رِوَاضٌ</span></span> <small>(riwâDũ)</small> («&nbsp;{{p}} jardins&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-mu**a*ũ", "ar-rwd"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">مُرَادٌ</span></span> <small>(murâdũ)</small> («&nbsp;désiré, sens&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*a**â'u", "ar-Xbr"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">خَبْرَاءُ</span></span> <small>(Xabrâ\\\'u)</small> («&nbsp;grand sac de voyage&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-ma**i*ũ", "ar-jls"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">مَجْلِسٌ</span></span> <small>(majlisũ)</small> («&nbsp;lieu ou temps où l\\\'on est assis&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*i*â*ũ", "ar-jhd"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">جِهَادٌ</span></span> <small>(jihâdũ)</small> («&nbsp;lutte, effort&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*a*î*ũ", "ar-nZr"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">نَظِيرٌ</span></span> <small>(naZîrũ)</small> («&nbsp;pareil ; en face&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*i**ũ", "ar-jnn"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">جِنٌّ</span></span> <small>(jinnũ)</small> («&nbsp;djinn&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-**â*ũ", "ar-Hrm"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">إِحْرَامٌ</span></span> <small>(iHrâmũ)</small> («&nbsp;consécration&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*u**@ũ", "ar-sWr"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">سُورَةٌ</span></span> <small>(sûr@ũ)</small> («&nbsp;rang, sourate&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*â*a*a", "ar-ktb"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">كَاتَبَ</span></span> <small>(kâtaba)</small> («&nbsp;entretenir une correspondance&nbsp;»)'
        >>> last_template_handler(["ar-cf", "ar-*a*aba", "ar-c3b"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">شَعَبَ</span></span> <small>(ca3aba)</small>'
        >>> last_template_handler(["ar-cf", "ar-*i*a*ũ", "ar-jnn"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">جِنَنٌ</span></span> <small>(jinanũ)</small>'

        >>> last_template_handler(["ar-mot", "elHasan_"], "fr")
        '<span style="line-height: 0px;"><span style="font-size:larger">الحَسَن</span></span> <small>(elHasan_)</small>'

        >>> last_template_handler(["ar-racine/nom", "ar-ktb"], "fr")
        "كتب: relatif à l'action d'écrire, relier"

        >>> last_template_handler(["ar-sch", "ar-*â*a*a"], "fr")
        'زَارَزَ'

        >>> last_template_handler(["ar-terme", "mu'ad²ibũ"], "fr")
        "مُؤَدِّبٌ (<i>mu'ad²ibũ</i>) /mu.ʔad.di.bun/"

        >>> last_template_handler(["nom langue", "gcr"], "fr")
        'créole guyanais'
        >>> last_template_handler(["langue", "gcr"], "fr")
        'Créole guyanais'

        >>> last_template_handler(["rouge", "un texte"], "fr")
        '<span style="color:red">un texte</span>'
        >>> last_template_handler(["rouge", "texte=un texte"], "fr")
        '<span style="color:red">un texte</span>'
        >>> last_template_handler(["rouge", "fond=1", "1=un texte"], "fr")
        '<span style="background-color:red">un texte</span>'

        >>> last_template_handler(["wp"], "fr")
        'sur l’encyclopédie Wikipédia'
        >>> last_template_handler(["wp"], "fr", "word")
        'word sur l’encyclopédie Wikipédia'
        >>> last_template_handler(["wp","Sarcoscypha coccinea"], "fr")
        'Sarcoscypha coccinea sur l’encyclopédie Wikipédia'
        >>> last_template_handler(["wp","Vénus (planète)", "Planète Vénus"], "fr")
        'Planète Vénus sur l’encyclopédie Wikipédia'
        >>> last_template_handler(["wp","Norv%C3%A8ge#%C3%89tymologie)", 'la section "Étymologie" de l\\'article Norvège'], "fr")
        'la section "Étymologie" de l\\'article Norvège sur l’encyclopédie Wikipédia'
        >>> last_template_handler(["wp", "Dictionary", "lang=en"], "fr")
        'Dictionary sur l’encyclopédie Wikipédia (en anglais)'

        >>> last_template_handler(["zh-l", "餃子/饺子", "jiǎozi", "jiaozi bouillis"], "fr")
        '餃子／饺子 (<i>jiǎozi</i>, «&nbsp;jiaozi bouillis&nbsp;»)'

    """  # noqa
    from ...user_functions import (
        capitalize,
        chinese,
        extract_keywords_from,
        italic,
        person,
        term,
    )
    from ..defaults import last_template_handler as default
    from .langs import langs
    from .template_handlers import lookup_template, render_template

    if lookup_template(template[0]):
        return render_template(word, template)

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
        if not date:
            return italic(book) if book else author
        return f"{author}, {italic(book)}, {date}, page {page}" if page else f"{author}, {italic(book)}, {date}"

    if tpl == "Citation bloc":
        return f"<br/>«&nbsp;{parts[0]}&nbsp;»<br/>"

    if tpl == "code langue":
        lang = parts[0]
        return next((code for code, l10n in langs.items() if l10n == lang), "")

    if tpl == "diminutif":
        phrase = "Diminutif" if data["m"] in ("1", "oui") else "diminutif"
        if data["de"]:
            phrase += f" de {italic(data['de'])}"
        else:
            phrase = term(phrase)
        return phrase

    if tpl in ("ellipse", "par ellipse"):
        return f'{italic("(Ellipse de")} {data["de"]}{italic(")")}' if data["de"] else term("Par ellipse")

    if tpl == "R:DAF6":
        w = parts[0] if parts else word
        return f"«&nbsp;{w}&nbsp;», dans <i>Dictionnaire de l’Académie française, sixième édition</i>, 1832-1835"

    if tpl == "R:TLFi":
        w = parts[0] if parts else word
        return f"«&nbsp;{w}&nbsp;», dans <i>TLFi, Le Trésor de la langue française informatisé</i>, 1971–1994"

    if tpl == "emploi":
        return term(capitalize(parts[0]))

    if tpl == "fr-verbe-flexion":
        return data.get("1", parts[0] if parts else "")

    if tpl.startswith(("fr-accord-rég", "fr-rég")):
        if not (singular := data["s"] or data["m"] or data["ms"]):
            singular = word.rstrip("s")
        if data["inv"]:
            singular += f" {data['inv']}"
        return singular

    if tpl.startswith("fr-accord-"):
        if not (singular := data["s"] or data["m"] or data["ms"]):
            singular = word.rstrip("s") if len(parts) < 2 else f"{parts[0]}{tpl.split('-')[-1]}"
            if tpl == "fr-accord-in" and singular == word.rstrip("s"):
                singular = singular.removesuffix("ne" if data["deux_n"] else "e")
        if data["inv"]:
            singular += f" {data['inv']}"
        return singular

    if tpl == "Légifrance":
        return data["texte"]

    if tpl in ("langue", "nom langue"):
        phrase = langs[parts[0]]
        if tpl == "langue":
            phrase = phrase[0].capitalize() + phrase[1:]
        return phrase

    if tpl in {"ar-ab", "ar-mo"}:
        return arabiser(parts[0])

    if tpl == "ar-cf":
        scheme = appliquer(parts[0], parts[1], var=parts[2] if len(parts) > 2 else "")
        w = arabiser(scheme)
        from ...utils import clean
        from .racines_arabes import racines_schemes_arabes

        sens = (
            f"ici, «&nbsp;{data['ici']}&nbsp;»"
            if data["ici"]
            else f"«&nbsp;{clean(racines_schemes_arabes[parts[1]][parts[0]])}&nbsp;»"
            if parts[1] in racines_schemes_arabes and parts[0] in racines_schemes_arabes[parts[1]]
            else ""
        )
        sens = f" ({sens})" if sens else ""

        return (
            f'<span style="line-height: 0px;"><span style="font-size:larger">{w}</span></span>'
            f" <small>({scheme})</small>"
            f"{sens}"
        )

    if tpl == "ar-mot":
        return f'<span style="line-height: 0px;"><span style="font-size:larger">{arabiser(parts[0])}</span></span> <small>({parts[0]})</small>'  # noqa

    if tpl == "ar-racine/nom":
        from .racines_arabes import racines_schemes_arabes

        return f"{arabiser(parts[0].split('-')[1])}: {racines_schemes_arabes[parts[0]]['aa_sens']}"

    if tpl == "ar-sch":
        return arabiser(appliquer(parts[0], parts[1] if len(parts) > 1 else "ar-zrzr"))

    if tpl == "ar-terme":
        arab = arabiser(parts[0])
        return f"{arab} ({italic(parts[0])}) /{toIPA(arab)}/"

    if tpl == "rouge":
        prefix_style = "background-" if data["fond"] == "1" else ""
        phrase = parts[0] if parts else data["texte"] or data["1"]
        return f'<span style="{prefix_style}color:red">{phrase}</span>'

    if tpl in ("Wikipedia", "Wikipédia", "wikipédia", "wp", "WP"):
        start = ""
        if parts:
            start = parts[1] if len(parts) > 1 else parts[0]
        elif word:
            start = word
        phrase = "sur l’encyclopédie Wikipédia"
        if data["lang"]:
            l10n = langs[data["lang"]]
            phrase += f" (en {l10n})"
        return f"{start} {phrase}" if start else phrase

    if tpl in ("zh-l", "zh-m"):
        return chinese(parts, data, laquo="«&nbsp;", raquo="&nbsp;»")

    # This is a country in the current locale
    return langs[tpl] if tpl in langs else default(template, locale, word=word)
