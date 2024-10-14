"""Utilities for internal use."""

import logging
import os
import re
from collections import defaultdict, namedtuple
from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime
from functools import partial
from pathlib import Path

import regex
import requests
import wikitextparser

from . import svg
from .constants import (
    DOWNLOAD_URL_DICTFILE,
    DOWNLOAD_URL_DICTORGFILE,
    DOWNLOAD_URL_KOBO,
    DOWNLOAD_URL_STARDICT,
    WIKIMEDIA_HEADERS,
    WIKIMEDIA_URL_MATH_CHECK,
    WIKIMEDIA_URL_MATH_RENDER,
)
from .hiero_utils import render_hiero
from .lang import (
    last_template_handler,
    release_description,
    templates_ignored,
    templates_italic,
    templates_multi,
    templates_other,
    thousands_separator,
)
from .user_functions import *  # noqa: F403

# Magic words (small part, only data/time related)
# https://www.mediawiki.org/wiki/Help:Magic_words
NOW = datetime.now(tz=UTC)
MAGIC_WORDS = {
    "CURRENTYEAR": str(NOW.year),
    "CURRENTMONTH": NOW.strftime("%m"),
    "CURRENTMONTH1": str(NOW.month),
    "CURRENTDAY": str(NOW.day),
    "CURRENTDAY2": NOW.strftime("%d"),
    "CURRENTDOW": NOW.strftime("%w"),
    "CURRENTTIME": NOW.strftime("%H:%M"),
    "CURRENTHOUR": NOW.strftime("%H"),
    "CURRENTWEEK": NOW.strftime("%V"),
    "CURRENTTIMESTAMP": NOW.strftime("%Y%m%d%H%M%S"),
}

# Templates needed to be kept after transform()
Template = namedtuple("Template", "placeholder value")
SPECIAL_TEMPLATES = {
    "{{!}}": Template("##pipe##!##pipe##", "|"),
    "{{=}}": Template("##equal##!##equal##", "="),
}

# subtitution for double curly parenthesis
OPEN_DOUBLE_CURLY = "##opendoublecurly##"
CLOSE_DOUBLE_CURLY = "##closedoublecurly##"

log = logging.getLogger(__name__)


def check_for_missing_templates() -> bool:
    from .render import MISSING_TEMPLATES

    if not (missing_templates := list(MISSING_TEMPLATES)):
        return False

    missings_counts: dict[str, int] = defaultdict(int)
    missings: dict[str, set[str]] = defaultdict(set)
    for tpl, word in missing_templates:
        missings_counts[tpl] += 1
        missings[tpl].add(word)
    for tpl, _ in sorted(missings_counts.items(), key=lambda x: x[1], reverse=True):
        words = sorted(missings[tpl])
        log.warning(
            "Missing %r template support (%s times), example in: %s",
            tpl,
            f"{len(words):,}",
            ", ".join(f'"{word}"' for word in words[:3]),
        )
    log.warning("Unhandled templates count: %s", f"{len(missings_counts):,}")
    return True


def process_special_pipe_template(text: str) -> str:
    splitter = SPECIAL_TEMPLATES["{{!}}"].placeholder
    if splitter in text:
        text = text.split(splitter)[1]
    return text


def convert_gender(genders: list[str]) -> str:
    """Return the HTML code to include for gender(s) of a word."""
    if not genders:
        return ""
    genders = [f"<i>{gender}</i>" for gender in genders]
    return f" {', '.join(genders)}."


def convert_pronunciation(pronunciations: list[str]) -> str:
    """Return the HTML code to include for pronunciation(s) of a word."""
    return f" {', '.join(pronunciations)}" if pronunciations else ""


def get_random_word(locale: str) -> str:
    """Retrieve a random word."""
    url = f"https://{locale}.wiktionary.org/w/api.php?action=query&list=random&format=json"
    with requests.get(url) as req:
        word = str(req.json()["query"]["random"][0]["title"])

    if "CI" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "ab") as fh:
            fh.write(f"word={word}\n".encode())

    return word


def format_description(locale: str, output_dir: Path) -> str:
    """Generate the release description."""

    # Get the words count
    words_count = (output_dir / "words.count").read_text().strip()

    # Format the words count
    thousands_sep = thousands_separator[locale]
    words_count = f"{int(words_count):,}".replace(",", thousands_sep)

    # Format the snapshot's date
    dump_date = (output_dir / "words.snapshot").read_text().strip()
    dump_date = f"{dump_date[:4]}-{dump_date[4:6]}-{dump_date[6:8]}"

    download_links_full = f"""
- [Kobo]({DOWNLOAD_URL_KOBO.format(locale, "")}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({DOWNLOAD_URL_STARDICT.format(locale, "")}) (dict-{locale}-{locale}.zip)
- [DictFile]({DOWNLOAD_URL_DICTFILE.format(locale, "")}) (dict-{locale}-{locale}.df.bz2)
- [DICT.org]({DOWNLOAD_URL_DICTORGFILE.format(locale, "")}) (dictorg-{locale}-{locale}.zip)
""".strip()
    download_links_noetym = f"""
- [Kobo]({DOWNLOAD_URL_KOBO.format(locale, "-noetym")}) (dicthtml-{locale}-{locale}-noetym.zip)
- [StarDict]({DOWNLOAD_URL_STARDICT.format(locale, "-noetym")}) (dict-{locale}-{locale}-noetym.zip)
- [DictFile]({DOWNLOAD_URL_DICTFILE.format(locale, "-noetym")}) (dict-{locale}-{locale}-noetym.df.bz2)
- [DICT.org]({DOWNLOAD_URL_DICTORGFILE.format(locale, "-noetym")}) (dictorg-{locale}-{locale}-noetym.zip)
""".strip()

    creation_date = NOW.isoformat()
    return release_description[locale].format(**locals())


def guess_prefix(word: str) -> str:
    """Determine the word prefix for the given *word*.

    Inspiration: https://github.com/pettarin/penelope/blob/master/penelope/prefix_kobo.py#L16
    Inspiration: https://pgaskin.net/dictutil/dicthtml/prefixes.html
    Inspiration: me ᕦ(ò_óˇ)ᕤ

    Note: for words like "°GL", the Kobo will first check "11.html" and then "gl.html",
          so to speed-up the lookup, let's store such words into "11.html".

    Here are some debug logs to help understand what Kobo does:

        (dictionary.debug) got alternative search terms: "°GL", "°gl", "GL" for word "°GL"
        (ui.debug) static QByteArray Unzipper::extractFile() "/mnt/onboard/.kobo/dict/dicthtml-fr.zip", "11.html")

        (dictionary.debug) got alternative search terms: "X temps", "x temps", "X TEMPS", "Xtemps" for word "X temps"
        (ui.debug) static QByteArray Unzipper::extractFile("/mnt/onboard/.kobo/dict/dicthtml-fr.zip", "xa.html")

        (dictionary.debug) got alternative search terms: "A/cm2", "a/cm2", "A/CM2", "Acm2" for word "A/cm2"
        (ui.debug) static QByteArray Unzipper::extractFile("/mnt/onboard/.kobo/dict/dicthtml-fr.zip", "11.html")

        (dictionary.debug) got alternative search terms: ".vi", ".VI", "vi" for word ".vi"
        (ui.debug) static QByteArray Unzipper::extractFile("/mnt/onboard/.kobo/dict/dicthtml-fr.zip", "11.html")

        >>> guess_prefix("test")
        'te'
        >>> guess_prefix("a")
        'aa'
        >>> guess_prefix("aa")
        'aa'
        >>> guess_prefix("aaa")
        'aa'
        >>> guess_prefix("Èe")
        'èe'
        >>> guess_prefix("multiple words")
        'mu'
        >>> guess_prefix("àççèñts")
        'àç'
        >>> guess_prefix("à")
        'àa'
        >>> guess_prefix("ç")
        'ça'
        >>> guess_prefix("")
        '11'
        >>> guess_prefix(" ")
        '11'
        >>> guess_prefix(" x")
        'xa'
        >>> guess_prefix(" 123")
        '11'
        >>> guess_prefix("42")
        '11'
        >>> guess_prefix("x 23")
        'xa'
        >>> guess_prefix("дaд")
        'дa'
        >>> guess_prefix("未未")
        '11'
        >>> guess_prefix("未")
        '11'
        >>> guess_prefix(" 未")
        '11'
        >>> guess_prefix(".vi")
        '11'
        >>> guess_prefix("/aba")
        '11'
        >>> guess_prefix("a/b")
        '11'
        >>> guess_prefix("’alif")
        '11'
        >>> guess_prefix("°GL")
        '11'
        >>> guess_prefix("وهيبة")
        '11'
    """
    prefix = word.strip()[:2].lower().strip()
    if not prefix or prefix[0].isnumeric():
        return "11"
    return prefix.ljust(2, "a") if all(c.isalpha() and c.islower() for c in prefix) else "11"


def clean(text: str, locale: str = "en") -> str:
    r"""Cleans up the provided Wikicode.
    Removes templates, tables, parser hooks, magic words, HTML tags and file embeds.
    Keeps links.
    Source: https://github.com/macbre/mediawiki-dump/blob/3f1553a/mediawiki_dump/tokenizer.py#L8

        >>> clean(r"<math>x \in ]x_0 - \epsilon, x_0[</math> och <math>f(x) > f(x_0)</math> för alla <math>x \in ]x_0, x_0 + \epsilon[</math>")
        '<math>x \\in ]x_0 - \\epsilon, x_0[</math> och <math>f(x) > f(x_0)</math> för alla <math>x \\in ]x_0, x_0 + \\epsilon[</math>'

        >>> clean("{{Lien web|url=http://stella.atilf.fr/few/|titre=Französisches Etymologisches Wörterbuch}}")
        '{{Lien web|url=http://stella.atilf.fr/few/|titre=Französisches Etymologisches Wörterbuch}}'
        >>> clean("d'<nowiki/>''Arvernus'', surnom ethnique, ou composé d'''are''")
        "d'<i>Arvernus</i>, surnom ethnique, ou composé d'<i>are</i>"
        >>> clean("<ref name=oed/>Modelled<ref>Gerhard</ref> English<ref name=oed>Press.</ref>")
        'Modelled English'

        >>> clean("")
        ''
        >>> clean("<span style='color:black'>[[♣]]</span>")
        "<span style='color:black'>♣</span>"
        >>> clean("<ref>{{Import:CFC}}</ref>")
        ''
        >>> clean("<ref>{{Import:CFC}}</ref>bla bla bla <ref>{{Import:CFC}}</ref>")
        'bla bla bla'
        >>> clean("<ref>{{Lit-Pfeifer: Etymologisches Wörterbuch|A=8}}, Seite 1551, Eintrag „Wein“<br />siehe auch: {{Literatur | Online=zitiert nach {{GBS|uEQtBgAAQBAJ|PA76|Hervorhebung=Wein}} | Autor=Corinna Leschber| Titel=„Wein“ und „Öl“ in ihren mediterranen Bezügen, Etymologie und Wortgeschichte | Verlag=Frank & Timme GmbH | Ort= | Jahr=2015 | Seiten=75–81 | Band=Band 24 von Forum: Rumänien, Culinaria balcanica, herausgegeben von Thede Kahl, Peter Mario Kreuter, Christina Vogel | ISBN=9783732901388}}.")
        ''
        >>> clean('<ref name="CFC" />')
        ''
        >>> clean('<ref name="CFC">{{Import:CFC}}</ref>')
        ''
        >>> clean('<ref name="CFC">{{CFC\\n|foo}}</ref>')
        ''
        >>> clean("<ref>D'après ''Dictionnaire du tapissier : critique et historique de l’ameublement français, depuis les temps anciens jusqu’à nos jours'', par J. Deville, page 32 ({{Gallica|http://gallica.bnf.fr/ark:/12148/bpt6k55042642/f71.image}})</ref>")
        ''
        >>> clean("<ref>")
        ''
        >>> clean("</ref>")
        ''
        >>> clean("''italic''")
        '<i>italic</i>'
        >>> clean("'''strong'''")
        '<b>strong</b>'
        >>> clean("''italic and '''strong'''''")
        '<i>italic and <b>strong</b></i>'
        >>> clean("'''strong and ''italic'''''")
        '<b>strong and <i>italic</b></i>'
        >>> clean("'''''Parer à'''''")
        '<i><b>Parer à</b></i>'
        >>> clean("''Contraction de [[préposition]] ''[[à]]'' et de l'[[article]] défini ''[[les]]'' .''")
        "<i>Contraction de préposition </i>à<i> et de l'article défini </i>les<i>.</i>"
        >>> clean("'''Contraction de [[préposition]] '''[[à]]''' et de l'[[article]] défini '''[[les]]''' .'''")
        "<b>Contraction de préposition </b>à<b> et de l'article défini </b>les<b>.</b>"

        >>> clean("[[{{nom langue|gcr}}]]")
        '{{nom langue|gcr}}'
        >>> clean("[[a|b]]")
        'b'
        >>> clean("[[-au|-[e]au]]")
        '-[e]au'
        >>> clean("[[Stó:lō]]", locale="fr")
        'Stó:lō'
        >>> clean("[[Annexe:Principales puissances de 10|10{{e|&minus;6}}]] [[gray#fr-nom|gray]]", locale="fr")
        '10{{e|&minus;6}} gray'

        >>> clean("[http://www.bertrange.fr/bienvenue/historique/]")
        ''
        >>> clean("[https://fr.wikipedia.org/wiki/Gerardus_Johannes_Mulder Gerardus Johannes Mulder]")
        'Gerardus Johannes Mulder'
        >>> clean("[//www.nps.gov/ande/historyculture/myth-shebang.htm the US National Park Service]")
        'the US National Park Service'
        >>> clean("<sup>[http://www.iupac.org/6612x2419.pdf]</sup> à la [[place]] en 1997<sup>[http://www.iupac.org/6912x2471.pdf]</sup>")
        'à la place en 1997'
        >>> clean("[[http://www.tv5monde.com/cms/chaine-francophone/lf/Merci-Professeur/p-17081-Une-peur-bleue.htm?episode=10 Voir aussi l’explication de Bernard Cerquiglini en images]]")
        ''

        >>> clean('<ref name="Marshall 2001"><sup>he</sup></ref>')
        ''
        >>> clean("<nowiki/>")
        ''
        >>> clean("foo|anticuado por [[cerrojo]] e influido por [[fierro]] [http://books.google.es/books?id=or7_PqeALCMC&pg=PA21&dq=%22ferrojo%22]|yeah")
        'foo|anticuado por cerrojo e influido por fierro |yeah'
        >>> clean("<<country>>")
        'country'
        >>> clean("<<region/Middle East>>")
        'Middle East'

        >>> clean("__NOTOC__")
        ''
        >>> clean("A_____B, B_____A")
        'A_____B, B_____A'

        >>> clean("<gallery>\nImage: Hydra (creature).jpg|due idre minacciose\nImage: Hydre.jpg|idra minacciosa\nImage: Chateauneuf-Randon de Joyeuse.svg|d'oro, a tre pali d'azzurro; al capo di rosso caricato di tre idre minacciose del campo<br /></gallery>")
        ''
    """

    # Speed-up lookup
    sub = re.sub
    sub2 = regex.sub

    # Save <math> formulas to prevent altering them
    if formulas := re.findall(r"(<math>[^<]+</math>)", text):
        for idx, formula in enumerate(formulas):
            text = text.replace(formula, f"##math{idx}##")

    # Remove line breaks
    text = text.replace("\n", "")

    # Parser hooks
    # <ref name="CFC"/> → ''
    text = sub(r"<ref[^>]*/>", "", text)
    # <ref>foo → ''
    # <ref>foo</ref> → ''
    # <ref name="CFC">{{Import:CFC}}</ref> → ''
    # <ref name="CFC"><tag>...</tag></ref> → ''
    text = sub(r"<ref[^>]*/?>[\s\S]*?(?:</ref>|$)", "", text)
    # <ref> → ''
    # </ref> → ''
    text = text.replace("<ref>", "").replace("</ref>", "")

    # HTML
    # Source: https://github.com/5j9/wikitextparser/blob/b24033b/wikitextparser/_wikitext.py#L83
    text = sub2(r"'''(\0*+[^'\n]++.*?)(?:''')", "<b>\\1</b>", text)
    # ''foo'' → <i>foo></i>
    text = sub2(r"''(\0*+[^'\n]++.*?)(?:'')", "<i>\\1</i>", text)
    # <br> / <br /> → ''
    text = sub(r"<br[^>]+/?>", "", text)

    # <nowiki/> → ''
    text = text.replace("<nowiki/>", "")

    # <gallery>
    text = sub(r"<gallery>[\s\S]*?</gallery>", "", text)

    # Local links
    text = sub(r"\[\[([^||:\]]+)\]\]", "\\1", text)  # [[a]] → a

    # Links
    # Internal: [[{{a|b}}]] → {{a|b}}
    text = sub(r"\[\[({{[^}]+}})\]\]", "\\1", text)
    # Internal: [[a|b]] → b
    text = sub(r"\[\[[^|]+\|(.+?(?=\]\]))\]\]", "\\1", text)
    # External: [[http://example.com Some text]] → ''
    text = sub(r"\[\[https?://[^\s]+\s[^\]]+\]\]", "", text)
    # External: [http://example.com] → ''
    text = sub(r"\[https?://[^\s\]]+\]", "", text)
    # External: [http://example.com Some text] → 'Some text'
    text = sub(r"\[https?://[^\s]+\s([^\]]+)\]", r"\1", text)
    # External: [//example.com Some text] → 'Some text'
    text = sub(r"\[//[^\s]+\s([^\]]+)\]", r"\1", text)
    text = text.replace("[[", "").replace("]]", "")

    # Tables
    # {|foo..|}
    text = sub(r"{\|[^}]+\|}", "", text)

    # Headings
    # == a == → a
    text = sub(r"^=+\s?([^=]+)\s?=+", lambda matches: matches.group(1).strip(), text)

    # Lists
    text = sub(r"^\*+\s?", "", text)

    # Magic words
    text = sub(r"__[A-Z]+__", "", text)  # __TOC__

    # Remove extra quotes left
    text = text.replace("''", "")

    # Remove extra brackets left
    text = text.replace(" []", "")
    text = text.replace(" ]", "")

    # Remove empty HTML tags
    # <sup></sup> → ''
    text = sub(r"<([^>]+)></\1>", "", text)

    # Remove extra spaces
    text = sub(r"\s{2,}", " ", text)
    text = sub(r"\s{1,}\.", ".", text)

    # <<bar>> → foo
    # <<foo/bar>> → bar
    text = sub(r"<<([^/>]+)>>", "\\1", text)
    text = sub(r"<<(?:[^/>]+)/([^>]+)>>", "\\1", text)

    # Restore math formulas
    for idx, formula in enumerate(formulas):
        text = text.replace(f"##math{idx}##", formula)

    return text.strip()


def process_templates(word: str, wikicode: str, locale: str, callback: Callable[[str, str], str] = clean) -> str:
    r"""Process all templates.

    It will also handle the <math> HTML tag as it is not part of the *clean()* function on purpose.

        >>> process_templates("foo", "{{}}", "fr")
        ''
        >>> process_templates("foo", "{{unknown}}", "fr")
        '{{unknown}}'
        >>> process_templates("foo", "{{foo|{{bar}}|123}}", "fr")
        ''
        >>> process_templates("foo", "{{fchim|OH|2|{{!}}OH|2}}", "fr")
        'OH<sub>2</sub>|OH<sub>2</sub>'
        >>> process_templates("EPR=ER", "{{alternative form of|mul|ER{{=}}EPR}}", "en")
        '<i>Alternative form of</i> <b>ER=EPR</b>'

        >>> process_templates("octonion", " <math>V^n</math>", "fr")  # doctest: +ELLIPSIS
        '<svg ...'
        >>> process_templates("test", r"<math>\frac</math>", "fr")
        '\\frac'
        >>> process_templates("", r"<chem>C10H14N2O4</chem>", "fr") # doctest: +ELLIPSIS
        '<svg ...'
        >>> process_templates("test", r"<chem>C10HX\xz14N2O4</chem>", "fr")
        'C10HX\\xz14N2O4'
        >>> process_templates("test", r"<hiero>R11</hiero>", "fr")
        '<table class="mw-hiero-table mw-hiero-outer" dir="ltr" style=" border: 0; border-spacing: 0; font-size:1em;"><tr><td style="padding: 0; text-align: center; vertical-align: middle; font-size:1em;">\n<table class="mw-hiero-table" style="border: 0; border-spacing: 0; font-size:1em;"><tr>\n<td style="padding: 0; text-align: center; vertical-align: middle; font-size:1em;"><img src="data:image/gif;base64...'

        >>> process_templates("hasta", "<i>حتى</i>", "es")
        'حتى'
        >>> process_templates("tasse", "<i>س tas'</i>", "fr")
        "س tas'"

    """

    sub = re.sub

    # Clean-up the code
    if not (text := callback(wikicode, locale)):
        return ""

    # {{foo}}
    # {{foo|bar}}
    # {{foo|{{bar}}|123}}
    # {{foo|{{bar|baz}}|123}}
    # {{foo|{{bar|lang|{{baz|args}}}}|123}}

    # Handle all templates
    while "there are templates":
        templates = set(re.findall(r"({{[^{}]*}})", text))
        if not templates:
            break
        for tpl in templates:
            if tpl in SPECIAL_TEMPLATES:
                text = text.replace(tpl, SPECIAL_TEMPLATES[tpl].placeholder)
            # Transform the template
            text = text.replace(tpl, transform(word, tpl[2:-2], locale))

    for tpl in SPECIAL_TEMPLATES.values():
        text = text.replace(tpl.placeholder, tpl.value)

    text = text.replace(OPEN_DOUBLE_CURLY, "{{")
    text = text.replace(CLOSE_DOUBLE_CURLY, "}}")

    # Handle <math> HTML tags
    text = sub(r"<math>([^<]+)</math>", partial(convert_math, word=word), text)
    text = sub(r"<chem>([^<]+)</chem>", partial(convert_chem, word=word), text)
    text = sub(r"<hiero>(.+)</hiero>", partial(convert_hiero, word=word), text)

    # Issue #584: move Arabic/Persian characters out of italic tags
    text = sub(r"<i>([^<]*[\u0627-\u064a]+[^<]*)</i>", r"\1", text)

    # Remove extra spaces (it happens when a template is ignored for instance)
    text = sub(r"\s{2,}", " ", text)
    text = sub(r"\s{1,}\.", ".", text)

    return text.strip()


def render_formula(formula: str, cat: str = "tex", output_format: str = "svg") -> str:
    """
    Convert mathematic/chemical symbols to a SVG string.

    Technical details can be found on those websites:
        - https://en.wikipedia.org/api/rest_v1/#/Math
        - https://github.com/maxbuchan/viv/blob/d9dc1f95348b458e0251bcf908084f2e0b8baf1f/apps/mediawiki/htdocs/extensions/Math/math/texutil.ml#L513
        - https://github.com/wikimedia/restbase/blob/ecef17bda6f4efc0d6e187fb05b1eeb389bf7120/sys/mathoid.js#L33
        - https://phabricator.wikimedia.org/diffusion/GMAT/browse/master/lib/math.js
    """

    if cat == "chem":
        formula = f"\\ce{{{formula}}}"

    headers = WIKIMEDIA_HEADERS

    # 1. Get the formula hash (type can be tex, inline-tex, or chem)
    url_hash = WIKIMEDIA_URL_MATH_CHECK.format(type=cat)
    with requests.post(url_hash, headers=headers, json={"q": formula}) as req:
        res = req.json()
        assert res["success"]
        formula_hash = req.headers["x-resource-location"]

    # 2. Get the rendered formula (format can be svg, mml, or png)
    url_render = WIKIMEDIA_URL_MATH_RENDER.format(format=output_format, hash=formula_hash)
    with requests.get(url_render, headers=headers) as req:
        return req.text


def formula_to_svg(formula: str, cat: str = "tex") -> str:
    """Return an optimized SVG file as a string."""
    force = "FORCE_FORMULA_RENDERING" in os.environ
    if force or not (svg_raw := svg.get(formula)):
        svg_raw = render_formula(formula, cat=cat, output_format="svg")
        svg.set(formula, svg_raw)
    return svg.optimize(svg_raw)


def convert_math(match: str | re.Match[str], word: str) -> str:
    """Convert mathematics symbols to a base64 encoded GIF file."""
    formula: str = (match.group(1) if isinstance(match, re.Match) else match).strip()
    try:
        return formula_to_svg(formula)
    except Exception:
        log.exception("<math> ERROR with %r in [%s]", formula, word)
        return formula


def convert_chem(match: str | re.Match[str], word: str) -> str:
    """Convert chemistry symbols to a base64 encoded GIF file."""
    formula: str = (match.group(1) if isinstance(match, re.Match) else match).strip()
    try:
        return formula_to_svg(formula, cat="chem")
    except Exception:
        log.exception("<chem> ERROR with %r in [%s]", formula, word)
        return formula


def convert_hiero(match: str | re.Match[str], word: str) -> str:
    """Convert hiretoglyph symbols to a base64 encoded GIF file."""
    expr: str = (match.group(1) if isinstance(match, re.Match) else match).strip()
    return render_hiero(expr)


def table2html(word: str, locale: str, table: wikitextparser.Table) -> str:
    phrase = "<table>"
    style_table = 'style="border: 1px solid black; border-collapse: collapse;"'
    style_td = 'style="border: 1px solid black; padding: 0.2em 0.4em; font-size: 2.5em;"'
    phrase = f"<table {style_table}>"
    for row in table.cells(span=False):
        phrase += "<tr>"
        for cell in row:
            tag = "th" if cell.is_header else "td"
            phrase += f"<{tag} {style_td}>{process_templates(word, cell.value, locale)}</{tag}>"
        phrase += "</tr>"
    phrase += "</table>"
    return phrase


def transform(word: str, template: str, locale: str) -> str:
    """Convert the data from the *template" template.
    This function also checks for template style.

        >>> transform("séga", "w", "fr")
        'séga'
        >>> transform("foo", "formatnum:123", "fr")
        '123'
        >>> transform("foo", "grammaire |fr", "fr")
        '<i>(Grammaire)</i>'
        >>> transform("foo", "conj|grp=1|fr", "fr")
        ''

        >>> # Magic words
        >>> transform("De_Witte", "PAGENAME", "fr")
        'De Witte'

        >>> # Magic word (date/time formats)
        >>> assert len(transform("foo", "CURRENTYEAR", "fr")) == 4
        >>> assert len(transform("foo", "CURRENTMONTH", "fr")) == 2
        >>> assert len(transform("foo", "CURRENTMONTH1", "fr")) in (1, 2)
        >>> assert len(transform("foo", "CURRENTDAY", "fr")) in (1, 2)
        >>> assert len(transform("foo", "CURRENTDAY2", "fr")) == 2
        >>> assert len(transform("foo", "CURRENTDOW", "fr")) == 1
        >>> assert len(transform("foo", "CURRENTTIME", "fr")) == 5
        >>> assert len(transform("foo", "CURRENTHOUR", "fr")) == 2
        >>> assert len(transform("foo", "CURRENTWEEK", "fr")) in (1, 2)
        >>> assert len(transform("foo", "CURRENTTIMESTAMP", "fr")) == 14
    """

    parts_raw = template.split("|")
    parts = [p.strip() for p in parts_raw]
    parts = [p.strip("\u200e") for p in parts]  # Left-to-right mark
    tpl = parts[0]

    # {{formatnum:-1000000}}
    if ":" in tpl and tpl not in (
        "R:TLFi",
        "R:Larousse2vol1922",
        "R:Littré",
        "R:Rivarol",
        "R:DAF6",
        "R:Tosti",
    ):
        parts_raw = template.split(":")
        parts = [p.strip() for p in parts_raw]
        tpl = parts[0]

    # Stop early
    if not tpl or tpl in templates_ignored[locale]:
        return ""

    # Magic words
    if tpl in MAGIC_WORDS:
        return MAGIC_WORDS[tpl]
    elif tpl == "PAGENAME" or (tpl == "w" and len(parts) == 1):
        return word.replace("_", " ")

    # Apply transformations

    with suppress(KeyError):
        return str(eval(templates_multi[locale][tpl]))

    if len(parts) == 1:
        with suppress(KeyError):
            return f"<i>({templates_italic[locale][tpl]})</i>"

    with suppress(KeyError):
        return templates_other[locale][tpl]

    return str(last_template_handler[locale](parts, locale, word=word))
