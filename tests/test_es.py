from collections.abc import Callable

import pytest

from wikidict.render import parse_word
from wikidict.stubs import Definitions
from wikidict.utils import process_templates


@pytest.mark.parametrize(
    "word, pronunciations, etymology, definitions, variants",
    [
        (
            "-acho",
            [],
            ["Del latín <i>-acĕus</i>. De allí también <i>-áceo</i>."],
            [
                "<i>Forma aumentativos, a veces despectivos, a partir de adjetivos y sustantivos</i>.",
            ],
            [],
        ),
        (
            "bicicleta",
            [],
            [
                'Del francés <i>bicyclette</i> y este diminutivo del francés <i>bicycle</i>, formado sobre el modelo del francés <i>tricycle</i>, del latín <i>bis</i>) y <i>-cycle</i> ( del latín <i>cyclus</i>, del griego <i>κύκλος</i> (<i>kýklos</i>, "círculo; rueda")).'
            ],
            [
                "<i>(Vehículos, ciclismo)</i>: Vehículo, comúnmente de dos ruedas iguales, propulsado mediante la aplicación de la fuerza de las piernas sobre los pedales que la transmiten hacia los piñones y una cadena moviendo la rueda trasera."
            ],
            [],
        ),
        (
            "cartel",
            [],
            ["Del occitano <i>cartel</i>."],
            [
                "Lámina que se expone para dar información mediante palabras o imágenes.",
                "Prestigio.",
            ],
            [],
        ),
        (
            "comer",
            [],
            [
                'Del latín <i>comedĕre</i>, infinitivo del latín <i>comedo</i>, formado a partir <i>cum</i> ("con") y <i>edō</i> ("comer").'
            ],
            [
                "Ingerir o tomar alimentos.",
                "Tomar la principal comida del día.",
                "Malgastar bienes o recursos.",
                "Corroer o consumir.",
                "Producir comezón.",
                "<i>(Juegos)</i>: En los juegos de mesa, eliminar una pieza del contrario.",
                "Omitir elementos de información cuando se habla o escribe.",
                "Llevar encogidas algunas prendas de ropa, como los calcetines.",
                "Tener relaciones sexuales con alguien.",
            ],
            [],
        ),
        (
            "entrada",
            [],
            ["De <i>entrado</i> (<i>participio de <i>entrar</i></i>) y el sufijo flexivo <i>-a</i> para el femenino."],
            [
                "Ticket o boleto; credencial, billete o documento que autoriza a entrar en un evento, espectáculo o lugar.",
                "<i>(Gastronomía)</i>: Plato que se sirve al comienzo de la comida.",
                "<i>(Lingüística)</i>:",
                (
                    "Vocablo que titula un artículo de diccionario.",
                    "Artículo de un diccionario, enciclopedia u obra de referencia.",
                ),
                "Espacio por donde se tiene acceso a un lugar, especialmente algún edificio o propiedad.",
                "Acción o efecto de entrar a un lugar.",
                "Evento o acto que se realiza para recibir a un nuevo miembro en alguna institución, organización, empresa, cargo, empleo o dignidad.",
                "Salón, sala o estancia que se encuentra junto a la puerta principal de un edificio, especialmente un hotel o una vivienda.",
                "Oportunidad para hacer o lograr algo.",
                "Conjunto de personas que pagan por entrar a un espectáculo o evento y, por extensión, cantidad de dinero recaudado en tal evento.",
                "Comienzo de una obra de literatura, de música, etc.",
                "Amistad o acogida que recibe alguien en una familia.",
                "En ciertos juegos de naipes, acción de indicar qué cartas se guardan y por qué.",
                "Autorización para ingresar en ciertos recintos reservados, tales como oficinas, recámaras, etc., en especial de palacios o sitios de gobierno.",
                "<i>(Anatomía)</i>: Zona sin cabello en la parte superior de la frente.",
                "<i>(Comercio)</i>: Cantidad de dinero que ingresa en una caja o cuenta.",
                "<i>(Comercio)</i>: Anotación o partida en el haber que indica dinero entrante (el aumento de un activo o la disminución de un pasivo).",
                "<i>(Comercio)</i>: Cuota inicial; primer pago que se hace en la compra de algo a crédito o a plazos.",
                "<i>(Milicia)</i>: Ingreso inicial de una tropa, un enemigo, etc., en el proceso de invadir un territorio.",
                "Días iniciales de un periodo (un año, un mes, una temporada, una estación, etc.).",
                "<i>(Deporte)</i>: Enfrentamiento o pase inicial entre contrarios.",
                "<i>(Béisbol)</i>: Cada división de un partido, en que uno de los equipos tiene el turno para batear.",
                "<i>(Arquitectura)</i>: Extremo o punta de un travesaño o madero que está metido en una pared o asentado sobre una solera.",
                "<i>(Ingeniería)</i>: Turno o periodo en que trabaja un grupo de operarios.",
                "<i>(Música)</i>: Momento en que una voz o instrumento comienza a intervenir en una pieza musical.",
                "Castigo con golpes; tunda, zurra, pela.",
                "Información que se recibe en un mensaje o proceso de recibirla.",
            ],
            ["entrado"],
        ),
        (
            "extenuado",
            [],
            [],
            [
                "Cansado, debilitado.",
                "Se dice de un individuo: sin energía, debido a un gran esfuerzo físico o mental.",
            ],
            ["extenuar"],
        ),
        (
            "futuro",
            ["[fuˈtu.ɾo]"],
            [
                'Del latín <i>futūrus</i>, participio activo futuro irregular de <i>esse</i> ("ser"), y este el protoindoeuropeo <i>*bhū-</i>, <i>*bʰew-</i> ("existir", "llegar a ser").'
            ],
            [
                "Que está aún por ocurrir o hacerse efectivo.",
                "Tiempo que aún no ha llegado.",
                "<i>(Lingüística)</i>: Tiempo verbal que expresa una acción que aún no ha sido realizada.",
                "Novio o prometido de una mujer a la que va a desposar.",
            ],
            [],
        ),
        (
            "gracias",
            [],
            [],
            [
                "<i>Úsase para expresar agradecimiento</i>.",
                "<i>Irónicamente expresa desagrado, desprecio o enfado</i>.",
            ],
            [],
        ),
        (
            "hasta",
            [],
            [
                'Del castellano antiguo <i>fasta</i>, del castellano antiguo <i>hata</i>, <i>fata</i>, del árabe حتى (<i>ḥattā</i>), influido por el latín <i>ad</i> ("a") <i>ista</i> ("esta").',
            ],
            [
                "Preposición que indica el fin o término de una actividad, sea en sentido locativo, cronológico o cuantitativo.",
                "Seguida de <i>cuando</i> o de un gerundio, preposición que indica valor inclusivo.",
                "Seguida de <i>que</i>, preposición que indica valor exclusivo.",
                "Indica que pese a las circunstancias ocurre el hecho.",
                "Indica que una situación eventual o hipotética no impide que ocurra el hecho.",
                "Indica el comienzo de una acción o cuando ocurrirá.",
                "<i>Grafía obsoleta de</i> asta.",
            ],
            [],
        ),
        (
            "hocico",
            [],
            ["Del endo <i>hocicar</i>."],
            [
                "<i>(Zootomía)</i>: Parte más o menos prolongada de la cabeza de algunos animales en que están la boca y las narices.",
                "<i>(Anatomía)</i>: Hocico de una persona cuando tiene muy abultados los labios.",
                "Cara.",
                "Gesto que denota enojo o enfado.",
                "Forma despectiva para referirse a la boca de alguien.",
                "Boca de una persona, especialmente de la que dice malas palabras.",
            ],
            [],
        ),
        (
            "los",
            [],
            ["Del latín <i>illōs</i>, acusativo masculino plural del latín <i>ille</i>."],
            [
                "<i>Artículo determinado masculino plural.</i>.",
                "<i>Pronombre personal masculino de objeto directo (acusativo), tercera persona del plural.</i>.",
            ],
            [],
        ),
        (
            "Mús.",
            [],
            [],
            ["<i>Abreviatura lexicográfica convencional de la palabra</i> música."],
            [],
        ),
        (
            "ruego",
            [],
            [],
            [
                "Súplica, petición hecha con el fin de alcanzar lo que se pide.",
            ],
            ["rogar"],
        ),
        (
            "también",
            ["[tamˈbjen]"],
            ["Compuesto de <i>tan</i> y <i>bien</i>"],
            [
                "<i>Utilizado para especificar que una o varias cosas son similares, o que comparten atributos con otra previamente nombrada</i>.",
                "<i>Usado para añadir algo a lo anteriormente mencionado</i>.",
            ],
            [],
        ),
        (
            "uni-",
            [],
            ["Del latín <i>uni-</i>, del latín <i>unus</i>."],
            [
                "<i>Elemento compositivo que significa</i> uno. un único, relativo a uno solo.",
            ],
            [],
        ),
        (
            "zzz",
            [],
            [],
            [
                "Onomatopeya que representa el sonido del ronquido. Se usa para indicar que alguien está dormido.",
            ],
            [],
        ),
    ],
)
def test_parse_word(
    word: str,
    pronunciations: list[str],
    etymology: list[Definitions],
    definitions: list[Definitions],
    variants: list[str],
    page: Callable[[str, str], str],
) -> None:
    """Test the sections finder and definitions getter."""
    code = page(word, "es")
    details = parse_word(word, code, "es", force=True)
    assert pronunciations == details.pronunciations
    assert etymology == details.etymology
    assert definitions == details.definitions
    assert variants == details.variants


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        (
            "{{adjetivo de sustantivo|el mundo árabe}}",
            "Que pertenece o concierne a el mundo árabe",
        ),
        (
            "{{adjetivo de sustantivo|chamán o al chamanismo|al}}",
            "Que pertenece o concierne al chamán o al chamanismo",
        ),
        ("{{contexto|Educación}}", "<i>(Educación)</i>"),
        ("{{coord|04|39|N|74|03|O|type:country}}", "04°39′N 74°03′O"),
        ("{{diminutivo|historia}}", "<i>Diminutivo de</i> historia"),
        ("{{etimología2}}", ""),
        ("{{etimología2|...}}", ""),
        ("{{forma diminutivo|leng=es|cuchara}}", "<i>Diminutivo de</i> cuchara"),
        ("{{formatnum:22905}}", "22 905"),
        (
            "{{impropia|Utilizado para especificar...}}",
            "<i>Utilizado para especificar...</i>",
        ),
        ("{{l|es|tamo}}", "tamo"),
        ("{{l+|pt|freguesia}}", "<i>freguesia</i>"),
        ("{{neologismo|feminismo}}", "<b>Neologismo, Feminismo</b>"),
        ("{{nombre científico}}", "<sup>nombre científico</sup>"),
        ("{{plm|cansado}}", "Cansado"),
        ("{{redirección suave|protocelta}}", "<i>Véase</i> protocelta"),
        ("{{-sub|4}}", "<sub>4</sub>"),
        ("{{subíndice|5}}", "<sub>5</sub>"),
        ("{{-sup|2}}", "<sup>2</sup>"),
        ("{{superíndice|5}}", "<sup>5</sup>"),
        ("{{ucf}}", "Foo"),
        ("{{ucf|mujer}}", "Mujer"),
        ("{{variante|atiesar}}", "<i>Variante de</i> atiesar"),
        (
            "{{variante|diezmo|texto=Variante anticuada de}}",
            "<i>Variante anticuada de</i> diezmo",
        ),
        ("{{variante obsoleta|hambre}}", "<i>Variante obsoleta de</i> hambre"),
        ("{{verde|*exfollare}}", "<i>*exfollare</i>"),
    ],
)
def test_process_templates(wikicode: str, expected: str) -> None:
    """Test templates handling."""
    assert process_templates("foo", wikicode, "es") == expected
