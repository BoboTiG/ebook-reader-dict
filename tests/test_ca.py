from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, genders, etymology, definitions, variants",
    [
        (
            "-ass-",
            [],
            [],
            ["Del sufix <i>-às</i> amb valor augmentatiu."],
            ["Infix que afegeix un matís augmentatiu."],
            [],
        ),
        (
            "-itzar",
            [],
            [],
            ["Del llatí <i>-izare</i>, del grec antic <i>-ίζειν</i> (<i>-ízein</i>)."],
            [
                "<i>Aplicat a un substantiu o adjectiu forma un verb que expressa la seva realització o convertir-se'n.</i>",  # noqa
            ],
            [],
        ),
        (
            "AFI",
            [],
            [],
            [],
            [
                "<i>(masculí)</i> <i>Sigles de</i> <b>Alfabet Fonètic Internacional</b>",
                "<i>(femení)</i> <i>Sigles de</i> <b>Associació Fonètica Internacional</b>",
            ],
            [],
        ),
        (
            "avui",
            [],
            [],
            [],
            ["En el dia actual.", "Metafòricament, en el present."],
            [],
        ),
        (
            "bio-",
            [],
            [],
            [],
            ['Element que entra en la composició de paraules amb el sentit de "vida".'],
            [],
        ),
        (
            "bot",
            [],
            ["m"],
            ["[1] Per la forma de bóta: del llatí vulgar <i>buttis</i> («bóta»), segle XIII."],
            [
                "Recipient de cuir, originalment de boc per a contenir vi.",
                "sac de gemecs",
                "Reclam a manera d'ocell.",
                "Peix (<i>Mola mola</i>) de la família els mòlids, de color gris i textura aspra, de cos discoïdal aplanat, però que s'unfla com un globus com a sistema de defensa.",  # noqa
                "Peix subtropical de la família dels diodòntids. (<i>Chilomycterus reticulatus</i>)",
                "<i>(peixos)</i> ballesta",
                "Salt enlaire amb un impuls ràpid.",
                "Moviment elàstic d’un cos que en topar és llançat enlaire.",
                "Embarcació petita sense coberta.",
                "<i>(informàtica)</i> Programa informàtic dissenyat per a completar tasques d’assistència, especialment quan opera com un usuari.",  # noqa
            ],
            ["botar", "botre"],
        ),
        (
            "cap",
            [],
            ["m", "mf"],
            [
                "Del llatí vulgar <i>*capu(m)</i>, variant de l’acusatiu <i>caput</i>, segle XIII. Com a adjectiu pel sentit d’«extrem, punta». Com a preposició pel sentit de «part anterior (vers un lloc)»."  # noqa
            ],
            [
                "<i>(anatomia)</i> Part superior i anterior del cos d'un animal.",
                "Part superior del cos de l'ésser humà, considerada com a seu del pensament, l'intel·lecte, judici, talent, seny.",  # noqa
                "Lloc de preferència, central.",
                "Localitat principal d'un territori; capital.",
                "La part més alta d'una cosa.",
                "Individu considerat com a membre d’una col·lectivitat.",
                "Extremitat en general.",
                (
                    "Part anterior, per on comença una cosa.",
                    "Part final, per on acaba una cosa.",
                ),
                "Part de terra que s'endinsa en la mar.",
                "<i>(nàutica)</i> corda",
                "En un repartiment, cadascun dels participants.",
                "<i>(golf)</i> Part final d'un bastó, que impacta en la bola en executar el colp.",
                "<i>(pilota basca)</i> Part més ampla d'una eina.",
                "<i>(bàdminton)</i> base",
                "Persona que ocupa el primer lloc, que mana o que dirigeix quelcom; capitost.",
                "Grau militar.",
                "<i>(negatiu)</i> Ni un.",
                "<i>(interrogatiu, condicional)</i> Algun.",
                "<i>(negatiu)</i> Gens de.",
                "<i>(interrogatiu, condicional)</i> Alguna mena de.",
                "cap a",
            ],
            ["cabre"],
        ),
        (
            "cas",
            [],
            ["m"],
            ["Del llatí <i>casus</i>."],
            [
                "Situació particular que es produeix entre les diverses possibles.",
                "Objecte d'estudi d'alguna disciplina.",
                "<i>(lingüística)</i> Categoria gramatical que marca la funció sintàctica d’un mot.",
                "Atenció, cura.",
                "Contracció entre el nom <i>casa</i> i l'article salat <i>es</i> quan és usat com un article personal. S'utilitza tant per referir-se a un habitatge com a una família. Sempre s'escriu davant de nom o de sobrenom.",  # noqa
            ],
            ["casar"],
        ),
        (
            "Castell",
            [],
            [],
            ["De <i>castell</i>."],
            [
                "Diversos topònims, especialment:",
                (
                    "Es Castell, municipi de Menorca.",
                    "Castell de l'Areny, municipi del Berguedà.",
                    "Castell de Cabres, municipi del Baix Maestrat.",
                    "Castell de Castells, municipi de la Marina Alta.",
                    "El Castell de Guadalest, municipi de la Marina Baixa.",
                    "Castell de Mur, municipi del Pallars Jussà.",
                    "Castell i Platja d'Aro, municipi del Baix Empordà.",
                    "Castell de Vernet, municipi del Conflent.",
                    "El Castell de Vilamalefa, municipi de l’Alt Millars.",
                ),
            ],
            [],
        ),
        (
            "català",
            [],
            ["m"],
            [
                "D’origen incert, paral·lel al de <i>Catalunya</i>, possiblement metàtesi del llatí <i>lacetani</i> («lacetans»)."  # noqa
            ],
            [
                "Relatiu o pertanyent a Catalunya, als seus habitants o a la llengua catalana.",
                "Relatiu o pertanyent als Països Catalans o als seus habitants.",
                "Natural de Catalunya.",
                "Natural dels Països Catalans.",
                "<i>(masculí singular)</i> Llengua històricament parlada a Catalunya, "
                "Andorra, País Valencià, les illes Balears, la Catalunya Nord, l'Alguer i la "
                "Franja de Ponent.",
                "catalanoparlant",
            ],
            [],
        ),
        (
            "ch",
            [],
            [],
            [],
            [
                "Codi de llengua ISO 639-1 del chamorro.",
                "<i>(arcaisme)</i> Especialment a final de mot, dígraf amb una consonant muda per remarcar la grafia d’una oclusiva velar sorda [k] i no pas una de sonora [ɡ].",  # noqa
            ],
            [],
        ),
        (
            "compte",
            [],
            ["m"],
            ["Del llatí <i>compŭtus</i>, segle XIII."],
            [
                "Acte de comptar.",
                "Cura, atenció.",
                "Suma de la quantitat a pagar.",
                "<i>(beisbol)</i> Acció i efecte de l'àrbitre principal de determinar el nombre de boles i strikes d'un batedor en un temps de bat.",  # noqa
                "atenció",
            ],
            ["comptar"],
        ),
        (
            "disset",
            [],
            ["m", "f"],
            ["Del llatí <i>decem et septem</i> (literalment «deu i set»)."],
            [
                "<i>(cardinal)</i> Nombre enter situat entre el setze i el divuit.",
                "<i>(valor ordinal)</i> Dissetè, dissetena.",
                "Xifra i nombre 17.",
                "Dissetena hora.",
            ],
            [],
        ),
        (
            "el",
            ["/əɫ/"],
            ["f"],
            [],
            [
                "Codi de llengua ISO 639-1 del grec modern.",
                "<i>Article determinat masculí singular que serveix per actualitzar i concretar el contingut del substantiu que acompanya.</i>",  # noqa
                'Acusatiu del masculí singular del pronom personal "ell".',
                'Substitueix el complement directe quan aquest porta l\'article "el".',
            ],
            ["ela"],
        ),
        (
            "expertes",
            [],
            [],
            [],
            [],
            ["experta"],
        ),
        ("halloweeniana", [], [], [], [], ["halloweenià"]),
        (
            "hivernacle",
            [],
            ["m"],
            ["Del llatí <i>hibernaculum</i>."],
            ["Cobert per a protegir plantes del vent o del fred extrem."],
            [],
        ),
        ("Mn.", [], [], [], ["mossèn com a tractament davant el nom"], []),
        ("PMF", [], [], [], ["<i>Sigles de</i> <b>preguntes més freqüents</b>"], []),
        ("pen", [], [], [], [], ["penar"]),
        (
            "si",
            [],
            ["m"],
            [],
            [
                "Codi de llengua ISO 639-1 del singalès.",
                "Cavitat interna del cos.",
                "<i>(per extensió)</i> Part interna d'una cosa.",
                "Setena nota musical de l'escala.",
                "<i>Forma del pronom reflexiu de tercera persona quan s'usa darrere de preposicions.</i>",
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
    code = page(word, "ca")
    details = parse_word(word, code, "ca", force=True)
    assert pronunciations == details.pronunciations
    assert genders == details.genders
    assert definitions == details.definitions
    assert etymology == details.etymology
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{AFI|/ˈwujt/}}", "/ˈwujt/"),
        ("{{claudàtors|[[milliarum]]}}", "[milliarum]"),
        ("{{color|#E01010}}", "[RGB #E01010]"),
        ("{{comp|ca|-oma}}", "sufix <i>-oma</i>"),
        ("{{doblet|ca|Castellar}}", "<i>Castellar</i>"),
        ("{{e|la|longifolius|longifolia}}", "longifolia"),
        ("{{e-propi|ca|grèvol}}", "<b>grèvol</b>"),
        ("{{IPAchar|[θ]}}", "[θ]"),
        ("{{pron|ca|/kənˈta/}}", "/kənˈta/"),
        ("{{pron|en|/əˈkrɔs/|/əˈkrɑs/}}", "/əˈkrɔs/, /əˈkrɑs/"),
        ("{{q|tenir bona planta}}", "<i>(tenir bona planta)</i>"),
        (
            "{{q|una planta|una cosa del terra}}",
            "<i>(una planta, una cosa del terra)</i>",
        ),
        ("{{romanes|XIX}}", "<span style='font-variant:small-caps'>xix</span>"),
        ("{{etim-s|ca|XIV}}", "segle XIV"),
        ("{{etim-s|ca|XVII|1617}}", "1617"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "ca") == expected
