import json
import os
from contextlib import suppress

import pytest
import responses
from requests.exceptions import HTTPError

os.environ["WIKI_LOCALE"] = "fr"

# Must be imported after *WIKI_LOCALE* is set
from scripts import constants as C  # noqa
from scripts import get  # noqa


WIKTIONARY_INDEX = """<html>
<head><title>Index of /frwiktionary/</title></head>
<body bgcolor="white">
<h1>Index of /frwiktionary/</h1><hr><pre><a href="../">../</a>
<a href="20191120/">20191120/</a>                                          02-Jan-2020 01:29                   -
<a href="20191201/">20191201/</a>                                          21-Jan-2020 01:36                   -
<a href="20191220/">20191220/</a>                                          02-Feb-2020 01:28                   -
<a href="20200101/">20200101/</a>                                          21-Feb-2020 01:38                   -
<a href="20200120/">20200120/</a>                                          02-Mar-2020 01:28                   -
<a href="20200201/">20200201/</a>                                          02-Apr-2020 01:36                   -
<a href="20200220/">20200220/</a>                                          24-Feb-2020 17:32                   -
<a href="20200301/">20200301/</a>                                          09-Mar-2020 03:42                   -
<a href="{date}/">{date}/</a>                                          17-Apr-2020 15:20                   -
<a href="latest/">latest/</a>                                            17-Apr-2020 15:20                   -
</pre><hr></body>
</html>
"""


@pytest.mark.parametrize(
    "word, pron",
    [
        ("accueil", "a.kœj"),
        ("aux", "o"),
        ("barbe à papa", "baʁ.b‿a pa.pa"),
        ("Bogotanais", "bɔ.ɡɔ.ta.nɛ"),
        ("pinyin", "pin.jin"),
        ("sapristi", "sa.pʁis.ti"),
        ("suis", "sɥi"),
        ("Slovène", "slɔ.vɛn"),
    ],
)
def test_find_pronunciation(word, pron, page):
    """Test the pronunciation finder."""
    data = page(word)
    text = get.find_pronunciation(data["revision"]["text"]["#text"])
    assert text == pron


@pytest.mark.parametrize(
    "word, genre",
    [
        ("accueil", "m"),
        ("aux", "mf"),
        ("barbe à papa", "f"),
        ("pinyin", "m"),
        ("suis", ""),
    ],
)
def test_find_genre(word, genre, page):
    """Test the genre finder."""
    data = page(word)
    text = get.find_genre(data["revision"]["text"]["#text"])
    assert text == genre


@pytest.mark.parametrize(
    "word, defs",
    [
        (
            "accueil",
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
            [
                "<i>(Linguistique)</i> <i>(Rare)</i> Système graphique qui consiste à peindre, pour représenter les idées, l’image des objets dont le nom commence par la même lettre que celui par lequel ces idées sont exprimées dans le langage ordinaire.",  # noqa
                "<i>(Linguistique)</i> <i>(Par extension)</i> <i>(Rare)</i> Se dit lorsque deux termes commencent par la même lettre et qu’ils sont apparentés par le sens.",  # noqa
                "<i>(Philosophie)</i> <i>(Très rare)</i> Recherche ou exposition des principes suprêmes, ou du mieux absolu.",  # noqa
                "<i>(Sport)</i> Étude ou pratique de l’acrobatie.",
            ],
        ),
        (
            "aux",
            [
                "<i>(Linguistique)</i> Code ISO 639-3 de l’aurá.",
                "<i>Contraction obligatoire de la préposition </i>à<i> et de l'article défini </i>les<i>.</i>",
            ],
        ),
        (
            "base",
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
                "<i>(Hippisme)</i> Cheval ou groupe de chevaux que l’on retient dans toutes ses combinaisons de paris hippiques pour une course donnée, car on estime qu’ils ont de très bonnes chances de figurer parmi les premiers.",  # noqa
                "<i>(Politique)</i> Ensemble des électeurs, des soutiens d’un politique ou d’un parti.",
                "<i>(Figuré)</i> Ce qui est le principe, la donnée fondamentale d’une chose ou ce sur quoi elle repose.",  # noqa
            ],
        ),
        ("Bogotanais", []),
        (
            "corps portant",
            [
                "<i>(Astronautique)</i> Aéronef à fuselage porteur, sur lequel la portance est produite par le fuselage, destiné aux usages spatiaux ou hypersoniques, afin de limiter l'effet de traînée ou la surface de friction.",  # noqa
                "<i>(Astronautique)</i> <i>(Aérodynamique)</i> Engin aérospatial possédant, à vitesse hypersonique, une portance qui lui assure une bonne manœuvrabilité lors de la rentrée atmosphérique.",  # noqa
            ],
        ),
        ("corollaires", ["<i>Pluriel de</i> corollaire."]),
        (
            "DES",
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
            [
                "Utiliser ; user ; se servir de.",
                "<i>(Spécialement)</i> <i>(Grammaire)</i> S’en servir en parlant ou en écrivant, en parlant d'une phrase, d'un mot ou d'une locution.",  # noqa
                "Pourvoir d’une occupation ou d’un travail pour son usage ou pour son profit.",
            ],
        ),
        (
            "encyclopædie",
            ["<i>(Archaïsme)</i> Variante orthographique de encyclopédie."],
        ),
        (
            "éperon",
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
            [
                "<i>(Droit)</i> Officier public préposé au greffe.",
                "<i>(Figuré)</i> Celui qui prend note et tient le registre de ses notes.",
                "<i>(Populaire)</i> Chat.",
                "Poisson-chat commun (poisson).",
            ],
        ),
        ("ich", ["<i>(Linguistique)</i> Code ISO 639-3 de l’etkywan."]),
        (
            "mutiner",
            [
                "Se porter à la sédition, à la révolte.",
                "Enfant qui se dépite et manque à l’obéissance.",
            ],
        ),
        (
            "naguère",
            [
                "Récemment ; il y a peu.",
                "Il y a longtemps. <b>Note :</b> contrairement à l’étymologie qui implique un temps passé récent, l’usage moderne consacre le sens d’un temps antérieur, lointain, révolu.",  # noqa
            ],
        ),
        (
            "pinyin",
            [
                "Système de transcription de la langue chinoise, permettant de romaniser les sons des sinogrammes, et d’indiquer le ton utilisé lors de la prononciation.",  # noqa
                "Langue bantoïde parlée dans la Région du Nord-Ouest au Cameroun.",
            ],
        ),
        (
            "précepte",
            [
                "Règle ; leçon ; enseignement.",
                "<i>(Philosophie)</i> Ce qui ne peut pas ne pas être autrement.",
                "<i>(Religion)</i> Commandement et, surtout, commandement de Dieu, ou commandement de l’Église, etc.",
            ],
        ),
        (
            "rance",
            [
                "Se dit des corps gras qui, laissés au contact de l’air, ont pris une odeur forte et un goût désagréable.",  # noqa
                "S’emploie quelquefois comme nom masculin.",
                "Variante de ranche.",
            ],
        ),
        ("sapristi", ["Pour marquer l’étonnement."]),
        (
            "silicone",
            [
                "<i>(Chimie)</i> Composé inorganique formés d’une chaine silicium-oxygène (…-Si-O-Si-O-Si-O-…) sur laquelle des groupes se fixent, sur les atomes de silicium.",  # noqa
            ],
        ),
        ("suis", []),
    ],
)
def test_find_sections_and_definitions(word, defs, page):
    """Test the sections finder and definitions getter."""
    data = page(word)
    sections = get.find_sections(data["revision"]["text"]["#text"])
    assert get.find_definitions(word, sections) == defs


@responses.activate
def test_main_0(craft_data, capsys):
    """Test the whole script. It will generate data for test_fr_1_convert.py."""

    date = "20200417"
    pages_xml = C.SNAPSHOT / f"pages-{date}.xml"
    pages_bz2 = C.SNAPSHOT / f"pages-{date}.xml.bz2"

    # Clean-up before we start
    for file in (
        C.SNAPSHOT_DATA,
        C.SNAPSHOT_COUNT,
        C.SNAPSHOT_FILE,
        pages_xml,
        pages_bz2,
    ):
        with suppress(FileNotFoundError):
            file.unlink()

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages()
    responses.add(responses.GET, C.BASE_URL, body=WIKTIONARY_INDEX.format(date=date))
    responses.add(
        responses.GET,
        f"{C.BASE_URL}/{date}/{C.WIKI}-{date}-pages-meta-current.xml.bz2",
        body=craft_data(date, "fr"),
    )

    # Start the whole process
    with capsys.disabled():
        assert get.main() == 0

    # Check for generated files

    # Check that files are created
    assert pages_xml.is_file()
    assert pages_bz2.is_file()
    assert C.SNAPSHOT_DATA.is_file()

    # Here we do -3 because of:
    #   - "Bogotanais.wiki" (no definition found)
    #   - "no section.wiki"
    #   - "suis.wiki" (conjugated verb)
    expected_count = len(list(C.SNAPSHOT.glob("*.wiki"))) - 3

    # Check the words data
    words = json.loads(C.SNAPSHOT_DATA.read_text(encoding="utf-8"))
    assert len(words.keys()) == expected_count

    # Check other files
    assert int(C.SNAPSHOT_COUNT.read_text()) == expected_count
    assert C.SNAPSHOT_FILE.read_text() == "20200417"


@responses.activate
def test_main_1(craft_data, capsys):
    """Test the whole script again. There should be updates."""

    date = "20200418"
    pages_xml = C.SNAPSHOT / f"pages-{date}.xml"
    pages_bz2 = C.SNAPSHOT / f"pages-{date}.xml.bz2"

    # Clean-up before we start
    for file in (pages_xml, pages_bz2):
        with suppress(FileNotFoundError):
            file.unlink()

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages()
    responses.add(responses.GET, C.BASE_URL, body=WIKTIONARY_INDEX.format(date=date))
    responses.add(
        responses.GET,
        f"{C.BASE_URL}/{date}/{C.WIKI}-{date}-pages-meta-current.xml.bz2",
        body=craft_data(
            date,
            "fr",
            to_add=(("mot el", "42"), ("mot us", "42")),
            to_alter=("aux",),
            to_remove=("suis",),
        ),
    )

    # Run against the new snapshot
    assert get.main() == 0

    # Files should be created
    assert pages_xml.is_file()
    assert pages_bz2.is_file()
    assert C.SNAPSHOT_DATA.is_file()

    # Trigger manual calls for coverage
    file = get.fetch_pages(date)
    get.decompress(file)

    # Check the words list has been updated
    # Here we do -4 because of:
    #   - "Bogotanais.wiki" (no definition found)
    #   - "no section.wiki"
    #   - "suis" dynamically removed
    # And we do +2 because of:
    #   - "mot el" dynamically added
    #   - "mot us" dynamically added
    expected_count = len(list(C.SNAPSHOT.glob("*.wiki"))) - 3 + 2

    # Check the words data
    words = json.loads(C.SNAPSHOT_DATA.read_text(encoding="utf-8"))
    assert len(words.keys()) == expected_count


@responses.activate
def test_main_2(craft_data, capsys):
    """Test the whole script when the dump is not finished on the Wiktionary side."""

    # Clean-up before we start
    for date in ("20200301", "20200514"):
        with suppress(FileNotFoundError):
            (C.SNAPSHOT / f"pages-{date}.xml").unlink()
        with suppress(FileNotFoundError):
            (C.SNAPSHOT / f"pages-{date}.xml.bz2").unlink()

    # List of requests responses to falsify:
    #   - fetch_snapshots()
    #   - fetch_pages()
    responses.add(responses.GET, C.BASE_URL, body=WIKTIONARY_INDEX.format(date="20200514"))
    responses.add(
        responses.GET,
        f"{C.BASE_URL}/20200514/{C.WIKI}-20200514-pages-meta-current.xml.bz2",
        status=404,
    )
    responses.add(
        responses.GET,
        f"{C.BASE_URL}/20200301/{C.WIKI}-20200301-pages-meta-current.xml.bz2",
        body=craft_data(
            date,
            "fr",
            to_add=(("mot el", "42"), ("mot us", "42")),
            to_alter=("aux",),
            to_remove=("suis",),
        ),
    )

    # Start the whole process
    assert get.main() == 0


def test_xml_parse_word_with_colons(tmp_path):
    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
<page>
    <title>MediaWiki:Sitetitle</title>
    <ns>8</ns>
    <id>12</id>
    <revision>
        <id>403956</id>
        <parentid>33016</parentid>
        <timestamp>2006-02-13T09:08:31Z</timestamp>
        <contributor>
        <username>Bob</username>
        <id>-42</id>
        </contributor>
        <comment>changement de titre pour meilleur référencement dans les moteurs de recherche</comment>
        <model>wikitext</model>
        <format>text/x-wiki</format>
        <text bytes="46" xml:space="preserve">Wiktionnaire : dictionnaire libre et universel</text>
        <sha1>40helna9646ffk0utvwm8bkdlzi1eck</sha1>
    </revision>
</page>
</mediawiki>
"""
    )

    words = get.process(file)
    assert not words


def test_xml_parse_not_word(tmp_path):
    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
<siteinfo>
    <sitename>Wiktionnaire</sitename>
    <dbname>frwiktionary</dbname>
    <base>https://fr.wiktionary.org/wiki/Wiktionnaire:Page_d%E2%80%99accueil</base>
    <generator>MediaWiki 1.35.0-wmf.25</generator>
    <case>case-sensitive</case>
    <namespaces>
        <namespace key="-2" case="case-sensitive">Média</namespace>
        <namespace key="-1" case="first-letter">Spécial</namespace>
        <namespace key="0" case="case-sensitive" />
    </namespaces>
</siteinfo>
</mediawiki>
"""
    )

    words = get.process(file)
    assert not words


def test_xml_parse_redirected_word(tmp_path):
    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
<page>
    <title>MediaWiki:Sitetitle</title>
    <ns>8</ns>
    <id>12</id>
    <redirect></redirect>
</page>
</mediawiki>
"""
    )

    words = get.process(file)
    assert not words


def test_xml_parse_restricted_word(tmp_path):
    """For instance, "cunnilingus" was filtered out. Ensure no regressions."""

    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
<page>
    <title>cunnilingus</title>
    <ns>0</ns>
    <id>27758</id>
    <restrictions>edit=autoconfirmed:move=autoconfirmed</restrictions>
    <revision>
        <id>27636792</id>
        <parentid>27249625</parentid>
        <timestamp>2020-04-05T23:27:40Z</timestamp>
        <contributor>
            <username>Alice</username>
            <id>-42</id>
        </contributor>
        <minor />
        <comment></comment>
        <model>wikitext</model>
        <format>text/x-wiki</format>
        <text bytes="292" xml:space="preserve">{{voir|Cunnilingus}}
=== {{S|nom|fr}} ===
{{fr-inv|ky.ni.lɛ̃.gys|sp=1}}
[[Fichier:Édouard-Henri Avril (23).jpg|thumb|Un '''cunnilingus''']]
'''cunnilingus''' {{pron|ky.ni.lɛ̃.ɡys|fr}} {{m}}, {{sp}}
# {{sexe|fr}} [[excitation|Excitation]] [[buccal]]e des [[organe]]s [[génitaux]] [[féminins]].</text>
        <sha1>aimljsg0qagdsp5yyz38fgv3rh0ksm1</sha1>
    </revision>
</page>
</mediawiki>
"""
    )

    words = get.process(file)
    assert len(words) == 1

    word, details = list(words.items())[0]
    assert word == "cunnilingus"
    assert len(details) == 3

    pronunciation, genre, definitions = details
    assert pronunciation == "ky.ni.lɛ̃.ɡys"
    assert genre == "m"
    assert len(definitions) == 1
    assert len(definitions[0]) == 68


def test_xml_parse_word_without_definitions(tmp_path):
    file = tmp_path / "page.xml"
    file.write_text(
        """\
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xml:lang="fr">
<page>
    <title>MediaWiki:Sitetitle</title>
    <ns>8</ns>
    <id>12</id>
    <revision>
        <id>403956</id>
        <parentid>33016</parentid>
        <timestamp>2006-02-13T09:08:31Z</timestamp>
        <contributor>
        <username>Bob</username>
            <id>-42</id>
            </contributor>
        <comment>changement de titre pour meilleur référencement dans les moteurs de recherche</comment>
        <model>wikitext</model>
        <format>text/x-wiki</format>
        <sha1>40helna9646ffk0utvwm8bkdlzi1eck</sha1>
    </revision>
</page>
</mediawiki>
"""
    )

    words = get.process(file)
    assert not words
