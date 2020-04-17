import os
from pathlib import Path
from unittest.mock import patch

import pytest

os.environ["WIKI_LOCALE"] = "fr"

# Must be imported after *WIKI_LOCALE* is set
import get  # noqa


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
                "Cérémonie ou prestation réservée à un nouvel arrivant, consistant généralement à lui souhaiter la bienvenue et à l’aider dans son intégration ou ses démarches.",
                "Lieu où sont accueillies les personnes.",
                "Fait d’accueillir ou héberger.",
                "Page d’accès ou d’accueil (lieu ci-dessus) à un site web.",
                "Manière dont une œuvre a été acceptée lors de sa sortie par le public et les critiques.",
            ],
        ),
        (
            "aux",
            [
                "Code de l’aurá.",
                "Contraction obligatoire de la préposition à et de l'article défini les.",
            ],
        ),
        ("Bogotanais", []),
        (
            "employer",
            [
                "Utiliser ; user ; se servir de.",
                "S’en servir en parlant ou en écrivant, en parlant d'une phrase, d'un mot ou d'une locution.",
                "Pourvoir d’une occupation ou d’un travail pour son usage ou pour son profit.",
            ],
        ),
        ("ich", ["Code de l’etkywan."]),
        (
            "pinyin",
            [
                "Système de transcription de la langue chinoise, permettant de romaniser les sons des sinogrammes, et d’indiquer le ton utilisé lors de la prononciation.",
                "Langue bantoïde parlée dans la Région du Nord-Ouest au Cameroun.",
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
    """Test the sections finder definitions getter."""
    data = page(word)
    sections = get.find_sections(data["revision"]["text"]["#text"])

    res = []
    for section in sections:
        res.extend(get.find_definitions(section))
    assert res == defs


@pytest.mark.parametrize(
    "word, ignored",
    [
        ("accueil", False),
        ("2", True),
        ("22", True),
        ("222", True),
        ("222" * 12, True),
        ("en", True),
        ("", True),
        (" ", True),
    ],
)
def test_is_ignored(word, ignored):
    """Test words filtering."""
    assert get.is_ignored(word) is ignored


@patch("get.fetch_snapshots")
def test_main(mocked_fetch_snapshots, craft_data):
    """Test the whole script. It will generate data for test_fr_1_convert.py."""

    # Fake
    date = "20200417"

    data_dir = Path(os.environ["CWD"]) / "data" / "fr"
    data = data_dir / "data.json"
    count = data_dir / "words.count"
    snapshot = data_dir / "words.snapshot"
    wordlist = data_dir / "words.list"
    pages_xml = data_dir / f"pages-{date}.xml"
    pages_bz2 = data_dir / f"pages-{date}.xml.bz2"

    # Clean-up before we start
    for file in (data, count, snapshot, wordlist, pages_xml, pages_bz2):
        file.unlink()

    # fetch_snapshots() should return the specific date to prevent downloading anything
    mocked_fetch_snapshots.return_value = [date]
    assert get.fetch_snapshots() == [date]

    # Generate the *pages* file using data from the test folder
    craft_data(date, "fr")
    assert pages_xml.is_file()
    assert pages_bz2.is_file()

    # Start the whole process
    assert get.main() == 0

    # Check for generated files
    # Here we do -1 because "Bogotanais.wiki" will not work (no definition found)
    expected_count = len(list(data_dir.glob("*.wiki"))) - 1
    assert int(count.read_text()) == expected_count
    assert snapshot.read_text() == "20200417"
    words = wordlist.read_text(encoding="utf-8").splitlines()
    assert len(words) == expected_count
    for line in words:
        assert len(line.split("|")) == 2

    # Call it again and no new action should be made
    assert get.main() == 1
