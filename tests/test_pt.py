import pytest

from wikidict.render import parse_word
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genre, etymology, definitions",
    [
        ("ababalhar", [], "", ["De baba."], ["<i>(popular)</i> babar; conspurcar"]),
        (
            "alguém",
            ["aw.ˈgẽj"],
            "",
            ["Do latim <i>alĭquem</i> <sup>(la)</sup>."],
            ["pessoa não identificada"],
        ),
        (
            "algo",
            [],
            "",
            [],
            ["um pouco, de certo modo", "objeto (não-identificado) de que se fala"],
        ),
        (
            "baiano",
            [],
            "",
            ["Derivado de Bahia, mais o sufixo ano, com perda do H."],
            [
                "do Estado da Bahia, Brasil",
                "natural ou habitante do Estado da Bahia, Brasil",
                "<i>(São Paulo, Brasil; popular; pejorativo)</i> pessoa que se veste de maneira incomum ou brega; fora da moda",  # noqa
            ],
        ),
        (
            "cabrum",
            [],
            "mf",
            ['Do latim <i>caprunu</i> <sup>(la)</sup> "cabra".'],
            [
                "<i>(Pecuária)</i> de cabras:",
                "<i>(Regionalismo, Brasil)</i> marido de mulher adúltera",
                "indica estrondo",
            ],
        ),
        (
            "COPOM",
            [],
            "m",
            [],
            [
                "<b>C</b>entro de <b>O</b>perações da <b>Po</b>lícia <b>M</b>ilitar",
                "<i>(Brasil)</i> <b>Co</b>mitê de <b>Po</b>lítica <b>M</b>onetária",
            ],
        ),
        (
            "dezassete",
            [],
            "",
            ["Contração do latim vulgar <i>decem</i> + <i>ac</i> + <i>septem</i>."],
            [
                "o número dezassete (17, XVII)",
                "nota correspondente a dezassete valores",
                "pessoa ou coisa que apresenta o número dezassete numa ordenação",
                "vide dezessete",
            ],
        ),
        (
            "etc",
            [],
            "",
            [],
            [
                'abreviação do latim <i>et cetera</i>, que significa "e outros", "e os restantes" e "e outras coisas mais"',  # noqa
            ],
        ),
        (
            "-ista",
            [],
            "",
            [
                "Do grego antigo <i>-ιστεσ</i> (<i>-istes</i>) através do latim <i>-ista</i> através do francês antigo <i>-iste</i>."  # noqa
            ],
            [
                "que segue um princípio",
                "que é estudioso ou profissional de um assunto",
                "que usa algo",
                "que tem uma visão preconceituosa",
            ],
        ),
        (
            "neo-",
            [],
            "",
            ["Do grego antigo <i>νέος</i>."],
            [
                "exprime a ideia de <i>novo</i>",
                "<b>Nota:</b> Liga-se por hífen ao morfema seguinte quando este começa por <b>vogal</b>, <b>h</b>, <b>r</b> ou <b>s</b>.",  # noqa
            ],
        ),
        ("para", [], "", [], ["exprime fim, destino, lugar, tempo, direção etc"]),
        (
            "paulista",
            [],
            "",
            [],
            [
                "diz-se de pessoa de origem do Estado de São Paulo, Brasil",
                "diz-se de artigo ou objeto do Estado de São Paulo",
                "pessoa de origem do Estado de São Paulo, Brasil",
                "artigo ou objeto do Estado de São Paulo",
            ],
        ),
        ("tenui-", [], "", [], ["variante ortográfica de <b>tenu-</b>"]),
        (
            "to",
            [],
            "",
            [],
            [
                '<i>(antigo)</i> contração do pronome pessoal "te" com o pronome pessoal ou demonstrativo "o"',
                "<i>(coloquial e Brasil)</i> forma aferética (muito comum na linguagem falada) de estou",
            ],
        ),
        (
            "ũa",
            [],
            "",
            [
                "Do Latim <i>una-</i>: <i>una-</i> deu <b>ũa</b> por queda do <b>n</b> com a nasalação do <b>ũ</b>."
            ],
            ["ortografia antiga de uma"],
        ),
        ("UTC", [], "", [], ["<i>(estrangeirismo)</i> ver TUC"]),
    ],
)
def test_parse_word(word, pronunciations, genre, etymology, definitions, page):
    """Test the sections finder and definitions getter."""
    code = page(word, "pt")
    details = parse_word(word, code, "pt", force=True)
    assert pronunciations == details.pronunciations
    assert genre == details.genre
    assert etymology == details.etymology
    assert definitions == details.definitions


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{AFI|/k/|pt}}", "/k/"),
        ("{{barra de cor|yellow|#FFFF00}}", "[RGB #FFFF00]"),
        ("{{escopo2|Informática}}", "<i>(Informática)</i>"),
        ("{{escopo2|Brasil|governo}}", "<i>(Brasil)</i>"),
        ("{{escopoCat|Árvore|pt}}", "<i>(Botânica)</i>"),
        ("{{escopoCat|Náutica|pt}}", "<i>(Náutica)</i>"),
        ("{{escopoCatLang|Alimentação|pt}}", "<i>(Culinária)</i>"),
        ("{{escopoCatLang|Verbo auxiliar|pt}}", "<i>(Verbo auxiliar)</i>"),
        ("{{escopoUso|Portugal|pt}}", "<i>(Portugal)</i>"),
        ("{{escopoUso|Coloquialismo|pt}}", "<i>(coloquialismo)</i>"),
        ("{{fem|heliostático}}", "feminino de <b>heliostático</b>"),
        ("{{fl|la|occŭlo}}", "occŭlo"),
        ("{{l|pt|usar|usar}}", "usar"),
        ("{{l.o.|jurídico|jurídica}}", "jurídica"),
        ("{{l.s.|uso}}", "uso"),
        ("{{link preto|ciconiforme}}", "ciconiforme"),
        ("{{ll|publicar}}", "publicar"),
        ("{{m|ar|شيشة|tr=šīša}}", "<i>masculino</i>"),
        ("{{mq|palavra}}", "o mesmo que <b>palavra</b>"),
        ("{{mq|word|en}}", "o mesmo que <i>word</i>"),
        ("{{PE|cu}}", "cu <sup>(português de Portugal)</sup>"),
        ("{{r|la|basium|basĭum}}", "basĭum"),
        ("{{r.l|la|utor|ūtor}}", "ūtor"),
        ("{{varort|tenu-|pt}}", "variante ortográfica de <b>tenu-</b>"),
    ],
)
def test_process_templates(wikicode, expected):
    """Test templates handling."""
    assert process_templates("foo", wikicode, "pt") == expected
