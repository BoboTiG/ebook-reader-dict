import pytest

from scripts import utils


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("", ""),
        ("{{absol}}", "(Absolument)"),
        ("{{au pluriel}}", "(Au pluriel)"),
        ("{{au singulier}}", "(Au singulier)"),
        ("{{BE|fr}}", "(Belgique)"),
        ("{{bioch|nocat}}", "(Biochimie)"),
        ("du XX{{e}} siècle", "du XXème siècle"),
        ("{{élec|fr}}", "(Électricité)"),
        ("{{finan|fr}}", "(Finance)"),
        ("{{FR|fr}}", "(France)"),
        ("{{géom|fr}}", "(Géométrie)"),
        ("{{juri|fr}}", "(Droit)"),
        ("{{ling|fr}}", "(Linguistique)"),
        ("{{math|fr}}", "(Mathématiques)"),
        ("{{méton|fr}}", "(Par métonymie)"),
        ("{{métrol|nocat=1}}", "(Métrologie)"),
        ("{{moderne}}", "(Moderne)"),
        ("{{néol|fr}}", "(Néologisme)"),
        ("{{par ext}} ou {{figuré|fr}}", "(Par extension) ou (Figuré)"),
        ("{{part}}", "(En particulier)"),
        ("{{pronl|fr}}", "(Pronominal)"),
        ("{{QC|fr}}", "(Québec)"),
        ("{{région}}", "(Régionalisme)"),
    ],
)
def test_clean_template(wikicode, expected):
    assert utils.clean(wikicode) == expected
