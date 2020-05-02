import pytest

from scripts import utils


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("", ""),
        ("{{absol}}", "(Absolument)"),
        ("{{agri|fr}}", "(Agriculture)"),
        ("{{antiq|fr}}", "(Antiquité)"),
        ("{{ancre|sens_sexe}}", ""),
        ("{{emploi|au passif}}", "(Au passif)"),
        ("{{au pluriel}}", "(Au pluriel)"),
        ("{{au singulier}}", "(Au singulier)"),
        ("{{BE|fr}}", "(Belgique)"),
        ("{{bioch|nocat}}", "(Biochimie)"),
        ("du XX{{e}} siècle", "du XXème siècle"),
        ("{{élec|fr}}", "(Électricité)"),
        ("{{finan|fr}}", "(Finance)"),
        ("{{FR|fr}}", "(France)"),
        ("{{géom|fr}}", "(Géométrie)"),
        ("{{graphe|fr}}", "(Théorie des graphes)"),
        ("{{improprement|fr}}", "(Usage critiqué)"),
        ("{{info|fr}}", "(Informatique)"),
        ("{{juri|fr}}", "(Droit)"),
        ("{{langage SMS}} ", "(Langage SMS)"),
        ("{{ling|fr}}", "(Linguistique)"),
        ("{{math|fr}}", "(Mathématiques)"),
        ("{{mélio|fr}}", "(Mélioratif)"),
        ("{{méton|fr}}", "(Par métonymie)"),
        ("{{métrol|nocat=1}}", "(Métrologie)"),
        ("{{moderne}}", "(Moderne)"),
        ("{{néol|fr}}", "(Néologisme)"),
        ("{{par ext}} ou {{figuré|fr}}", "(Par extension) ou (Figuré)"),
        ("{{part}}", "(En particulier)"),
        ("{{pronl|fr}}", "(Pronominal)"),
        ("{{QC|fr}}", "(Québec)"),
        ("{{région}}", "(Régionalisme)"),
        ("{{réf}}", ""),
        ("{{siècle2|XIX}}", "XIXème"),
        ("{{unités|fr}}", "(Métrologie)"),
    ],
)
def test_clean_template(wikicode, expected):
    assert utils.clean(wikicode) == expected
