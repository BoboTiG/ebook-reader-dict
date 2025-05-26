from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "ανα-",
            ["/a.na/"],
            [],
            [],
            [
                "που δηλώνει τόπο, κατεύθυνση προς τα πάνω, ή ανώτερο στάδιο ιεραρχικά ή τοπικά",
                "<i>επιτατικό</i>",
                "με υποκοριστική σημασία",
                "που δηλώνει επανάληψη (ξανα-, επαν-)",
                "(<i>στερητικό</i>) <i>άλλη μορφή του</i> <b>α-</b>",
            ],
            [],
        ),
        (
            "-ης",
            [],
            [],
            [
                "<b>-ης</b> &lt; <i>αρχαία ελληνική</i> -ης",
                "<b>-ης</b> &lt; (<i>ελληνιστική κοινή</i>) -ις &lt; <i>αρχαία ελληνική</i> -(ε)ιος (<i>αρχαία ελληνική</i> κύριος, <i><b>αιτιατική</b></i> τόν κύριον &gt; (<i>ελληνιστική κοινή</i>) τόν κῦριν →ὁ κῦρις &gt; <i>μεσαιωνική ελληνική</i> κύρης &gt; <i>νέα ελληνική</i> νοικοκύρης)",
                "<b>-ης</b> &lt; <i>μεσαιωνική ελληνική</i> <b>-ης</b>",
                "<b>-ης</b> &lt; <i>αρχαία ελληνική</i> <b>-ης, -ης, -ες</b> & <b>-ής, -ής, -ές</b>",
                "<b>-ης</b> &lt; (<i>ελληνιστική κοινή</i>) <b>-ῆς</b> (γενική ενικού θηλυκών: κατά γ<b>ῆς</b>)",
                "<b>-ης</b> &lt; <i>τουρκική</i> <b>-i</b> (fıstık &gt; fıstık<b>i</b>)",
            ],
            ["επίθημα τρικατάληκτων τριγενών επιθέτων (-<b>ής</b>, -<b>ιά</b>, -<b>ί</b>)"],
            [],
        ),
        (
            "επίπεδο",
            ["/eˈpi.pe.ðo/"],
            ["ουδέτερο"],
            [
                "<b>επίπεδο</b>, επί- &lt; (διαχρονικό δάνειο) <i>αρχαία ελληνική</i> ἐπίπεδον",
            ],
            [
                "(<i>γεωμετρία</i>) η λεία ομοιόμορφη γεωμετρική επιφάνεια η οποία μπορεί να εφαρμόσει πλήρως με τον εαυτό της ακόμα και εν κινήσει",
                "η στάθμη",
                "το ύψος όπου βρίσκεται κάτι σε μια ιεραρχική κλίμακα",
                "(<i>μεταφορικά</i>) η σπουδαιότητα, η σημαντικότητα",
            ],
            [],
        ),
        (
            "λαμβάνω",
            ["/laɱˈva.no/"],
            [],
            [
                "<b>λαμβάνω</b> &lt; (διαχρονικό δάνειο) <i>αρχαία ελληνική</i> λαμβάνω &lt; <i>πρωτοϊνδοευρωπαϊκή</i> *<i>sleh₂gʷ</i>-",
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
        (
            "-αίικο",
            ["/ˈe.i.ko/"],
            ["ουδέτερο"],
            [
                "<b>-αίικο</b> &lt; <i>ουσιαστικοποιημένο ουδέτερο του επιθέτου</i> -αίικος επίθημα σε επίθετα ή οικογενειακά επώνυμα -αί(οι) + -ικος"
            ],
            [
                "(<i>λαϊκότροπο</i>) επίθημα με πρώτο συνθετικό",
                (
                    "οικογενειακό επώνυμο που δηλώνει",
                    (
                        "την οικογένεια ή το σπίτι",
                        "τη συνοικία ή τον τόπο όπου κατοικεί η οικογένεια",
                    ),
                    "(<i>περιληπτικό</i>) πατριδωνυμικό ή εθνικό όνομα",
                ),
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
    print(f"{word = }")
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
        ("{{IPAchar|/ˈsɛləteɪp/}}", "/ˈsɛləteɪp/"),
        ("{{IPAstyle|ˈɑɹ.kən.sɔ}}", "ˈɑɹ.kən.sɔ"),
        ("{{resize|Βικιλεξικό|140}}", '<span style="font-size:140%;">Βικιλεξικό</span>'),
        ("{{κνε}}", "<i>κοινή νεοελληνική</i>"),
        ("{{νε}}", "<i>νέα ελληνική</i>"),
        ("{{θηλ ισσα|Αβαριτσιώτης|Αβαριτσιώτ(ης)}}", "Αβαριτσιώτ(ης) + κατάληξη θηλυκού -ισσα"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "el") == expected
