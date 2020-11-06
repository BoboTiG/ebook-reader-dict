import pytest

from scripts.get import parse_word
from scripts.utils import clean


@pytest.mark.parametrize(
    "word, pronunciation, genre, definitions",
    [
        ("-ass-", "as", "", ["Infix que afegeix un matís augmentatiu."]),
        (
            "-itzar",
            "",
            "",
            [
                "Aplicat a un substantiu o adjectiu forma un verb que expressa la seva realització o convertir-se'n.",  # noqa
            ],
        ),
        (
            "AFI",
            "ˈa.fi",
            "",
            [
                "(<i>m</i>) Alfabet Fonètic Internacional.",
                "(<i>f</i>) Associació Fonètica Internacional.",
            ],
        ),
        ("avui", "", "", ["En el dia actual.", "Metafòricament, en el present."]),
        (
            "bio-",
            "",
            "",
            ['Element que entra en la composició de paraules amb el sentit de "vida".'],
        ),
        (
            "cap",
            "kap",
            "m",
            [
                "<i>(anatomia)</i> Part superior del cos d'un animal.",
                "Cervell.",
                "Persona que mana o dirigeix quelcom, líder.",
                "Punta, extrem, final.",
                "Part de terra que s'endinsa en el mar.",
                "Grau militar.",
                "<i>(nàutica)</i> Corda.",
                "En un repartiment, cadascun dels participants.",
                "<i>(golf)</i> Part final d'un bastó, que impacta en la bola en executar el cop.",
                "<i>(pilota basca)</i> Part més ampla d'una eina.",
                "<i>(bàdminton)</i> base",
                "<i>(negatiu)</i> Ni un.",
                "<i>(interrogatiu, condicional)</i> Algun.",
                "<i>(negatiu)</i> Gens de.",
                "<i>(interrogatiu, condicional)</i> Alguna mena de.",
                "cap a",
            ],
        ),
        (
            "cas",
            "ˈkas",
            "m",
            [
                "Situació particular que es produeix entre les diverses possibles.",
                "Objecte d'estudi d'alguna disciplina.",
                "Cadascuna de les formes que presenta una paraula segons la seva declinació, que marca la funció sintàctica.",  # noqa
                "Atenció, cura (<i>fer cas</i>).",
                "Contracció entre el nom <i>casa</i> i l'article salat <i>es</i> quan és usat com un article personal. S'utilitza tan per referir-se a un habitatge com a una família. Sempre s'escriu davant de nom o de sobrenom.",  # noqa
            ],
        ),
        (
            "Castell",
            "",
            "",
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
        ),
        (
            "català",
            "",
            "m",
            [
                "Relatiu o pertanyent a Catalunya, als seus habitants o a la llengua catalana.",
                "Relatiu o pertanyent als Països Catalans o als seus habitants.",
                "Natural de Catalunya.",
                "Natural dels Països Catalans.",
                "<i>(masculí singular)</i> Llengua històricament parlada a Catalunya, "
                "Andorra, País Valencià, les illes Balears, la Catalunya Nord, l'Alguer i la "
                "Franja de Ponent.",
            ],
        ),
        (
            "ch",
            "",
            "",
            [
                "Codi de llengua ISO 639-1 del chamorro.",
                "<i>(arcaisme)</i> Especialment a final de mot, dígraf amb una consonant muda per remarcar la grafia d’una oclusiva velar sorda [k] i no pas una de sonora [ɡ].",  # noqa
            ],
        ),
        (
            "compte",
            "",
            "m",
            [
                "Acte de comptar.",
                "Cura, atenció.",
                "Suma de la quantitat a pagar.",
                "<i>(beisbol)</i> Acció i efecte de l'àrbitre principal de determinar el nombre de boles i strikes d'un batedor en un temps de bat.",  # noqa
                "atenció",
            ],
        ),
        (
            "disset",
            "",
            "m",
            [
                "<i>(cardinal)</i> Nombre enter situat entre el setze i el divuit.",
                "<i>(valor ordinal)</i> Dissetè, dissetena.",
                "Xifra i nombre 17.",
                "Dissetena hora.",
            ],
        ),
        (
            "el",
            "əɫ",
            "f",
            [
                "Codi de llengua ISO 639-1 del grec modern.",
                "Article determinat masculí singular que serveix per actualitzar i concretar el contingut del substantiu que acompanya.",  # noqa
                'Acusatiu del masculí singular del pronom personal "ell".',
                'Substitueix el complement directe quan aquest porta l\'article "el".',
                "<i>(obsolet)</i> <i>forma alternativa de</i> <b>ela</b>",
            ],
        ),
        ("Mn.", "", "", ["mossèn com a tractament davant el nom"]),
        ("PMF", "ˌpeˈe.məˌe.fə", "", ["Preguntes Més Freqüents."]),
        ("pen", "", "", []),
        (
            "si",
            "si",
            "m",
            [
                "Codi de llengua ISO 639-1 del singalès.",
                "Cavitat interna del cos",
                "(<i>per extensió</i>) Part interna d'una cosa",
                "Setena nota musical de l'escala",
                "Forma del pronom reflexiu de tercera persona quan s'usa darrere de preposicions.",
            ],
        ),
    ],
)
def test_parse_word(word, pronunciation, genre, definitions, page):
    """Test the pronunciation, genre and definitions getters."""
    code = page(word, "ca")
    details = parse_word(word, code, "ca", force=True)
    assert pronunciation == details.pronunciation
    assert genre == details.genre
    assert definitions == details.definitions


@pytest.mark.parametrize(
    "wikicode, expected",
    [
        ("{{color|#E01010}}", "[RGB #E01010]"),
        ("{{e|la|lupus}}", "lupus"),
        (
            "{{forma-|abreujada|ca|bicicleta}}",
            "<i>forma abreujada de</i> <b>bicicleta</b>",
        ),
        ("{{forma-a|ca|Beget}}", "<i>forma alternativa de</i> <b>Beget</b>"),
        ("{{forma-pron|ca|estimar}}", "<i>forma pronominal de</i> <b>estimar</b>"),
        ("{{IPAchar|[θ]}}", "[θ]"),
        ("{{marca|ca|alguerès-verb}}", "<i>(alguerès)</i>"),
        ("{{marca|ca|fruits}}", "<i>(botànica)</i>"),
        ("{{marca|ca|plantes}}", "<i>(botànica)</i>"),
        ("{{marca|ca|interrogatiu|condicional}}", "<i>(interrogatiu, condicional)</i>"),
        ("{{marca|ca|antigament|_|en plural}}", "<i>(antigament en plural)</i>"),
        ("{{marca|ca|valencià-verb}}", "<i>(valencià)</i>"),
        ("{{marca-nocat|ca|balear}}", "<i>(balear)</i>"),
        ("{{marca-nocat|ca|occidental|balear}}", "<i>(occidental, balear)</i>"),
        ("{{q|tenir bona planta}}", "<i>(tenir bona planta)</i>"),
        ("{{q|{{m}}}}", "<i>(m.)</i>"),
        ("{{etim-s|ca|XIV}}", "segle XIV"),
    ],
)
def test_clean_template(wikicode, expected):
    """Test templates handling."""
    assert clean("foo", wikicode, "ca") == expected
