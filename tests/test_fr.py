import pytest

from scripts.get import parse_word
from scripts.utils import clean


@pytest.mark.parametrize(
    "word, pronunciations, genre, etymology, definitions, variants",
    [
        (
            "a",
            ["ɑ", "a"],
            "m",
            "",
            [
                "<i>(Linguistique)</i> Symbole de l’alphabet phonétique international pour la voyelle (ou vocoïde) ouverte antérieure non arrondie.",  # noqa
                "<i>(Métrologie)</i> Symbole du Système international (SI) pour le préfixe atto- (&times;10<sup>&minus;18</sup>).",  # noqa
                "<i>(Métrologie)</i> Symbole de l’are, une unité de surface non SI. Elle prend souvent le préfixe h pour former ha (hectare).",  # noqa
                "<i>(Métrologie)</i> Symbole (dérivé du système SI) de l’année (365,25 jours de 86,4 ks), du latin <i>annum</i>.",  # noqa
                "Première lettre et première voyelle de l’alphabet français.",
                r"Le son \a\ ou \ɑ\ de cette lettre. <b>Note :</b> Le français parisien a perdu la distinction entre les deux.",  # noqa
                "<i>(Familier)</i> Pronom personnel (indéterminé en genre et en personne : première, deuxième ou troisième).",  # noqa
                "<i>(Québec)</i> <i>(Familier)</i> Elle.",
            ],
            [],
        ),
        (
            "π",
            ["p"],
            "",
            "",
            [
                "<i>(Mathématiques)</i> Symbole représentant le rapport constant entre la circonférence d’un cercle et son diamètre, aussi appelé en français la <i>constante d’Archimède</i>.",  # noqa
                "<i>(Bases de données)</i> Symbole de la projection.",
            ],
            [],
        ),
        (
            "42",
            ["ka.ʁɑ̃t.dø"],
            "msing",
            "",
            [
                "Numéral en chiffres arabes du nombre quarante-deux, en notation décimale. Selon la base utilisée, ce numéral peut représenter d’autres nombres. En notation hexadécimale, par exemple, ce numéral représente le nombre soixante-six ; en octal, le nombre trente-quatre.",  # noqa
                "<i>(Par ellipse)</i> <i>(Dans la plupart des langues)</i> Une année qui se termine par <b>42</b>.",
                "Quarante-deux.",
                "<i>(Par ellipse)</i> Une année qui se termine par <b>42</b>.",
                "<i>(France)</i> <i>(Familier)</i> Habitant du département de la Loire.",
                "<i>(France)</i> Département de la Loire.",
            ],
            [],
        ),
        (
            "accueil",
            ["a.kœj"],
            "m",
            "<i>(XII<sup>e</sup> siècle)</i> Déverbal de <i>accueillir</i>.",
            [
                "Cérémonie ou prestation réservée à un nouvel arrivant, consistant généralement à lui souhaiter la bienvenue et à l’aider dans son intégration ou ses démarches.",  # noqa
                "Lieu où sont accueillies les personnes.",
                "<i>(Vieilli)</i> Fait d’accueillir ou héberger.",
                "Page d’accès ou d’accueil (lieu ci-dessus) à un site web.",
                "Manière dont une œuvre a été acceptée lors de sa sortie par le public et les critiques.",
            ],
            [],
        ),
        (
            "acrologie",
            ["a.kʁɔ.lɔ.ʒi"],
            "f",
            "Du grec ancien ἄκρος, <i>akros</i> («&nbsp;extrémité&nbsp;»), voir <i>acro-</i>, avec le suffixe <i>-logie</i>.",  # noqa
            [
                "<i>(Linguistique)</i> <i>(Rare)</i> Système graphique qui consiste à peindre, pour représenter les idées, l’image des objets dont le nom commence par la même lettre que celui par lequel ces idées sont exprimées dans le langage ordinaire.",  # noqa
                "<i>(Linguistique)</i> <i>(Par extension)</i> <i>(Rare)</i> Se dit lorsque deux termes commencent par la même lettre et qu’ils sont apparentés par le sens.",  # noqa
                "<i>(Philosophie)</i> <i>(Très rare)</i> Recherche ou exposition des principes suprêmes, ou du mieux absolu.",  # noqa
                "<i>(Sport)</i> Étude ou pratique de l’acrobatie.",
            ],
            [],
        ),
        (
            "aux",
            ["o"],
            "mf",
            "",
            [
                "<i>(Linguistique)</i> Code ISO 639-3 de l’aurá.",
                "<i>Contraction obligatoire de la préposition </i>à<i> et de l'article défini </i>les<i>.</i>",
            ],
            [],
        ),
        (
            "base",
            ["bɑz"],
            "f",
            "<i>(Date à préciser)</i> Du latin <i>basis</i> («&nbsp;id.&nbsp;»), du grec ancien βάσις, <i>básis</i> («&nbsp;marche&nbsp;»).",  # noqa
            [
                "Partie inférieure d’un corps quelconque qui lui sert de soutien.",
                "<i>(En particulier)</i> <i>(Architecture)</i> Ce qui soutient le fût de la colonne.",
                "<i>(Héraldique)</i> Désigne le piédestal d’une colonne surtout quand il est d’un émail différent de la colonne.",  # noqa
                "<i>(Mathématiques)</i>",
                (
                    "<i>(Géométrie)</i> Surface sur laquelle on conçoit que certains corps solides sont appuyés.",
                    (
                        "<i>(Par extension)</i> Côté du triangle opposé à l’angle qui est regardé comme le sommet.",
                        "Côté d’une figure géométrique naturellement choisi comme côté principal.",
                    ),
                    "<i>(Algèbre)</i> Famille libre de vecteurs, génératrice d’un espace vectoriel.",
                    "<i>(Analyse réelle)</i> Nombre réel élevé à une puissance variable.",
                    "<i>(Arithmétique)</i> Nombre de chiffres utilisé pour dénombrer.",
                ),
                "<i>(Par analogie)</i> <i>(Botanique)</i> <i>(Anatomie)</i> Côté opposé à la partie la plus pointue d’un organe.",  # noqa
                "<i>(Géodésie)</i> Côté initial mesuré directement sur le terrain.",
                "<i>(Militaire)</i> Ensemble des points de ravitaillement avec lesquels une armée en campagne se tient en relations constantes.",  # noqa
                "<i>(Marine)</i> Port de ravitaillement ou de refuge des navires en temps de guerre.",  # noqa
                "<i>(Chimie)</i> Toute matière qui a la propriété de réagir aux acides et de les neutraliser, du moins en partie. Solution ayant un pH supérieur à 7.",  # noqa
                "<i>(Médecine)</i> Ce qui entre comme ingrédient principal dans un mélange.",
                "<i>(Télécommunications)</i> Appareil relié à une ligne fixe permettant le fonctionnement de téléphones sans fil à usage domestique.",  # noqa
                "<i>(Électronique)</i> Nom d’une des électrodes d’un transistor bipolaire.",
                "<i>(Baseball)</i> Une des trois zones où le coureur peut rester sans être mis hors jeu.",  # noqa
                "<i>(Sports hippiques)</i> Cheval ou groupe de chevaux que l’on retient dans toutes ses combinaisons de paris hippiques pour une course donnée, car on estime qu’ils ont de très bonnes chances de figurer parmi les premiers.",  # noqa
                "<i>(Politique)</i> Ensemble des électeurs, des soutiens d’un politique ou d’un parti.",
                "<i>(Figuré)</i> Ce qui est le principe, la donnée fondamentale d’une chose ou ce sur quoi elle repose.",  # noqa
            ],
            [],
        ),
        (
            "Bogotanais",
            ["bɔ.ɡɔ.ta.nɛ"],
            "m",
            "Du nom Bogota avec le préfixe -ais.",
            [],
            [],
        ),
        (
            "colligeait",
            ["kɔ.li.ʒɛ"],
            "",
            "",
            [],
            ["colliger"],
        ),
        (
            "corps portant",
            ["kɔʁ pɔʁ.tɑ̃"],
            "m",
            "Locution composée de <i>corps</i> et de <i>portant</i>.",
            [
                "<i>(Astronautique)</i> Aéronef à fuselage porteur, sur lequel la portance est produite par le fuselage, destiné aux usages spatiaux ou hypersoniques, afin de limiter l'effet de traînée ou la surface de friction.",  # noqa
                "<i>(Astronautique)</i> <i>(Aérodynamique)</i> Engin aérospatial possédant, à vitesse hypersonique, une portance qui lui assure une bonne manœuvrabilité lors de la rentrée atmosphérique.",  # noqa
            ],
            [],
        ),
        (
            "DES",
            [],
            "m",
            "<i>(Commerce international)</i> <i>(1936)</i> Terme créé par la Chambre de commerce internationale. Sigle de l’anglais <i>delivered ex ship</i>; « rendu par navire ».",  # noqa
            [
                "<i>(Aviation)</i> Code AITA de l’aéroport de Desroches, aux Seychelles.",
                "<i>(Commerce international)</i> Incoterm qui signifie que le vendeur a dûment livré sa marchandise dès lors que celle-ci, dédouanée à l’exportation et non à l’importation, est mise à disposition de l’acheteur à bord du navire, au port de destination convenu. Les frais de déchargement sont à la charge de l’acheteur.",  # noqa
                "<i>(Biochimie)</i> Diéthylstilbestrol, un œstrogène de synthèse, source de graves complications chez les filles de ses utilisatrices.",  # noqa
                "<i>(Québec)</i> Diplôme d’études secondaires, un diplôme obtenu après cinq années d’études secondaires au Québec ; anciennement <i>Certificat d’études secondaires</i> (CES ou CÉS).",  # noqa
                "<i>(France)</i> Diplôme d’études spécialisées, un diplôme de troisième cycle médical, pharmaceutique, vétérinaire ou odontologique en France, d’une durée de 3 à 5 ans correspondant à l’Internat.",  # noqa
                "<i>(Belgique)</i> Diplôme d’études spécialisées, un diplôme de troisième cycle universitaire en Belgique.",  # noqa
                "<i>(France)</i> Diplôme d’études supérieures, un diplôme français.",
                "<i>(Mathématiques)</i> Décomposition en éléments simples, une méthode de calcul mathématique.",  # noqa
            ],
            [],
        ),
        (
            "dubitatif",
            [],
            "",
            "Du latin <i>dubitativus</i>.",
            [
                "Qui sert à exprimer le doute.",
                "Qui éprouve un doute.",
            ],
            [],
        ),
        (
            "effluve",
            ["e.flyv"],
            "mf",
            "Du latin <i>effluvium</i>, du préfixe <i>ex-</i> indiquant la séparation et de <i>fluxus</i> (« écoulement »).",  # noqa
            [
                "<i>(Médecine)</i> <i>(Vieilli)</i> Substances organiques altérées, tenues en suspension dans l’air, principalement aux endroits marécageux, et donnant particulièrement lieu à des fièvres intermittentes, rémittentes et continues.",  # noqa
                "Émanation qui se dégage d’un corps quelconque.",
            ],
            [],
        ),
        (
            "employer",
            ["ɑ̃.plwa.je"],
            "",
            "Du latin <i>implico</i> («&nbsp;impliquer&nbsp;»).",
            [
                "Utiliser ; user ; se servir de.",
                "<i>(Spécialement)</i> <i>(Grammaire)</i> S’en servir en parlant ou en écrivant, en parlant d'une phrase, d'un mot ou d'une locution.",  # noqa
                "Pourvoir d’une occupation ou d’un travail pour son usage ou pour son profit.",
            ],
            [],
        ),
        (
            "encyclopædie",
            ["ɑ̃.si.klɔ.pe.di"],
            "f",
            "→ voir <i>encyclopédie</i>",
            ["<i>(Archaïsme)</i> Variante orthographique de encyclopédie."],
            [],
        ),
        (
            "éperon",
            ["e.pʁɔ̃"],
            "m",
            "De l’ancien français <i>esperon</i>, du vieux-francique *<i>sporo</i>.",
            [
                "<i>(Équitation)</i> Pièce de métal à deux branches, qui s’adapte au talon du cavalier et dont l’extrémité pointue ou portant une molette sert à piquer les flancs du cheval pour le stimuler.",  # noqa
                "<i>(Botanique)</i> Prolongement en forme de tube de la corolle ou du calice (ne concerne parfois qu’un pétale ou sépale particulier).",  # noqa
                "<i>(Marine)</i> Partie de la proue d’un bâtiment qui se termine en pointe et qui a plus ou moins de saillie en avant.",  # noqa
                "<i>(Maçonnerie)</i>",
                (
                    "Sorte de fortification en angle saillant qu’on élève au milieu des courtines, ou devant des portes, pour les défendre.",  # noqa
                    "Ouvrage en pointe qui sert à rompre le cours de l’eau, devant les piles des ponts, ou sur les bords des rivières.",  # noqa
                    "Tout pilier qu’on construit extérieurement d’un mur de terrasse de distance en distance, et qui se lie avec le corps du mur pour tenir la poussée des terres (Contrefort, anciennement contre-fort).",  # noqa
                ),
                "<i>(Géographie)</i> Partie d’un contrefort, d’une chaîne de collines ou de montagnes qui se termine en pointe.",  # noqa
                "<i>(Héraldique)</i> Meuble représentant l’objet du même nom dans les armoiries. Il est composé d’une branche en métal en U avec une tige au bout de laquelle se trouve une molette à six rais mais le nombre peut varier d'un illustrateur à l’autre. Il est représenté en pal, la molette vers le chef (haut). Dans les représentations anciennes, il est parfois muni d’une sangle en cuir. À rapprocher de molette d’éperon.",  # noqa
            ],
            [],
        ),
        (
            "greffier",
            ["ɡʁɛ.fje", "ɡʁe.fje"],
            "m",
            "(<i>Nom commun 1</i>) <i>(Date à préciser)</i> Du latin <i>graphiarius</i> («&nbsp;d’écriture, de style, de poinçon&nbsp;») ou dérivé de <i>greffe</i> avec le suffixe <i>-ier</i>.",  # noqa
            [
                "<i>(Droit)</i> Officier public préposé au greffe.",
                "<i>(Figuré)</i> Celui qui prend note et tient le registre de ses notes.",
                "<i>(Populaire)</i> Chat.",
                "Poisson-chat commun (poisson).",
            ],
            [],
        ),
        (
            "ich",
            ["ɪç"],
            "",
            "",
            ["<i>(Linguistique)</i> Code ISO 639-3 de l’etkywan."],
            [],
        ),
        (
            "koro",
            ["kɔʁo"],
            "m",
            "",
            [
                "Langue tibéto-birmane parlée dans l’Arunachal Pradesh (Inde)",
                "Langue malayo-polynésienne parlée dans les îles de l'Amirauté (Papouasie-Nouvelle-Guinée)",
                "Forme d'hystérie de nature sexuelle propre aux humains mâles.",
            ],
            [],
        ),
        (
            "mutiner",
            ["my.ti.ne"],
            "",
            "Dénominal de <i>mutin</i>.",
            [
                "Se porter à la sédition, à la révolte.",
                "Enfant qui se dépite et manque à l’obéissance.",
                "<i>(Poétique)</i> …",
            ],
            [],
        ),
        (
            "naguère",
            ["na.ɡɛʁ"],
            "",
            "De <i>il n’y a guère</i> (de temps). Voir aussi <i>na</i>.",
            [
                "Récemment ; il y a peu.",
                "Il y a longtemps. <b>Note :</b> contrairement à l’étymologie qui implique un temps passé récent, l’usage moderne consacre le sens d’un temps antérieur, lointain, révolu.",  # noqa
            ],
            [],
        ),
        (
            "pinyin",
            ["pin.jin"],
            "m",
            "<i>(Nom 1)</i> (Vers 1950) Du chinois 拼音, <i>pīnyīn</i>, formé de 拼 <i>pīn</i> (« épeler ») et de 音 <i>yīn</i> (« son »), donc « épeler les sons ».",  # noqa
            [
                "Système de transcription de la langue chinoise, permettant de romaniser les sons des sinogrammes, et d’indiquer le ton utilisé lors de la prononciation.",  # noqa
                "Langue bantoïde parlée dans la Région du Nord-Ouest au Cameroun.",
            ],
            [],
        ),
        (
            "précepte",
            ["pʁe.sɛpt"],
            "m",
            "Emprunté au latin <i>praeceptum</i> («&nbsp;précepte, leçon, règle&nbsp;»), dérivé de <i>praecipere</i> signifiant « prendre avant, prendre le premier » ou encore « recommander », « conseiller », « prescrire ».",  # noqa
            [
                "Règle ; leçon ; enseignement.",
                "<i>(Philosophie)</i> Ce qui ne peut pas ne pas être autrement.",
                "<i>(Religion)</i> Commandement et, surtout, commandement de Dieu, ou commandement de l’Église, etc.",
            ],
            [],
        ),
        (
            "rance",
            ["ʁɑ̃s"],
            "mf",
            "Du latin <i>rancidus</i> par l’intermédiaire de l’ancien occitan.",
            [
                "Se dit des corps gras qui, laissés au contact de l’air, ont pris une odeur forte et un goût désagréable.",  # noqa
                "S’emploie quelquefois comme nom masculin.",
                "Variante de ranche.",
            ],
            [],
        ),
        (
            "sapristi",
            ["sa.pʁis.ti"],
            "",
            "Déformation de <i>sacristi</i>, afin de ne pas blasphémer ouvertement.",
            ["Pour marquer l’étonnement."],
            [],
        ),
        (
            "silicone",
            ["si.li.kon"],
            "f",
            "<i>(1863)</i> De l’allemand <i>Silikon</i>, mot créé par Friedrich Wöhler et, pour les équivalents français du mot allemand, dérivé de <i>silicium</i> avec le suffixe <i>-one</i>.",  # noqa
            [
                "<i>(Chimie)</i> Composé inorganique formés d’une chaine silicium-oxygène (…-Si-O-Si-O-Si-O-…) sur laquelle des groupes se fixent, sur les atomes de silicium.",  # noqa
            ],
            [],
        ),
        (
            "suis",
            ["sɥi"],
            "",
            "<i>(Forme de verbe 1)</i> De l’ancien français <i>suis</i> (forme du verbe <i>estre</i>), lui-même issu du latin <i>sum</i> (forme du verbe <i>esse</i>).",  # noqa
            [],
            ["être", "suivre"],
        ),
    ],
)
def test_parse_word(
    word, pronunciations, genre, etymology, definitions, variants, page
):
    """Test the sections finder and definitions getter."""
    code = page(word, "fr")
    details = parse_word(word, code, "fr", force=True)
    assert pronunciations == details.pronunciations
    assert genre == details.genre
    assert definitions == details.definitions
    assert etymology == details.etymology
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{adj-indéf-avec-de}}", "<i>(Avec de)</i>"),
        ("{{ancre|sens_sexe}}", ""),
        ("{{emploi|au passif}}", "<i>(Au passif)</i>"),
        ("{{cf}}", "→ voir"),
        ("{{cf|immortelle}}", "→ voir <i>immortelle</i>"),
        ("{{cf|lang=fr|faire}}", "→ voir <i>faire</i>"),
        ("{{cf|triner|lang=fr}}", "→ voir <i>triner</i>"),
        ("{{cf|lang=fr|in-|extinguible}}", "→ voir <i>in-</i> et <i>extinguible</i>"),
        ("{{circa|1150}}", "<i>(c. 1150)</i>"),
        ("{{couleur|#B0F2B6}}", "[RGB #B0F2B6]"),
        ("du XX{{e}} siècle", "du XX<sup>e</sup> siècle"),
        (
            "{{étyl|grc|fr|mot=ἄκρος|tr=akros|sens=extrémité}}",
            "grec ancien ἄκρος, <i>akros</i> («&nbsp;extrémité&nbsp;»)",
        ),
        ("{{divinités|fr|grecques}}", "<i>(Divinité)</i>"),
        ("{{info lex|boulangerie}}", "<i>(Boulangerie)</i>"),
        ("{{info lex|équitation|sport}}", "<i>(Équitation, Sport)</i>"),
        ("[[J·K-1|'''J·K{{e|-1}}''']]", "<b>J·K<sup>-1</sup></b>"),
        ("{{FR|fr}}", "<i>(France)</i>"),
        ("{{graphie|u}}", "‹&nbsp;u&nbsp;›"),
        ("{{lang|en|other rank}}", "other rank"),
        ("{{Lang|la|[[Martis]] [[dies]]}}", "Martis dies"),
        ("{{langues|fr|de Chine}}", "<i>(Linguistique)</i>"),
        ("{{lexique|philosophie|fr}}", "<i>(Philosophie)</i>"),
        ("{{lexique|philosophie|sport|fr}}", "<i>(Philosophie, Sport)</i>"),
        ("{{lien|étrange|fr}}", "étrange"),
        ("{{lien|D{{e}}}}", "D<sup>e</sup>"),
        ("{{ling|fr}}", "<i>(Linguistique)</i>"),
        ("{{in|5}}", "<sub>5</sub>"),
        ("{{instruments à cordes|fr}}", "<i>(Musique)</i>"),
        ("{{musiciens|fr}}", "<i>(Musique)</i>"),
        ("{{nobr|1 000 000 000 000}}", "1&nbsp;000&nbsp;000&nbsp;000&nbsp;000"),
        ("{{nobr|ℶ₀ {{=}} [[ℵ₀]]}}", "ℶ₀&nbsp;=&nbsp;ℵ₀"),
        ("{{nobr|1=ℶ₀ = [[ℵ₀]]}}", "ℶ₀&nbsp;=&nbsp;ℵ₀"),
        ("{{nobr|a {{!}} b}}", "a&nbsp;|&nbsp;b"),
        ("{{nombre romain|12}}", "XII"),
        ("{{par ext}} ou {{figuré|fr}}", "<i>(Par extension)</i> ou <i>(Figuré)</i>"),
        ("{{région}}", "<i>(Régionalisme)</i>"),
        ("{{pron|zjø|fr}}", "\\zjø\\"),
        ("{{pron-API|/j/}}", "/j/"),
        ("{{recons|lang-mot-vedette=fr|sporo|lang=frk|sc=Latn}}", "*<i>sporo</i>"),
        ("{{région|Lorraine et Dauphiné}}", "<i>(Lorraine et Dauphiné)</i>"),
        ("{{réf}}", ""),
        ("{{smo}}", "samoan"),
        ("{{sport}}", "<i>(Sport)</i>"),
        ("{{sport|fr|collectif}}", "<i>(Sport collectif)</i>"),
        ("{{trad+|conv|Sitophilus granarius}}", "Sitophilus granarius"),
        (
            "{{variante ortho de|acupuncture|fr}}",
            "Variante orthographique de acupuncture",
        ),
        (
            "{{variante orthographique de|acupuncture|fr}}",
            "Variante orthographique de acupuncture",
        ),
        ("{{W|Jacques Brandenberger}}", "Jacques Brandenberger"),
        ("{{w|lang=en|The Little Prince}}", "The Little Prince"),
        ("{{w|Li Ptit Prince (roman)|Li Ptit Prince|lang=wa}}", "Li Ptit Prince"),
        (
            "{{wp|Sarcoscypha coccinea}}",
            "<i>Sarcoscypha coccinea sur l'encyclopédie Wikipedia</i>",
        ),
        ("{{ws|Bible Segond 1910/Livre de Daniel|Livre de Daniel}}", "Livre de Daniel"),
        (
            "{{ws|Les Grenouilles qui demandent un Roi}}",
            "Les Grenouilles qui demandent un Roi",
        ),
        ("{{wsp|Panthera pardus|''Panthera pardus''}}", "<i>Panthera pardus</i>"),
        ("{{wsp|Brassicaceae}}", "Brassicaceae"),
        ("{{WSP|Panthera leo}}", "<i>(Panthera leo)</i>"),
        # Complex one: the "chambre" etymology
        (
            "{{siècle|lang=fr|XI}} Du {{étyl|frm|fr|chambre}}<ref>{{R:DMF}}</ref>, de l’{{étyl|fro|fr|chambre}}, {{lien|''cambre''|fro}}, {{lien|''cambra''|fro}}<ref>{{R:DÉCT}}</ref>{{,}}{{R|TLFi}}, du {{étyl|bas latin|fr|mot=camera|sens=pièce, chambre}}{{R|TLFi}}, du {{étyl|latin classique|fr|mot=camera}}{{R|TLFi}}, {{lien|''camara''|sens=voute, plafond vouté|la}}, du {{étyl|grc|fr|mot=καμάρα|tr=kamárā|sens=voute, lieu couvert par une construction}}{{R|TLFi}}.",  # noqa
            "<i>(XI<sup>e</sup> siècle)</i> Du moyen français <i>chambre</i>, de l’ancien français <i>chambre</i>, <i>cambre</i>, <i>cambra</i>, du bas latin <i>camera</i> («&nbsp;pièce, chambre&nbsp;»), du latin classique <i>camera</i>, <i>camara</i> («&nbsp;voute, plafond vouté&nbsp;»), du grec ancien καμάρα, <i>kamárā</i> («&nbsp;voute, lieu couvert par une construction&nbsp;»).",  # noqa
        ),
    ],
)
def test_clean_template(wikicode, expected):
    """Test templates handling."""
    assert clean("foo", wikicode, "fr") == expected
