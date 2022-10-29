"""
Arabiser: manual conversion of arabiser function from
https://fr.wiktionary.org/wiki/Module:arabe

Current version: 11 mars 2022 10:19
    https://fr.wiktionary.org/w/index.php?title=Module:arabe&oldid=30261022

"""
import unicodedata
from re import sub
from typing import Tuple

# Translittérations de API / romain / . vers arabe

en_arabe = {
    " ": " ",  # blancs entre mots
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
    "É": "ى",
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
    diacritiques = any(
        char in texte for char in ["a", "i", "u", "ã", "ĩ", "ũ", "²", "°"]
    )
    for curseur in range(1, len(texte) - 1):
        a_traiter = texte[curseur]
        # orthographe différente suivant qu'on est en "début" ou en milieu de mot.
        # début de mot
        if (
            texte[curseur - 1] == " "
            or (  # précédé d'un blanc = début de mot
                # derrière el- il faut écrire comme en début de mot malgré la liaison :
                # idem derrière particules inséparables
                curseur > 1
                # Pb de la hamza dans des mots comme bi'r, ne pas traiter comme un préfixe
                and a_traiter != "'"
                and texte[curseur - 3 : curseur]
                in (" el", " ^l", " bi", " fa", " ka", " la", " li", " wa")
            )
            or (
                curseur > 1
                # idem si plusieurs particules séparées par un blanc souligné
                and texte[curseur - 3 : curseur]
                in ("_el", "_^l", "_bi", "_fa", "_ka", "_la", "_li", "_wa")
            )
            or (
                curseur > 1
                # un blanc souligné permet de couper le mot s'il faut forcer un fa'tu en fa_'tu par exemple
                and texte[curseur - 3 : curseur]
                in ("el_", "^l_", "bi_", "fa_", "ka_", "la_", "li_", "wa_")
            )
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
                elif suivant in ["a", "u", "û"]:
                    transcription += "أ"  # support en haut
                elif suivant in ["i", "î"]:
                    transcription += "إ"  # support en bas
                else:
                    transcription += "ا"  # par défaut, alif
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
            if (
                texte[curseur - 1] == "l"
                and texte[curseur - 2] in ["e", "^"]
                and (
                    a_traiter
                    in (
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
                    )
                    and diacritiques
                )
            ):
                transcription += en_arabe["²"]
                    # faire le test solaire

        elif a_traiter in (
                "a",
                "i",
                "u",
                "e",
                "^",
                "î",
                "A",
                "I",
                "U",
                "E",
                "É",
                "ĩ",
                "ũ",
                "õ",
                "_",
            ):
            transcription = transcription + en_arabe[a_traiter]

        elif a_traiter == "é":
            if texte[curseur - 1] not in ["ã", "_", "E"]:
                transcription = transcription + en_arabe["a"]
            transcription = transcription + en_arabe[a_traiter]
        elif a_traiter == "û":  # cas particulier d'un u final : alif muet
            # plus simple de ne pas le mettre.
            transcription = transcription + en_arabe[a_traiter]
            # if (mw.ustring.sub( texte, curseur+1, curseur+1 ) == " ")
            # then transcription = transcription .. en_arabe["e"]

        elif a_traiter == "~":
            transcription = transcription + en_arabe["a"] + en_arabe["~"]

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
            # ta arbouta : précédé de 'a' implicite, sauf quand derrière une voyelle longue
            if texte[curseur - 1] not in ["â", "î", "û", "_"] and diacritiques:
                transcription += en_arabe["a"]
            transcription += en_arabe["@"]
        elif a_traiter == "°":  # Sukun explicite
            transcription += en_arabe["°"]
        elif a_traiter in ["*", "."]:
            transcription += en_arabe["*"]

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
                    "É",
                    "A",
                    "I",
                    "U",
                    "E",
                    "ñ",
                    "õ",
                    "-",
                    "~",
                    ",",
                    "é",
                    "_",
                    "°",
                    "^",
                    "?",
                )
                and texte[curseur - 3 : curseur]
                not in [
                    " el",
                    " ^l",
                    "_el",
                    "_^l",
                ]  # pas de sukun après el- en début de mot + cas du alif wasla
                and diacritiques
            ):
                transcription += en_arabe["°"]
                # Traitement différent suivant qu'on est en fin de mot ou en milieu :
            if (
                    curseur > len(texte) - 4
                    or apres == " "
                    or (
                        texte[curseur + 2] == " "
                        and apres
                        != "â"  # il ne faut pas de lettre de prolongation non plus
                        and apres != "î"
                        and apres != "û"
                        and apres != "é"
                        and apres != "A"
                        and apres != "I"
                        and apres != "U"
                        and apres != "E"
                    )
                ):
                    # hamza en fin de mot
                if avant == "a":
                    transcription += en_arabe["à"]
                elif avant == "i":
                    transcription += en_arabe["ì"]
                elif avant == "u":
                    transcription += en_arabe["ù"]
                else:
                    transcription += en_arabe["'"]
                                # fin de mot
            else:  # hamza en milieu de mot
                if apres in ["'", "²"]:
                    apres = texte[curseur + 2]

                    # derrière un i, support ya
                if avant in ["i", "î", "I", "y"]:
                    transcription += en_arabe["ì"]
                elif avant in ["û", "w"]:
                    transcription += en_arabe["'"]
                elif avant == "u":
                    transcription += en_arabe["ì"] if apres in ["i", "î"] else en_arabe["ù"]
                elif avant == "a":
                    if apres in ["i", "î"]:
                        transcription += en_arabe["ì"]
                    elif apres in ["û", "u"]:
                        transcription += en_arabe["ù"]
                    elif apres == "â":
                        transcription += en_arabe["~"]  # madda, et â sera omis
                    elif texte[curseur - 2] != " ":
                        transcription += en_arabe["à"]

                elif avant == "â":
                        # il y a nécessairement une consonne après
                    if apres in ["i", "î"]:
                        transcription += en_arabe["ì"]
                    elif apres == "u":
                        transcription += en_arabe["ù"]
                    else:
                        transcription += en_arabe["'"]  # en ligne
                elif apres in ["i", "î"]:
                    transcription += en_arabe["ì"]
                elif apres in ["û", "u"]:
                    transcription += en_arabe["ù"]
                elif apres == "â":
                    transcription += en_arabe["~"]
                else:
                    transcription += en_arabe["à"]
                                # traitement milieu de mot
                        # fin ou pas
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
                    "É",
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
                    "^",
                    "?",
                )
                and a_traiter != " "
                and texte[curseur - 3 : curseur]
                not in [
                    " el",
                    " ^l",
                    "_el",
                    "_^l",
                ]  # pas de sukun après el- en début de mot + pas de sukun sur un alof wasla
                and texte[curseur - 3 : curseur]
                != " a'"  # pas de sukun après el- en début de mot ou sur un alif madda
                and diacritiques
            ):
                transcription += en_arabe["°"]

            if en_arabe.get(a_traiter):
                transcription += en_arabe[a_traiter]
            # cas d'une consonne en fin de mot - rajouter un sukun final
            if texte[curseur + 1] == " " and diacritiques:
                transcription += en_arabe["°"]

    transcription = "".join(
        [c for c in transcription if unicodedata.name(c) != "DOTTED CIRCLE"]
    )

    # for - boucle de traitement
    return unicodedata.normalize("NFC", transcription)


def est_voyelle(char: str) -> bool:
    """La voyelle peut être tout ce qui permet à une consonne d'être une
    initiale de syllabe : courte ou longue, tanwîn, ou ta marbuta.
    """
    return char in "aeiuâîûãĩũ@ñõ"


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
        return "vo" if est_voyelle(scheme[position + 2]) else "vf"
    # cas consonne
    if not scheme[position + 1]:
        # la consonne est la dernière lettre, donc finale fermée
        return "ff"
    if scheme[position + 1] in {"²", char}:
        # consonne double, voir la nature de la voyelle nécessairement présente à pos+2
        return f"d{nature(scheme, position+2)[1]}"
    if scheme[position - 1] == char:
        # 2ème de double, voir la nature de la voyelle nécessairement présente à pos+1
        return f"d{nature(scheme, position+1)[1]}"
    if not est_voyelle(scheme[position - 1]):
        # 2ème de deux consonnes, idem
        return f"i{nature(scheme, position+1)[1]}"
    return (
        f"i{nature(scheme, position + 1)[1]}"
        if est_voyelle(scheme[position + 1])
        else "fo"
    )


def appliquer(scheme: str, racine: str, var: str = "") -> Tuple[str, str]:
    if not var:  # ne dit rien
        from .racines_arabes import racines_arabes

        var = racines_arabes.get(scheme, "")

    # Dans les modèles de la forme ar-*a*a*a-i, les deux dernières lettres indiquent conventionnellement la voyelle
    # de l'inaccompli et doivent être supprimées dans un affichage normal
    if scheme[-2] == "-":  # avant-dernière lettre = "-" ?
        scheme = scheme[:-3]  # supprimer les deux dernières, donc limiter au rang -3.

    # voyelle préfixe mobile éventuelle
    mobile = "u" if scheme[3] in {"u", "û"} else "i"

    # Dans le schème, les lettres radicales sont symbolisées par des *, sauf si elles sont répétées, auquel cas elles
    # sont symbolisées par leur numéro d'ordre.
    # remplacement des étoiles successives par le rang d'ordre des lettres radicales (pour homogénéiser le traitement
    # des verbes irréguliers) si le n° correspondant est absent :
    if "1" not in scheme:
        scheme = sub(r"\*", "1", scheme, count=1)
    if "2" not in scheme:
        scheme = sub(r"\*", "2", scheme, count=1)
    if "3" not in scheme:
        scheme = sub(r"\*", "3", scheme, count=1)
    if "4" not in scheme:
        scheme = sub(r"\*", "4", scheme, count=1)
    # sauf pour 3, parce que sinon, on a des problèmes si "3" est présent comme lettre radicale...
    # donc on remet un caractère jocker.
    scheme = scheme.replace("3", "µ")

    # NB : on présume que les chiffres sont dans l'ordre avec ce système, un "schème" de type ar-3a2a1a réalise en
    # fait une inversion des lettres - pas malin, mais bon.
    # De même, on peut forcer une lettre faible à une autre valeur par exemple ar-mi**â*ũ peut être forcé sur
    # ar-mi*yâ3ũ quand le W doit se transformer en Y.
    # Les radicales faibles sont w et y. Pour "régulariser" sinon, mettre la radicale faible en majuscule.
    shemeinit = scheme  # sauvegarde de la valeur primitive

    # deuxième radicale
    if (
        racine[2] in {"w", "y"}
        and var
        not in {
            "(2)",
            "(3)",
            "(5)",
            "(6)",
        }  # ces formes sont régulières, cf Schier p.64.
        and scheme != "a12aµu"  # invariant, cf Ryding p. 246.
    ):
        # verbe creux en W, cf Schier p. 71

        position = scheme.find("2")

        # La 2ème radicale a pu être forcée à autre chose.
        if position > -1:
            # contexte de la radicale : quelles sont les voyelles (courtes ou longues) avant et après la consonne 2 :
            contexte = (
                f"{scheme[position-1]}2" if est_voyelle(scheme[position - 1]) else "°2"
            )
            if scheme[position + 1] in {"²", scheme[position]}:
                contexte += "²"
                contexte += (
                    scheme[position + 2] if est_voyelle(scheme[position + 2]) else "°"
                )
            elif est_voyelle(scheme[position + 1]):
                contexte += scheme[position + 1]
            else:
                contexte += "°"

            if contexte == "a2a" and position == 3:
                # la lettre en position +2 est-elle une finale de syllable ?
                if nature(scheme, position + 2)[0] in {"f", "d"}:
                    if racine[2] == "w":
                        scheme = f"{scheme[1:-2]}u{scheme[position+2]}"
                    else:
                        scheme = f"{scheme[1:-2]}i{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-2]}â{scheme[position+2]}"

            elif contexte == "a2a" and position != 3:
                # la lettre en position +2 est-elle une finale de syllable ?
                if nature(scheme, position + 2)[0] == "f":
                    scheme = f"{scheme[1:-2]}a{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-2]}â{scheme[position+2]}"

            # a2i remplacé par â ou i
            elif contexte == "a2i":
                # la lettre en position +2 est-elle une finale de syllable ?
                if nature(scheme, position + 2)[0] in {"f", "d"}:
                    scheme = f"{scheme[1:-2]}i{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-2]}â{scheme[position+2]}"

            # a2u remplacé par â ou u
            elif contexte == "a2u":
                # la lettre en position +2 est-elle une finale de syllable ?
                if nature(scheme, position + 2)[0] in {"f", "d"}:
                    scheme = f"{scheme[1:-2]}u{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-2]}â{scheme[position+2]}"

            # a2î remplacé par âyi dans ar-*a*î*ũ
            elif contexte == "a2î":
                scheme = f"{scheme[1:-2]}âyi{scheme[position+2]}"

            # a2²i remplacé par ay²i dans ar-*a2²i*ũ (ad hoc...) mais pas dans ar-mu*a2²i*ũ (forme 2 invariable)
            elif scheme == "1a2²iµũ":
                # NB : pré-digestions du schème déjà faite
                scheme = f"{scheme[1:-2]}ay²i{scheme[position+2]}"

            # âwi : remplacé par â'i sauf formes verbales 2, 3, 5 et 6
            elif contexte == "â2i":
                scheme = f"{scheme[1:-2]}â'i{scheme[position+2]}"

            # i2° remplacé par î
            elif contexte == "i2°":
                scheme = f"{scheme[1:-2]}î{scheme[position+2]}"

            # iwâ remplacé par iyâ
            elif contexte == "i2â":
                scheme = f"{scheme[1:-2]}iyâ{scheme[position+2]}"

            # uwi (passif) remplacé par î ou i
            elif contexte == "u2i":
                if nature(scheme, position + 2)[0] in {"f", "d"}:
                    scheme = f"{scheme[1:-2]}i{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-2]}î{scheme[position+2]}"

            # °2a : problème à l'impératif pour toutes ces formes : quand l'impératif se termine par
            # la troisième radicale, celle-ci doit fermer la syllabe, et non ouvrir sur une terminaison.
            elif contexte == "°2a":
                # °wa : â si la syllable longue est possible, a sinon
                suite = nature(scheme, position + 2)
                if suite == "ff":
                    scheme = f"{scheme[1:-1]}a{scheme[position+2]}"
                elif suite[0] == "f":
                    scheme = f"{scheme[1:-1]}a{scheme[position+2]}"
                elif suite[0] == "d":
                    scheme = f"{scheme[1:-1]}a{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-1]}â{scheme[position+2]}"

            # °2â : â, et w supprimé
            elif contexte == "°2â":
                # distinction entre le nom verbal de la forme (iv) **â*ũ
                # et le pluriel irrégulier a**â*ũ (régulier) & mi**â*ũ régulier
                if scheme[1] == "a" or scheme[1:2] == "mi":
                    scheme = f"{scheme[1:-1]}wâ{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-1]}â{scheme[position+2]}"

            # °2i : î si la syllable longue est possible, i sinon
            elif contexte == "°2i":
                if nature(scheme, position + 2)[0] == "f":
                    scheme = f"{scheme[1:-1]}i{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-1]}î{scheme[position+2]}"

            # °2u : û si la syllable longue est possible, u sinon
            elif contexte == "°2u":
                if nature(scheme, position + 2)[0] in {"f", "d"}:
                    scheme = f"{scheme[1:-1]}u{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-1]}û{scheme[position+2]}"

            # °2û remplacé par û ou î (participe passif)
            elif contexte == "°2û":
                if racine[2] == "w":
                    scheme = f"{scheme[1:-1]}û{scheme[position+2]}"
                else:
                    scheme = f"{scheme[1:-1]}î{scheme[position+2]}"

            elif contexte == "°û":
                scheme = f"{scheme[1:-1]}û{scheme[position+2]}"

            # voiture balai : on remplace tous les "2" par la lettre radicale :
            scheme = scheme.replace("2", racine[2])

    # première radicale en W
    if racine[1] == "w":
        position = scheme.find("1")
        # La 1ère radicale a pu être forcée à autre chose.
        if position > -1:
            # première forme, suppression du w dans les formes w2i3, sauf dans les verbes sourds (2=3)
            if scheme[position + 2] == "i" and var == "(1)" and racine[2] != racine[3]:
                scheme = f"{scheme[1:-1]}{scheme[position+1]}"
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
    position3 = scheme.find("µ")
    if (
        racine[2] == racine[3]  # deux consonnes identiques
        and racine[2] not in {"*", ".", "?"}  # "lettres" bidon dans les modèles
        and position3
        > -1  # si un petit malin propose un schème sans position 3 en redoublant la 2...
        and scheme != "1a2aµũ"  # exception : doit rester intact.
    ):
        # on est dans un cas "sourd"
        position2 = scheme.find("2")
        if (
            position2 > -1
        ):  # sécurité : exclusion du cas des modèles d'exception imposant la deuxième radicale
            nature2 = nature(scheme, position2)

            # initiale d'une syllabe ouverte, donc 2 porte une voyelle courte et 3 une voyelle.
            if nature2 == "io":
                if est_voyelle(
                    scheme[position2 - 1]
                ):  # ie, la première radicale est vocalisée
                    # alors on peut supprimer la deuxième radicale
                    scheme = f"{scheme[1:position3-2]}{scheme[position3]}"
                else:
                    # sinon on transfère la voyelle de la deuxième radicale sur la première
                    scheme = "".join(
                        [
                            # début jusqu'à la deuxième radicale
                            scheme[1 : position2 - 1],
                            # insertion de la voyelle de la seconde radicale
                            scheme[position3 - 1],
                            # deuxième radicale
                            scheme[position2],
                            # et directement la troisième (le signe de redoublement sera inséré lors
                            # de la translittération en arabe).
                            scheme[position3],
                        ]
                    )

    # fin exclusion de sécurité.

    # Cas des formes sourdes à quatre radicales = idem sur 3 et 4
    position4 = scheme.find("4")
    if (
        racine[4] == racine[3]  # deux consonnes identiques
        and racine[4] not in {"*", ".", "?"}  # "lettres" bidon dans les modèles
        and position4
        > -1  # si un petit malin propose un schème sans position 3 en redoublant la 2...
    ):
        # on est dans un cas "sourd"
        position3 = scheme.find("µ")
        nature3 = nature(scheme, position3)
        # initiale d'une syllabe ouverte, donc 3 porte une voyelle courte et 4 une voyelle.
        if nature3 == "io":
            if est_voyelle(scheme[position3 - 1]):
                # ie, la deuxième radicale est vocalisée
                # alors on peut supprimer la troisième radicale
                scheme = f"{scheme[1:position4-2]}{scheme[position4]}"
            else:
                # sinon on transfère la voyelle de la troisième radicale sur la deuxième
                scheme = "".join(
                    [
                        # début jusqu'à la troisième radicale
                        scheme[1 : position3 - 1],
                        # insertion de la voyelle de la troisième radicale
                        scheme[position4 - 1],
                        # troisième radicale
                        scheme[position3],
                        # et directement la troisième (le signe de redoublement sera inséré lors
                        # de la translittération en arabe).
                        scheme[position4],
                    ]
                )

    # Inversement, les verbes où la troisième radicale est redoublée dans le schème doivent se
    # conjuguer comme des sourds
    # ie, si le schème contient un µµ ou un µ² il faut séparer les deux, et boucher le trou avec un "a".
    if scheme.find("µµ") > -1 or scheme.find("µ²") > -1:
        scheme = sub(r"µ²", "µµ", scheme, count=1)  # homogénéisation des cas
        position3 = scheme.find("µµ")
        if not est_voyelle(scheme[position3 + 2]) or not scheme[position3 + 2]:
            scheme = f"{scheme[1:position3]}a{scheme[position3+1]}"

    scheme = scheme.replace("2", racine[2])

    # Toisième radicale : cas des verbes défectifs
    if racine[3] in {"w", "y"}:
        # préparation du contexte
        position = scheme.find("µ")
        if position > -1:  # La 3ème radicale a pu être forcée à autre chose.
            # contexte de la radicale : quelles sont les voyelles (courtes ou longues) avant et après la consonne 3 :
            contexte += (
                f"{scheme[position-1]}3" if est_voyelle(scheme[position - 1]) else "°3"
            )
            if len(scheme) == position:
                contexte = contexte  # fin de schème
            elif scheme[position + 1] in {"²", scheme[position]}:
                contexte += "²"
                contexte += (
                    scheme[position + 2] if est_voyelle(scheme[position + 2]) else "°"
                )
            elif est_voyelle(scheme[position + 1]):
                contexte += scheme[position + 1]
            else:
                contexte += "°"

            # troisième radicale défective en w
            if racine[3] == "w" and var in {"(1)", ""}:
                # verbe défectif en W, cf Schier p. 74

                if contexte == "a3a":
                    # awa final devient â au prétérit de la première forme, é sinon
                    if position == len(scheme) - 1:
                        # position finale
                        if position == 5 and scheme[2] == "a":  # première forme
                            scheme = f"{scheme[1:position-2]}â{scheme[position+2]}"
                        else:
                            scheme = f"{scheme[1:position-2]}é{scheme[position+2]}"
                    else:
                        scheme = f"{scheme[1:position-2]}a{scheme[position+2]}"

                # test sur première forme
                elif contexte == "a3â":
                    # awâ final devient ayâ au passif devant a3âni final
                    if (
                        position == len(scheme) - 3
                        and scheme[position + 2 : position + 3] == "ni"
                        and (var != "")
                    ):  # les duels ne sont pas concernés.
                        scheme = f"{scheme[1:position-2]}ayâ{scheme[position+2]}"
                    else:
                        scheme = (
                            f"{scheme[1:position-1]}{racine[3]}{scheme[position+1]}"
                        )

                elif contexte == "a3@":
                    scheme = f"{scheme[1:position-2]}â@{scheme[position+2]}"

                elif contexte == "a3î":
                    scheme = f"{scheme[1:position-2]}ay{scheme[position+2]}"

                elif contexte == "a3u":
                    scheme = f"{scheme[1:position-2]}é{scheme[position+2]}"

                elif contexte == "a3û":
                    scheme = f"{scheme[1:position-2]}aw{scheme[position+2]}"

                elif contexte == "a3ũ":
                    # Pb ici, "ã" pour *a*a*ũ, *i*a*ũ et *u*a*ũ, "ãé" sinon. Cf. Palmer §50 p100
                    if shemeinit in {"1a2aµũ", "1i2aµũ", "1u2aµũ"}:
                        scheme = f"{scheme[1:position-2]}ã"
                    else:
                        scheme = f"{scheme[1:position-2]}ãé"

                elif contexte == "a3ã":
                    # Pb ici, "ã" pour *a*a*ũ, *i*a*ũ et *u*a*ũ, "ãé" sinon. Cf. Palmer §50 p100
                    if shemeinit in {"1a2aµã", "1i2aµã", "1u2aµã"}:
                        scheme = f"{scheme[1:position-2]}ã"
                    else:
                        scheme = f"{scheme[1:position-2]}ãé"

                elif contexte == "a3ĩ":
                    # Pb ici, "ã" pour *a*a*ũ, *i*a*ũ et *u*a*ũ, "ãé" sinon. Cf. Palmer §50 p100
                    if shemeinit in {"1a2aµĩ", "1i2aµĩ", "1u2aµĩ"}:
                        scheme = f"{scheme[1:position-2]}ã"
                    else:
                        scheme = f"{scheme[1:position-2]}ãé"

                elif contexte == "â3ũ":
                    # seul cas pratique derrière un â long?
                    scheme = f"{scheme[1:position-2]}â'u"  # diptote dans ce cas

                elif contexte == "a3°":
                    # inaccompli passif (2FP, 3FP) en ay
                    # versus accompli actif en voyelle de l'inaccompli (?) :
                    if scheme[position - 3] == "a":  # on est à l'inaccompli
                        scheme = f"{scheme[1:position-2]}aw{scheme[position+1]}"
                    else:
                        scheme = f"{scheme[1:position-2]}ay{scheme[position+1]}"

                elif contexte == "i3a":
                    scheme = f"{scheme[1:position-2]}iya{scheme[position+2]}"

                elif contexte == "i3@":
                    scheme = f"{scheme[1:position-2]}iy@{scheme[position+2]}"

                elif contexte == "i3i":
                    scheme = f"{scheme[1:position-2]}i{scheme[position+2]}"

                elif contexte == "i3â":
                    scheme = f"{scheme[1:position-2]}iyâ{scheme[position+2]}"

                elif contexte == "i3î":
                    scheme = f"{scheme[1:position-2]}î{scheme[position+2]}"

                elif contexte == "i3ĩ":
                    scheme = f"{scheme[1:position-2]}ĩ{scheme[position+2]}"

                elif contexte == "i3u":
                    scheme = f"{scheme[1:position-2]}iy{scheme[position+2]}"

                elif contexte == "i3û":
                    scheme = f"{scheme[1:position-2]}û{scheme[position+2]}"

                elif contexte == "i3ũ":
                    scheme = f"{scheme[1:position-2]}ĩ{scheme[position+2]}"

                elif contexte == "i3°":
                    scheme = f"{scheme[1:position-2]}î{scheme[position+2]}"

                elif contexte == "u3i":
                    scheme = f"{scheme[1:position-2]}i{scheme[position+2]}"

                elif contexte == "u3î":
                    scheme = f"{scheme[1:position-2]}î{scheme[position+2]}"

                elif contexte == "u3u":
                    # dépend si c'est en fin de mot
                    if position == len(scheme) - 1:
                        scheme = f"{scheme[1:position-2]}îû{scheme[position+2]}"
                    else:
                        scheme = f"{scheme[1:position-2]}u{scheme[position+2]}"

                elif contexte == "u3û":
                    scheme = f"{scheme[1:position-2]}îû{scheme[position+2]}"

                elif contexte == "u3ũ":
                    scheme = f"{scheme[1:position-2]}ĩ{scheme[position+2]}"

                elif contexte == "u3":  # en fin de mot
                    scheme = f"{scheme[1:position-2]}u{scheme[position+1]}"

                elif contexte == "u3°":
                    scheme = f"{scheme[1:position-2]}û{scheme[position+1]}"

                elif (
                    scheme[position - 1] == "y"
                ):  # cas du diminutif en *u*ay*ũ ou *u*ay*@ũ:
                    scheme = f"{scheme[1:position-1]}y{scheme[position+1]}"

                elif contexte == "û3ũ":  # Pb d'écriture
                    scheme = f"{scheme[1:position-2]}uw²ũ{scheme[position+2]}"

                elif contexte == "°3ũ" and scheme[position - 2] == "a":
                    # traitement différent de *a*wũ et *u*wũ - bon, enfin, du moins ça marche :-/
                    scheme = f"{scheme[1:position-1]}wũ{scheme[position+2]}"

                elif contexte in {"°3ũ", "°3ĩ"}:
                    scheme = f"{scheme[1:position-1]}ã{scheme[position+2]}"

                elif contexte == "°3ã" and scheme[position + 2] != "é":
                    scheme = f"{scheme[1:position-1]}ã{scheme[position+2]}"

                # la radicale faible disparaît parfois devant @, mais il faut dans ce cas la supprimer à la main.
                # fin traitement des cas particuliers en w

            else:
                # verbe défectif en Y, cf Schier p. 74
                # ou formes dérivées d'un verbe défectif, traité comme un "y"
                if contexte == "a3a":
                    if position == len(scheme) - 1:  # position finale
                        scheme = f"{scheme[1:position-2]}é{scheme[position+2]}"
                    else:
                        scheme = f"{scheme[1:position-2]}a{scheme[position+2]}"

                elif contexte == "a3â":
                    scheme = f"{scheme[1:position-2]}ayâ{scheme[position+2]}"

                elif contexte == "a3@":
                    scheme = f"{scheme[1:position-2]}â@{scheme[position+2]}"

                elif contexte == "â3@":
                    scheme = f"{scheme[1:position-2]}ây@{scheme[position+2]}"

                elif contexte == "a3î":
                    scheme = f"{scheme[1:position-2]}ay{scheme[position+2]}"

                elif contexte == "a3u":
                    # dépend si c'est en fin de mot
                    if position == len(scheme) - 1:
                        scheme = f"{scheme[1:position-2]}é{scheme[position+2]}"
                    else:
                        scheme = f"{scheme[1:position-2]}ay{scheme[position+2]}"

                elif contexte == "a3û":
                    scheme = f"{scheme[1:position-2]}aw{scheme[position+2]}"

                elif contexte in {"a3ũ", "a3ã", "a3ĩ"}:
                    scheme = f"{scheme[1:position-2]}ãé"

                elif contexte == "â3i":
                    scheme = f"{scheme[1:position-2]}â'i{scheme[position+2]}"
                    # typiquement -*i*â*iy²ũ doit conserver la hamza de -*i*â*ũ

                elif contexte == "â3ũ":
                    scheme = f"{scheme[1:position-2]}â'u"  # diptote dans ce cas

                elif contexte == "a3°":  # ay devant consonne, é en finale
                    scheme = f"{scheme[1:position-2]}ay{scheme[position+1]}"

                elif contexte == "a3":
                    scheme = f"{scheme[1:position-2]}i"

                elif contexte == "i3a":
                    scheme = f"{scheme[1:position-2]}iya{scheme[position+2]}"

                elif contexte == "i3@":
                    scheme = f"{scheme[1:position-2]}iy@{scheme[position+2]}"

                elif contexte == "î3@":
                    scheme = f"{scheme[1:position-2]}îy@{scheme[position+2]}"

                elif contexte == "i3â":
                    scheme = f"{scheme[1:position-2]}iyâ{scheme[position+2]}"

                elif contexte == "i3i":
                    scheme = f"{scheme[1:position-2]}i{scheme[position+2]}"

                elif contexte == "i3î":  # î
                    scheme = f"{scheme[1:position-2]}î{scheme[position+2]}"

                elif contexte == "i3ĩ":
                    scheme = f"{scheme[1:position-2]}ĩ{scheme[position+2]}"

                elif contexte == "i3u":  # dépend si c'est en fin de mot
                    if position == len(scheme) - 1:
                        scheme = f"{scheme[1:position-2]}î{scheme[position+2]}"
                    else:
                        scheme = f"{scheme[1:position-2]}u{scheme[position+2]}"

                elif contexte == "i3û":
                    scheme = f"{scheme[1:position-2]}û{scheme[position+2]}"

                elif contexte == "i3ũ":
                    scheme = f"{scheme[1:position-2]}ĩ"

                elif contexte == "i3°":
                    scheme = f"{scheme[1:position-2]}î{scheme[position+1]}"

                elif contexte == "i3":  # en fin de mot
                    scheme = f"{scheme[1:position-2]}i{scheme[position+1]}"

                elif contexte == "u3ũ":
                    scheme = f"{scheme[1:position-2]}ĩ{scheme[position+2]}"

                elif (contexte == "û3ũ") and scheme[1:3] == "ma1":
                    # contamination du y sur le û dans la forme ma**û*ũ, cf Wright 1874 §170,
                    # mais la 2 est déjà remplacée dans le schème donc on ne peut pas tester le schème d'origine
                    scheme = f"{scheme[1:position-2]}iy²ũ{scheme[position+2]}"

                # fin traitement des cas particuliers en y
            # verbe défectifs

        # 3ème radicale présente

    # verbes défectifs
    # voiture balai :
    scheme = scheme.replace("µ", racine[3])

    # quatrième radicale éventuelle
    # si on applique un schème quadrilittère à une racine à trois consonnes, on redouble simplement la dernière
    scheme = scheme.replace("4", racine[3 if racine[4] == "" else 4])

    # première radicale
    scheme = scheme.replace("1", racine[1])

    # pb : si le schème est en "1°" le "i" prosthétique est virtuel à ce stade :
    # le cas général "de prolongation" ne marche pas, il faut forcer à la main :
    if scheme[1] == "w" and not est_voyelle(scheme[2]):
        scheme = f"î{scheme[2]}"

    # Nettoyage éventuel : Y et W des verbes réguliers
    scheme = scheme.replace("Y", "y").replace("W", "w")

    # Accord des W et Y de prolongation :
    while (position := scheme.find("iw")) > -1:
        if est_voyelle(scheme[position + 2]):
            scheme = f"{scheme[1:position-1]}iW{scheme[1:position+2]}"  # éviter une boucle infinie
        else:
            scheme = f"{scheme[1:position-1]}î{scheme[1:position+2]}"

    while (position := scheme.find("uw")) > -1:
        if est_voyelle(scheme[position + 2]):
            scheme = f"{scheme[1:position-1]}uW{scheme[1:position+2]}"
        else:
            scheme = f"{scheme[1:position-1]}û{scheme[1:position+2]}"

    while (position := scheme.find("uy")) > -1:
        if est_voyelle(scheme[position + 2]):
            scheme = f"{scheme[1:position-1]}uY{scheme[1:position+2]}"
        else:
            scheme = f"{scheme[1:position-1]}û{scheme[1:position+2]}"

    while (position := scheme.find("îy")) > -1:
        scheme = f"{scheme[1:position-1]}iy²{scheme[1:position+2]}"

    while (position := scheme.find("yî")) > -1:
        scheme = f"{scheme[1:position-1]}y²i{scheme[1:position+2]}"

    while (position := scheme.find("û²")) > -1:
        scheme = f"{scheme[1:position-1]}uw²{scheme[1:position+2]}"

    while (position := scheme.find("ûw")) > -1:
        scheme = f"{scheme[1:position-1]}uw²{scheme[1:position+2]}"

    # Re-nettoyage éventuel : Y et W des verbes réguliers
    scheme = scheme.replace("Y", "y").replace("W", "w")

    # ajout d'une voyelle mutable, si le mot commence par deux consonnes :
    if not est_voyelle(scheme[1]) and not est_voyelle(scheme[2]):
        # Consonne en première position et pas de voyelle en deuxième position = il faut rajouter une voyelle préfixe.
        scheme = f"{mobile}{scheme}"

    # ajustement de l'initiale pour les verbes hamzés en 1 : i' se transforme en î et u' en û
    # (une même syllabe ne peut pas être à la fois ouverte et fermée par une hamza)
    if scheme[1:2] == "i'":
        scheme = f"iy{scheme[3]}" if est_voyelle(scheme[3]) else f"î{scheme[3]}"
    if scheme[1:2] == "u'":
        scheme = f"uw{scheme[3]}" if est_voyelle(scheme[3]) else f"û{scheme[3]}"
    if scheme[1:2] == "a'":
        scheme = f"aw{scheme[3]}" if est_voyelle(scheme[3]) else f"â{scheme[3]}"

    # ajustement pour les verbes assimilés en y
    if (position := scheme.find("uy")) > -1:
        if not est_voyelle(scheme[position + 2]):
            scheme = f"{scheme[1:position-1]}û{scheme[1:position+2]}"

    return scheme, var
