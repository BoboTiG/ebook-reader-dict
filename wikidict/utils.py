"""Utilities for internal use."""
import re
from contextlib import suppress
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import List, Match, Set, Tuple, Union
from warnings import warn

from cachetools import cached
from cachetools.keys import hashkey
import regex
import requests

from .constants import (
    DOWNLOAD_URL_DICTFILE,
    DOWNLOAD_URL_KOBO,
    DOWNLOAD_URL_STARDICT,
    IMG_CSS,
)
from .lang import (
    last_template_handler,
    pattern_file,
    release_description,
    templates_ignored,
    templates_italic,
    templates_multi,
    templates_other,
    thousands_separator,
)
from .user_functions import *  # noqa


# Used to store not-yet-handled templates to display a warning
# only once
MISSING_TPL_SEEN: Set[str] = set()

# Magic words (small part, only data/time related)
# https://www.mediawiki.org/wiki/Help:Magic_words
NOW = datetime.utcnow()
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


def convert_genre(genre: str) -> str:
    """Return the HTML code to include for the genre of a word."""
    return f" <i>{genre}.</i>" if genre else ""


def convert_pronunciation(pronunciations: List[str]) -> str:
    """Return the HTML code to include for the etymology of a word."""
    if not pronunciations:
        return ""
    return " " + ", ".join(f"\\{p}\\" for p in pronunciations)


def get_word_of_the_day(locale: str) -> str:
    """Retrieve the word of the day."""
    months = {
        "en": [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
    }

    word_of_the_day = {
        "ca": ("", ""),  # Doesn't seem to have a word of the day
        "es": (
            # Plantilla:palabra de la semana/4
            f"Plantilla:palabra_de_la_semana/{NOW.strftime('%-V')}",
            r" palabra= ([^\|]+)",
        ),
        "en": (
            # Wiktionary:Word of the day/2021/January_30
            f"Wiktionary:Word_of_the_day/{NOW.strftime('%Y')}/{months['en'][int(NOW.strftime('%-m')) - 1]}_{NOW.strftime('%d')}",  # noqa
            r"{{WOTD\|([^\|]+)\|",
        ),
        "fr": (
            # Modèle:Entrée du jour/2021/01/30
            f"Mod%C3%A8le:Entr%C3%A9e_du_jour/{NOW.strftime('%Y/%m/%d')}",
            r"<span style=\"font-size:120%;\">'''\[\[([^\]]+)\]\]'''</span>",
        ),
        "pt": ("", ""),  # Doesn't seem to have a word of the day
        "sv": (
            "Mall:högkvalitativt",
            r"<big>\[\[([^\]]+)\]\]</big>",
        ),
    }

    special_word, pattern = word_of_the_day[locale]
    url = f"https://{locale}.wiktionary.org/wiki/{special_word}?action=raw"
    with requests.get(url) as req:
        matches = re.findall(pattern, req.text)
        return str(matches[0].strip()) if matches else ""


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

    # Download links
    url_dictfile = DOWNLOAD_URL_DICTFILE.format(locale)
    url_kobo = DOWNLOAD_URL_KOBO.format(locale)
    url_stardict = DOWNLOAD_URL_STARDICT.format(locale)

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
    return (
        prefix.ljust(2, "a")
        if all(c.isalpha() and c.islower() for c in prefix)
        else "11"
    )


def clean(text: str) -> str:
    """Cleans up the provided Wikicode.
    Removes templates, tables, parser hooks, magic words, HTML tags and file embeds.
    Keeps links.
    Source: https://github.com/macbre/mediawiki-dump/blob/3f1553a/mediawiki_dump/tokenizer.py#L8

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
        >>> clean('<ref name="CFC" />')
        ''
        >>> clean('<ref name="CFC">{{Import:CFC}}</ref>')
        ''
        >>> clean('<ref name="CFC">{{CFC\\n|foo}}</ref>')
        ''
        >>> clean("<ref>D'après ''Dictionnaire du tapissier : critique et historique de l’ameublement français, depuis les temps anciens jusqu’à nos jours'', par J. Deville, page 32 ({{Gallica|http://gallica.bnf.fr/ark:/12148/bpt6k55042642/f71.image}})</ref>")
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
        >>> clean("[[Annexe:Principales puissances de 10|10{{e|&minus;6}}]] [[gray#fr-nom|gray]]")
        '10{{e|&minus;6}} gray'
        >>> clean("[[Fichier:Blason ville fr Petit-Bersac 24.svg|vignette|120px|'''Base''' d’or ''(sens héraldique)'']]")  # noqa
        ''
        >>> clean("[[File:Sarcoscypha_coccinea,_Salles-la-Source_(Matthieu_Gauvain).JPG|vignette|Pézize écarlate]]")
        ''
        >>> clean("<!-- {{sco}} -->")
        ''
        >>> clean("<!-- <i>sco</i> -->")
        ''
        >>> clean('<ref name="Marshall 2001"><sup>he</sup></ref>')
        ''
        >>> clean("<nowiki/>")
        ''
        >>> clean("foo|anticuado por [[cerrojo]] e influido por [[fierro]] [http://books.google.es/books?id=or7_PqeALCMC&pg=PA21&dq=%22ferrojo%22]|yeah")
        'foo|anticuado por cerrojo e influido por fierro|yeah'
        >>> clean("<<country>>")
        'country'
        >>> clean("<<region/Middle East>>")
        'Middle East'
    """

    # Speed-up lookup
    sub = re.sub
    sub2 = regex.sub

    # Remove line breaks
    text = text.replace("\n", "")

    # Parser hooks
    # <ref name="CFC"/> -> ''
    text = sub(r"<ref[^>]*/>", "", text)
    # <ref>foo</ref> -> ''
    # <ref name="CFC">{{Import:CFC}}</ref> -> ''
    # <ref name="CFC"><tag>...</tag></ref> -> ''
    text = sub(r"<ref[^>]*/?>[\s\S]*?</ref>", "", text)

    # Files
    pattern = "|".join(iter(pattern_file))
    text = sub(fr"\[\[(?:{pattern}):[^\]]+\]\]", "", text)

    # HTML
    # <-- foo --> -> ''
    text = sub(r"<!--(?:.+-->)?", "", text)
    # Source: https://github.com/5j9/wikitextparser/blob/b24033b/wikitextparser/_wikitext.py#L83
    text = sub2(r"'''(\0*+[^'\n]++.*?)(?:''')", "<b>\\1</b>", text)
    # ''foo'' -> <i>foo></i>
    text = sub2(r"''(\0*+[^'\n]++.*?)(?:'')", "<i>\\1</i>", text)
    # <br> / <br /> -> ''
    text = sub(r"<br[^>]+/?>", "", text)

    # <nowiki/> -> ''
    text = text.replace("<nowiki/>", "")

    # Local links
    text = sub(r"\[\[([^|\]]+)\]\]", "\\1", text)  # [[a]] -> a
    text = sub(r"\[\[({{[^}]+}})\]\]", "\\1", text)  # [[{{a|b}}]] -> {{a|b}}
    text = sub(r"\[\[[^|]+\|([^\]]+)\]\]", "\\1", text)  # [[a|b]] -> b

    text = text.replace("[[", "").replace("]]", "")

    # Tables
    text = sub(r"{\|[^}]+\|}", "", text)  # {|foo..|}

    # Headings
    text = sub(
        r"^=+\s?([^=]+)\s?=+",
        lambda matches: matches.group(1).strip(),
        text,
        flags=re.MULTILINE,
    )  # == a == -> a

    # Files and other links with namespaces
    text = sub(r"\[\[[^:\]]+:[^\]]+\]\]", "", text)  # [[foo:b]] -> ''

    # External links
    # [[http://example.com foo]] -> foo
    text = sub(r"\[http[^\s]+ ([^\]]+)\]", "\\1", text)
    # [http://example.com] -> ''
    text = sub(r"\[https?://[^\s\]]+", "", text)

    # Lists
    text = sub(r"^\*+\s?", "", text, flags=re.MULTILINE)

    # Magic words
    text = sub(r"__\w+__", "", text)  # __TOC__

    # Remove extra quotes left
    text = text.replace("''", "")

    # Remove extra brackets left
    text = text.replace(" []", "")
    text = text.replace(" ]", "")

    # Remove extra spaces
    text = sub(r"\s{2,}", " ", text)
    text = sub(r"\s{1,}\.", ".", text)

    # <<bar>> -> foo
    # <<foo/bar>> -> bar
    text = sub(r"<<([^/>]+)>>", "\\1", text)
    text = sub(r"<<(?:[^/>]+)/([^>]+)>>", "\\1", text)

    return text.strip()


def process_templates(word: str, text: str, locale: str) -> str:
    r"""Process all templates.

    It will also handle the <math> HTML tag as it is not part of the *clean()* function on purpose.

        >>> process_templates("foo", "{{}}", "fr")
        ''
        >>> process_templates("foo", "{{unknown}}", "fr")
        '<i>(Unknown)</i>'
        >>> process_templates("foo", "{{foo|{{bar}}|123}}", "fr")
         !! Missing 'foo' template support for word 'foo'
        ''
        >>> process_templates("octonion", " <math>V^n</math>", "fr")  # doctest: +ELLIPSIS
        '<img style="height:100%;max-height:0.8em;width:auto;vertical-align:bottom" src="data:image/gif;base64,...'
        >>> process_templates("test", r"<math>\R^n</math>", "fr")
        <math> ERROR with \R^n in [test]
        '\\R^n'
        >>> process_templates("", r"<chem>C10H14N2O4</chem>", "fr") # doctest: +ELLIPSIS
        '<img style="height:100%;max-height:0.8em;width:auto;vertical-align:bottom" src="data:image/gif;base64,...'
        >>> process_templates("test", r"<chem>C10HX\xz14N2O4</chem>", "fr")
        <chem> ERROR with C10HX\xz14N2O4 in [test]
        'C10HX\\xz14N2O4'
    """

    sub = re.sub

    # {{foo}}
    # {{foo|bar}}
    # {{foo|{{bar}}|123}}
    # {{foo|{{bar|baz}}|123}}

    # Simplify the parsing logic: this line will return a list of nested templates.
    for tpl in set(re.findall(r"({{[^{}]*}})", text)):
        # Transform the nested template.
        # This will remove any nested templates from the original text.
        text = text.replace(tpl, transform(word, tpl[2:-2], locale))

    # Now that all nested templates are done, we can process top-level ones
    while "{{" in text:
        start = text.find("{{")
        pos = start + 2
        subtext = ""

        while pos < len(text):
            if text[pos : pos + 2] == "}}":
                # We hit the end of the template
                pos += 1
                break

            # Save the template contents
            subtext += text[pos]
            pos += 1

        # The template is now completed
        transformed = transform(word, subtext, locale)
        text = f"{text[:start]}{transformed}{text[pos + 1 :]}"

    # Handle <math> HTML tags
    text = sub(r"<math>([^<]+)</math>", partial(convert_math, word=word), text)
    text = sub(r"<chem>([^<]+)</chem>", partial(convert_chem, word=word), text)

    # Remove extra spaces (it happens when a template is ignored for instance)
    text = sub(r"\s{2,}", " ", text)
    text = sub(r"\s{1,}\.", ".", text)

    return text.strip()


def _convert_math(expr: str, packages: List[str] = []) -> str:
    """Convert mathematics symbols to a base64 encoded GIF file."""
    from base64 import b64encode
    from io import BytesIO

    from PIL import Image
    from sympy import preview

    dvioptions = ["-T", "tight", "-z", "0", "-D 150", "-bg", "Transparent"]
    with BytesIO() as buf, BytesIO() as im:
        preview(
            f"${expr}$",
            output="png",
            viewer="BytesIO",
            outputbuffer=buf,
            dvioptions=dvioptions,
            packages=tuple(packages),
        )
        Image.open(buf).convert("L").save(im, format="gif", optimize=True)

        im.seek(0)
        raw = im.read()

    return f'<img style="{IMG_CSS}" src="data:image/gif;base64,{b64encode(raw).decode()}"/>'


def convert_math(match: Union[str, Match[str]], word: str) -> str:
    """Convert mathematics symbols to a base64 encoded GIF file."""
    expr: str = (match.group(1) if isinstance(match, re.Match) else match).strip()
    try:
        return _convert_math(
            expr,
            packages=["amssymb", "bbm"],
        )
    except Exception:
        print(f"<math> ERROR with {expr} in [{word}]", flush=True)
        return expr


def convert_chem(match: Union[str, Match[str]], word: str) -> str:
    """Convert chemistry symbols to a base64 encoded GIF file."""
    expr: str = (match.group(1) if isinstance(match, re.Match) else match).strip()
    try:
        return _convert_math(f"\\ce{{{expr}}}", packages=["mhchem"])
    except Exception:
        print(f"<chem> ERROR with {expr} in [{word}]", flush=True)
        return expr


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
         !! Missing 'conj' template support for word 'foo'
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
    if ":" in tpl and tpl not in ("R:TLFi"):
        parts_raw = template.split(":")
        parts = [p.strip() for p in parts_raw]
        tpl = parts[0]

    # Stop early
    if not tpl or tpl in templates_ignored[locale]:
        return ""

    # Help fixing formatting on Wiktionary
    # - Filtering out ES because some contributors are not open to fix such issues ... sadly.
    # - Filtering out the FR "fchim" template because it is actually OK to have spaces in there.
    if locale != "es" and tpl != "fchim" and parts != parts_raw:
        warn(f"Extra character found in the Wikicode of {word!r} (parts={parts_raw})")

    # Magic words
    if tpl in MAGIC_WORDS:
        return MAGIC_WORDS[tpl]
    elif tpl == "PAGENAME" or (tpl == "w" and len(parts) == 1):
        return word.replace("_", " ")

    # Convert *parts* from a list to a tuple because list are not hashable and thus cannot be used
    # with the LRU cache.
    result: str = transform_apply(word, tpl, tuple(parts), locale)

    # Some templates are returning an empty string on purpose, skip the warning then.
    # - SV: tagg
    if not result and tpl not in MISSING_TPL_SEEN and (locale != "sv" or tpl != "tagg"):
        print(f" !! Missing {tpl!r} template support for word {word!r}", flush=True)
        MISSING_TPL_SEEN.add(tpl)
    return result


@cached(cache={}, key=lambda word, tpl, parts, locale: hashkey(tpl, parts, locale))  # type: ignore
def transform_apply(word: str, tpl: str, parts: Tuple[str, ...], locale: str) -> str:
    """Convert the data from the *tpl* template of the *word* using the *locale*."""
    with suppress(KeyError):
        return eval(templates_multi[locale][tpl])  # type: ignore

    if len(parts) == 1:
        with suppress(KeyError):
            return f"<i>({templates_italic[locale][tpl]})</i>"

    with suppress(KeyError):
        result: str = templates_other[locale][tpl]
        return result

    return last_template_handler[locale](parts, locale, word=word)
