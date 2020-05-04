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
        ("{{term|Avec ''[[le#fr-art-déf|le]]''}}", "(Avec le)"),
        (
            "{{term|Avec un [[déterminant]] défini comme ''[[le#fr-art-déf|le]]'', ''[[mon#fr-adj-pos|mon]]'', etc., et avec un adjectif ou un adverbe}}",
            "(Avec un déterminant défini comme le, mon, etc., et avec un adjectif ou un adverbe)",
        ),
        ("{{emploi|au passif}}", "(Au passif)"),
        ("{{au pluriel}}", "(Au pluriel)"),
        ("{{au singulier}}", "(Au singulier)"),
        ("{{BE|fr}}", "(Belgique)"),
        ("{{bioch|nocat}}", "(Biochimie)"),
        ("{{couleur|#B0F2B6}}", "(Code RGB #B0F2B6)"),
        ("du XX{{e}} siècle", "du XX<sup>e</sup> siècle"),
        ("{{élec|fr}}", "(Électricité)"),
        ("{{finan|fr}}", "(Finance)"),
        ("{{FR|fr}}", "(France)"),
        ("{{géom|fr}}", "(Géométrie)"),
        ("{{graphe|fr}}", "(Théorie des graphes)"),
        ("{{improprement|fr}}", "(Usage critiqué)"),
        ("{{info|fr}}", "(Informatique)"),
        ("{{juri|fr}}", "(Droit)"),
        ("{{langage SMS}} ", "(Langage SMS)"),
        ("{{lien|étrange|fr}}", "étrange"),
        ("{{ling|fr}}", "(Linguistique)"),
        ("{{math|fr}}", "(Mathématiques)"),
        ("{{mélio|fr}}", "(Mélioratif)"),
        ("{{méton|fr}}", "(Par métonymie)"),
        ("{{métrol|nocat=1}}", "(Métrologie)"),
        ("{{moderne}}", "(Moderne)"),
        ("{{néol|fr}}", "(Néologisme)"),
        ("{{nombre romain|12}}", "XII"),
        ("{{nombre romain|19}}", "XIX"),
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
