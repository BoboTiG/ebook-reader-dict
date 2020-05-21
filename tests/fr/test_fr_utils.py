import pytest

from scripts import constants as C  # noqa
from scripts import utils


# Set the locale
C.reload("fr")


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{adj-indéf-avec-de}}", "<i>(Avec de)</i>"),
        ("{{ancre|sens_sexe}}", ""),
        ("{{date|1957}}", "<i>(1957)</i>"),
        ("{{date|1957-2057}}", "<i>(1957-2057)</i>"),
        ("{{emploi|au passif}}", "<i>(Au passif)</i>"),
        ("{{cf|immortelle}}", "→ voir immortelle"),
        ("{{cf|lang=fr|faire}}", "→ voir faire"),
        ("{{couleur|#B0F2B6}}", "[RGB #B0F2B6]"),
        ("du XX{{e}} siècle", "du XX<sup>e</sup> siècle"),
        ("[[J·K-1|'''J·K{{e|-1}}''']]", "<b>J·K<sup>-1</sup></b>"),
        ("{{FR|fr}}", "<i>(France)</i>"),
        ("{{lien|étrange|fr}}", "étrange"),
        ("{{lien|D{{e}}}}", "D<sup>e</sup>"),
        ("{{ling|fr}}", "<i>(Linguistique)</i>"),
        ("{{in|5}}", "<sub>5</sub>"),
        ("{{nombre romain|12}}", "XII"),
        ("{{par ext}} ou {{figuré|fr}}", "<i>(Par extension)</i> ou <i>(Figuré)</i>"),
        ("{{région}}", "<i>(Régionalisme)</i>"),
        ("{{région|Lorraine et Dauphiné}}", "<i>(Lorraine et Dauphiné)</i>"),
        ("{{réf}}", ""),
        ("{{smo}}", "samoan"),
        ("{{trad+|conv|Sitophilus granarius}}", "Sitophilus granarius"),
        (
            "{{variante ortho de|acupuncture|fr}}",
            "Variante orthographique de acupuncture",
        ),
        (
            "{{variante orthographique de|acupuncture|fr}}",
            "Variante orthographique de acupuncture",
        ),
        (
            "{{wp|Sarcoscypha coccinea}}",
            "<i>Sarcoscypha coccinea sur l'encyclopédie Wikipedia</i>",
        ),
        ("{{ws|Bible Segond 1910/Livre de Daniel|Livre de Daniel}}", "Livre de Daniel"),
        (
            "{{ws|Les Grenouilles qui demandent un Roi}}",
            "Les Grenouilles qui demandent un Roi",
        ),
        ("{{wsp|Panthera pardus|''Panthera pardus''}}", "<i>Panthera pardus</i>"),
        ("{{wsp|Brassicaceae}}", "Brassicaceae"),
        ("{{WSP|Panthera leo}}", "<i>(Panthera leo)</i>"),
    ],
)
def test_clean_template(wikicode, expected):
    assert utils.clean("foo", wikicode) == expected
