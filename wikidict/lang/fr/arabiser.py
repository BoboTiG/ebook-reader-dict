"""
Arabiser: manual conversion of Module:arabe from
https://fr.wiktionary.org/wiki/Module:arabe

Current version: 12 juillet 2025 07:43
    https://fr.wiktionary.org/w/index.php?title=Module:arabe&oldid=38396854

"""

import unicodedata
from re import sub

# Translittérations de API / romain / . vers arabe

en_arabe = {
    "0": "٠",
    "1": "١",
    "2": "٢",
    "M": "٣",  # 3 est pris par le 3ain... avec imagination on bascule le 3 pour faire un m
    "4": "٤",
    "5": "٥",
    "6": "٦",
    "7": "٧",
    "8": "٨",
    "9": "٩",
    " ": " ",  # blancs entre mots
    "(": "(",  # parenthèse
    ")": ")",  # parenthèse
    "_": "",  # underscore ignoré pour décontextualisation éventuelle
    "؛": "؛",  # point virgule arabe
    "،": "،",  # virgule inversée
    ",": "،",
    ";": "؛",
    "؞": "؞",  # trois points
    "؟": "؟",  # point d'interrogation
    "?": "؟",
    "!": "!",  # exclamation
    "ء": "ء",  # Hamza
    "ò": "ٔ",  # Hamza suscrite
    "`": "ء",
    "'": "ء",
    "‘": "ء",
    "ʾ": "ء",
    "ʼ": "ء",
    "ˈ": "ء",
    "ٱ": "ٱ",  # Alif wasla
    "^": "ٱ",
    "آ": "آ",  # Alif madda
    "~": "آ",
    "أ": "أ",  # Alif hamza
    "à": "أ",
    "ؤ": "ؤ",  # Waw hamza
    "ù": "ؤ",
    "إ": "إ",  # Alif hamza souscrite
    "è": "إ",
    "ئ": "ئ",  # Ya hamza
    "ì": "ئ",
    "ا": "ا",  # Alif
    "A": "ا",
    "â": "◌َا",  # diacritique intégré
    "ā": "◌َا",  # diacritique intégré
    "e": "ا",  # permet d'écrire "el-"
    "ب": "ب",  # Ba
    "b": "ب",
    "ة": "ة",  # Ta marbouta
    "@": "ة",
    "ت": "ت",  # Té
    "t": "ت",
    "ث": "ث",  # Thé
    "θ": "ث",
    "ṯ": "ث",
    "F": "ث",
    "ج": "ج",  # Djim
    "ʒ": "ج",
    "ǧ": "ج",
    "j": "ج",
    # "g": "ج",
    "ح": "ح",  # Ha
    "ḥ": "ح",
    "ħ": "ح",
    "ḩ": "ح",
    "H": "ح",
    "خ": "خ",  # Kha
    "ḵ": "خ",
    "ẖ": "خ",
    "ḫ": "خ",
    "x": "خ",
    "X": "خ",
    "K": "خ",
    "د": "د",  # Dal
    "d": "د",
    "ذ": "ذ",  # Dhal
    "ð": "ذ",
    "ḏ": "ذ",
    "V": "ذ",
    "ر": "ر",  # Ra
    "r": "ر",
    "ز": "ز",  # Zain
    "z": "ز",
    "س": "س",  # Sîn
    "s": "س",
    "ش": "ش",  # Chîn
    "ʃ": "ش",
    "š": "ش",
    "c": "ش",
    "C": "ش",
    "ص": "ص",  # Çad
    "ṣ": "ص",
    "ş": "ص",
    "S": "ص",
    "ç": "ص",
    "Ç": "ص",
    "ض": "ض",  # Dad
    "ḍ": "ض",
    "ḑ": "ض",
    "D": "ض",
    "ط": "ط",  # Ta
    "ṭ": "ط",
    "ţ": "ط",
    "T": "ط",
    "ظ": "ظ",  # Zza
    "ẓ": "ظ",
    "Z": "ظ",
    "ع": "ع",  # Rain
    "ʕ": "ع",
    "ʿ": "ع",
    "ʻ": "ع",
    "3": "ع",
    "غ": "غ",  # Ghain
    "ɣ": "غ",
    "ḡ": "غ",
    "ğ": "غ",
    "ġ": "غ",
    "g": "غ",
    "R": "غ",
    "ـ": "ـ",  # tiret
    "-": "ـ",
    "ف": "ف",  # Fa
    "f": "ف",
    "ق": "ق",  # Qaf
    "q": "ق",
    "ك": "ك",  # Kaf
    "k": "ك",
    "ل": "ل",  # Lam
    "l": "ل",
    "م": "م",  # Mîm
    "m": "م",
    "ن": "ن",  # Noun
    "n": "ن",
    "ه": "ه",  # Hé
    "h": "ه",
    "و": "و",  # Waw
    "U": "و",
    "w": "و",
    "W": "و",
    "û": "◌ُو",  # préfixage du diacritique
    "ū": "◌ُو",  # préfixage du diacritique
    "ى": "ى",  # Alif maksoura
    "é": "ى",
    # "É": "ى",
    "ي": "ي",  # Waw
    "I": "ي",
    "y": "ي",
    "Y": "ي",
    "î": "◌ِي",
    "ī": "◌ِي",
    "◌ً": "◌ً",  # Fathatan
    "ã": "◌ً",
    "◌ٌ": "◌ٌ",  # Dammatan
    "ũ": "◌ٌ",
    "õ": "◌ٌ",
    "◌ٍ": "◌ٍ",  # Kasratan
    "ĩ": "◌ٍ",
    "ñ": "◌ٍ",
    "◌َ": "◌َ",  # Fatha
    "a": "◌َ",
    "◌ُ": "◌ُ",  # Damma
    "u": "◌ُ",
    "◌ِ": "◌ِ",  # Damma
    "i": "◌ِ",
    "◌ّ": "◌ّ",  # Chadda
    "²": "◌ّ",
    "◌ْ": "◌ْ",  # Soukoun
    "°": "◌ْ",
    "٭": "٭",  # *
    "*": "٭",
    "◌ٰ": "◌ٰ",  # Alif suscrit
    "E": "◌ٰ",
    # Lettres additionnelles diverses
    "p": "پ",  # pa
    "v": "ڤ",  # ve
    "B": "ڥ",  # ve algérien
    "J": "چ",  # tch perse
    "£": "'ٓ",  # madda arabe en chef
}


def arabiser(texte: str) -> str:
    """
    >>> arabiser("rajulâã")
    'رَجُلَاًا'

    >>> arabiser("mu'ad²ibũ")
    'مُؤَدِّبٌ'
    >>> arabiser("ad²aba")
    'أَدَّبَ'
    >>> arabiser("elHasan_")
    'الحَسَن'
    >>> arabiser("zabala")
    'زَبَلَ'
    >>> arabiser("izballa")
    'إِزْبَلَّ'
    >>> arabiser("d")
    'د'
    >>> arabiser("qanTara")
    'قَنْطَرَ'

    >>> arabiser("qur'ân")
    'قُرْآنْ'
    >>> arabiser("a'mana")
    'آمَنَ'
    >>> arabiser("aelVakarayni")
    'أَالْذَكَرَيْنِ'
    >>> arabiser("hay'@")
    'هَيْءَة'
    >>> arabiser("cifâ'ã")
    'شِفَاءًا'

    >>> arabiser("ra''asa")
    'رَأَّسَ'
    >>> arabiser("ru''isa")
    'رُئِّسَ'

    >>> arabiser("katabâ")
    'كَتَبَا'
    >>> arabiser("maktûb")
    'مَكْتُوبْ'
    >>> arabiser("kattaba")
    'كَتَّبَ'
    >>> arabiser("katabû")
    'كَتَبُو'
    >>> arabiser("katabûA")
    'كَتَبُوا'
    >>> arabiser("elkalb")
    'الكَلْبْ'
    >>> arabiser("elrum")
    'الرُّمْ'
    >>> arabiser("ellamad")
    'اللَّمَدْ'
    >>> arabiser("elamad")
    'الأَمَدْ'
    >>> arabiser("Xalîfâ@")
    'خَلِيفَاة'
    >>> arabiser("kitabũ")
    'كِتَبٌ'
    >>> arabiser("kitabã")
    'كِتَبًا'
    >>> arabiser("kitabĩ")
    'كِتَبٍ'
    >>> arabiser("zawé")
    'زَوَى'

    >>> arabiser("'ir")
    'إِرْ'
    >>> arabiser("arbi")
    'أَرْبِ'
    >>> arabiser("'arbi")
    'أَرْبِ'

    >>> arabiser("cuìûn")
    'شُئُونْ'
    >>> arabiser("cu'ûn")
    'شُؤُونْ'

    >>> arabiser("k_t_b_")
    'كتب'
    >>> arabiser("ktb")
    'كتب'

    >>> arabiser("elmubdi'u wa elmu3îdu")
    'المُبْدِئُ وَ المُعِيدُ'

    >>> arabiser("famu ^lHûti")
    'فَمُ ٱلحُوتِ'
    """
    # translittération en arabe du paramètre, suivant l'assoc-liste en_arabe.
    texte = f" {texte} "

    # on rajoute un blanc devant et derrière pour uniformiser les tests de début et fin de mot
    transcription = ""
    a_traiter = ""

    # à faire un jour : transformer tous les ² en redoublements explicites avant traitement
    # à faire un jour : reporter sur la lettre attendue toutes les lettres équivalentes admissibles
    diacritiques = any(char in texte for char in "aiuâîûãĩũ°")
    for curseur in range(1, len(texte) - 1):
        a_traiter = texte[curseur]
        # orthographe différente suivant qu'on est en "début" ou en milieu de mot.
        # début de mot
        if (
            # précédé d'un blanc = début de mot
            texte[curseur - 1] == " "
            # blanc souligné précédé d'un blanc = début de mot
            or texte[curseur - 1 : curseur] == " _"
            # derrière el- il faut écrire comme en début de mot malgré la liaison :
            # idem derrière particules inséparables
            or (
                curseur > 1
                # pb spécifique de bi'r
                and texte[curseur - 3 : curseur + 1] != "bi'r"
                # On regarde ce qu'il y avait trois caractères avant
                and texte[curseur - 2 : curseur] == "el"  # normalement le "e" n'apparaît que pour le "el" préfixe
                and texte[curseur - 3 : curseur] in {" ^l", " bi", " fa", " ka", " la", " li", " sa", " wa"}
            )
            # idem si plusieurs particules séparées par un blanc souligné
            or (
                curseur > 1
                and texte[curseur - 3 : curseur] in {"_el", "_^l", "_bi", "_fa", "_ka", "_la", "_li", "_sa", "_wa"}
            )
            # -- un blanc souligné permet de couper le mot s'il faut forcer un fa'tu en fa_'tu par exemple
            or (
                curseur > 1
                and texte[curseur - 3 : curseur] in {"el_", "^l_", "bi_", "fa_", "ka_", "la_", "li_", "sa_", "wa_"}
            )
        ):
            # le curseur est en début de mot, indépendamment du préfixe
            # Si le début du mot est une voyelle il faut insérer en amont une hamza préfixe
            # Mais il faut intercepter en amont les cas du alif madda,
            # Mais c'est plus facile à traiter si on traite d'abord normalement les cas de type a & hamza & voyelle :
            # Pour ça, on regarde les trois premiers caractères à partir du courant :
            debut = texte[curseur : curseur + 3]
            if debut in {"a'i", "a'î", "a'u", "a'û", "a'a", "a'â"}:
                # il y aura superposition d'une hamza instable et d'une hamza structurelle portant voyelle
                transcription += "أ◌َ"  # alif hamza + fatha
                # ... et la hamza suivante sera traitée par le cas général.

            # Traitement à présent des cas où il faut un alif madda
            # débuts de la forme a & hamza (donc sans voyelle, puisque interceptées précédemment), ou hamza & â, ou â :
            elif texte[curseur : curseur + 2] in {"a'", "'â"} or a_traiter == "â":
                transcription += "آ"  # alif madda

            # Traitement de la hamza explicite en début de mot
            elif a_traiter == "'":  # hamza explicite en début de mot
                suivant = texte[curseur + 1]
                if suivant == "â":
                    transcription += "آ"  # alif madda
                elif suivant in "auû":
                    transcription += "أ"  # support en haut
                elif suivant in "iî":
                    transcription += "إ"  # support en bas
                elif suivant == " ":
                    transcription += "ءا"  # hamza isolée
                else:
                    transcription += "ا"  # par défaut, alif
                # hamza explicite en début de mot, la hamza préfixe a été insérée, la voyelle suivante sera transcrite ensuite

            # Il faut rajouter la lettre courante à la transcription.
            else:
                # Mais d'abord si c'est une voyelle, on met une hamza préfixe
                if a_traiter in "auû":
                    # le â est un cas à part traité précédemment
                    transcription += "أ"  # support en haut
                elif a_traiter in "iî":
                    transcription += "إ"  # support en bas
                # la hamza préfixe a été insérée, le reste suit.

                # Ensuite si on est sur le "e" d'une structure de type "liel" en début de mot,
                # elle s'écrit sans alif donc il faut sauter le "e" et passer à la lettre suivante :
                if texte[curseur - 3 : curseur + 1] != "liel":
                    transcription += en_arabe[a_traiter]

            # end cas hamza préfixe à insérer.

            # post-traitement : si la consonne est derrière el (ou ^l) il faut rajouter un chadda aux lettres solaires
            # il faut que le "el" soit collé au mot, donc une forme comme el_sadatu supprime le chadda. Faut pas pousser.
            if (
                texte[curseur - 1] == "l"
                and texte[curseur - 2] in {"e", "^"}
                # faire le test solaire
                and (a_traiter in "tFdVrzsCSDTZln" and diacritiques)
            ):
                transcription += en_arabe["²"]

        # on n'est pas en début de mot
        else:
            # Ne présentent jamais de redoublement :
            if a_traiter in "aiue^îAIUEÉĩũõ_":
                transcription += en_arabe[a_traiter]

            elif a_traiter == "é":
                if texte[curseur - 1] not in "ã_E~" and diacritiques:
                    transcription += en_arabe["a"]
                transcription += en_arabe[a_traiter]

            # cas particulier d'un u final : alif muet
            elif a_traiter == "û":
                # plus simple de ne pas le mettre.
                transcription += en_arabe[a_traiter]
                # if (mw.ustring.sub( texte, curseur+1, curseur+1 ) == " ")
                # then transcription = transcription .. en_arabe["e"] end

            # ne pas rajouter un "a" s'il y en a déjà un avant.
            elif a_traiter == "~":
                if diacritiques and texte[curseur - 1] != "a":
                    transcription += en_arabe["a"]
                transcription = en_arabe["~"]

            # Traitement des différents cas particuliers dépendants du contexte
            elif a_traiter == "ã":
                # le ã est suivi d'un alif muet, mais pas derrière ât et @ :
                transcription += en_arabe[a_traiter]
                if (
                    texte[curseur - 1] == "@"
                    or texte[curseur - 2 : curseur] == "ât"
                    or texte[curseur + 1]
                    in {
                        "é",
                        # ni devant une hamza précédé d'une voyelle longue
                        "â'",
                        "î'",
                        "û'",
                        # et si on veut le neutraliser on met un blanc souligné
                        "_",
                    }
                ):  # skip
                    pass
                else:
                    transcription += en_arabe["A"]

            elif a_traiter == "â":
                if (
                    # pas de nouvel alif derrière une hammza portée par alif
                    texte[curseur - 1] == "'"
                    # mais si un petit malin a codé deux hamza de suite...
                    and texte[curseur - 2] != "'"
                ):
                    avant = texte[curseur - 2]
                    if avant == "'":
                        avant = texte[curseur - 3]
                    if avant in "iîIyuûwâ":
                        transcription += en_arabe["â"]
                    # sinon : la hamza a déjà inséré un alif madda et on ne fait rien
                else:
                    transcription += en_arabe["â"]

            elif a_traiter == "@":
                # ta arbouta : précédé de 'a' implicite, sauf quand derrière une voyelle longue
                if texte[curseur - 1] not in "âîû_" and diacritiques:
                    transcription += en_arabe["a"]
                transcription += en_arabe["@"]

            elif a_traiter == "é":
                # alif maksoura : précédé de 'a' implicite, sauf quand devant un 'ã' ou quand on efface les voyelles
                if texte[curseur + 1] != "ã" and texte[curseur - 1] != "_":
                    transcription += en_arabe["a"]
                transcription += en_arabe["é"]

            # Quelques cas où on ne veut pas examiner la présence d'un ²
            elif a_traiter == "°":  # Sukun explicite
                transcription += en_arabe["°"]

            elif a_traiter in "*.":
                transcription += en_arabe["*"]

            # Lettre redoublée de la précédente :
            elif a_traiter == texte[curseur - 1] and a_traiter != "-" and diacritiques:
                # pas de gemmination sur les tirets
                # Pas de gemmination si on est derrière un el- préfixe (el-lah)
                # mais dans ce cas le second l est traité comme début de mot : pas cette branche.
                transcription += en_arabe["²"]

            elif a_traiter == "'":  # hamza
                # Hamza : problème du support
                avant = texte[curseur - 1]
                apres = texte[curseur + 1]

                # insertion d'un sukun si nécessaire
                if (
                    avant not in "aeiuâîûéãĩñÉAIUEñõ-~,_°^()! ,012M456789"
                    and texte[curseur - 3 : curseur]
                    not in {
                        # pas de sukun après el- en début de mot
                        " el",
                        " ^l",
                        "_el",
                        "_^l",  # cas du alif wasla
                    }
                    and diacritiques
                ):
                    transcription += en_arabe["°"]

                # Traitement différent suivant qu'on est en fin de mot ou en milieu :
                if (
                    curseur > len(texte) - 3
                    or apres == " "
                    or (
                        texte[curseur + 2] == " "
                        and apres
                        not in {
                            # il ne faut pas de lettre de prolongation non plus
                            "â",
                            "î",
                            "û",
                            "é",
                            "A",
                            "I",
                            "U",
                            "E",
                            # et piège, après un a̋ le alif orthographique compte comme lettre, donc ce n'est pas une fin de mot...
                            "ã",
                        }
                    )
                ):
                    # hamza en fin de mot
                    if avant == "i":
                        transcription += en_arabe["ì"]
                    elif avant == "u":
                        transcription += en_arabe["ù"]
                    elif avant == "a":
                        transcription += en_arabe["à"]
                    else:
                        transcription += en_arabe["'"]
                    # fin de mot

                # hamza en milieu de mot
                else:
                    double = False
                    if apres in "'²":
                        double = True
                        apres = texte[curseur + 2]

                    # derrière un i, support ya sans point
                    if avant in "iîIy":
                        transcription += en_arabe["ì"]

                    # derrière un waw, hamza en ligne
                    elif avant in "ûw":
                        transcription += en_arabe["'"]

                    # derrière un u faut voir après
                    elif avant == "u":
                        if apres in "iî":
                            transcription += en_arabe["ì"]
                        else:
                            transcription += en_arabe["ù"]

                    # derrière un a faut voir après
                    elif avant == "a":
                        if apres in {"i", "î"}:
                            transcription += en_arabe["ì"]
                        elif apres in {"û", "u"}:
                            transcription += en_arabe["ù"]
                        elif apres == "â":
                            # cas particulier : si la hamza est double il faut la mettre en ligne
                            if double:
                                transcription += en_arabe["`"]  # en ligne
                            else:
                                transcription += en_arabe["~"]  # madda, et â sera omis
                        # dans les autres cas, support alif, sauf le cas a' initial déjà traité avec le a initial
                        elif texte[curseur - 2] != " ":
                            transcription += en_arabe["à"]

                    # derrière un â, on risque de trouver une hamza en ligne pour ā’a, ū’a & aw’a
                    elif avant == "â":
                        # il y a nécessairement une consonne après
                        if apres in {"i", "î"}:
                            transcription += en_arabe["ì"]
                        elif apres == "u":
                            transcription += en_arabe["ù"]
                        else:
                            transcription += en_arabe["'"]  # en ligne
                    else:  # pas de voyelle avant, donc sukun
                        if apres in {"i", "î"}:
                            transcription += en_arabe["ì"]
                        elif apres in {"û", "u"}:
                            transcription += en_arabe["ù"]
                        elif apres == "â":
                            transcription += en_arabe["~"]
                        else:
                            transcription += en_arabe["à"]
                    # traitement milieu de mot
                # fin ou pas
            # fin du cas de la hamza
            # Ici il faut isoler le traitement des caractères sur lesquels il n'y aura jamais de sukkun
            elif a_traiter == ",":
                transcription += en_arabe[","]
            elif a_traiter == "-":
                transcription += en_arabe["-"]
            elif a_traiter == "²":
                transcription += en_arabe["²"]
            elif a_traiter == "^":
                transcription += en_arabe["^"]
            elif a_traiter == "?":
                transcription += en_arabe["?"]
            elif a_traiter == "!":
                transcription += en_arabe["!"]
            else:  # dans les autres cas, translittération de la consonne, mais avec sukun éventuel
                avant = texte[curseur - 1]
                # on ne met pas de sukun après...
                if (
                    avant not in "aeiuâîûéãĩñÉAIUEñõ-~_°^?012M456789(), "
                    and a_traiter != " "
                    and texte[curseur - 3 : curseur]
                    not in {
                        # pas de sukun après el- en début de mot
                        " el",
                        " ^l",
                        "_el",
                        "_^l",  # pas de sukun sur un alif wasla
                        " a'",  # pas de sukun sur un alif madda
                    }
                    and diacritiques
                ):
                    transcription += en_arabe["°"]

                if en_arabe.get(a_traiter):
                    transcription += en_arabe[a_traiter]
                # cas d'une consonne en fin de mot - rajouter un sukun final
                if texte[curseur + 1] == " " and diacritiques and avant not in "012M3456789":
                    transcription += en_arabe["°"]

    transcription = "".join([c for c in transcription if unicodedata.name(c) != "DOTTED CIRCLE"])

    # for - boucle de traitement
    return unicodedata.normalize("NFC", transcription)


def est_voyelle(char: str) -> bool:
    """La voyelle peut être tout ce qui permet à une consonne d'être une initiale de syllabe : courte ou longue, tanwîn, ou ta marbuta."""
    return char in "aeiuâîûãĩũ@ñõ"


def est_voyelle_courte(scheme: str, position: int) -> bool:
    """Détecte la presence d'une voyelle courte à cette position comme ci-dessus mais sans les voyelles longues."""
    return (len(scheme) > position) and (scheme[position] in "aeiuãĩũ@ñõ")


def nature(scheme: str, position: int) -> str:
    """
    Renvoit la nature de la lettre du schème=scheme située à la position=position (retranscrit par `char` ici).
    Ce peut être :
            (voyelles)
    "vo" = voyelle courte dans une syllable ouverte ;
    "vf" = voyelle courte dans une syllable fermée ;
    "vl" = voyelle longue (dans une syllable longue) ;
            (consonnes initiales)
    "io" = consonne initiale d'une syllable ouverte ;
    "if" = consonne initiale d'une syllable fermée ;
    "il" = consonne initiale d'une syllable longue ;
            (consonnes doubles)
    "do" = consonne double, fermant une syllable et debutant une syllable ouverte ;
    "df" = consonne double debutant une syllable fermée ;
    "dl" = consonne double, debutant une syllable longue ;
            (consonnes de fermeture)
    "fo" = fin de syllable fermée suivie d'une autre consonne ;
    "ff" = fin de syllable fermée et fin de mot (imperatif).
    """
    char = scheme[position]

    if est_voyelle(char):
        if char in "âîû":
            # voyelle longue
            return "vl"
        if char in "ãĩũ@ñõ":
            # par convention ; une consonne précédente sera toujours "ouverte"
            return "vo"
        if not scheme[position + 1]:
            # voyelle courte finale donc ouverte
            return "vo"
        if not scheme[position + 2]:
            # voyelle courte + consonne finale donc fermée
            return "vf"
        if est_voyelle(scheme[position + 2]):
            # voyelle courte + consonne + voyelle donc ouverte
            return "vo"
        return "vf"

    # cas consonne
    if not scheme[position + 1]:
        # la consonne est la dernière lettre, donc finale fermée
        return "ff"
    if scheme[position + 1] in {"²", char}:
        # consonne double, voir la nature de la voyelle nécessairement présente à pos+2
        return f"d{nature(scheme, position + 2)[1]}"
    if scheme[position - 1] == char:
        # 2ème de double, voir la nature de la voyelle nécessairement présente à pos+1
        return f"d{nature(scheme, position + 1)[1]}"
    if not est_voyelle(scheme[position - 1]):
        # 2ème de deux consonnes, idem
        return f"i{nature(scheme, position + 1)[1]}"
    if not est_voyelle(scheme[position + 1]):
        # precede de voyelle et suivie de consonne
        return "fo"

    return f"i{nature(scheme, position + 1)[1]}"


def pagename_interne(name: str) -> str:
    """
    Nettoie un nom de page en remplaçant les &#...; par les vrais caractères parce que le wikicode substitue à présent l'apostrophe simple (symbolisant la hamza) à son code &#39; ce qui a des conséquences erratiques en aval...
    """
    return (
        name.replace("&#39;", "'")  # apostrophe double, apostrophe simple, apostrophe double...
        .replace("&#42;", "*")
        .replace("&#226;", "â")
        .replace("&#238;", "î")
        .replace("&#251;", "û")
        .replace("&#227;", "ã")
        .replace("&#297;", "ĩ")
        .replace("&#361;", "ũ")
    )


def appliquer(scheme: str, racine: str, *, var: str = "") -> str:
    """
    >>> appliquer("ar-ma**û*ũ", "ar-ktb")
    'maktûbũ'
    >>> appliquer("ar-*a*a*a-a", "ar-'by")
    "'abé"
    """
    # passe de nettoyage parce que le wikicode substitue à présent l'apostrophe simple (symbolisant la hamza) à son code &#39; ce qui a des conséquences erratiques en aval...
    scheme = pagename_interne(scheme)
    # idem pour la racine
    racine = pagename_interne(racine)

    if not var:  # ne dit rien
        # from .racines_arabes import racines_arabes
        if scheme == "ar-*i*â*ũ":
            var = "(3)"
        # TODO GET VERBAL FORM for all schemes, here it works for the word "Ryad"

    scheme = scheme[3:]
    racine = racine[3:]

    # Dans les modèles de la forme ar-*a*a*a-i, les deux dernières lettres indiquent conventionnellement la voyelle
    # de l'inaccompli et doivent être supprimées dans un affichage normal
    if scheme[-2] == "-":  # avant-dernière lettre = "-" ?
        scheme = scheme[:-2]  # supprimer les deux dernières, donc limiter au rang -3.

    # voyelle préfixe mobile éventuelle
    mobile = "u" if scheme[2] in {"u", "û"} else "i"

    # Dans le schème, les lettres radicales sont symbolisées par des *, sauf si elles sont répétées, auquel cas elles
    # sont symbolisées par leur numéro d'ordre.
    # remplacement des étoiles successives par le rang d'ordre des lettres radicales (pour homogénéiser le traitement
    # des verbes irréguliers) si le n° correspondant est absent :
    if "1" not in scheme:
        scheme = scheme.replace("*", "1", 1)
    if "2" not in scheme:
        scheme = scheme.replace("*", "2", 1)
    if "3" not in scheme:
        scheme = scheme.replace("*", "3", 1)
    if "4" not in scheme:
        scheme = scheme.replace("*", "4", 1)
    # sauf pour 3, parce que sinon, on a des problèmes si "3" est présent comme lettre radicale...
    # donc on remet un caractère jocker.
    scheme = scheme.replace("3", "µ")

    # NB : on présume que les chiffres sont dans l'ordre avec ce système, un "schème" de type ar-3a2a1a réalise en
    # fait une inversion des lettres - pas malin, mais bon.
    # De même, on peut forcer une lettre faible à une autre valeur par exemple ar-mi**â*ũ peut être forcé sur
    # ar-mi*yâ3ũ quand le W doit se transformer en Y.
    # Les radicales faibles sont w et y. Pour "régulariser" sinon, mettre la radicale faible en majuscule.
    shemeinit = scheme  # sauvegarde de la valeur primitive

    # verbes hamzés en 2 et défectifs : dans les formes 1 et 4 la hamza saute sur les formes de type **a* ou **i* mais pas la forme 10 en sta**a* ou sti**a* ou sta**i*
    # si la hamza ne saute pas, employer ` (hamza invariable) à la place de ' (hamza variable).
    if racine[1:3] == "'y":
        if "12aµ" in scheme and "st" not in scheme:
            scheme = scheme.replace("12aµ", "1aµ")
        if "12iµ" in scheme and "st" not in scheme:
            scheme = scheme.replace("12iµ", "1iµ")
        if "12uµ" in scheme and "st" not in scheme:
            scheme = scheme.replace("12uµ", "1uµ")

    # deuxième radicale = creuse ?
    if var in {"(2)", "(3)", "(5)", "(6)", "(9)"} and racine[1] in {"w", "y"}:
        # ces formes sont régulières, cf Schier p.64. cf Ryding p. 580.
        racine = racine[0] + racine[1].upper() + racine[2]
    if racine[1:3] in {"wy", "wY", "yy", "yY"}:
        # ces formes sont régulières.
        racine = racine[0] + racine[1].upper() + racine[2]

    # Sinon, traitement des formes creuses après neutralisation des formes verbales invariables :
    if racine[1] in {"w", "y"} and scheme != "a12aµu":  # invariant, cf Ryding p. 246.
        # verbe creux en W, cf Schier p. 71

        position = scheme.find("2")

        # La 2ème radicale a pu être forcée à autre chose.
        if position > -1:
            # contexte de la radicale : quelles sont les voyelles (courtes ou longues) avant et après la consonne 2 :
            contexte = f"{scheme[position - 1]}2" if est_voyelle(scheme[position - 1]) else "°2"
            if scheme[position + 1] in {"²", scheme[position]}:
                contexte += "²"
                contexte += scheme[position + 2] if est_voyelle(scheme[position + 2]) else "°"
            elif est_voyelle(scheme[position + 1]):
                contexte += scheme[position + 1]
            else:
                contexte += "°"

            if contexte == "a2a" and position == 2:
                # la lettre en position +2 est-elle une finale de syllable ?
                if nature(scheme, position + 2)[0] in {"f", "d"}:
                    if racine[1] == "w":
                        scheme = f"{scheme[: position - 1]}u{scheme[position + 2 :]}"
                    else:
                        scheme = f"{scheme[: position - 1]}i{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[: position - 1]}â{scheme[position + 2 :]}"

            elif contexte == "a2a" and position != 2:
                # la lettre en position +2 est-elle une finale de syllable ?
                if nature(scheme, position + 2)[0] == "f":
                    scheme = f"{scheme[: position - 1]}a{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[: position - 1]}â{scheme[position + 2 :]}"

            # a2i remplacé par â ou i
            elif contexte == "a2i":
                # la lettre en position +2 est-elle une finale de syllable ?
                if nature(scheme, position + 2)[0] in {"f", "d"}:
                    scheme = f"{scheme[: position - 1]}i{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[: position - 1]}â{scheme[position + 2 :]}"

            # a2u remplacé par â ou u
            elif contexte == "a2u":
                # la lettre en position +2 est-elle une finale de syllable ?
                if nature(scheme, position + 2)[0] in {"f", "d"}:
                    scheme = f"{scheme[: position - 1]}u{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[: position - 1]}â{scheme[position + 2 :]}"

            # a2î remplacé par âyi dans ar-*a*î*ũ -- erreur d'interprétation, c'est en fait un ar-*â*i*ũ où la hamza est mal écrite
            # elif contexte == "a2î":
            #     scheme = f"{scheme[: position - 1]}âyi{scheme[position + 2 :]}"

            # a2²i remplacé par ay²i mais pas dans ar-mu*a2²i*ũ (forme 2 invariable)
            elif contexte == "a2²i" and scheme != "mu1a2²iµũ":
                scheme = f"{scheme[: position - 1]}ay²i{scheme[position + 2 :]}"

            # âwi : remplacé par â'i sauf formes verbales 2, 3, 5 et 6
            elif contexte == "â2i":
                scheme = f"{scheme[: position - 1]}â'i{scheme[position + 2 :]}"

            # i2° remplacé par î
            elif contexte == "i2°":
                scheme = f"{scheme[: position - 1]}î{scheme[position + 2 :]}"

            # iwâ remplacé par iyâ
            elif contexte in {"i2â", "î2â"}:
                scheme = f"{scheme[: position - 1]}iyâ{scheme[position + 2 :]}"

            # uwi (passif) remplacé par î ou i
            elif contexte == "u2i":
                if nature(scheme, position + 2)[0] in "fd":
                    scheme = f"{scheme[: position - 1]}i{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[: position - 1]}î{scheme[position + 2 :]}"

            # °2a : problème à l'impératif pour toutes ces formes : quand l'impératif se termine par
            # la troisième radicale, celle-ci doit fermer la syllabe, et non ouvrir sur une terminaison.
            elif contexte == "°2a":
                # °wa : â si la syllable longue est possible, a sinon
                suite = nature(scheme, position + 2)
                if suite == "ff":
                    scheme = f"{scheme[:position]}a{scheme[position + 2 :]}"
                elif suite[0] == "f":
                    scheme = f"{scheme[:position]}a{scheme[position + 2 :]}"
                elif suite[0] == "d":
                    scheme = f"{scheme[:position]}a{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[:position]}â{scheme[position + 2 :]}"

            # °2â : â, et w supprimé
            elif contexte == "°2â":
                # distinction entre le nom verbal de la forme (iv) **â*ũ
                # et le pluriel irrégulier a**â*ũ (régulier) & mi**â*ũ régulier
                if scheme[0] == "a" or scheme[:2] == "mi":
                    scheme = f"{scheme[:position]}wâ{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[:position]}â{scheme[position + 2 :]}"

            # °2i : î si la syllable longue est possible, i sinon
            elif contexte == "°2i":
                if nature(scheme, position + 2)[0] == "f":
                    scheme = f"{scheme[:position]}i{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[:position]}î{scheme[position + 2 :]}"

            # °2u : û si la syllable longue est possible, u sinon
            elif contexte == "°2u":
                if nature(scheme, position + 2)[0] in {"f", "d"}:
                    scheme = f"{scheme[:position]}u{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[:position]}û{scheme[position + 2 :]}"

            # °2û remplacé par û ou î (participe passif)
            elif contexte == "°2û":
                if racine[1] == "w":
                    scheme = f"{scheme[:position]}û{scheme[position + 2 :]}"
                else:
                    scheme = f"{scheme[:position]}î{scheme[position + 2 :]}"

            elif contexte == "°û":
                scheme = f"{scheme[:position]}û{scheme[position + 2 :]}"

            # voiture balai : on remplace tous les "2" par la lettre radicale :
            scheme = scheme.replace("2", racine[1])

    # première radicale en W
    if racine[0] == "w":
        position = scheme.find("1")
        # La 1ère radicale a pu être forcée à autre chose.
        if position > -1:
            # première forme, suppression du w dans les formes w2i3, sauf dans les verbes sourds (2=3)
            if scheme[position + 2] == "i" and var == "(1)" and racine[1] != racine[2]:
                scheme = f"{scheme[:-1]}{scheme[position + 1 :]}"
            # huitième forme : iwta2a3 => it²a2a3 : à faire à la main, la forme i*ta*a*a est une "exception régulière"

    # fin verbes assimilés en W

    # verbe sourd, on supprime la voyelle intercalaire entre 2 et 3 si c'est possible (forme contractée préférentielle)
    # * Si la 3 porte un sukkun (la 2 est alors une initiale de syllabe fermée), pas de suppression (forme déployée).
    # * Si la 3 porte une voyelle courte, la 2 peut porter un sukkun (forme contractée), dans ce cas :
    #    * Si la 1 porte une voyelle on peut supprimer la voyelle (courte et éventuelle) de la 2
    #    * Si la 1 ne porte pas de voyelle on doit y transférer la voyelle courte de la 2.
    #  because of a phonological rule that prevents two identical consonants from being
    # in sequence with a short vowel between them when they are directly followed by a vowel,
    # However, if the second identical stem consonant is followed by another consonant,
    # the identical consonants remain separated
    position2 = scheme.find("2")
    position3 = scheme.find("µ")
    if (
        racine[1] == racine[2]  # deux consonnes identiques
        and racine[1] not in {"*", ".", "?"}  # "lettres" bidon dans les modèles
        and position3 > -1  # si un petit malin propose un schème sans position 3 en redoublant la 2...
    ):
        # on est dans un cas "sourd"
        if position2 > -1:  # sécurité : exclusion du cas des modèles d'exception imposant la deuxième radicale
            nature2 = nature(scheme, position2)  # Quelle est la nature de la seconde radicale?

            # initiale d'une syllabe ouverte, donc 2 porte une voyelle courte et 3 une voyelle.
            # contraction sur les verbes (var~=""), formes verbales, ou sur les noms (var=="") dont l'infixe n'est pas de la forme *v*v* (voyelle courte avant la deuxième radicale).
            # le cas des noms n'est pas très clair, mais on constate que les **v* sont contractés, et certains *v*v* ne le sont pas, on suppose que ce qui apparaissent contractés sont des *v** d'origine (?)
            if nature2 == "io" and (var != "" or var == "" and scheme[position2 - 1] not in "aiu"):
                if est_voyelle(scheme[position2 - 1]):  # ie, la première radicale est vocalisée
                    # alors on peut supprimer la voyelle de la deuxième radicale
                    # La surdité n'est normalement réalisée que si la voyelle de la première radicale est courte.
                    # On ne peut normalement pas faire suivre une voyelle longue par une consonne avec tchechid (ce qui formerait une super-longue).
                    # Mais c'est une variante d'orthographe. Au besoin, créer un modèle de type ar-*â**a pour imposer la configuration.
                    if est_voyelle_courte(scheme, position2 - 1):
                        scheme = scheme[: position3 - 2] + scheme[position3 - 1 :]

                # sinon on transfère la voyelle de la deuxième radicale sur la première
                else:
                    scheme = "".join(
                        [
                            # début jusqu'à la deuxième radicale
                            scheme[:position2],
                            # insertion de la voyelle de la seconde radicale
                            scheme[position3 - 1],
                            # deuxième radicale
                            scheme[position2],
                            # et directement la troisième (le signe de redoublement sera inséré lors
                            # de la translittération en arabe).
                            scheme[position3:],
                        ]
                    )

    # fin exclusion de sécurité.

    # Cas des formes sourdes à quatre radicales = idem sur 3 et 4
    position4 = scheme.find("4")
    if (
        len(racine) > 3
        and racine[3] == racine[2]  # deux consonnes identiques
        and racine[3] not in {"*", ".", "?"}  # "lettres" bidon dans les modèles
        and position4 > -1  # si un petit malin propose un schème sans position 3 en redoublant la 2...
    ):
        # on est dans un cas "sourd"
        position3 = scheme.find("µ")
        nature3 = nature(scheme, position3)
        # initiale d'une syllabe ouverte, donc 3 porte une voyelle courte et 4 une voyelle.
        if nature3 == "io":
            if est_voyelle(scheme[position3 - 1]):
                # ie, la deuxième radicale est vocalisée
                # alors on peut supprimer la troisième radicale
                if est_voyelle_courte(scheme, position2 - 1):
                    scheme = f"{scheme[: position4 - 2]}{scheme[position4 - 1 :]}"
                    # scheme = f"{scheme[: position4 - 1]}{scheme[position4:]}"

            # sinon on transfère la voyelle de la troisième radicale sur la deuxième
            else:
                scheme = "".join(
                    [
                        # début jusqu'à la troisième radicale
                        scheme[:position3],
                        # insertion de la voyelle de la troisième radicale
                        scheme[position4 - 1],
                        # troisième radicale
                        scheme[position3],
                        # et directement la troisième (le signe de redoublement sera inséré lors
                        # de la translittération en arabe).
                        scheme[position4:],
                    ]
                )

    # Inversement, les verbes où la troisième radicale est redoublée dans le schème doivent se
    # conjuguer comme des sourds
    # ie, si le schème contient un µµ ou un µ² devant une consonne il faut séparer les deux, et boucher le trou avec un "a" pour ne pas avoir trois consonnes d'affilée.
    if scheme.find("µµ") > -1 or scheme.find("µ²") > -1:
        scheme = sub(r"µ²", "µµ", scheme, count=1)  # homogénéisation des cas
        position3 = scheme.find("µµ")
        if not est_voyelle(scheme[position3 + 2]) or not scheme[position3 + 2]:
            scheme = f"{scheme[: position3 - 1]}a{scheme[position3 + 1 :]}"

    scheme = scheme.replace("2", racine[1])

    # Toisième radicale : cas des verbes défectifs
    if racine[2] in {"w", "y"}:
        # préparation du contexte
        position = scheme.find("µ")
        contexte = ""
        if position > -1:  # La 3ème radicale a pu être forcée à autre chose.
            # contexte de la radicale : quelles sont les voyelles (courtes ou longues) avant et après la consonne 3 :
            contexte += f"{scheme[position - 1]}3" if est_voyelle(scheme[position - 1]) else "°3"
            if len(scheme) == position:
                contexte = contexte  # fin de schème
            elif scheme[position + 1] in {"²", scheme[position]}:
                contexte += "²"
                contexte += scheme[position + 2] if est_voyelle(scheme[position + 2]) else "°"
            elif est_voyelle(scheme[position + 1]):
                contexte += scheme[position + 1]
            else:
                contexte += "°"

            # troisième radicale défective en w
            if racine[2] == "w" and var in {"(1)", ""}:
                # verbe défectif en W, cf Schier p. 74

                if contexte == "a3a":
                    # awa final devient â au prétérit de la première forme, é sinon
                    if position == len(scheme) - 1:
                        # position finale
                        if position == 5 and scheme[1] == "a":  # première forme
                            scheme = f"{scheme[: position - 1]}â{scheme[position + 2 :]}"
                        else:
                            scheme = f"{scheme[: position - 1]}é{scheme[position + 2 :]}"
                    else:
                        scheme = f"{scheme[: position - 1]}a{scheme[position + 2 :]}"

                # test sur première forme
                elif contexte == "a3â":
                    # awâ final devient ayâ au passif devant a3âni final
                    if (
                        position == len(scheme) - 3 and scheme[position + 2 : position + 4] == "ni" and (var != "")
                    ):  # les duels ne sont pas concernés.
                        scheme = f"{scheme[: position - 1]}ayâ{scheme[position + 2 :]}"
                    else:
                        scheme = f"{scheme[:position]}{racine[2]}{scheme[position + 1 :]}"

                elif contexte == "a3@":
                    scheme = f"{scheme[: position - 1]}â@{scheme[position + 2 :]}"

                elif contexte == "a3î":
                    scheme = f"{scheme[: position - 1]}ay{scheme[position + 2 :]}"

                elif contexte == "a3u":
                    scheme = f"{scheme[: position - 1]}é{scheme[position + 2 :]}"

                elif contexte == "a3û":
                    scheme = f"{scheme[: position - 1]}aw{scheme[position + 2 :]}"

                elif contexte == "a3ũ":
                    # Pb ici, "ã" pour *a*a*ũ, *i*a*ũ et *u*a*ũ, "ãé" sinon. Cf. Palmer §50 p100
                    if shemeinit in {"1a2aµũ", "1i2aµũ", "1u2aµũ"}:
                        scheme = f"{scheme[: position - 1]}ã"
                    else:
                        scheme = f"{scheme[: position - 1]}ãé"

                elif contexte == "a3ã":
                    # Pb ici, "ã" pour *a*a*ũ, *i*a*ũ et *u*a*ũ, "ãé" sinon. Cf. Palmer §50 p100
                    if shemeinit in {"1a2aµã", "1i2aµã", "1u2aµã"}:
                        scheme = f"{scheme[: position - 1]}ã"
                    else:
                        scheme = f"{scheme[: position - 1]}ãé"

                elif contexte == "a3ĩ":
                    # Pb ici, "ã" pour *a*a*ũ, *i*a*ũ et *u*a*ũ, "ãé" sinon. Cf. Palmer §50 p100
                    if shemeinit in {"1a2aµĩ", "1i2aµĩ", "1u2aµĩ"}:
                        scheme = f"{scheme[: position - 1]}ã"
                    else:
                        scheme = f"{scheme[: position - 1]}ãé"

                elif contexte == "â3ũ":
                    # seul cas pratique derrière un â long?
                    scheme = f"{scheme[: position - 1]}â'u"  # diptote dans ce cas

                elif contexte == "a3°":
                    # inaccompli passif (2FP, 3FP) en ay
                    # versus accompli actif en voyelle de l'inaccompli (?) :
                    if scheme[position - 3] == "a":  # on est à l'inaccompli
                        scheme = f"{scheme[: position - 1]}aw{scheme[position + 1 :]}"
                    else:
                        scheme = f"{scheme[: position - 1]}ay{scheme[position + 1 :]}"

                elif contexte == "i3a":
                    scheme = f"{scheme[: position - 1]}iya{scheme[position + 2 :]}"

                elif contexte == "i3@":
                    scheme = f"{scheme[: position - 1]}iy@{scheme[position + 2 :]}"

                elif contexte == "i3i":
                    scheme = f"{scheme[: position - 1]}i{scheme[position + 2 :]}"

                elif contexte == "i3â":
                    scheme = f"{scheme[: position - 1]}iyâ{scheme[position + 2 :]}"

                elif contexte == "i3î":
                    scheme = f"{scheme[: position - 1]}î{scheme[position + 2 :]}"

                elif contexte == "i3ĩ":
                    scheme = f"{scheme[: position - 1]}ĩ{scheme[position + 2 :]}"

                elif contexte == "i3u":
                    scheme = f"{scheme[: position - 1]}iy{scheme[position + 2 :]}"

                elif contexte == "i3û":
                    scheme = f"{scheme[: position - 1]}û{scheme[position + 2 :]}"

                elif contexte == "i3ũ":
                    scheme = f"{scheme[: position - 1]}ĩ{scheme[position + 2 :]}"

                elif contexte == "i3°":
                    scheme = f"{scheme[: position - 1]}î{scheme[position + 2 :]}"

                elif contexte == "u3i":
                    scheme = f"{scheme[: position - 1]}i{scheme[position + 2 :]}"

                elif contexte == "u3î":
                    scheme = f"{scheme[: position - 1]}î{scheme[position + 2 :]}"

                elif contexte == "u3u":
                    # dépend si c'est en fin de mot
                    if position == len(scheme) - 1:
                        scheme = f"{scheme[: position - 1]}îû{scheme[position + 2 :]}"
                    else:
                        scheme = f"{scheme[: position - 1]}u{scheme[position + 2 :]}"

                elif contexte == "u3û":
                    scheme = f"{scheme[: position - 1]}îû{scheme[position + 2 :]}"

                elif contexte == "u3ũ":
                    scheme = f"{scheme[: position - 1]}ĩ{scheme[position + 2 :]}"

                elif contexte == "u3":  # en fin de mot
                    scheme = f"{scheme[: position - 1]}u{scheme[position + 1 :]}"

                elif contexte == "u3°":
                    scheme = f"{scheme[: position - 1]}û{scheme[position + 1 :]}"

                elif scheme[position - 1] == "y":  # cas du diminutif en *u*ay*ũ ou *u*ay*@ũ:
                    scheme = f"{scheme[:position]}y{scheme[position + 1 :]}"

                elif contexte == "û3ũ":  # Pb d'écriture
                    scheme = f"{scheme[: position - 1]}uw²ũ{scheme[position + 2 :]}"

                elif contexte == "°3ũ" and scheme[position - 2] == "a":
                    # traitement différent de *a*wũ et *u*wũ - bon, enfin, du moins ça marche :-/
                    scheme = f"{scheme[:position]}wũ{scheme[position + 2 :]}"

                elif contexte in {"°3ũ", "°3ĩ"}:
                    scheme = f"{scheme[:position]}ã{scheme[position + 2 :]}"

                elif contexte == "°3ã" and scheme[position + 2] != "é":
                    scheme = f"{scheme[:position]}ã{scheme[position + 2 :]}"

                # la radicale faible disparaît parfois devant @, mais il faut dans ce cas la supprimer à la main.
                # fin traitement des cas particuliers en w

            else:
                # verbe défectif en Y, cf Schier p. 74
                # ou formes dérivées d'un verbe défectif, traité comme un "y"
                if contexte == "a3a":
                    if position == len(scheme) - 1:  # position finale
                        scheme = f"{scheme[: position - 1]}é{scheme[position + 2 :]}"
                    else:
                        scheme = f"{scheme[: position - 1]}a{scheme[position + 2 :]}"

                elif contexte == "a3â":
                    scheme = f"{scheme[: position - 1]}ayâ{scheme[position + 2 :]}"

                elif contexte == "a3@":
                    scheme = f"{scheme[: position - 1]}â@{scheme[position + 2 :]}"

                elif contexte == "â3@":
                    scheme = f"{scheme[: position - 1]}ây@{scheme[position + 2 :]}"

                elif contexte == "a3î":
                    scheme = f"{scheme[: position - 1]}ay{scheme[position + 2 :]}"

                elif contexte == "a3u":
                    # dépend si c'est en fin de mot
                    if position == len(scheme) - 1:
                        scheme = f"{scheme[: position - 1]}é{scheme[position + 2 :]}"
                    else:
                        scheme = f"{scheme[: position - 1]}ay{scheme[position + 2 :]}"

                elif contexte == "a3û":
                    scheme = f"{scheme[: position - 1]}aw{scheme[position + 2 :]}"

                elif contexte in {"a3ũ", "a3ã", "a3ĩ"}:
                    scheme = f"{scheme[: position - 1]}ãé"

                elif contexte == "â3i":
                    scheme = f"{scheme[: position - 1]}â'i{scheme[position + 2 :]}"
                    # typiquement -*i*â*iy²ũ doit conserver la hamza de -*i*â*ũ
                    # en fait on peut neutraliser via un W fort.
                elif contexte == "â3ũ":  # and racine[1] != "'")  # exception pour la hamza en 2 ?
                    scheme = f"{scheme[: position - 1]}â'u"  # diptote dans ce cas

                elif contexte == "a3°":
                    # ay devant consonne, é en finale
                    scheme = f"{scheme[: position - 1]}ay{scheme[position + 1 :]}"

                elif contexte == "a3" and racine[1] == "'":
                    # exemple de ar-r'y impératif sur un schème de type ar-*a3
                    scheme = f"{scheme[: position - 1]}a"

                elif contexte == "a3":
                    scheme = f"{scheme[: position - 1]}i"

                elif contexte == "i3a":
                    scheme = f"{scheme[: position - 1]}iya{scheme[position + 2 :]}"

                elif contexte == "i3@":
                    scheme = f"{scheme[: position - 1]}iy@{scheme[position + 2 :]}"

                elif contexte == "î3@":
                    scheme = f"{scheme[: position - 1]}îy@{scheme[position + 2 :]}"

                elif contexte == "i3â":
                    scheme = f"{scheme[: position - 1]}iyâ{scheme[position + 2 :]}"

                elif contexte == "i3i":
                    scheme = f"{scheme[: position - 1]}i{scheme[position + 2 :]}"

                elif contexte == "i3î":  # î
                    scheme = f"{scheme[: position - 1]}î{scheme[position + 2 :]}"

                elif contexte == "i3ĩ":
                    scheme = f"{scheme[: position - 1]}ĩ{scheme[position + 2 :]}"

                elif contexte == "i3u":  # dépend si c'est en fin de mot
                    if position == len(scheme) - 1:
                        scheme = f"{scheme[: position - 1]}î{scheme[position + 2 :]}"
                    else:
                        scheme = f"{scheme[: position - 1]}u{scheme[position + 2 :]}"

                elif contexte == "i3û":
                    scheme = f"{scheme[: position - 1]}û{scheme[position + 2 :]}"

                elif contexte == "i3ũ":
                    scheme = f"{scheme[: position - 1]}ĩ"

                elif contexte == "i3°":
                    scheme = f"{scheme[: position - 1]}î{scheme[position + 1 :]}"

                elif contexte == "i3":  # en fin de mot
                    scheme = f"{scheme[: position - 1]}i{scheme[position + 1 :]}"

                elif contexte == "u3ũ":
                    scheme = f"{scheme[: position - 1]}ĩ{scheme[position + 2 :]}"

                elif (contexte == "û3ũ") and scheme[:3] == "ma1":
                    # contamination du y sur le û dans la forme ma**û*ũ, cf Wright 1874 §170,
                    # mais la 2 est déjà remplacée dans le schème donc on ne peut pas tester le schème d'origine
                    scheme = f"{scheme[: position - 1]}iy²ũ{scheme[position + 2 :]}"

                elif (contexte == "û3@") and scheme[:3] == "ma1":
                    # idem féminin
                    scheme = f"{scheme[: position - 1]}iy²@{scheme[position + 2 :]}"

                # fin traitement des cas particuliers en y
            # verbe défectifs

        # 3ème radicale présente

    # verbes défectifs
    # voiture balai :
    scheme = scheme.replace("µ", racine[2])

    # quatrième radicale éventuelle
    # si on applique un schème quadrilittère à une racine à trois consonnes, on redouble simplement la dernière
    scheme = scheme.replace("4", racine[2 if (len(racine) <= 3 or racine[3] == "") else 3])

    # première radicale
    scheme = scheme.replace("1", racine[0])

    # pb : si le schème est en "1°" le "i" prosthétique est virtuel à ce stade :
    # le cas général "de prolongation" ne marche pas, il faut forcer à la main :
    if scheme[0] == "w" and not est_voyelle(scheme[1]):
        scheme = f"î{scheme[1]}"

    # Accord des w et y de prolongation en fonction du contexte vocalique
    # (ne concerne pas les W et Y, invariables par principe) :
    while (position := scheme.find("iw")) > -1:
        if est_voyelle(scheme[position + 2]):
            scheme = f"{scheme[:position]}iW{scheme[position + 2 :]}"  # éviter une boucle infinie
        elif (
            scheme[position + 2] == "²"
        ):  # Pb sinon avec les -iw²- qu'il ne faut pas transformer en î², ce qui n'aurait aucun sens...
            scheme = f"{scheme[:position]}iY{scheme[position + 2 :]}"
        else:
            scheme = f"{scheme[:position]}î{scheme[position + 2 :]}"

    while (position := scheme.find("uy")) > -1:
        if est_voyelle(scheme[position + 2]):
            scheme = f"{scheme[:position]}uY{scheme[position + 2 :]}"
        else:
            scheme = f"{scheme[:position]}û{scheme[position + 2 :]}"

    while (position := scheme.find("wî")) > -1:
        scheme = f"{scheme[:position]}yi{scheme[position + 2 :]}"

    # nettoyage éventuel : Y et W des verbes réguliers; neutralisation des verbes hamzé
    scheme = (
        scheme.replace("Y", "y")
        .replace("W", "w")
        .replace("`", "'")  # remplacement de l'accent grave par un guillement simple
    )

    # écriture des lettres de prolongations
    while (position := scheme.find("ûw")) > -1:
        scheme = f"{scheme[:position]}uw²{scheme[position + 2 :]}"

    while (position := scheme.find("uw")) > -1:
        if est_voyelle(scheme[position + 2]):
            scheme = f"{scheme[:position]}uW{scheme[position + 2 :]}"
        else:
            scheme = f"{scheme[:position]}û{scheme[position + 2 :]}"

    while (position := scheme.find("iy")) > -1:
        if est_voyelle(scheme[position + 2]) or scheme[position + 2] == "²":  # Pb sinon avec les -iy²-
            scheme = f"{scheme[:position]}iY{scheme[position + 2 :]}"
        else:
            scheme = f"{scheme[:position]}î{scheme[position + 2 :]}"

    while (position := scheme.find("îy")) > -1:
        scheme = f"{scheme[:position]}iy²{scheme[position + 2 :]}"

    while (position := scheme.find("yî")) > -1:
        if est_voyelle_courte(scheme, position - 1):
            # intercepter des cas comme taXyîTũ => taXYîTũ et pas taXy²iTũ ;
            # d'autre part des séquences de type âyî restent invariables (pas de redoublement possible après une voyelle longue).
            scheme = f"{scheme[:position]}y²i{scheme[position + 2 :]}"
        else:
            scheme = f"{scheme[:position]}Yî{scheme[position + 2 :]}"

    while (position := scheme.find("û²")) > -1:
        scheme = f"{scheme[:position]}uw²{scheme[position + 2 :]}"

    # nettoyage éventuel : Y et W repassent en minuscule pour l'affichage :
    scheme = scheme.replace("Y", "y").replace("W", "w")

    # ajout d'une voyelle mutable, si le mot commence par deux consonnes :
    if not est_voyelle(scheme[0]) and not est_voyelle(scheme[1]):
        # Consonne en première position et pas de voyelle en deuxième position = il faut rajouter une voyelle préfixe.
        scheme = f"{mobile}{scheme}"

    # ajustement de l'initiale pour les verbes hamzés en 1 : i' se transforme en î et u' en û
    # (une même syllabe ne peut pas être à la fois ouverte et fermée par une hamza)
    if scheme[:3] == "i'":
        scheme = f"iy{scheme[2]}" if est_voyelle(scheme[2]) else f"î{scheme[2]}"
    if scheme[:3] == "u'":
        scheme = f"uw{scheme[2]}" if est_voyelle(scheme[2]) else f"û{scheme[2]}"
    if scheme[:3] == "a'":
        scheme = f"aw{scheme[2]}" if est_voyelle(scheme[2]) else f"â{scheme[2]}"

    # ajustement pour les verbes assimilés en y
    if (position := scheme.find("uy")) > -1:
        if not est_voyelle(scheme[position + 2]):
            scheme = f"{scheme[:position]}û{scheme[position + 2 :]}"

    # Ajustement des redoublements en ² en doublant la consonne à la place :
    while "²" in scheme:
        position = scheme.find("²")
        lettre = scheme[position - 1]
        scheme = f"{scheme[:position]}{lettre}{scheme[position + 1 :]}"

    # ... mais pas la hamza sinon pb d'affichage
    if "''" in scheme:
        position = scheme.find("''")
        scheme = f"{scheme[: position + 1]}²{scheme[position + 2 :]}"

    # Pb d'affichage de deux hamza de suite : mettre la première en ligne (pas sûr que ce soit la meilleure solution)
    if "'a'" in scheme:
        position = scheme.find("'a'")
        scheme = f"{scheme[:position]}`a'{scheme[position + 3 :]}"

    # the end !
    return scheme
