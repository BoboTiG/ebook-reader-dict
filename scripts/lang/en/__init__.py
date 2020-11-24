"""English language."""
from typing import Tuple

# Regex to find the pronunciation
pronunciation = r"{IPA\|en\|/([^/]+)/"

# Float number separator
float_separator = "."

# Thousads separator
thousands_separator = ","

# Markers for sections that contain interesting text to analyse.
head_sections = ("english",)
section_sublevels = (4, 3)
etyl_section = ["Etymology", "Etymology 1"]
sections = (
    "Adjective",
    "Adverb",
    "Article",
    "Conjunction",
    "Contraction",
    "Determiner",
    *etyl_section,
    "Interjection",
    "Noun",
    "Numeral",
    "Particle",
    "Prefix",
    "Preposition",
    "Pronoun",
    "Proper noun",
    "Suffix",
    "Symbol",
    "Verb",
)

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = (
    "en-past of",
    "en-simple past of",
    "infl of",
    "inflection of",
    "plural of",
    "rfdef",
)

# Templates to ignore: the text will be deleted.
templates_ignored = ("cln", "+obj", "rel-bottom", "rel-top", "rfex", "senseid")

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "AAVE": "African-American Vernacular",
    "American": "US",
    "Early ME": "Early Middle English",
}

# Templates more complex to manage.
templates_multi = {
    # {{abbr of|en|abortion}}
    "abbr of": "italic('Abbreviation of') + ' ' + strong(parts[-1])",
    # {{alt case|en|angstrom}}
    "alt case": "italic('Alternative letter-case form of') + ' ' + strong(parts[-1])",
    # {{defdate|from 15th c.}}
    "defdate": "small('[' + parts[1] + ']')",
    # {{eye dialect of|en|is}}
    "eye dialect of": "italic('Eye dialect spelling of') + ' ' + strong(parts[-1])",
    # {{form of|en|obsolete emphatic|ye}}
    "form of": "italic(parts[2] + ' of') + ' ' + strong(parts[-1])",
    # {{gloss|liquid H<sub>2</sub>O}}
    "gloss": "parenthesis(parts[1])",
    # {{IPAchar|[tʃ]|lang=en}})
    "IPAchar": "parts[1]",
    # {{IPAfont|[[ʌ]]}}
    "IPAfont": 'f"⟨{parts[1]}⟩"',
    # {{l|en|water vapour}}
    "l": "parts[-1]",
    # {{ll|en|cod}}
    "ll": "parts[-1]",
    # {{link|en|water vapour}}
    "link": "parts[-1]",
    # {{n-g|Definite grammatical ...}}
    "n-g": "italic(parts[-1].lstrip('1='))",
    # {{ngd|Definite grammatical ...}}
    "ngd": "italic(parts[-1].lstrip('1='))",
    # {{non-gloss definition|Definite grammatical ...}}
    "non-gloss definition": "italic(parts[-1].lstrip('1='))",
    # {{qual|Used only ...}}
    "qual": "'(' + italic(parts[1]) + ')'",
    # {{qualifier|Used only ...}}
    "qualifier": "'(' + italic(parts[1]) + ')'",
    # {{taxlink|Gadus macrocephalus|species|ver=170710}}
    "taxlink": "italic(parts[1])",
    # {{vern|Pacific cod}}
    "vern": "parts[-1]",
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["alternative form of", "enm" , "theen"], "en")
        '<i>Alternative form of</i> <b>theen</b>'
        >>> last_template_handler(["alt form", "enm" , "a", "pos=indefinite article"], "en")
        '<i>Alternative form of</i> <b>a</b> (indefinite article)'
        >>> last_template_handler(["alt form", "enm" , "worth", "t=to become"], "en")
        '<i>Alternative form of</i> <b>worth</b> (“to become”)'
        >>> last_template_handler(["alt form", "en" , "ess", "nodot=1"], "en")
        '<i>Alternative form of</i> <b>ess</b>'

        >>> last_template_handler(["der", "en", "fro", "-"], "en")
        'Old French'

        >>> last_template_handler(["etyl", "enm", "en"], "en")
        'Middle English'

        >>> last_template_handler(["inh", "en", "enm", "water"], "en")
        'Middle English <i>water</i>'
        >>> last_template_handler(["inh", "en", "ang", "wæter", "", "water"], "en")
        'Old English <i>wæter</i> (“water”)'
        >>> last_template_handler(["inh", "en", "ang", "etan", "t=to eat"], "en")
        'Old English <i>etan</i> (“to eat”)'
        >>> last_template_handler(["inh", "en", "ine-pro", "*werdʰh₁om", "*wr̥dʰh₁om"], "en")
        'Proto-Indo-European <i>*wr̥dʰh₁om</i>'

        >>> last_template_handler(["label", "en" , "Australia", "slang", "nocat=1"], "en")
        '<i>(Australia, slang)</i>'
        >>> last_template_handler(["lb", "en" , "Australia"], "en")
        '<i>(Australia)</i>'
        >>> last_template_handler(["lb", "en" , "Australia", "or", "foobar"], "en")
        '<i>(Australia or foobar)</i>'
        >>> last_template_handler(["lb", "en" , "foobar", "and", "Australia", "or", "foobar"], "en")
        '<i>(foobar and Australia or foobar)</i>'
        >>> last_template_handler(["lb", "en" , "foobar", "_", "Australia", "foobar"], "en")
        '<i>(foobar Australia, foobar)</i>'
        >>> # last_template_handler(["lb", "en" , "roa-lor"], "en")
        >>> # '<i>(Lorrain)</i>'
        >>> last_template_handler(["lbl", "en" , "transitive"], "en")
        '<i>(transitive)</i>'

        >>> last_template_handler(["m", "en", "more"], "en")
        '<b>more</b>'
        >>> last_template_handler(["m", "ine-pro", "*h₁ed-", "t=to eat"], "en")
        '<i>*h₁ed-</i> (“to eat”)'

        >>> last_template_handler(["standard spelling of", "en", "from=Irish English", "Irish Traveller"], "en")
        '<i>Irish English standard spelling of</i> <b>Irish Traveller</b>.'
        >>> last_template_handler(["standard spelling of", "en", "enroll"], "en")
        '<i>Standard spelling of</i> <b>enroll</b>.'

        >>> last_template_handler(["surname", "en"], "en")
        '<i>A surname.</i>'
        >>> last_template_handler(["surname", "en", "nodot=1"], "en")
        '<i>A surname</i>'
        >>> last_template_handler(["surname", "en", "rare"], "en")
        '<i>A rare surname.</i>'
        >>> last_template_handler(["surname", "en", "A=An", "occupational"], "en")
        '<i>An occupational surname.</i>'
        >>> last_template_handler(["surname", "en", "from=Latin", "dot=,"], "en")
        '<i>A surname,</i>'
    """
    from itertools import zip_longest

    from .langs import langs
    from ...user_functions import (
        capitalize,
        extract_keywords_from,
        italic,
        lookup_italic,
        strong,
        term,
    )

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl in ("alt form", "alternative form of"):
        res = italic("Alternative form of")
        res += f" {strong(parts[1])}"
        if data["t"]:
            res += f" (“{data['t']}”)"
        if data["pos"]:
            res += f" ({data['pos']})"
        return res

    if tpl in ("bor", "cog", "der", "etyl", "inh", "m"):
        if tpl not in ("cog", "etyl", "m"):
            parts.pop(0)  # Remove the destination language

        if tpl == "etyl":
            parts.pop(1)

        lang = langs.get(parts.pop(0), "")
        phrase = f"{lang}" if tpl != "m" else ""

        if not parts:
            return phrase

        word = parts.pop(0)
        if word == "-":
            return phrase

        word = data["alt"] or word
        gloss = data["t"] or data["gloss"]

        if parts:
            word = parts.pop(0) or word  # 4, alt=

        if tpl == "m":
            phrase += strong(word) if not data["t"] else italic(word)
        else:
            phrase += f" {italic(word)}"

        if parts:
            gloss = parts.pop(0)  # 5, t=, gloss=
        if gloss:
            phrase += f" (“{gloss}”)"

        return phrase

    if tpl in ("label", "lb", "lbl"):
        if len(parts) == 2:
            return term(parts[1])

        res = ""
        for word1, word2 in zip_longest(parts[1:], parts[2:]):
            if word1 in ("_", "and", "or"):
                continue

            res += lookup_italic(word1, locale)

            if word2 == "_":
                res += " "
            elif word2 == "and":
                res += " and "
            elif word2 == "or":
                res += " or "
            elif word2:
                res += ", "

        return term(res.rstrip(", "))

    if tpl == "standard spelling of":
        if data["from"]:
            phrase = italic(f"{data['from']} {tpl}")
        else:
            phrase = italic("Standard spelling of")
        return f"{phrase} {strong(parts[1])}."

    if tpl == "surname":
        parts.pop(0)  # Remove the lang

        art = data["A"] or "A"
        dot = data["dot"] or ("" if data["nodot"] else ".")
        if not parts:
            return italic(f"{art} {tpl}{dot}")
        return italic(f"{art} {parts[0]} {tpl}{dot}")

    try:
        return f"{italic(capitalize(tpl))} {strong(parts[1])}"
    except IndexError:
        return capitalize(tpl)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/en
release_description = """\
Words count: {words_count}
Wiktionary dump: {dump_date}

Installation:

1. Copy the [dicthtml-{locale}.zip <sup>:floppy_disk:</sup>]({url}) file into the `.kobo/custom-dict/` folder of the reader.
2. **Restart** the reader.

<sub>Updated on {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"
