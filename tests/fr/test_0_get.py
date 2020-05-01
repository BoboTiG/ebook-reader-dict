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
                (
                    "Cérémonie ou prestation réservée à un nouvel arrivant, consistant généralement à lui souhaiter la"
                    " bienvenue et à l’aider dans son intégration ou ses démarches."
                ),
                "Lieu où sont accueillies les personnes.",
                "(Vieilli) Fait d’accueillir ou héberger.",
                "Page d’accès ou d’accueil (lieu ci-dessus) à un site web.",
                "Manière dont une œuvre a été acceptée lors de sa sortie par le public et les critiques.",
            ],
        ),
        (
            "aux",
            [
                "(Linguistique) Code ISO 639-3 de l’aurá.",
                "Contraction obligatoire de la préposition à et de l'article défini les.",
            ],
        ),
        ("Bogotanais", []),
        (
            "employer",
            [
                "Utiliser ; user ; se servir de.",
                "(Spécialement) (Grammaire) S’en servir en parlant ou en écrivant, en parlant d'une phrase, "
                "d'un mot ou d'une locution.",
                "Pourvoir d’une occupation ou d’un travail pour son usage ou pour son profit.",
            ],
        ),
        ("corollaires", ["Pluriel de corollaire."]),
        ("ich", ["(Linguistique) Code ISO 639-3 de l’etkywan."]),
        (
            "pinyin",
            [
                (
                    "Système de transcription de la langue chinoise, permettant de romaniser les sons des sinogrammes,"
                    " et d’indiquer le ton utilisé lors de la prononciation."
                ),
                "Langue bantoïde parlée dans la Région du Nord-Ouest au Cameroun.",
            ],
        ),
        ("encyclopædie", []),
        (
            "éperon",
            [
                "(Équitation) Pièce de métal à deux branches, qui s’adapte au talon du "
                "cavalier et dont l’extrémité pointue ou portant une molette sert à piquer "
                "les flancs du cheval pour le stimuler.",
                "(Botanique) Prolongement en forme de tube de la corolle ou du calice (ne "
                "concerne parfois qu’un pétale ou sépale particulier).",
                "(Marine) Partie de la proue d’un bâtiment qui se termine en pointe et qui a "
                "plus ou moins de saillie en avant.",
                "(Géographie) Partie d’un contrefort, d’une chaîne de collines ou de "
                "montagnes qui se termine en pointe.",
                "(Meubles Héraldiques) Meuble représentant l’objet du même nom dans les "
                "armoiries. Il est composé d’une branche en métal en U avec une tige au bout "
                "de laquelle se trouve une molette à six rais mais le nombre peut varier d'un "
                "illustrateur à l’autre. Il est représenté en pal, la molette vers le chef "
                "(haut). Dans les représentations anciennes, il est parfois muni d’une sangle "
                "en cuir. À rapprocher de molette d’éperon.",
            ],
        ),
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
                "Il y a longtemps. Note : contrairement à l’étymologie qui implique un temps "
                "passé récent, l’usage moderne consacre le sens d’un temps antérieur, lointain, "
                "révolu.",
            ],
        ),
        (
            "précepte",
            [
                "Règle ; leçon ; enseignement.",
                "(Philosophie) Ce qui ne peut pas ne pas être autrement.",
                "(Religion) Commandement et, surtout, commandement de Dieu, ou commandement de l’Église, etc.",
            ],
        ),
        (
            "rance",
            [
                "Se dit des corps gras qui, laissés au contact de l’air, ont pris une odeur "
                "forte et un goût désagréable.",
                "S’emploie quelquefois comme nom masculin.",
                "Variante de ranche.",
                "Première personne du singulier de l’indicatif présent de rancer.",
                "Troisième personne du singulier de l’indicatif présent de rancer.",
                "Première personne du singulier du subjonctif présent de rancer.",
                "Troisième personne du singulier du subjonctif présent de rancer.",
                "Deuxième personne du singulier de l’impératif présent de rancer.",
            ],
        ),
        (
            "suis",
            [
                "Première personne du singulier de l’indicatif présent de être.",
                "Première personne du singulier de l’indicatif présent de suivre.",
                "Deuxième personne du singulier de l’indicatif présent de suivre.",
                "Deuxième personne du singulier de l’impératif présent de suivre.",
            ],
        ),
    ],
)
def test_find_sections_and_definitions(word, defs, page):
    """Test the sections finder and definitions getter."""
    data = page(word)
    sections = get.find_sections(data["revision"]["text"]["#text"])
    assert get.find_definitions(sections) == defs


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
        C.SNAPSHOT_LIST,
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
    #   - "en.wiki" (ignored)
    #   - "encyclopædie.wiki" (no definition found)
    #   - "no section.wiki"
    expected_count = len(list(C.SNAPSHOT.glob("*.wiki"))) - 4

    # Check the words data
    words = json.loads(C.SNAPSHOT_DATA.read_text(encoding="utf-8"))
    assert len(words.keys()) == expected_count

    # Check other files
    assert int(C.SNAPSHOT_COUNT.read_text()) == expected_count
    assert C.SNAPSHOT_FILE.read_text() == "20200417"
    words = C.SNAPSHOT_LIST.read_text(encoding="utf-8").splitlines()
    assert len(words) == expected_count
    for line in words:
        assert len(line.split("|")) == 2

    # Call it again and no new action should be made
    assert get.main() == 1
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == ">>> Snapshot up-to-date!"


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

    # There is no data.json but the wordlist containing revisions
    assert C.SNAPSHOT_LIST.is_file()
    C.SNAPSHOT_DATA.unlink()

    # Run against the new snapshot
    assert get.main() == 0

    # Files should be created
    assert pages_xml.is_file()
    assert pages_bz2.is_file()
    assert C.SNAPSHOT_DATA.is_file()

    # Trigger manual calls for coverage
    file = get.fetch_pages(date)
    get.decompress(file)

    captured = capsys.readouterr()
    assert "++ Updated 'aux'" in captured.out
    assert "++ Added 'mot el'" in captured.out
    assert "++ Added 'mot us'" in captured.out
    assert "-- Removed 'suis'" in captured.out

    # Check the words list has been updated
    # Here we do -4 because of:
    #   - "Bogotanais.wiki" (no definition found)
    #   - "en.wiki" (ignored)
    #   - "encyclopædie.wiki" (no definition found)
    #   - "no section.wiki"
    #   - "suis" dynamically removed
    # And we do +2 because of:
    #   - "mot el" dynamically added
    #   - "mot us" dynamically added
    expected_count = len(list(C.SNAPSHOT.glob("*.wiki"))) - 5 + 2

    # Check the words data
    words = json.loads(C.SNAPSHOT_DATA.read_text(encoding="utf-8"))
    assert len(words.keys()) == expected_count

    # Check other files
    wordlist = C.SNAPSHOT_LIST.read_text(encoding="utf-8").splitlines()
    assert len(wordlist) == expected_count
    for line in wordlist:
        assert len(line.split("|")) == 2

    # Call it again and no new action should be made
    assert get.main() == 1
    captured = capsys.readouterr()
    assert captured.out.splitlines()[-1] == ">>> Snapshot up-to-date!"


@pytest.mark.parametrize("err_code", [404, 500])
@responses.activate
def test_main_2(err_code, capsys):
    """Test the whole script when the dump is not finishd on the Wiktionary side."""

    os.environ["WIKI_DUMP"] = date = "20200419"
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
        status=err_code,
    )

    # Start the whole process
    if err_code != 404:
        with pytest.raises(HTTPError):
            assert get.main() == 1
    else:
        assert get.main() == 1
        captured = capsys.readouterr()
        assert captured.out.splitlines()[-1] == ">>> Wiktionary dump is ongoing ... "
