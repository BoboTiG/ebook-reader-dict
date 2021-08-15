from unittest.mock import patch

import pytest

from wikidict import check_word


def test_simple():
    assert check_word.main("fr", "vendre") == 0


def test_word_of_the_day():
    assert check_word.main("fr", "") == 0


def test_etymology_list():
    assert check_word.main("fr", "bath") == 0


def test_sublist():
    assert check_word.main("fr", "éperon") == 0


def test_subsublist():
    assert check_word.main("fr", "vache") == 0


def test_error():
    with patch.object(check_word, "contains", return_value=False):
        assert check_word.main("fr", "42") > 0


def test_no_definition_nor_etymology():
    assert check_word.main("es", "42") == 0


def test_filter_obsolete_tpl():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += "<span id='FormattingError'>bouh !</span>"
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_math_chem():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += '<span class="mwe-math-element"></span>'
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_anchors():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += '<a href="#cite">[1]</a>'
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("en", "42") == 0


def test_filter_en_nbof():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += '<span title="doubt, doubten, dought, doughten, douti, douʒte, dut, duten, duti">and other forms</span>'
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("en", "doubt") == 0


def test_filter_es():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += "<dl><dt>1 Finanzas.</dt></dl>"
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("es", "cartel") == 0


def test_filter_es_2():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += "<dl><dt>2 Coloquial</dt></dl>"
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("es", "buena") == 0


def test_filter_es_color():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<span style="color:#FFFFFF;">_____________</span><span id="ColorRect" dir="LTR" style="position:'
            " absolute; width: 1.8cm; height: 0.45cm; border: 0.50pt solid #000000; padding: 0cm; background:"
            ' #CF1020"></span>'
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("es", "lava") == 0


def test_filter_es_cite():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<a href="#cite_note-drae-1"><span class="corchete-llamada">[</span>1<span class="corchete-'
            'llamada">]</span></a>'
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("es", "urdú") == 0


def test_filter_es_cita_requerida():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<sup>[<i><a href="/wiki/Ayuda:Tutorial_(Ten_en_cuenta)#Citando_tus_fuentes" class="mw-'
            'redirect" title="Ayuda:Tutorial (Ten en cuenta)">cita&nbsp;requerida</a></i>]</sup>'
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("es", "Magdalena") == 0


def test_filter_es_external_autonumber():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<a rel="nofollow" class="external autonumber" href="http://books.google.es/books?id='
            '9nOz63haQysC&amp;pg=PA296&amp;dq=%22gesticulor%22">[1]</a>'
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("es", "gesticulación") == 0


def test_filter_fr_refnec():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += '<span><sup><i><b>Référence nécessaire</b></i></sup></span><span id="refnec"></span>'
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_fr_sources():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<span class="sources"><span class="tiret">—&nbsp;</span>(<i>Ordonnance de Louis XI pour la formation d'
            "un port et château fort à la Hague</i>)</span>"
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_fr_external_autonumber():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<a rel="nofollow" class="external autonumber" href="http://www.iupac.org/publications/pac/1994'
            '/pdf/6612x2419.pdf">[2]</a>'
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_fr_attention():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<a href="/wiki/Fichier:Twemoji12_26a0.svg" class="image" title="alt = attention"><img alt="'
            'alt = attention" src="//26a0.svg.png"></a>'
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_fr_wikispecies():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<i><a href="https://species.wikimedia.org/wiki/Panthera_leo" class="extiw" title="wikispecies'
            ':Panthera leo">Panthera leo</a></i> sur Wikispecies'
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_fr_invisible():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            'Du latin ecclésiastique<span class="invisible" style="display:none">latin <i><span class="lang-la"'
            ' lang="la"><a href="/wiki/Dalmatica#la" title="Dalmatica">Dalmatica</a></span></i></span> <i><a hr'
            'ef="/wiki/Dalmatica" title="Dalmatica">Dalmatica</a></i>'
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_fr_lien_rouge_trad():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<a href="https://en.wiktionary.org/wiki/Reconstruction:Proto-Indo-European/wemh%E2%82%81-" class="'
            'extiw" title="en:Reconstruction:Proto-Indo-European/wemh₁-"><span style="font-family:monospace;font'
            '-weight:bold;font-size:small;font-style:normal;" title="Équivalent de l’article « Reconstruction:i'
            'ndo-européen commun/*wem- » dans une autre langue">(en)</span></a>'
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


def test_filter_fr_a_preciser():
    orig = check_word.filter_html

    def new_filter_html(html: str, locale: str) -> str:
        html += (
            '<span title="Cette information a besoin d’être précisée"><small>&nbsp;<span style="color:red">('
            "information&nbsp;<i>à préciser ou à vérifier</i>)</span></small></span>"
        )
        return orig(html, locale)

    with patch.object(check_word, "filter_html", new=new_filter_html):
        assert check_word.main("fr", "42") == 0


@pytest.mark.parametrize(
    "wiktionary_text, parsed_html, ret_code, is_highlighted",
    [
        ("some text", "text", 0, False),
        ("this is orginal text", "foo bar", 1, False),
        ("this is orginal text", "originaal text", 1, True),
        ("this is orginal text", "tiis is original text", 1, False),
        ("this is orginal text", "This is original text", 1, False),
    ],
)
def test_check_highlighting(
    wiktionary_text, parsed_html, ret_code, is_highlighted, capsys
):
    error = check_word.check(wiktionary_text, parsed_html, "Test")
    assert error == ret_code
    if is_highlighted:
        stdout = capsys.readouterr()[0]
        assert "\033[31m" in stdout
