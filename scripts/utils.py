"""Utilities for internal use."""
import os
import re
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import List, Match, Tuple, Union
from warnings import warn

from cachetools import cached
from cachetools.keys import hashkey
import regex

from .constants import DOWNLOAD_URL, IMG_CSS
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


def convert_etymology(etymology: str) -> str:
    """Return the HTML code to include for the etymology of a word."""
    return f"<p>{etymology}</p><br/>" if etymology else ""


def convert_genre(genre: str) -> str:
    """Return the HTML code to include for the genre of a word."""
    return f" <i>{genre}.</i>" if genre else ""


def convert_pronunciation(pronunciations: List[str]) -> str:
    """Return the HTML code to include for the etymology of a word."""
    if not pronunciations:
        return ""
    return " " + ", ".join(f"\\{p}\\" for p in pronunciations)


def format_description(locale: str, output_dir: Path) -> str:
    """Generate the release description."""

    # Get the words count
    count = (output_dir / "words.count").read_text().strip()

    # Format the words count
    thousands_sep = thousands_separator[locale]
    count = f"{int(count):,}".replace(",", thousands_sep)

    # Format the snapshot's date
    date = (output_dir / "words.snapshot").read_text().strip()
    date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"

    # The current date, UTC
    now = datetime.utcnow().isoformat()

    # The download link
    url = DOWNLOAD_URL.format(locale)

    return release_description[locale].format(
        creation_date=now,
        dump_date=date,
        locale=locale,
        url=url,
        words_count=count,
    )


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


def clean(word: str, text: str, locale: str) -> str:
    r"""Cleans up the provided Wikicode.
    Removes templates, tables, parser hooks, magic words, HTML tags and file embeds.
    Keeps links.
    Source: https://github.com/macbre/mediawiki-dump/blob/3f1553a/mediawiki_dump/tokenizer.py#L8

        >>> clean("foo", "", "fr")
        ''
        >>> clean("foo", "{{}}", "fr")
        ''
        >>> clean("foo", "{{unknown}}", "fr")
        '<i>(Unknown)</i>'
        >>> clean("foo", "<span style='color:black'>[[♣]]</span>", "fr")
        "<span style='color:black'>♣</span>"
        >>> clean("foo", "{{foo|{{bar}}|123}}", "fr")
        ''
        >>> clean("foo", "<ref>{{Import:CFC}}</ref>", "fr")
        ''
        >>> clean("foo", "<ref>{{Import:CFC}}</ref>bla bla bla <ref>{{Import:CFC}}</ref>", "fr")
        'bla bla bla'
        >>> clean("foo", '<ref name="CFC" />', "fr")
        ''
        >>> clean("foo", '<ref name="CFC">{{Import:CFC}}</ref>', "fr")
        ''
        >>> clean("iatralipta", '<ref name="CFC">{{CFC\\n|foo}}</ref>', "ca")
        ''
        >>> clean("voyeuse", "<ref>D'après ''Dictionnaire du tapissier : critique et historique de l’ameublement français, depuis les temps anciens jusqu’à nos jours'', par J. Deville, page 32 ({{Gallica|http://gallica.bnf.fr/ark:/12148/bpt6k55042642/f71.image}})</ref>", "fr")
        ''
        >>> clean("foo", "''italic''", "fr")
        '<i>italic</i>'
        >>> clean("foo", "'''strong'''", "fr")
        '<b>strong</b>'
        >>> clean("foo", "''italic and '''strong'''''", "fr")
        '<i>italic and <b>strong</b></i>'
        >>> clean("foo", "'''strong and ''italic'''''", "fr")
        '<b>strong and <i>italic</b></i>'
        >>> clean("foo", "'''''Parer à'''''", "fr")
        '<i><b>Parer à</b></i>'
        >>> clean("aux", "''Contraction de [[préposition]] ''[[à]]'' et de l'[[article]] défini ''[[les]]'' .''", "fr")
        "<i>Contraction de préposition </i>à<i> et de l'article défini </i>les<i>.</i>"
        >>> clean("aux", "'''Contraction de [[préposition]] '''[[à]]''' et de l'[[article]] défini '''[[les]]''' .'''", "fr")
        "<b>Contraction de préposition </b>à<b> et de l'article défini </b>les<b>.</b>"
        >>> clean("μGy", "[[Annexe:Principales puissances de 10|10{{e|&minus;6}}]] [[gray#fr-nom|gray]]", "fr")
        '10<sup>&minus;6</sup> gray'
        >>> clean("base", "[[Fichier:Blason ville fr Petit-Bersac 24.svg|vignette|120px|'''Base''' d’or ''(sens héraldique)'']]", "fr")  # noqa
        ''
        >>> clean("coccigrole", "[[File:Sarcoscypha_coccinea,_Salles-la-Source_(Matthieu_Gauvain).JPG|vignette|Pézize écarlate]]", "fr")
        ''
        >>> clean("sco", "<!-- {{sco}} -->", "fr")
        ''
        >>> clean("sco", "<!-- <i>sco</i> -->", "fr")
        ''
        >>> clean("cornstalk", '<ref name="Marshall 2001"><sup>he</sup></ref>', "en")
        ''
        >>> clean("built like a brick shithouse", '<nowiki/>', "en")
        ''
        >>> clean("ferrojar", "foo|anticuado por [[cerrojo]] e influido por [[fierro]] [http://books.google.es/books?id=or7_PqeALCMC&pg=PA21&dq=%22ferrojo%22]|yeah", "es")
        'foo|anticuado por cerrojo e influido por fierro|yeah'
        >>> clean("octonion", " <math>V^n</math>", "fr")  # doctest: +ELLIPSIS
        '<img style="height:100%;max-height:0.8em;width:auto;vertical-align:bottom" src="data:image/gif;base64,...'
        >>> clean("", r"<math>\R^n</math>", "fr")
        <math> ERROR with <re.Match object; span=(0, 17), match='<math>\\R^n</math>'>
        '\\R^n'
    """

    # Speed-up lookup
    sub = re.sub
    sub2 = regex.sub

    # Remove line breaks
    text = text.replace("\n", "")

    # Parser hooks
    # <ref>foo</ref> -> ''
    # <ref name="CFC">{{Import:CFC}}</ref> -> ''
    # <ref name="CFC"><tag>...</tag></ref> -> ''
    text = sub(r"<ref[^>]*/?>[\s\S]*?</ref>", "", text)
    # <ref name="CFC"/> -> ''
    text = sub(r"<ref[^>]*/>", "", text)

    # <nowiki/> -> ''
    text = text.replace("<nowiki/>", "")

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

    # Local links
    text = sub(r"\[\[([^|\]]+)\]\]", "\\1", text)  # [[a]] -> a
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
    # http://example.com -> ''
    text = sub(r"https?://[^\s\]]+", "", text)

    # Lists
    text = sub(r"^\*+\s?", "", text, flags=re.MULTILINE)

    # Magic words
    text = sub(r"__\w+__", "", text)  # __TOC__

    # Remove extra quotes left
    text = text.replace("''", "")

    # Remove extra brackets left
    text = text.replace(" []", "")

    # Templates
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

    # Remove extra spaces
    text = sub(r"\s{2,}", " ", text)
    text = sub(r"\s{1,}\.", ".", text)

    # Handle <math> HTML tags
    text = sub(r"<math>([^<]+)</math>", convert_math, text)

    return text.strip()


def _convert_math(expr: str) -> str:
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
        )
        Image.open(buf).convert("L").save(im, format="gif", optimize=True)

        im.seek(0)
        raw = im.read()

    return f'<img style="{IMG_CSS}" src="data:image/gif;base64,{b64encode(raw).decode()}"/>'


def convert_math(match: Union[str, Match[str]]) -> str:
    """Convert mathematics symbols to a base64 encoded GIF file."""
    expr: str = (match.group(1) if isinstance(match, re.Match) else match).strip()
    try:
        return _convert_math(expr)
    except Exception:
        print(f"<math> ERROR with {match}", flush=True)
        return expr


def transform(
    word: str, template: str, locale: str, debug: bool = os.getenv("DEBUG", "0") == "1"
) -> str:
    """Convert the data from the *template" template.
    This function also checks for template style.

        >>> transform("foo", "w|ISO 639-3", "fr")
        'ISO 639-3'
        >>> transform("foo spaces", "w | ISO 639-3", "fr")
        'ISO 639-3'
        >>> transform("foo", "formatnum:123", "fr")
        '123'
        >>> transform("test", "w|Langenstriegis|lang=de", "fr")
        'Langenstriegis'
        >>> transform("test", "w|Gesse aphaca|Lathyrus aphaca", "fr")
        'Lathyrus aphaca'
        >>> transform("foo", "grammaire|fr", "fr")
        '<i>(Grammaire)</i>'
        >>> transform("foo", "conj|grp=1|fr", "fr", debug=True)
         !! Missing template support for 'conj' (word is 'foo')
        ''
    """

    parts_raw = [p for p in template.split("|") if not p.startswith("lang=")]
    parts = [p.strip() for p in parts_raw]
    parts = [p.strip("\u200e") for p in parts]  # Left-to-right mark
    tpl = parts[0]

    # {{formatnum:-1000000}}
    if ":" in tpl:
        parts_raw = template.split(":")
        parts = [p.strip() for p in parts_raw]
        tpl = parts[0]

    # Stop early
    if not tpl or tpl in templates_ignored[locale]:
        return ""

    # Help fixing formatting on Wiktionary
    if parts != parts_raw:
        warn(f"Extra character found in the Wikicode of {word!r} (parts={parts_raw})")

    # Convert *parts* from a list to a tuple because list are not hashable and thus cannot be used
    # with the LRU cache.
    result: str = transform_apply(word, tpl, tuple(parts), locale)
    if debug and not result and not tpl.startswith("?"):
        print(
            f" !! Missing template support for {tpl!r} (word is {word!r})", flush=True
        )
    return result


@cached(cache={}, key=lambda word, tpl, parts, locale: hashkey(tpl, parts, locale))  # type: ignore
def transform_apply(word: str, tpl: str, parts: Tuple[str, ...], locale: str) -> str:
    """Convert the data from the *tpl* template of the *word* using the *locale*."""
    # {{w|ISO 639-3}} -> ISO 639-3
    # {{w|Gesse aphaca|Lathyrus aphaca}} -> Lathyrus aphaca
    if tpl == "w":
        return parts[-1]

    with suppress(KeyError):
        return eval(templates_multi[locale][tpl])  # type: ignore

    if len(parts) == 1:
        with suppress(KeyError):
            return f"<i>({templates_italic[locale][tpl]})</i>"

    with suppress(KeyError):
        result: str = templates_other[locale][tpl]
        return result

    return last_template_handler[locale](parts, locale)
