import os

import pytest

os.environ["WIKI_LOCALE"] = "fr"


@pytest.mark.parametrize(
    "word, pron",
    [
        ("accueil", "a.kœj"),
        ("aux", "o"),
        ("barbe à papa", "baʁ.b‿a pa.pa"),
        ("Bogotanais", "bɔ.ɡɔ.ta.nɛ"),
        ("en", "ɑ̃"),
        ("pinyin", "pin.jin"),
        ("suis", "sɥi"),
        ("Slovène", "slɔ.vɛn"),
    ],
)
def test_find_pronunciation(word, pron, page):
    """Test the pronunciation finder."""
    from get import find_pronunciation

    data = page(word)
    text = find_pronunciation(data["revision"]["text"]["#text"])
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
    from get import find_genre

    data = page(word)
    text = find_genre(data["revision"]["text"]["#text"])
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
        (
            "en",
            [
                "Code ISO 639-1 (alpha-2) de l’anglais.",
                "Utilisé après certains verbes.",
                "Permet de préciser une matière.",
                "Indique le lieu.",
                "De ça.",
                "Personne, chose de cette espèce, d’entre eux, d’entre elles. Utilisé tout seul ou avec une quantification.",
                "De ça. Pour une personne, on utilise de lui, d’elle, etc. ou un adjectif possessif.",
                "De ce lieu. De là. De ce côté-là",
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
    from get import find_definitions, find_sections

    data = page(word)
    sections = find_sections(data["revision"]["text"]["#text"])

    res = []
    for section in sections:
        res.extend(find_definitions(section))
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
    from get import is_ignored

    assert is_ignored(word) is ignored
