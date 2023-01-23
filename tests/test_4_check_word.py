from threading import Lock
from typing import Any, Callable
from unittest.mock import patch

import pytest
import responses
from requests.exceptions import RequestException
from requests.models import Response

from wikidict import check_word

# Word used in test_filter_html()
WORD = {
    "ca": "pelegrí",
    "de": "volley",
    "en": "42",
    "es": "buena",
    "fr": "42",
    "it": "Upupidi",
    "pt": "-izar",
}


@pytest.fixture
def craft_urls(
    html: Callable[[str, str], str], page: Callable[[str, str], str]
) -> Callable[[str, str], str]:
    def _craft_urls(locale: str, word: str) -> str:
        responses.add(
            responses.GET,
            check_word.craft_url(word, locale, raw=True),
            body=page(word, locale),
        )
        responses.add(
            responses.GET,
            check_word.craft_url(word, locale),
            body=html(word, locale),
        )
        return word

    return _craft_urls


@pytest.fixture
def craft_urls_with_body() -> Callable[[str, str, str], str]:
    def _craft_urls(locale: str, word: str, body: str) -> str:
        responses.add(
            responses.GET,
            check_word.craft_url(word, locale, raw=True),
            body=body,
        )
        responses.add(
            responses.GET,
            check_word.craft_url(word, locale),
            body=body,
        )
        return word

    return _craft_urls


@responses.activate
def test_simple(craft_urls: Callable[[str, str], str]) -> None:
    craft_urls("fr", "42")
    assert check_word.main("fr", "42") == 0


def test_word_of_the_day() -> None:
    assert check_word.main("fr", "") == 0


@responses.activate
def test_etymology_list(craft_urls: Callable[[str, str], str]) -> None:
    craft_urls("fr", "bath")
    assert check_word.main("fr", "bath") == 0


@responses.activate
def test_sublist(craft_urls: Callable[[str, str], str]) -> None:
    craft_urls("fr", "éperon")
    assert check_word.main("fr", "éperon") == 0


@responses.activate
def test_subsublist(craft_urls: Callable[[str, str], str]) -> None:
    craft_urls("fr", "base")
    assert check_word.main("fr", "base") == 0


@responses.activate
def test_error_and_lock(craft_urls: Callable[[str, str], str]) -> None:
    craft_urls("fr", "42")
    with patch.object(check_word, "contains", return_value=False):
        assert check_word.main("fr", "42") > 0
        lock = Lock()
        assert check_word.check_word("42", "fr", lock=lock) > 0


@responses.activate
def test_no_definition_nor_etymology(craft_urls: Callable[[str, str], str]) -> None:
    craft_urls("fr", "<vide>")
    assert check_word.main("fr", "<vide>") == 0


@pytest.mark.parametrize(
    "locale, body, expected",
    [
        # CA - {{sense accepcions}}
        [
            "ca",
            '<i>a aquesta paraula li falten les accepcions o significats. Podeu <span class="plainlinks"><a class="external text" href="https://ca.wiktionary.org/w/index.php?title=pelegr%C3%AD&amp;action=edit">ajudar</a></span> el Viccionari incorporant-los</i>.',  # noqa
            "",
        ],
        # DE - other Wikis
        [
            "de",
            '<a href="https://en.wiktionary.org/wiki/Special:Search/volley" class="extiw" title="en:Special:Search/volley"><sup class="dewikttm">→&nbsp;en</sup></a>',  # noqa
            "",
        ],
        # DE - Wikipedia: WP template
        [
            "de",
            '<a href="https://de.wikipedia.org/wiki/Datenkompression" class="extiw" title="w:Datenkompression"><sup>→&nbsp;WP</sup></a>',  # noqa
            "",
        ],
        # DE - grey sup link
        [
            "de",
            '<sup style="color:slategray;">→&nbsp;grc</sup>',
            "",
        ],
        # EN - and other forms
        [
            "en",
            '<span title="doubt, doubten, dought, doughten, douti, douʒte, dut, duten, duti">and other forms</span>',
            "and other forms doubt, doubten, dought, doughten, douti, douʒte, dut, duten, duti",
        ],
        # EN - anchors
        [
            "en",
            '<a class="mw-jump-link" href="#mw-head">Jump to navigation</a>',
            "",
        ],
        # ES - 2 Historia. --> (Historia)
        [
            "es",
            "<dl><dt>1 Finanzas.</dt></dl>",
            "1 (Finanzas):",
        ],
        # ES - 2 Coloquial: --> (Coloquial):
        [
            "es",
            "<dl><dt>2 Coloquial</dt></dl>",
            "2 (Coloquial): 2 Coloquial:",
        ],
        # ES
        [
            "es",
            "</dl><dl><dt>3 Coloquial</dt><dd>Úsase.</dd>",
            "3(Coloquial):Úsase.3Coloquial:Úsase.",
        ],
        # ES - cita requerida
        [
            "es",
            (
                '<sup>[<i><a href="/wiki/Ayuda:Tutorial_(Ten_en_cuenta)#Citando_tus_fuentes" class="mw-'
                'redirect" title="Ayuda:Tutorial (Ten en cuenta)">cita&nbsp;requerida</a></i>]</sup>'
            ),
            "",
        ],
        # ES - cite
        [
            "es",
            (
                '<a href="#cite_note-drae-1"><span class="corchete-llamada">[</span>1<span class="corchete-'
                'llamada">]</span></a>'
            ),
            "",
        ],
        # ES - color
        [
            "es",
            (
                '<span style="color:#FFFFFF;">_____________</span><span id="ColorRect" dir="LTR" style="position:'
                " absolute; width: 1.8cm; height: 0.45cm; border: 0.50pt solid #000000; padding: 0cm; background:"
                ' #CF1020"></span>'
            ),
            "[RGB #CF1020]",
        ],
        # ES - external autonumber
        [
            "es",
            (
                '<a rel="nofollow" class="external autonumber" href="http://books.google.es/books?id='
                '9nOz63haQysC&amp;pg=PA296&amp;dq=%22gesticulor%22">[1]</a>'
            ),
            "",
        ],
        # FR - anchors
        [
            "fr",
            '<a href="#cite">[1]</a>',
            "",
        ],
        # FR - attention
        [
            "fr",
            (
                '<a href="/wiki/Fichier:Twemoji12_26a0.svg" class="image" title="alt = attention"><img alt="'
                'alt = attention" src="//26a0.svg.png"></a>'
            ),
            "⚠",
        ],
        # FR - à préciser
        [
            "fr",
            (
                '<span title="Cette information a besoin d’être précisée"><small>&nbsp;<span style="color:red">('
                "information&nbsp;<i>à préciser ou à vérifier</i>)</span></small></span>"
            ),
            "",
        ],
        # FR - external autonumber
        [
            "fr",
            (
                '<a rel="nofollow" class="external autonumber" href="http://www.iupac.org/publications/pac/1994'
                '/pdf/6612x2419.pdf">[2]</a>'
            ),
            "",
        ],
        # FR - invisible
        [
            "fr",
            (
                'Du latin ecclésiastique<span class="invisible" style="display:none">latin <i><span class="lang-la"'
                ' lang="la"><a href="/wiki/Dalmatica#la" title="Dalmatica">Dalmatica</a></span></i></span> <i><a hr'
                'ef="/wiki/Dalmatica" title="Dalmatica">Dalmatica</a></i>'
            ),
            "Du latin ecclésiastique Dalmatica",
        ],
        # FR - lien rouge trad
        [
            "fr",
            (
                '<a href="https://en.wiktionary.org/wiki/Reconstruction:Proto-Indo-European/wemh%E2%82%81-" class="'
                'extiw" title="en:Reconstruction:Proto-Indo-European/wemh₁-"><span style="font-family:monospace;font'
                '-weight:bold;font-size:small;font-style:normal;" title="Équivalent de l’article « Reconstruction:i'
                'ndo-européen commun/*wem- » dans une autre langue">(en)</span></a>'
            ),
            "",
        ],
        # FR - math chem
        [
            "fr",
            '<span class="mwe-math-element"></span>',
            "",
        ],
        # FR - obsolete tpl
        [
            "fr",
            "<span id='FormattingError'>bouh !</span>",
            "",
        ],
        # FR - ref nec
        [
            "fr",
            '<span><sup><i><b>Référence nécessaire</b></i></sup></span><span id="refnec"></span>',
            "",
        ],
        # FR - sources
        [
            "fr",
            (
                '<span class="sources"><span class="tiret">—&nbsp;</span>(<i>Ordonnance de Louis XI pour la formation d'
                "un port et château fort à la Hague</i>)</span>"
            ),
            "",
        ],
        # FR - Wikidata
        [
            "fr",
            (
                '<a href="https://www.wikidata.org/wiki/Q30092597" class="extiw" title="d:Q30092597">Frederick H. '
                '<span class="petites_capitales" style="font-variant: small-caps">Pough</span></a> dans la base de'
                ' données Wikidata <img alt="Wikidata-logo.svg" src="//upload.wikimedia.org/wikipedia/commons/thu'
                'mb/f/ff/Wikidata-logo.svg/20px-Wikidata-logo.svg.png" decoding="async" width="20" height="11" src'
                'set="//upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Wikidata-logo.svg/30px-Wikidata-logo.svg'
                ".png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Wikidata-logo.svg/40px-Wikidata-lo"
                'go.svg.png 2x" data-file-width="1050" data-file-height="590" />'
            ),
            "Frederick H. Pough",
        ],
        # FR - Wikispecies
        [
            "fr",
            (
                '<i><a href="https://species.wikimedia.org/wiki/Panthera_leo" class="extiw" title="wikispecies'
                ':Panthera leo">Panthera leo</a></i> sur Wikispecies'
            ),
            "Panthera leo",
        ],
        # IT - numbered external links
        [
            "it",
            '<a class="external autonumber" href="https://it.wikipedia.org/wiki/Scomber_scombrus">[1]</a>',  # noqa
            "",
        ],
        # IT - missing definition
        [
            "it",
            '<i>definizione mancante; se vuoi, <span class="plainlinks"><a class="external text" href="https://it.wiktionary.org/w/index.php?title=Upupidi&amp;action=edit">aggiungila</a></span> tu</i>',  # noqa
            "",
        ],
        # IT - <ref>
        [
            "it",
            '<sup id="cite_ref-1" class="reference"><a href="[#cite_note-1](view-source:https://it.wiktionary.org/wiki/autocrinia#cite_note-1)">[1]</a>',  # noqa
            "",
        ],
        # IT - Wikipedia
        [
            "it",
            '<small>&nbsp;(<a href="/wiki/File:Wikipedia-logo-v2.svg" class="image" title="Wikipedia"><img alt="Wikipedia" src="//upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/20px-Wikipedia-logo-v2.svg.png" decoding="async" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/30px-Wikipedia-logo-v2.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/40px-Wikipedia-logo-v2.svg.png 2x" data-file-width="103" data-file-height="94" width="20" height="18"></a> <b><a href="https://it.wikipedia.org/wiki/Banda_(araldica)" class="extiw" title="w:Banda (araldica)">approfondimento</a></b>)</small>',  # noqa
            "",
        ],
        # IT - Wikispecies
        [
            "it",
            '(<img alt="Wikispecies" src="//upload.wikimedia.org/wikipedia/commons/thumb/d/d9/WikiSpecies.svg/20px-WikiSpecies.svg.png" decoding="async" title="Wikispecies" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/d/d9/WikiSpecies.svg/30px-WikiSpecies.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/d/d9/WikiSpecies.svg/40px-WikiSpecies.svg.png 2x" data-file-width="125" data-file-height="177" width="20" height="28"> <b><a href="https://species.wikimedia.org/wiki/Aegypiinae" class="extiw" title="wikispecies:Aegypiinae">tassonomia</a></b>)',  # noqa
            "",
        ],
        # IT - Wikispecies (ensure next siblings are kept)
        [
            "it",
            '(<img alt="Wikispecies" src="//upload.wikimedia.org/wikipedia/commons/thumb/d/d9/WikiSpecies.svg/20px-WikiSpecies.svg.png" decoding="async" title="Wikispecies" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/d/d9/WikiSpecies.svg/30px-WikiSpecies.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/d/d9/WikiSpecies.svg/40px-WikiSpecies.svg.png 2x" data-file-width="125" data-file-height="177" width="20" height="28"> <b><a href="https://species.wikimedia.org/wiki/Aegypiinae" class="extiw" title="wikispecies:Aegypiinae">tassonomia</a></b>);',  # noqa
            ";",
        ],
        # PT - superscript locales
        [
            "pt",
            '<sup>(<a class="extiw" href="https://la.wiktionary.org/wiki/izare" title="la:izare"><span style="letter-spacing:1px" title="ver no Wikcionário em latim">la</span></a>)</sup>',  # noqa
            "",
        ],
        # PT - no print
        [
            "pt",
            '<span class="noprint"><a class="extiw" href="https://sr.wiktionary.org/wiki/%D0%88%D1%83%D0%B3%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D0%B8%D1%98%D0%B0" title="sr:Југославија"><sup><span style="letter-spacing:1px" title="Clique aqui para ver “Југославија” no Wikcionário em sérvio">(sr)</span></sup></a></span>',  # noqa
            "",
        ],
        # PT - keep anchors
        ["pt", '<a href="#Adjetivo">ainu</a>', "ainu"],
        # PT - external links
        [
            "pt",
            '<small>(<a href="https://la.wiktionary.org/wiki/aer" class="extiw" title="la:aer">ver no Wikcionário em Latim</a>)</small>',  # noqa
            "",
        ],
    ],
)
@responses.activate
def test_filter_html(
    locale: str,
    body: str,
    expected: str,
    craft_urls_with_body: Callable[[str, str, str], str],
) -> None:
    word = craft_urls_with_body(locale, WORD[locale], body)
    assert check_word.filter_html(body, locale) == expected.replace(" ", "")
    assert check_word.main(locale, word) == 0


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
    wiktionary_text: str,
    parsed_html: str,
    ret_code: int,
    is_highlighted: bool,
    capsys: pytest.CaptureFixture[Any],
) -> None:
    error = check_word.check(wiktionary_text, parsed_html, "Test")
    assert error == ret_code
    if is_highlighted:
        stdout = capsys.readouterr()[0]
        assert "\033[31m" in stdout


def test_get_url_content_timeout_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def get(*_: Any, **__: Any) -> None:
        raise TimeoutError()

    monkeypatch.setattr("wikidict.check_word.SLEEP_TIME", 0.01)
    monkeypatch.setattr("requests.get", get)
    with pytest.raises(RuntimeError):
        check_word.get_url_content("https://...")


def test_get_url_content_too_many_requests_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def get(*_: Any, **__: Any) -> None:
        response = Response()
        response.status_code = 429
        response.headers["retry-after"] = "1"
        raise RequestException(response=response)

    monkeypatch.setattr("wikidict.check_word.SLEEP_TIME", 0.01)
    monkeypatch.setattr("requests.get", get)
    with pytest.raises(RuntimeError):
        check_word.get_url_content("https://...")
