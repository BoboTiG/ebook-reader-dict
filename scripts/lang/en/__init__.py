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
sections = (
    "Adjective",
    "Adverb",
    "Article",
    "Conjunction",
    "Contraction",
    "Determiner",
    "Interjection",
    "Noun",
    "Numeral",
    "Particle",
    "Prefix",
    "Preposition",
    "Pronoun",
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
templates_ignored = ("cln", "+obj", "rfex", "senseid")

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "AAVE": "African-American Vernacular",
    "American": "US",
    "Early ME": "Early Middle English",
}

# Templates more complex to manage.
templates_multi = {
    # {{abbreviation of|en|abortion}}
    "abbreviation of": "italic(capitalize(parts[0])) + ' ' + strong(parts[-1])",
    # {{alternative spelling of|en|µs}}
    "alternative spelling of": "italic(capitalize(parts[0])) + ' ' + strong(parts[-1])",
    # {{clipping of|en|yuppie}}
    "clipping of": "italic(capitalize(parts[0])) + ' ' + strong(parts[-1])",
    # {{defdate|from 15th c.}}
    "defdate": "small('[' + parts[1] + ']')",
    # {{eye dialect of|en|is}}
    "eye dialect of": "italic('Eye dialect spelling of') + ' ' + strong(parts[-1])",
    # {{gloss|liquid H<sub>2</sub>O}}
    "gloss": "parenthesis(parts[1])",
    # {{initialism of|en|[[Inuit]] [[Qaujimajatuqangit]]|nodot=1}}
    "initialism of": "italic(capitalize(parts[0])) + ' ' + strong(parts[2])",
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
    # {{m|en|more}}
    "m": "strong(parts[-1])",
    # {{n-g|Definite grammatical ...}}
    "n-g": "italic(parts[-1].lstrip('1='))",
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


def last_template_handler(parts: Tuple[str, ...], locale: str) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["lb", "en" , "Australia"], "en")
        '<i>(Australia)</i>'
        >>> last_template_handler(["lbl", "en" , "transitive"], "en")
        '<i>(transitive)</i>'
        >>> last_template_handler(["label", "en" , "Australia", "slang"], "en")
        '<i>(Australia, slang)</i>'
        >>> last_template_handler(["lb", "en" , "Australia", "or", "foobar"], "en")
        '<i>(Australia or foobar)</i>'
        >>> last_template_handler(["lb", "en" , "foobar", "and", "Australia", "or", "foobar"], "en")
        '<i>(foobar and Australia or foobar)</i>'
        >>> last_template_handler(["lb", "en" , "foobar", "_", "Australia", "foobar"], "en")
        '<i>(foobar Australia, foobar)</i>'
        >>> # last_template_handler(["lb", "en" , "roa-lor"], "en")
        >>> # '<i>(Lorrain)</i>'
        >>> last_template_handler(["alt form", "enm" , "theen"], "en")
        '<i>Alternative form of</i> <b>theen</b>'
        >>> last_template_handler(["alt form", "enm" , "a", "pos=indefinite article"], "en")
        '<i>Alternative form of</i> <b>a</b> (indefinite article)'
        >>> last_template_handler(["alt form", "enm" , "worth", "t=to become"], "en")
        '<i>Alternative form of</i> <b>worth</b> (“to become”)'
        >>> last_template_handler(["alt form", "en" , "ess", "nodot=1"], "en")
        '<i>Alternative form of</i> <b>ess</b>'
        >>> last_template_handler(["surname", "en", "A=An", "English", "from=nicknames", "nodot=1"], "en")
        '<i>An English surname</i>'
    """
    from itertools import zip_longest

    from ...user_functions import italic, lookup_italic, strong, term

    # from .langs import langs

    # Handle the {{lb}} template
    if parts[0] in ("lb", "lbl", "label"):
        if len(parts) == 3:
            # return term(langs.get(parts[2], parts[2]))
            return term(parts[2])

        res = ""
        for word1, word2 in zip_longest(parts[2:], parts[3:]):
            if word1 in ("_", "and", "or"):
                continue
            if word1.startswith(("nocat=", "sort=")):
                continue

            # res += langs.get(word1, lookup_italic(word1, locale))
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

    # Handle the {{alt form}} template
    if parts[0] in ("alt form", "alternative form of"):
        res = italic("Alternative form of")
        res += f" {strong(parts[2])}"
        if len(parts) > 3:
            last = parts[-1]
            if "=" in last:
                cat, detail = last.split("=", 1)
                if cat == "t":
                    res += f" (“{detail}”)"
                elif cat != "nodot":
                    res += f" ({detail})"
            else:
                res += f" ({last})"
        return res

    # Handle the {{lb}} template
    if parts[0] == "surname":
        first = parts[2]
        second = parts[3]
        third = parts[0]
        if "=" in first:
            if second[0].lower() in "aeiouy":
                first = first.split("=")[1]
            else:
                first = first.split("=")[0]
        return italic(f"{first} {second} {third}")

    return term(parts[0])


# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"
