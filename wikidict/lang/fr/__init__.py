"""French language."""

import re

from ...user_functions import flatten, unique
from .ar_pronunciation import toIPA
from .arabiser import appliquer, arabiser
from .contexts import contexts
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
section_patterns = ("#", r"\*")
head_sections = ("{{langue|fr}}", "{{langue|conv}}", "{{caractère}}")
etyl_section = ("{{s|étymologie}}",)
sections = (
    *etyl_section,
    "{{s|abréviations}",
    "{{s|adjectif démonstratif|fr|",
    "{{s|adjectif démonstratif|fr}",
    "{{s|adjectif exclamatif|fr|",
    "{{s|adjectif exclamatif|fr}",
    "{{s|adjectif indéfini|fr|",
    "{{s|adjectif indéfini|fr}",
    "{{s|adjectif interrogatif|fr|",
    "{{s|adjectif interrogatif|fr}",
    "{{s|adjectif numéral|fr|",
    "{{s|adjectif numéral|fr}",
    "{{s|adjectif possessif|fr|",
    "{{s|adjectif possessif|fr}",
    "{{s|adjectif relatif|fr}",
    "{{s|adjectif|conv",
    "{{s|adjectif|fr|",
    "{{s|adjectif|fr}",
    "{{s|adj|fr|",
    "{{s|adj|fr}",
    "{{s|adverbe interrogatif|fr}",
    "{{s|adverbe relatif|fr}",
    "{{s|adverbe|conv",
    "{{s|adverbe|fr|",
    "{{s|adverbe|fr}",
    "{{s|article|fr|",
    "{{s|article|fr}",
    "{{s|article défini|fr|",
    "{{s|article défini|fr}",
    "{{s|article indéfini|fr|",
    "{{s|article indéfini|fr}",
    "{{s|article partitif|fr|",
    "{{s|article partitif|fr}",
    "{{s|caractère}",
    "{{s|conjonction de coordination|fr}",
    "{{s|conjonction|fr|",
    "{{s|conjonction|fr}",
    "{{s|erreur|fr|",
    "{{s|erreur|fr}",
    "{{s|infixe|fr|",
    "{{s|infixe|fr}",
    "{{s|interfixe|fr}",
    "{{s|interjection|fr|",
    "{{s|interjection|fr}",
    "{{s|lettre|fr}",
    "{{s|locution-phrase|fr|",
    "{{s|locution-phrase|fr}",
    "{{s|nom commun|fr|",
    "{{s|nom commun|fr}",
    "{{s|nom de famille|fr|",
    "{{s|nom de famille|fr}",
    "{{s|nom propre|conv",
    "{{s|nom propre|fr|",
    "{{s|nom propre|fr}",
    "{{s|nom scientifique|",
    "{{s|nom|conv",
    "{{s|nom|fr|",
    "{{s|nom|fr}",
    "{{s|numéral|conv",
    "{{s|onomatopée|fr}",
    "{{s|particule|fr}",
    "{{s|postposition|fr}",
    "{{s|pronom démonstratif|fr|",
    "{{s|pronom démonstratif|fr}",
    "{{s|pronom indéfini|fr|",
    "{{s|pronom indéfini|fr}",
    "{{s|pronom interrogatif|fr|",
    "{{s|pronom interrogatif|fr}",
    "{{s|pronom personnel|fr|",
    "{{s|pronom personnel|fr}",
    "{{s|pronom possessif|fr|",
    "{{s|pronom possessif|fr}",
    "{{s|pronom relatif|fr|",
    "{{s|pronom relatif|fr}",
    "{{s|pronom|fr|",
    "{{s|pronom|fr}",
    "{{s|préfixe|conv",
    "{{s|préfixe|fr|",
    "{{s|préfixe|fr}",
    "{{s|prénom|fr|",
    "{{s|prénom|fr}",
    "{{s|préposition|fr|",
    "{{s|préposition|fr}",
    "{{s|pronom indéfini|fr}",
    "{{s|pronom indéfini|fr|",
    "{{s|substantif|fr}",
    "{{s|suffixe|conv",
    "{{s|suffixe|fr|",
    "{{s|suffixe|fr}",
    "{{s|symbole|conv",
    "{{s|symbole|fr|",
    "{{s|symbole|fr}",
    "{{s|variante typographique|conv",
    "{{s|variante typographique|fr|",
    "{{s|variante typographique|fr}",
    "{{s|verbe|fr|loc",
    "{{s|verbe|fr|num",
    "{{s|verbe|fr}",
    "{{s|verbe|fr|flexion",
)

# Variantes
variant_titles = (
    "{{s|adjectif|fr}",
    "{{s|adjectif|fr|flexion",
    "{{s|adjectif indéfini|fr|flexion",
    "{{s|nom|fr|flexion",
    "{{s|pronom indéfini|fr|flexion",
    "{{s|suffixe|fr|flexion",
    "{{s|verbe|fr|flexion",
)
variant_templates = (
    "{{flexion",
    "{{fr-accord-",
    "{{fr-rég",
    "{{fr-verbe-flexion",
)

# Certaines définitions ne sont pas intéressantes à garder (pluriel, genre, ...)
definitions_to_ignore = (
    *variant_templates,
    "eo-excl-étyl",
    "Gallica",
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
    "{exemple|",
)

# Modèle à ignorer : le texte sera supprimé.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les/Bandeaux
templates_ignored = (
    "*",
    ",",
    "?",
    "???",
    "ACC-animaux",
    "ACC-tiges célestes",
    "ACC-mains",
    "ACC-branches terrestres",
    "ACC-hommes",
    "ACC-coiffures",
    "ACC-vases",
    "ACC-paires",
    "ACC亠&囗",
    "Article",
    "article",
    "Accord des couleurs",
    "alphabet chinois",
    "ancre",
    "car-tracé",
    "casse",
    "casse/géorgien",
    "clé de tri",
    "composition",
    "couleurN",
    "créer-séparément",
    "désabrévier",
    "ébauche-déf",
    "ébauche-étym",
    "ébauche-exe",
    "étymologie-chinoise-SVG",
    "exemple",
    "fr-inv",
    "Gallica",
    "ja-mot",
    "ibid",
    "Import",
    "lettre",
    "lettre tifinaghe",
    "Lien 639-3",
    "lire en ligne",
    "Modèle",
    "mot-inv",
    "Ouvrage",
    "ouvrage",
    "périodique",
    "préciser",
    "R",
    "RÉF",
    "réf",
    "sens écriture",
    "source",
    "Source-wikt",
    "source-w",
    "trad",
    "trad-exe",
    "trier",
    "User",
    "vérifier",
    "voir",
    "voir-conj",
)

# Modèles qui seront remplacés par du texte italique.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les
templates_italic = {
    **contexts,
    **domain_templates,
    **regions,
    "adj-indéf-avec-de": "Avec de",
    "adverbe de lieu": "adverbe de lieu",
    "adverbe de manière": "adverbe de manière",
    "adverbe de quantité": "adverbe de quantité",
    "adverbe de temps": "adverbe de temps",
    "apposition": "En apposition",
    "argot de la Famille": "Argot de la Famille",
    "argot de l’université Paris-Cité": "Argot de l’université Paris-Cité",
    "argot internet": "Argot Internet",
    "argot Internet": "Argot Internet",
    "argot militaire": "Argot militaire",
    "argot poilu": "Argot poilu",
    "argot polytechnicien": "Argot polytechnicien",
    "attestation pays de Retz": "Pays de Retz",
    "au figuré": "Sens figuré",
    "avant 1835": "Archaïque, orthographe d’avant 1835",
    "Canton de La Mure": "Canton de La Mure",
    "dénombrable": "Dénombrable",
    "diaéthique": "Variations diaéthiques",
    "ex-rare": "Extrêmement rare",
    "extrêmement_rare": "Extrêmement rare",
    "énallages": "Énallage",
    "figuré": "Sens figuré",
    "génériquement": "Génériquement",
    "idiom": "Idiotisme",
    "idiomatique": "Sens figuré",
    "idiomatisme": "Idiotisme",
    "intransitif": "Intransitif",
    "langage SMS": "Langage SMS",
    "louchébem": "Louchébem",
    "marque": "Marque commerciale",
    "marque commerciale": "Marque commerciale",
    "marque déposée": "Marque commerciale",
    "militant": "Vocabulaire militant",
    "métaphore": "Sens figuré",
    "nom collectif": "Nom collectif",
    "noms de domaine": "Internet",
    "nom-déposé": "Marque commerciale",
    "Nouvelle-Angleterre": "Nouvelle-Angleterre",
    "ortho1990": "orthographe rectifiée de 1990",
    "Ortograf altêrnativ": "Ortograf altêrnativ",
    "par litote": "Par litote",
    "par troponymie": "Par troponymie",
    "parler bellifontain": "Parler bellifontain",
    "pâtes": "Cuisine",
    "pyrologie": "pyrologie",
    "réciproque2": "Réciproque",
    "réfléchi": "Réfléchi",
    "réflexif": "Réfléchi",
    "RSS-URSS": "Histoire, Communisme, URSS",
    "sens propre": "Sens propre",
    "spécifiquement": "Spécifiquement",
    "transitif": "Transitif",
    "transitif indir": "Transitif indirect",
    "tradit": "orthographe traditionnelle",
    "très familier": "Très familier",
    "très très rare": "Très très rare",
}
templates_italic["intrans"] = templates_italic["intransitif"]
templates_italic["m-cour"] = templates_italic["moins courant"]
templates_italic["un_os"] = templates_italic["un os"]
templates_italic["popu"] = templates_italic["populaire"]
templates_italic["prov"] = templates_italic["proverbial"]
templates_italic["RSSA-URSS"] = templates_italic["RSS-URSS"]
templates_italic["SMS"] = templates_italic["langage SMS"]
templates_italic["trans"] = templates_italic["transitif"]
templates_italic["vieux"] = templates_italic["vieilli"]

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
    # {{+|函}}
    "+": "parts[1]",
    # {{1|Descendant}}
    "1": "parts[1]",
    # {{1er}}
    # {{1er|mai}}
    "1er": "f\"1{superscript('er')}{'&nbsp;' + parts[1] if len(parts) > 1 else ''}\"",
    # {{1re}}
    # {{1re|fois}}
    "1re": "f\"1{superscript('re')}{'&nbsp;' + parts[1] if len(parts) > 1 else ''}\"",
    # {{2e|edition}}
    **{f"{idx}e": f"f\"{idx}<sup>e</sup>{{'&nbsp;' + parts[1] if len(parts) > 1 else ''}}\"" for idx in range(2, 13)},
    # {{Arabe|ن و ق}}
    "Arab": "parts[1] if len(parts) > 1 else 'arabe'",
    "Arabe": "parts[1] if len(parts) > 1 else 'arabe'",
    "Braille": "parts[1]",
    # {{caractère Unicode|266D}}
    "caractère Unicode": 'f"Unicode : U+{parts[1]}"',
    # {{chiffre romain|15}}
    "chiffre romain": "int_to_roman(int(parts[1]))",
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
    # {{forme pronominale|mutiner}}
    "forme pronominale": 'f"{capitalize(tpl)} de {parts[1]}"',
    # {{fr-accord-oux|d|d}}
    "fr-accord-oux": "parts[1] + 'oux'",
    # {{fr-accord-t-avant1835|abondan|a.bɔ̃.dɑ̃}}
    "fr-accord-t-avant1835": "parts[1]",
    # {{généralement singulier|fr}}
    "généralement singulier": "'Ce terme est généralement utilisé au singulier.'",
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
    "ISBN": "'ISBN ' + concat(parts[1:], ', ', last_sep=' et ')",
    # {{Lang-ar||[[نهر ابراهيم]]|100}}
    "Lang-ar": "parts[2]",
    # {{lexique|philosophie|fr}}
    # {{lexique|philosophie|sport|fr}}
    "lexique": "term(', '.join(capitalize(p) for p in [a for a in parts if '=' not in a][1:-1]))",
    # {{littéral|système de positionnement mondial}}
    "littéral": "f'Littéralement « {parts[1]} ».'",
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
    # {{numéros|111-112}}
    "numéros": 'f\'n{superscript("os")}{parts[1] if len(parts) > 1 else ""}\'',
    # {{o}}
    "o": "superscript('o')",
    # {{Pas clair|...}}
    "Pas clair": 'f\'{underline(parts[1]) if len(parts) > 1 else ""}{small("&nbsp;")}{superscript(italic(strong("Pas clair")))}\'',
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
    "R:Littré": "f'«&nbsp;{parts[-1]}&nbsp;», dans <i>Émile Littré, Dictionnaire de la langue française</i>, 1872–1877'",
    # {{R:Tosti|Turgeon}})
    "R:Tosti": "f'«&nbsp;{parts[-1]}&nbsp;» dans Jean {small_caps(\"Tosti\")}, <i>Les noms de famille</i>'",
    # {{RFC|5322}}
    "RFC": "sentence(parts)",
    # {{région}}
    # {{région|Lorraine et Dauphiné}}
    "régionalisme": "term(parts[1] if len(parts) > 1 and '=' not in parts[1] else 'Régionalisme')",
    # {{re}}
    "re": "superscript(parts[1] if len(parts) > 1 else 're')",
    # {{registre|traditionnellement}}
    "registre": "italic(f\"({capitalize(parts[1])})\") if len(parts) > 1 else ''",
    # {{ruby|泡盛|あわもり}}
    "ruby": "f'<ruby>{parts[1]}<rt>{parts[2]}</rt></ruby>'",
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
    "sport": "term(capitalize(concat(parts, ' ', indexes=[0, 2])))",
    # {{superlatif de|petit|fr}}
    "superlatif de": "sentence(parts)",
    # {{wd|Q30092597|Frederick H. Pough}}
    "wd": "parts[2] if len(parts) == 3 else ''",
    # {{wsp|Panthera pardus|''Panthera pardus''}}
    # {{wsp|Brassicaceae}}
    "wsp": "parts[2] if len(parts) > 2 else parts[1]",
    # {{WSP|Panthera leo}}
    "WSP": "italic(parts[1]) if len(parts) > 1 else ''",
    # 1,23{{x10|9}}
    "x10": "f'×10{superscript(parts[1])}' if len(parts) > 1 else '×10'",
    #
    # For variants
    #
    # {{flexion|foo}}
    "flexion": "parts[-1]",
}
templates_multi["n°"] = templates_multi["numéro"]
templates_multi["nº"] = templates_multi["numéro"]
templates_multi["NO"] = templates_multi["numéro"]
templates_multi["régio"] = templates_multi["régionalisme"]
templates_multi["région"] = templates_multi["régionalisme"]
templates_multi["régional"] = templates_multi["régionalisme"]

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
    "C°": 'C<sup style="font-size:83.33%;line-height:1;">o</sup>',
    "collectif": "<i>collectif</i>",
    "commun": "<i>commun</i>",
    "convention verbe grc": "<b>Note&nbsp;:</b> Les verbes en grec ancien, d’après l’usage admis dans tous les dictionnaires, sont donnés à la première personne du présent de l’indicatif.",
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
    "improprement": "<i>(Usage critiqué)</i>",
    "indéterminé": "indéterminé",
    "invar": "<i>invariable</i>",
    "invariable": "<i>invariable</i>",
    "invisible": "",
    "la-note-ij": "Le ‹&nbsp;j&nbsp;›, absent du latin classique, traduit le ‹&nbsp;i&nbsp;› devant une voyelle dans la tradition scholastique française. Cf. «&nbsp;j en latin&nbsp;».",
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
    "notes": "<b>Notes&nbsp;:</b>",
    "note-fr-féminin-homme": "<i>Ce mot féminin n’a pas de masculin correspondant, et il peut désigner des hommes.</i>",
    "note-fr-masculin-femme": "<i>Ce mot masculin n'a pas de féminin correspondant, et il peut désigner des femmes.</i>",
    "note-gentilé": "Ce mot est un gentilé. Un gentilé désigne les habitants d’un lieu, les personnes qui en sont originaires ou qui le représentent (par exemple, les membres d’une équipe sportive).",
    "note-majuscule-taxo": "En biologie, le genre, premier mot du nom binominal et les autres noms scientifiques (en latin) prennent toujours une majuscule. Par exemple : Homme moderne : <i>Homo sapiens</i>, famille : Hominidae. Quand ils utilisent des noms en français, ainsi que dans d’autres langues, les naturalistes mettent fréquemment une majuscule aux noms de taxons supérieurs à l’espèce (par exemple : <i>les Hominidés</i>, ou <i>les hominidés</i>).",
    "note-majuscule-taxon": "En biologie, le genre, premier mot du nom binominal et les autres noms scientifiques (en latin) prennent toujours une majuscule. Par exemple : Homme moderne : <i>Homo sapiens</i>, famille : Hominidae. Quand ils utilisent des noms en français, ainsi que dans d’autres langues, les naturalistes mettent fréquemment une majuscule aux noms de taxons supérieurs à l’espèce (par exemple : <i>les Hominidés</i>, ou <i>les hominidés</i>)",
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
    "sic": "<small>[sic]</small>",
    "singulare tantum": "<i>au singulier uniquement</i>",
    "sp": "<i>singulier et pluriel identiques</i>",
    "sp ?": "<i>singulier et pluriel identiques ou différenciés (l’usage hésite)</i>",
    "R:Larousse2vol1922": "<i>Larousse universel en 2 volumes</i>, 1922",
    "R:Rivarol": "Antoine de Rivarol, <i>Dictionnaire classique de la langue française</i>, 1827 ",
    "réfl": "<i>réfléchi</i>",
    "réciproque": "<i>réciproque</i>",
    "t": "<i>transitif</i>",
    "tr-dir": "<i>transitif direct</i>",
    "tr-indir": "<i>transitif indirect</i>",
    "uplet/étym": "Tiré de la fin du suffixe <i>-uple</i> qu’on retrouve dans quintuple, sextuple, qui exprime une multiplication, dérivé du latin <i>-plus</i>.",
    "usage": "<b>Note d’usage&nbsp;:</b>",
    "vlatypas-pivot": "v’là-t-i’ pas",
}


# Contenu de la release sur GitHub :
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr
release_description = """\
### 🌟 Afin d'être régulièrement mis à jour, ce projet a besoin de soutien ; [cliquez ici](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) pour faire un don. 🌟

<br/>


Nombre de mots : {words_count}
Export Wiktionnaire : {dump_date}

Version complète :
{download_links_full}

Version sans étymologies :
{download_links_noetym}

<sub>Mis à jour le {creation_date}</sub>
"""

# Le nom du dictionnaire qui sera affiché en-dessous de chaque définition
wiktionary = "Wiktionnaire (ɔ) {year}"


def find_genders(
    code: str,
    *,
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
    return unique(flatten(pattern.findall(code)))


def find_pronunciations(
    code: str,
    *,
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
    return [f"\\{p}\\" for p in unique(pattern.findall(line))]


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    missed_templates: list[tuple[str, str]] | None = None,
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

        >>> last_template_handler(["Citation bloc", "Exemple simple."], "fr")
        '<br/>«&nbsp;Exemple simple.&nbsp;»<br/>'

        >>> last_template_handler(["code langue", "créole guyanais"], "fr")
        'gcr'
        >>> last_template_handler(["code langue", "foo"], "fr")
        ''

        >>> last_template_handler(["diminutif", "fr"], "fr")
        '<i>(Diminutif)</i>'
        >>> last_template_handler(["diminutif", "fr", "m=1"], "fr")
        '<i>(Diminutif)</i>'
        >>> last_template_handler(["diminutif", "fr", "de=balle"], "fr")
        'Diminutif de <i>balle</i>'

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
        >>> last_template_handler(["fr-accord-comp-mf", "capital", "p1=capitaux", "risque", "ka.pi.tal", "pp1=ka.pi.to", "ʁisk"], "fr")
        'capital-risque'
        >>> last_template_handler(["fr-accord-cons", "ɑ̃.da.lu", "z", "s", "ms=andalou"], "fr")
        'andalou'
        >>> last_template_handler(["fr-accord-cons", "ɑ̃.da.lu", "z", "s"], "fr")
        ''
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

        >>> last_template_handler(["R:TLFi"], "fr", word="pedzouille")
        '«&nbsp;pedzouille&nbsp;», dans <i>TLFi, Le Trésor de la langue française informatisé</i>, 1971–1994'
        >>> last_template_handler(["R:TLFi", "pomme"], "fr", word="pedzouille")
        '«&nbsp;pomme&nbsp;», dans <i>TLFi, Le Trésor de la langue française informatisé</i>, 1971–1994'
        >>> last_template_handler(["R:DAF6", "pomme"], "fr", word="pedzouille")
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

        >>> last_template_handler(["nucléide", "106", "48", "Cd"], "fr")
        '<span style="white-space:nowrap;"><span style="display:inline-block;margin-bottom:-0.3em;vertical-align:-0.4em;line-height:1.2em;font-size:85%;text-align:right;">106<br>48</span>Cd</span>'

        >>> last_template_handler(["par analogie"], "fr")
        '<i>(Par analogie)</i>'
        >>> last_template_handler(["par analogie", "de=forme"], "fr")
        '<i>(Par analogie de forme)</i>'

        >>> last_template_handler(["rouge", "un texte"], "fr")
        '<span style="color:red">un texte</span>'
        >>> last_template_handler(["rouge", "texte=un texte"], "fr")
        '<span style="color:red">un texte</span>'
        >>> last_template_handler(["rouge", "fond=1", "1=un texte"], "fr")
        '<span style="background-color:red">un texte</span>'

        >>> last_template_handler(["wp"], "fr")
        'sur l’encyclopédie Wikipédia'
        >>> last_template_handler(["wp"], "fr", word="word")
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

    """
    from ...user_functions import (
        capitalize,
        chinese,
        extract_keywords_from,
        italic,
        lookup_italic,
        person,
        term,
    )
    from .. import defaults
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
        code_lang = parts[0]
        return next((code for code, l10n in langs.items() if l10n == code_lang), "")

    if tpl == "diminutif":
        # sic see : https://fr.wiktionary.org/w/index.php?title=Mod%C3%A8le:diminutif&oldid=36661983
        phrase = "Diminutif" if data["m"] in ("1", "oui") else "Diminutif"
        if data["de"]:
            phrase += f" de {italic(data['de'])}"
        else:
            phrase = term(phrase)
        return phrase

    if tpl in ("ellipse", "par ellipse"):
        return f"{italic('(Ellipse de')} {data['de']}{italic(')')}" if data["de"] else term("Par ellipse")

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
        if tpl.startswith("fr-accord-cons"):
            singular = data["ms"] or ""
        elif tpl.startswith("fr-accord-comp"):
            singular = "-".join(parts[: len(parts) // 2])
        elif not (singular := data["s"] or data["m"] or data["ms"]):
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
        return f'<span style="line-height: 0px;"><span style="font-size:larger">{arabiser(parts[0])}</span></span> <small>({parts[0]})</small>'

    if tpl == "ar-racine/nom":
        from .racines_arabes import racines_schemes_arabes

        return f"{arabiser(parts[0].split('-')[1])}: {racines_schemes_arabes[parts[0]]['aa_sens']}"

    if tpl == "ar-sch":
        return arabiser(appliquer(parts[0], parts[1] if len(parts) > 1 else "ar-zrzr"))

    if tpl == "ar-terme":
        arab = arabiser(parts[0])
        return f"{arab} ({italic(parts[0])}) /{toIPA(arabic=arab)}/"

    if tpl == "nucléide":
        return (
            '<span style="white-space:nowrap;"><span style="display:inline-block;margin-bottom:-0.3em;'
            'vertical-align:-0.4em;line-height:1.2em;font-size:85%;text-align:right;">'
            f"{parts[0]}<br>{parts[1]}</span>{parts[2]}</span>"
        )

    if tpl == "par analogie":
        text = "Par analogie"
        if de := data["de"]:
            text += f" de {de}"
        return term(text)

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
    if lang := langs.get(tpl):
        return lang

    if context := lookup_italic(tpl, locale, empty_default=True):
        return term(context)

    return defaults.last_template_handler(template, locale, word=word, missed_templates=missed_templates)
