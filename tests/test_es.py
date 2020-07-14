import pytest

from scripts.get import parse_word
from scripts.utils import clean


@pytest.mark.parametrize(
    "word, pronunciation, genre, definitions",
    [
        (
            "-acho",
            "ˈa.t͡ʃo",
            "",
            [
                "<i>Forma aumentativos, a veces despectivos, a partir de adjetivos y sustantivos</i>.",
            ],
        ),
        (
            "cartel",
            "",
            "",
            [
                "Lámina que se expone para dar información mediante palabras o imágenes.",
                "Prestigio.",
            ],
        ),
        (
            "comer",
            "koˈmeɾ",
            "",
            [
                "Ingerir o tomar alimentos.",
                "Tomar la principal comida del día.",
                "Malgastar bienes o recursos.",
                "Corroer o consumir.",
                "Producir comezón.",
                "<i>(Juego)</i>: En los juegos de mesa, eliminar una pieza del contrario.",
                "Omitir elementos de información cuando se habla o escribe.",
                "Llevar encogidas algunas prendas de ropa, como los calcetines.",
                "Tener relaciones sexuales con alguien.",
            ],
        ),
        (
            "es decir",
            "es.ðeˈθiɾ",
            "",
            [
                "<i>Úsase para introducir una aclaración, explicación o definición de lo precedente</i>",
            ],
        ),
        (
            "extenuado",
            "eks.teˈnwa.ðo",
            "",
            [
                "Cansado, debilitado.",
                "Se dice de un individuo: sin energía, debido a un gran esfuerzo físico o mental.",
            ],
        ),
        (
            "futuro",
            "fuˈtu.ɾo",
            "",
            [
                "Que está aún por ocurrir o hacerse efectivo.",
                "Tiempo que aún no ha llegado.",
                "<i>(Lingüística)</i>: Tiempo verbal que expresa una acción que aún no ha sido realizada.",
                "Novio o prometido de una mujer a la que va a desposar. <i>El femenino es</i> futura.",
            ],
        ),
        (
            "gracias",
            "ˈgɾa.θjas",
            "",
            [
                "<i>Úsase para expresar agradecimiento</i>.",
                "<i>Irónicamente expresa desagrado, desprecio o enfado</i>",
            ],
        ),
        (
            "hasta",
            "ˈas.ta",
            "",
            [
                "Preposición que indica el fin o término de una actividad, sea en sentido locativo, cronológico o cuantitativo.",  # noqa
                "Seguida de <i>cuando</i> o de un gerundio, preposición que indica valor inclusivo.",
                "Seguida de <i>que</i>, preposición que indica valor exclusivo.",
                "Indica que pese a las circunstancias ocurre el hecho.",
                "Indica que una situación eventual o hipotética no impide que ocurra el hecho.",
                "Indica el comienzo de una acción o cuando ocurrirá.",
                "<i>Grafía obsoleta de</i> asta.",
            ],
        ),
        (
            "los",
            "",
            "",
            [
                "<i>Artículo determinado masculino plural.</i>",
                "<i>Pronombre personal masculino de objeto directo (acusativo), tercera persona del plural.</i>",
            ],
        ),
        (
            "Mús.",
            "",
            "",
            ["<i>Abreviatura lexicográfica convencional de la palabra</i> música"],
        ),
        (
            "también",
            "tamˈbjen",
            "",
            [
                "<i>Utilizado para especificar que una o varias cosas son similares, o que comparten atributos con otra previamente nombrada</i>.",  # noqa
                "<i>Usado para añadir algo a lo anteriormente mencionado</i>.",
            ],
        ),
        (
            "uni-",
            "ˈu.ni",
            "",
            [
                "<i>Elemento compositivo que significa</i> uno. un único, relativo a uno solo.",
            ],
        ),
        (
            "zzz",
            "",
            "",
            [
                "Onomatopeya que representa el sonido del ronquido. Se usa para indicar que alguien está dormido.",
            ],
        ),
    ],
)
def test_find_sections_and_definitions(word, pronunciation, genre, definitions, page):
    """Test the sections finder and definitions getter."""
    code = page(word, "es")
    details = parse_word(word, code, "es", force=True)
    assert pronunciation == details.pronunciation
    assert genre == details.genre
    assert definitions == details.definitions


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        (
            "{{adjetivo de sustantivo|el mundo árabe}}",
            "Que pertenece o concierne a el mundo árabe",
        ),
        ("{{Anatomía|y|Zootomía}}", "<i>(Anatomía y Zootomía)</i>"),
        (
            "{{Angiología|Endocrinología|Fisiología|Medicina}}",
            "<i>(Angiología, Endocrinología, Fisiología, Medicina)</i>",
        ),
        ("{{Arqueología}}", "<i>(Arqueología)</i>"),
        ("{{Arqueología|y|Geología}}", "<i>(Arqueología y Geología)</i>"),
        ("{{contexto|Educación}}", "<i>(Educación)</i>"),
        ("{{contracción|de|ellas|leng=es}}", "<i>Contracción de</i> de <i>y</i> ellas"),
        ("{{coord|04|39|N|74|03|O|type:country}}", "04°39′N 74°03′O"),
        ("{{diminutivo|historia}}", "<i>Diminutivo de</i> historia"),
        ("{{física}}", "<i>(Física)</i>"),
        ("{{física|óptica}}", "<i>(Física, Óptica)</i>"),
        ("{{forma diminutivo|leng=es|cuchara}}", "<i>Diminutivo de</i> cuchara"),
        ("{{gentilicio|Cataluña}}", "Originario, relativo a, o propio de Cataluña"),
        ("{{gentilicio1|Alemania}}", "Originario, relativo a, o propio de Alemania"),
        ("{{gentilicio2|Alemania}}", "Persona originaria de Alemania"),
        ("{{grafía|psicológico}}", "<i>Grafía alternativa de</i> <b>psicológico</b>"),
        ("{{grafía informal|al tiro}}", "<i>Grafía informal de</i> al tiro"),
        ("{{grafía obsoleta|asta}}", "<i>Grafía obsoleta de</i> asta"),
        ("{{grafía rara|exudar}}", "<i>Grafía poco usada de</i> exudar"),
        (
            "{{impropia|Utilizado para especificar...}}",
            "<i>Utilizado para especificar...</i>",
        ),
        ("{{l|es|tamo}}", "tamo"),
        ("{{l+|pt|freguesia}}", "<i>freguesia</i>"),
        ("{{moluscos}}", "<i>(Zoología)</i>"),
        ("{{moluscos|y|alimentos}}", "<i>(Zoología y Gastronomía)</i>"),
        ("{{psicología}}", "<i>(Psicología)</i>"),
        ("{{nombre científico}}", "<sup>nombre científico</sup>"),
        ("{{plm|cansado}}", "Cansado"),
        ("{{psicología|lgbt}}", "<i>(Psicología, LGBT)</i>"),
        ("{{redirección suave|protocelta}}", "<i>Véase</i> protocelta"),
        ("{{-sub|4}}", "<sub>4</sub>"),
        ("{{subíndice|5}}", "<sub>5</sub>"),
        ("{{sustantivo de adjetivo|urgente}}", "Condición o carácter de urgente"),
        (
            "{{sustantivo de adjetivo|abad|abadesa}}",
            "Condición o carácter de abad o abadesa",
        ),
        ("{{sustantivo de verbo|circular}}", "Acción o efecto de circular"),
        ("{{-sup|2}}", "<sup>2</sup>"),
        ("{{superlativo|abundante}}", "<i>Superlativo de</i> abundante"),
        ("{{ucf|mujer}}", "Mujer"),
        ("{{variante|atiesar}}", "<i>Variante de</i> atiesar"),
        (
            "{{variante|diezmo|texto=Variante anticuada de}}",
            "<i>Variante anticuada de</i> diezmo",
        ),
        ("{{variante obsoleta|hambre}}", "<i>Variante obsoleta de</i> hambre"),
    ],
)
def test_clean_template(wikicode, expected):
    """Test templates handling."""
    assert clean("foo", wikicode, "es") == expected
