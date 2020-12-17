"""
Arabiser: manual conversion of arabiser function from
https://fr.wiktionary.org/wiki/Module:arabe

Current version:
    https://fr.wiktionary.org/w/index.php?title=Module:arabe&oldid=28937329

"""

import unicodedata

# Translittérations de API / romain / . vers arabe

en_arabe = {
    " ": " ",  # blancs entre mots
    "_": "",  # underscore ignoré pour décontextualisation éventuelle
    "؛": "؛",  # point virgule arabe
    ";": "؛",
    "؞": "؞",  # trois points
    "؟": "؟",  # point d'interrogation
    "?": "؟",
    "ء": "ء",  # Hamza
    "ò": "ء",
    "`": "ء",
    "'": "ء",
    "‘": "ء",
    "ʾ": "ء",
    "ʼ": "ء",
    "ˈ": "ء",
    "'": "ء",
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
    "◌ٍ": "◌ٍ",  # Kasratan
    "ĩ": "◌ٍ",
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
}


def arabiser(texte: str) -> str:  # pragma: no cover
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
    'كْتْبْ'

    >>> arabiser("elmubdi'u wa elmu3îdu")
    'المُبْدِئُ وَ المُعِيدُ'

    """
    # translittération en arabe du paramètre, suivant l'assoc-liste en_arabe.
    texte = f" {texte} "
    # on rajoute un blanc devant et derrière pour uniformiser les tests de début et fin de mot
    transcription = ""
    a_traiter = ""
    # à faire un jour : transformer tous les ² en redoublements explicites avant traitement
    # à faire un jour : reporter sur la lettre attendue toutes les lettres équivalentes admissibles

    for curseur in range(1, len(texte) - 1):
        a_traiter = texte[curseur]
        # orthographe différente suivant qu'on est en "début" ou en milieu de mot.
        if texte[curseur - 1] == " " or (
            curseur > 1
            and texte[curseur - 3 : curseur]
            in (" el", " bi", " fa", " ka", " la", " li", " wa")
        ):
            # on est en début de mot
            # Si le début du mot est une voyelle il faut insérer en amont une hamza préfixe
            # Mais si la structure est a'° ou â'° ou â il faut un alif madda
            debut = texte[curseur : curseur + 3]
            if debut in ("a'i", "a'î", "a'u", "a'û", "a'a", "a'â"):
                # il y aura superposition d'une hamza instable et d'une hamza structurelle portant voyelle
                transcription += "أ◌َ"  # alif hamza + fatha
            elif (
                texte[curseur : curseur + 2] == "a'"
                or texte[curseur : curseur + 2] == "'â"
                or a_traiter == "â"
            ):
                transcription += "آ"  # alif madda
            elif a_traiter == "'":  # hamza explicite en début de mot
                suivant = texte[curseur + 1]
                if suivant == "â":
                    transcription += "آ"  # alif madda
                elif suivant == "a" or suivant == "u" or suivant == "û":
                    transcription += "أ"  # support en haut
                elif suivant == "i" or suivant == "î":
                    transcription += "إ"  # support en bas
                # la hamza préfixe a été insérée, la voyelle suivante sera transcrite ensuite
            else:  # Il faut rajouter la lettre à la transcription.

                # Mais d'abord si c'est une voyelle, on met une hamza préfixe
                if a_traiter in ("a", "u", "û"):
                    transcription += "أ"  # support en haut
                elif a_traiter in ("i", "î"):
                    transcription += "إ"  # support en bas
                # la hamza préfixe a été insérée

                # reste à transcrire la lettre
                transcription += en_arabe[a_traiter]
            # cas hamza préfixe
            # post-traitement : si la consonne est derrière el- il faut rajouter un chadda aux lettres solaires
            if texte[curseur - 1] == "l" and texte[curseur - 2] == "e":
                # faire le test solaire
                if a_traiter in (
                    "t",
                    "F",
                    "d",
                    "V",
                    "r",
                    "z",
                    "s",
                    "C",
                    "S",
                    "D",
                    "T",
                    "Z",
                    "l",
                    "n",
                ):
                    transcription += en_arabe["²"]
            # faire le test solaire

        else:  # on n'est pas en début de mot
            # Ne présentent jamais de redoublement :
            if a_traiter in (
                "a",
                "i",
                "u",
                "e",
                "î",
                "A",
                "I",
                "U",
                "E",
                "ĩ",
                "ũ",
                "õ",
                "_",
            ):
                transcription = transcription + en_arabe[a_traiter]

            elif a_traiter == "é":
                if texte[curseur - 1] != "ã":
                    transcription = transcription + en_arabe["a"]
                transcription = transcription + en_arabe[a_traiter]
            elif a_traiter == "û":  # cas particulier d'un u final : alif muet
                # plus simple de ne pas le mettre.
                transcription = transcription + en_arabe[a_traiter]
                # if (mw.ustring.sub( texte, curseur+1, curseur+1 ) == " ")
                # then transcription = transcription .. en_arabe["e"] end

            elif a_traiter == "~":
                transcription = transcription + en_arabe["a"] + en_arabe["~"]

            # Traitement des différents cas particuliers dépendants du contexte
            elif a_traiter == "ã":
                # le ã est suivi d'un alif muet, mais pas derrière ât et @ :
                transcription += en_arabe[a_traiter]
                if (
                    texte[curseur - 1] != "@"
                    and texte[curseur - 2 : curseur] != "ât"
                    and texte[curseur + 1] != "é"
                ):
                    transcription += en_arabe["A"]
            elif a_traiter == "â":
                # pas de nouvel alif derrière une hammza portée par alif
                if texte[curseur - 1] == "'":
                    avant = texte[curseur - 2]
                    if avant == "'":
                        avant = texte[curseur - 3]
                    if avant in ("i", "î", "I", "y", "u", "û", "w", "â"):
                        transcription = transcription + en_arabe["â"]
                    # sinon : la hamza a déjà inséré un alif madda et on ne fait rien
                else:
                    transcription = transcription + en_arabe["â"]
            elif a_traiter == "@":
                # ta arbouta : précédé de 'a' implicite, sauf quand derrière un 'â'
                if texte[curseur - 1] != "â":
                    transcription += en_arabe["a"]
                transcription += en_arabe["@"]
            elif a_traiter == "é":
                # alif maksoura : précédé de 'a' implicite, sauf quand devant un 'ã'
                if texte[curseur + 1] != "ã":
                    transcription += en_arabe["a"]
                transcription += en_arabe["é"]
            # Quelques cas où on ne veut pas examiner la présence d'un ²
            elif a_traiter == "°":  # Sukun explicite
                transcription += en_arabe["°"]
            elif a_traiter == "*" or a_traiter == ".":
                transcription += en_arabe["*"]

            # Lettre redoublée de la précédente :
            elif a_traiter == texte[curseur - 1]:
                # Pas de gemmination si on est derrière un el- préfixe (el-lah)
                # mais dans ce cas le second l est traité comme début de mot : pas cette branche.
                transcription += en_arabe["²"]

            elif a_traiter == "'":  # hamza
                # Hamza : problème du support
                avant = texte[curseur - 1]
                apres = texte[curseur + 1]

                # insertion d'un sukun si nécessaire
                if (
                    avant
                    not in (
                        "a",
                        "e",
                        "i",
                        "u",
                        "â",
                        "î",
                        "û",
                        "é",
                        "ã",
                        "ĩ",
                        "ñ",
                        "é",
                        "A",
                        "I",
                        "U",
                        "E",
                        "ñ",
                        "õ",
                        "-",
                        "~",
                        "é",
                        "_",
                        "°",
                    )
                    and texte[curseur - 3 : curseur] != " el"
                ):  # pas de sukun après el- en début de mot
                    transcription += en_arabe["°"]
                if (
                    curseur > len(texte) - 4
                    or apres == " "
                    or texte[curseur + 2] == " "
                    and apres != "â"
                    and apres != "î"
                    and apres != "û"
                    and apres != "é"
                    and apres != "A"
                    and apres != "I"
                    and apres != "U"
                    and apres != "E"
                ):
                    # il ne faut pas de lettre de prolongation non plus
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
                else:  # hamza en milieu de mot
                    if apres == "'" or apres == "²":
                        apres = texte[curseur + 2]

                    # derrière un i, support ya
                    if avant == "i" or avant == "î" or avant == "I" or avant == "y":
                        transcription += en_arabe["ì"]
                    # derrière un waw, hamza en ligne
                    elif avant == "û" or avant == "w":
                        transcription += en_arabe["'"]
                    # derrière un u faut voir après
                    elif avant == "u":
                        if apres == "i" or apres == "î":
                            transcription += en_arabe["ì"]
                        else:
                            transcription += en_arabe["ù"]
                    # derrière un a faut voir après
                    elif avant == "a":
                        if apres == "i" or apres == "î":
                            transcription += en_arabe["ì"]
                        elif apres == "û" or apres == "u":
                            transcription += en_arabe["ù"]
                        elif apres == "â":
                            transcription += en_arabe["~"]  # madda, et â sera omis
                        # dans les autres cas, support alif, sauf le cas a' initial déjà traité avec le a initial
                        elif texte[curseur - 2] != " ":
                            transcription += en_arabe["à"]

                    # derrière un â, on risque de trouver une hamza en ligne pour ā’a, ū’a & aw’a
                    elif avant == "â":
                        # il y a nécessairement une consonne après
                        if apres == "i" or apres == "î":
                            transcription += en_arabe["ì"]
                        elif apres == "u":
                            transcription += en_arabe["ù"]
                        else:
                            transcription += en_arabe["'"]  # en ligne
                    else:  # pas de voyelle avant, donc sukun
                        if apres == "i" or apres == "î":
                            transcription += en_arabe["ì"]
                        elif apres == "û" or apres == "u":
                            transcription += en_arabe["ù"]
                        elif apres == "â":
                            transcription += en_arabe["~"]
                        else:
                            transcription += en_arabe["à"]
                    # traitement milieu de mot
                # fin ou pas
            # fin du cas de la hamza

            elif a_traiter == "-":
                transcription += en_arabe["-"]
            elif a_traiter == "²":
                transcription += en_arabe["²"]
            else:  # dans les autres cas, translittération de la consonne, mais avec sukun éventuel
                avant = texte[curseur - 1]
                # on ne met pas de sukun après...
                if (
                    avant
                    not in (
                        "a",
                        "e",
                        "i",
                        "u",
                        "â",
                        "î",
                        "û",
                        "é",
                        "ã",
                        "ĩ",
                        "ñ",
                        "é",
                        "A",
                        "I",
                        "U",
                        "E",
                        "ñ",
                        "õ",
                        "-",
                        "~",
                        "_",
                        "°",
                    )
                    and a_traiter != " "
                    and texte[curseur - 3 : curseur] != " el"
                    and texte[curseur - 3 : curseur] != " a'"
                ):  # pas de sukun après el- en début de mot ou sur un alif madda
                    transcription += en_arabe["°"]

                if en_arabe.get(a_traiter):
                    transcription += en_arabe[a_traiter]
                # cas d'une consonne en fin de mot - rajouter un sukun final
                if texte[curseur + 1] == " ":
                    transcription += en_arabe["°"]

    transcription = "".join(
        [c for c in transcription if unicodedata.name(c) != "DOTTED CIRCLE"]
    )

    # for - boucle de traitement
    return unicodedata.normalize("NFC", transcription)
