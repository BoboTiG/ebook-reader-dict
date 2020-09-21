"""Utilities for internal use."""
import re
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import Tuple
from warnings import warn

from cachetools import cached
from cachetools.keys import hashkey
import regex

from .constants import DOWNLOAD_URL
from .lang import (
    all_langs,
    last_template_handler,
    pattern_file,
    release_description,
    templates_ignored,
    templates_italic,
    templates_multi,
    templates_other,
    templates_warning_skip,
    thousands_separator,
)
from .user_functions import *  # noqa


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
    """Cleans up the provided Wikicode.
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
    pattern = "|".join(p for p in pattern_file)
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

    return text.strip()


def transform(word: str, template: str, locale: str) -> str:
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
        >>> transform("foo", "conj|grp=1|fr", "fr")
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

    # Help fixing formatting on Wiktionary (some templates are more complex and cannot be fixed)
    if parts != parts_raw and tpl not in templates_warning_skip[locale]:
        warn(f"Extra character found in the Wikicode of {word!r} (parts={parts_raw})")

    # Convert *parts* from a list to a tuple because list are not hashable and thus cannot be used
    # with the LRU cache.
    result: str = transform_apply(word, tpl, tuple(parts), locale)
    return result


@cached(cache={}, key=lambda word, tpl, parts, locale: hashkey(tpl, parts, locale))  # type: ignore
def transform_apply(word: str, tpl: str, parts: Tuple[str, ...], locale: str) -> str:
    """Convert the data from the *tpl* template of the *word* using the *locale*."""
    if tpl in templates_ignored[locale]:
        return ""

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

    # This is a country in the current locale
    with suppress(KeyError):
        return all_langs[locale][tpl]

    return last_template_handler[locale](parts, locale)
