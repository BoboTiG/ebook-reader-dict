from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "-ης",
            [],
            [],
            [
                "<b>-ης</b> < <i>αρχαία ελληνική</i> -ης",
                "<b>-ης</b> < (<i>ελληνιστική κοινή</i>) -ις < <i>αρχαία ελληνική</i> -(ε)ιος (<i>αρχαία ελληνική</i> κύριος, <i><b>αιτιατική</b></i> τόν κύριον > (<i>ελληνιστική κοινή</i>) τόν κῦριν →ὁ κῦρις > <i>μεσαιωνική ελληνική</i> κύρης > <i>νέα ελληνική</i> νοικοκύρης)",
                "<b>-ης</b> < <i>μεσαιωνική ελληνική</i> <b>-ης</b>",
                "<b>-ης</b> < <i>αρχαία ελληνική</i> <b>-ης, -ης, -ες</b> & <b>-ής, -ής, -ές</b>",
                "<b>-ης</b> < (<i>ελληνιστική κοινή</i>) <b>-ῆς</b> (γενική ενικού θηλυκών: κατά γ<b>ῆς</b>)",
                "<b>-ης</b> < <i>τουρκική</i> <b>-i</b> (fıstık > fıstık<b>i</b>)",
            ],
            ["επίθημα τρικατάληκτων τριγενών επιθέτων (-<b>ής</b>, -<b>ιά</b>, -<b>ί</b>)"],
            [],
        ),
        (
            "επίπεδο",
            ["/eˈpi.pe.ðo/"],
            ["ουδέτερο"],
            [
                "<b>επίπεδο</b>, {{π}} <i>ουδέτερο του</i> <b>επίπεδος</b> < (διαχρονικό δάνειο) <i>αρχαία ελληνική</i> ἐπίπεδον",
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
        (
            "τσιγγάνα",
            [],
            ["θηλυκό"],
            [],
            [],
            ["τσιγγάνος"],
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
        ("{{IPAstyle|ˈɑɹ.kən.sɔ}}", "ˈɑɹ.kən.sɔ"),
        ("{{resize|Βικιλεξικό|140}}", '<span style="font-size:140%;">Βικιλεξικό</span>'),
        ("{{κνε}}", "<i>κοινή νεοελληνική</i>"),
        ("{{νε}}", "<i>νέα ελληνική</i>"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "el") == expected
