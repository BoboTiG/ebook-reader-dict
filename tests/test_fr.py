import pytest

from scripts.get import parse_word
from scripts.utils import clean


@pytest.mark.parametrize(
    "word, pronunciation, genre, definitions",
    [
        (
            "42",
            "ka.ʁɑ̃t.dø",
            "msing",
            [
                "Numéral en chiffres arabes du nombre quarante-deux, en notation décimale. Selon la base utilisée, ce numéral peut représenter d’autres nombres. En notation hexadécimale, par exemple, ce numéral représente le nombre soixante-six ; en octal, le nombre trente-quatre.",  # noqa
                "<i>(Par ellipse)</i> <i>(Dans la plupart des langues)</i> Une année qui se termine par <b>42</b>.",
                "Quarante-deux.",
                "<i>(Par ellipse)</i> Une année qui se termine par <b>42</b>.",
                "<i>(France)</i> <i>(Familier)</i> Habitant du département de la Loire.",
            ],
        ),
        (
            "accueil",
            "a.kœj",
            "m",
            [
                "Cérémonie ou prestation réservée à un nouvel arrivant, consistant généralement à lui souhaiter la bienvenue et à l’aider dans son intégration ou ses démarches.",  # noqa
                "Lieu où sont accueillies les personnes.",
                "<i>(Vieilli)</i> Fait d’accueillir ou héberger.",
                "Page d’accès ou d’accueil (lieu ci-dessus) à un site web.",
                "Manière dont une œuvre a été acceptée lors de sa sortie par le public et les critiques.",
            ],
        ),
        (
            "acrologie",
            "a.kʁɔ.lɔ.ʒi",
            "f",
            [
                "<i>(Linguistique)</i> <i>(Rare)</i> Système graphique qui consiste à peindre, pour représenter les idées, l’image des objets dont le nom commence par la même lettre que celui par lequel ces idées sont exprimées dans le langage ordinaire.",  # noqa
                "<i>(Linguistique)</i> <i>(Par extension)</i> <i>(Rare)</i> Se dit lorsque deux termes commencent par la même lettre et qu’ils sont apparentés par le sens.",  # noqa
                "<i>(Philosophie)</i> <i>(Très rare)</i> Recherche ou exposition des principes suprêmes, ou du mieux absolu.",  # noqa
                "<i>(Sport)</i> Étude ou pratique de l’acrobatie.",
            ],
        ),
        (
            "aux",
            "o",
            "mf",
            [
                "<i>(Linguistique)</i> Code ISO 639-3 de l’aurá.",
                "<i>Contraction obligatoire de la préposition </i>à<i> et de l'article défini </i>les<i>.</i>",
            ],
        ),
        (
            "base",
            "bɑz",
            "f",
            [
                "Partie inférieure d’un corps quelconque qui lui sert de soutien.",
                "<i>(En particulier)</i> <i>(Architecture)</i> Ce qui soutient le fût de la colonne.",
                "<i>(Héraldique)</i> Désigne le piédestal d’une colonne surtout quand il est d’un émail différent de la colonne.",  # noqa
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
        ),
        ("Bogotanais", "bɔ.ɡɔ.ta.nɛ", "m", []),
        (
            "corps portant",
            "kɔʁ pɔʁ.tɑ̃",
            "m",
            [
                "<i>(Astronautique)</i> Aéronef à fuselage porteur, sur lequel la portance est produite par le fuselage, destiné aux usages spatiaux ou hypersoniques, afin de limiter l'effet de traînée ou la surface de friction.",  # noqa
                "<i>(Astronautique)</i> <i>(Aérodynamique)</i> Engin aérospatial possédant, à vitesse hypersonique, une portance qui lui assure une bonne manœuvrabilité lors de la rentrée atmosphérique.",  # noqa
            ],
        ),
        (
            "DES",
            "",
            "m",
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
        ),
        (
            "employer",
            "ɑ̃.plwa.je",
            "",
            [
                "Utiliser ; user ; se servir de.",
                "<i>(Spécialement)</i> <i>(Grammaire)</i> S’en servir en parlant ou en écrivant, en parlant d'une phrase, d'un mot ou d'une locution.",  # noqa
                "Pourvoir d’une occupation ou d’un travail pour son usage ou pour son profit.",
            ],
        ),
        (
            "encyclopædie",
            "ɑ̃.si.klɔ.pe.di",
            "f",
            ["<i>(Archaïsme)</i> Variante orthographique de encyclopédie."],
        ),
        (
            "éperon",
            "e.pʁɔ̃",
            "m",
            [
                "<i>(Équitation)</i> Pièce de métal à deux branches, qui s’adapte au talon du cavalier et dont l’extrémité pointue ou portant une molette sert à piquer les flancs du cheval pour le stimuler.",  # noqa
                "<i>(Botanique)</i> Prolongement en forme de tube de la corolle ou du calice (ne concerne parfois qu’un pétale ou sépale particulier).",  # noqa
                "<i>(Marine)</i> Partie de la proue d’un bâtiment qui se termine en pointe et qui a plus ou moins de saillie en avant.",  # noqa
                "<i>(Géographie)</i> Partie d’un contrefort, d’une chaîne de collines ou de montagnes qui se termine en pointe.",  # noqa
                "<i>(Héraldique)</i> Meuble représentant l’objet du même nom dans les armoiries. Il est composé d’une branche en métal en U avec une tige au bout de laquelle se trouve une molette à six rais mais le nombre peut varier d'un illustrateur à l’autre. Il est représenté en pal, la molette vers le chef (haut). Dans les représentations anciennes, il est parfois muni d’une sangle en cuir. À rapprocher de molette d’éperon.",  # noqa
            ],
        ),
        (
            "greffier",
            "ɡʁɛ.fje",
            "m",
            [
                "<i>(Droit)</i> Officier public préposé au greffe.",
                "<i>(Figuré)</i> Celui qui prend note et tient le registre de ses notes.",
                "<i>(Populaire)</i> Chat.",
                "Poisson-chat commun (poisson).",
            ],
        ),
        ("ich", "ɪç", "", ["<i>(Linguistique)</i> Code ISO 639-3 de l’etkywan."]),
        (
            "mutiner",
            "my.ti.ne",
            "",
            [
                "Se porter à la sédition, à la révolte.",
                "Enfant qui se dépite et manque à l’obéissance.",
            ],
        ),
        (
            "naguère",
            "na.ɡɛʁ",
            "",
            [
                "Récemment ; il y a peu.",
                "Il y a longtemps. <b>Note :</b> contrairement à l’étymologie qui implique un temps passé récent, l’usage moderne consacre le sens d’un temps antérieur, lointain, révolu.",  # noqa
            ],
        ),
        (
            "pinyin",
            "pin.jin",
            "m",
            [
                "Système de transcription de la langue chinoise, permettant de romaniser les sons des sinogrammes, et d’indiquer le ton utilisé lors de la prononciation.",  # noqa
                "Langue bantoïde parlée dans la Région du Nord-Ouest au Cameroun.",
            ],
        ),
        (
            "précepte",
            "pʁe.sɛpt",
            "m",
            [
                "Règle ; leçon ; enseignement.",
                "<i>(Philosophie)</i> Ce qui ne peut pas ne pas être autrement.",
                "<i>(Religion)</i> Commandement et, surtout, commandement de Dieu, ou commandement de l’Église, etc.",
            ],
        ),
        (
            "rance",
            "ʁɑ̃s",
            "mf",
            [
                "Se dit des corps gras qui, laissés au contact de l’air, ont pris une odeur forte et un goût désagréable.",  # noqa
                "S’emploie quelquefois comme nom masculin.",
                "Variante de ranche.",
            ],
        ),
        ("sapristi", "sa.pʁis.ti", "", ["Pour marquer l’étonnement."]),
        (
            "silicone",
            "si.li.kon",
            "f",
            [
                "<i>(Chimie)</i> Composé inorganique formés d’une chaine silicium-oxygène (…-Si-O-Si-O-Si-O-…) sur laquelle des groupes se fixent, sur les atomes de silicium.",  # noqa
            ],
        ),
        ("suis", "sɥi", "", []),
    ],
)
def test_parse_word(word, pronunciation, genre, definitions, page):
    """Test the pronunciation, genre and definitions finder."""
    code = page(word, "fr")
    details = parse_word(word, code, "fr", force=True)
    assert pronunciation == details[0]
    assert genre == details[1]
    assert definitions == details[2]


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{adj-indéf-avec-de}}", "<i>(Avec de)</i>"),
        ("{{ancre|sens_sexe}}", ""),
        ("{{date|1957}}", "<i>(1957)</i>"),
        ("{{date|1957-2057}}", "<i>(1957-2057)</i>"),
        ("{{emploi|au passif}}", "<i>(Au passif)</i>"),
        ("{{cf|immortelle}}", "→ voir immortelle"),
        ("{{cf|lang=fr|faire}}", "→ voir faire"),
        ("{{couleur|#B0F2B6}}", "[RGB #B0F2B6]"),
        ("du XX{{e}} siècle", "du XX<sup>e</sup> siècle"),
        ("[[J·K-1|'''J·K{{e|-1}}''']]", "<b>J·K<sup>-1</sup></b>"),
        ("{{FR|fr}}", "<i>(France)</i>"),
        ("{{lien|étrange|fr}}", "étrange"),
        ("{{lien|D{{e}}}}", "D<sup>e</sup>"),
        ("{{ling|fr}}", "<i>(Linguistique)</i>"),
        ("{{in|5}}", "<sub>5</sub>"),
        ("{{nombre romain|12}}", "XII"),
        ("{{par ext}} ou {{figuré|fr}}", "<i>(Par extension)</i> ou <i>(Figuré)</i>"),
        ("{{région}}", "<i>(Régionalisme)</i>"),
        ("{{région|Lorraine et Dauphiné}}", "<i>(Lorraine et Dauphiné)</i>"),
        ("{{réf}}", ""),
        ("{{smo}}", "samoan"),
        ("{{trad+|conv|Sitophilus granarius}}", "Sitophilus granarius"),
        (
            "{{variante ortho de|acupuncture|fr}}",
            "Variante orthographique de acupuncture",
        ),
        (
            "{{variante orthographique de|acupuncture|fr}}",
            "Variante orthographique de acupuncture",
        ),
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
    ],
)
def test_clean_template(wikicode, expected):
    assert clean("foo", wikicode, "fr") == expected
