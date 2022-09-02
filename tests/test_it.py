import pytest

from wikidict.lang.it import find_pronunciations
from wikidict.render import parse_word
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "code, expected",
    [
        ("", []),
        ("{{IPA|/kondiˈvidere/}}", ["/kondiˈvidere/"]),
    ],
)
def test_find_pronunciations(code, expected):
    assert find_pronunciations(code) == expected


@pytest.mark.parametrize(
    "word, pronunciations, gender, etymology, definitions",
    [
        (
            "condividere",
            ["/kondiˈvidere/"],
            "",
            [
                "dal latino <i>cum</i> e <i>dividere</i>; l'attuale uso improprio del verbo <i>condividere</i> è dovuto alla diffusione dei social network negli anni 2000 e 2010",  # noqa
            ],
            [
                "spartire con altri",
                "avere qualcosa in comune con qualcun altro",
                "essere d'accordo con altri su un punto di vista",
                "<small><i>(filosofia)</i></small> <small><i>(economia)</i></small> mettere spazi e risorse in comune con altri",  # noqa
                "<small><i>(informatica)</i></small> ricevere o mettere un'informazione in comune con altri utenti",
            ],
        ),
        (
            "debolmente",
            ["/debolˈmente/"],
            "",
            ["composto dall'aggettivo debole e dal suffisso -mente"],
            [
                "in maniera debole, con debolezza",
            ],
        ),
        (
            "lettore",
            ["/letˈtore/"],
            "m",
            ['dal latino <i>lector</i>, derivazione di <i>legĕre</i> ossia "leggere"'],
            [
                "chi legge un libro, un giornale o una rivista",
                "<small><i>(religione)</i></small> persona che in alcune chiese cristiane, come la Chiesa cattolica, la Chiesa anglicana e quella ortodossa, è incaricata di proclamare la parola di Dio e altri testi nelle celebrazioni liturgiche e di esercitare altri compiti in campo pastorale",  # noqa
                "<small><i>(elettronica)</i></small> <small><i>(informatica)</i></small> <small><i>(tecnologia)</i></small> <small><i>(ingegneria)</i></small> dispositivo elettronico che decodifica e riceve informazioni da un supporto",  # noqa
            ],
        ),
    ],
)
def test_parse_word(word, pronunciations, gender, etymology, definitions, page):
    """Test the sections finder and definitions getter."""
    code = page(word, "it")
    details = parse_word(word, code, "it", force=True)
    assert pronunciations == details.pronunciations
    assert gender == details.gender
    assert etymology == details.etymology
    assert definitions == details.definitions


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{Vd|mamma}}", "vedi mamma"),
    ],
)
def test_process_templates(wikicode, expected):
    """Test templates handling."""
    assert process_templates("foo", wikicode, "it") == expected
