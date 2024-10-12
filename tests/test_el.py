from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "επίπεδο",
            ["/eˈpi.pe.ðo/"],
            ["ουδέτερο"],
            [
                "<b>επίπεδο</b>, <i>(Ουδ του)</i> < (διαχρονικό δάνειο) <i>αρχαία ελληνική</i> ἐπίπεδον",
            ],
            [
                "(<i>γεωμετρία</i>) λεία ομοιόμορφη γεωμετρική επιφάνεια η οποία μπορεί να εφαρμόσει πλήρως με τον εαυτό της ακόμα και εν κινήσει",
                "η στάθμη",
                "το ύψος όπου βρίσκεται κάτι σε μια ιεραρχική κλίμακα",
                "(<i>μεταφορικά</i>) σπουδαιότητα, σημαντικότητα",
            ],
            [],
        ),
        (
            "λαμβάνω",
            ["/laɱˈva.no/"],
            [],
            [
                "<b>λαμβάνω</b> < (διαχρονικό δάνειο) <i>αρχαία ελληνική</i> λαμβάνω < <i>πρωτοϊνδοευρωπαϊκή</i> *<i>sleh₂gʷ</i>-",
            ],
            [
                "παίρνω, δέχομαι",
                "εντοπίζω επιθυμητό σήμα (όπως από ασύρματο)",
                "(<i>μεταφορικά</i>) καταλαβαίνω",
            ],
            [],
        ),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: list[str],
    genders: list[str],
    etymology: list[Definitions],
    definitions: list[Definitions],
    variants: list[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "el")
    details = parse_word(word, code, "el", force=True)
    assert pronunciations == details.pronunciations
    assert genders == details.genders
    assert definitions == details.definitions
    assert etymology == details.etymology
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{resize|Βικιλεξικό|140}}", '<span style="font-size:140%;">Βικιλεξικό</span>'),
        ("{{ετικ|γαστρονομία|τρόφιμα|γλυκά}}", "(<i>γαστρονομία</i>, <i>τρόφιμα</i>, <i>γλυκά</i>)"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "el") == expected
