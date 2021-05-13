"""English language."""
from typing import Tuple

# Regex to find the pronunciation
pronunciation = r"{IPA\|en\|/([^/]+)/"

# Float number separator
float_separator = "."

# Thousads separator
thousands_separator = ","

# Markers for sections that contain interesting text to analyse.
head_sections = ("==English==", "english")
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
templates_ignored = (
    "c",
    "C",
    "cln",
    "elements",
    "multiple images",
    "+obj",
    "PIE word",
    "picdic",
    "picdicimg",
    "picdiclabel",
    "refn",
    "rel-bottom",
    "rel-top",
    "rfc-sense",
    "rfd-redundant",
    "rfd-sense",
    "rfv-etym",
    "rfv-sense",
    "rfex",
    "root",
    "senseid",
    "seeCites",
    "tea room",
    "tea room sense",
    "top",
    "topics",
    "was wotd",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "AAVE": "African-American Vernacular",
    "American": "US",
    "Early ME": "Early Middle English",
}

# Templates more complex to manage.
templates_multi = {
    # {{1|interactive}}
    "1": "capitalize(parts[-1])",
    # {{C.|21|st}}
    "C.": "parts[1] + (parts[2] if len(parts) > 2 else 'th') + f' c.'",
    # {{circa2|1850s}}
    "circa2": "italic('circa' if 'short=yes' not in parts and 'short=1' not in parts else 'c.') + f' {parts[1]}'",
    # {{defdate|from 15th c.}}
    "defdate": "small('[' + parts[1] + ']')",
    # {{en-archaic third-person singular of|term}}
    "en-archaic third-person singular of": "italic('(archaic) third-person singular simple present indicative form of') + f' {strong(parts[1])}'",  # noqa
    # {{en-comparative of|term}}
    "en-comparative of": "italic('comparative form of') + f' {strong(parts[1])}' + ': more ' + parts[1]",
    # {{en-archaic second-person singular of|term}}
    "en-archaic second-person singular of": "italic('(archaic) second-person singular simple present form of') + f' {strong(parts[1])}'",  # noqa
    # {{en-archaic second-person singular past of|term}}
    "en-archaic second-person singular past of": "italic('(archaic) second-person singular simple past form of') + f' {strong(parts[1])}'",  # noqa
    # {{en-ing form of|term}}
    "en-ing form of": "italic('Present participle and gerund of') + f' {strong(parts[1])}'",
    # {{en-simple past of|term}}
    "en-simple past of": "italic('simple past tense of') + f' {strong(parts[1])}'",
    # {{en-irregular plural of|term}}
    "en-irregular plural of": "italic('plural of') + f' {strong(parts[1])}'",
    # {{en-past of|term}}
    "en-past of": "italic('simple past tense and past participle of') + f' {strong(parts[1])}'",
    # {{en-superlative o|term}}
    "en-superlative of": "italic('superlative form of') + f' {strong(parts[1])}' + ': most ' + parts[1]",
    # {{en-third-person_singular_of|term}}
    "en-third-person_singular_of": "italic('Third-person singular simple present indicative form of') + f' {strong(parts[1])}'",  # noqa
    # {{gloss|liquid H<sub>2</sub>O}}
    "gloss": "parenthesis(parts[1])",
    # {{glossary|inflected}}
    "glossary": "parts[-1]",
    # {{IPAchar|[tʃ]|lang=en}})
    "IPAchar": "parts[1]",
    # {{IPAfont|[[ʌ]]}}
    "IPAfont": 'f"⟨{parts[1]}⟩"',
    # {{Latn-def|en|name|O|o}}
    "Latn-def": "f'{italic(\"The name of the Latin-script letter\")} {strong(parts[3])}.' if parts[2] == 'name' else ''",  # noqa
    # {{n-g|Definite grammatical ...}}
    "n-g": "italic(parts[-1].lstrip('1='))",
    # {{ngd|Definite grammatical ...}}
    "ngd": "italic(parts[-1].lstrip('1='))",
    # {{non-gloss definition|Definite grammatical ...}}
    "non-gloss definition": "italic(parts[-1].lstrip('1='))",
    # {{q|Used only ...}}
    "q": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{qual|Used only ...}}
    "qual": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{qualifier|Used only ...}}
    "qualifier": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{sub|KI}}
    "sub": "subscript(parts[1])",
    # {{sup|KI}}
    "sup": "superscript(parts[1])",
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
        >>> last_template_handler(["alt form", "en" , "a", "b", "t=t", "ts=ts", "tr=tr", "pos=pos", "from=from", "from2=from2", "lit=lit"], "en")
        '<i>From and from2 form of</i> <b>b</b> (<i>tr</i> /ts/, “t”, pos, literally “lit”)'
        >>> last_template_handler(["eye dialect of", "en" , "ye", "t=t", "from=from", "from2=from2"], "en")
        '<i>Eye dialect spelling of</i> <b>ye</b> (“t”)<i>, representing from and from2 English</i>.'
        >>> last_template_handler(["alternative spelling of", "en" , "ye", "from=from", "from2=from2"], "en")
        '<i>From and from2 spelling of</i> <b>ye</b>'

        >>> last_template_handler(["initialism of", "en", "optical character reader", "dot=&nbsp;(the scanning device)"], "en")
        '<i>Initialism of</i> <b>optical character reader</b>&nbsp;(the scanning device)'
        >>> last_template_handler(["init of", "en", "optical character reader", "tr=tr", "t=t", "ts=ts"], "en")
        '<i>Initialism of</i> <b>optical character reader</b> (<i>tr</i> /ts/, “t”).'
        >>> last_template_handler(["init of", "en", "OCR", "optical character reader", "nodot=1", "nocap=1"], "en")
        '<i>initialism of</i> <b>optical character reader</b>'

        >>> last_template_handler(["standard spelling of", "en", "from=Irish English", "Irish Traveller"], "en")
        '<i>Irish English standard spelling of</i> <b>Irish Traveller</b>.'
        >>> last_template_handler(["standard spelling of", "en", "enroll"], "en")
        '<i>Standard spelling of</i> <b>enroll</b>.'

    """  # noqa

    from .langs import langs

    from .form_of import form_of_templates
    from ...user_functions import (
        capitalize,
        chinese,
        extract_keywords_from,
        italic,
        strong,
    )
    from .template_handlers import (
        render_template,
        lookup_template,
        gloss_tr_poss,
        join_names,
    )

    if lookup_template(template[0]):
        return render_template(template)

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl in form_of_templates:
        template_model = form_of_templates[tpl]
        starter = str(template_model["text"])
        ender = ""
        lang = data["1"] or (parts.pop(0) if parts else "")
        word = data["2"] or (parts.pop(0) if parts else "")

        # form is the only one to be a bit different
        if tpl == "form of":
            starter = f"{word} of" if word else "form of"
            word = data["3"] or (parts.pop(0) if parts else "")
            text = data["4"] or (parts.pop(0) if parts else "")
            gloss = data["t"] or data["5"] or (parts.pop(0) if parts else "")
        else:
            text = data["alt"] or data["3"] or (parts.pop(0) if parts else "")
            gloss = data["t"] or data["4"] or (parts.pop(0) if parts else "")
        word = text or word

        fromtext = join_names(data, "from", " and ")
        if fromtext:
            cap = starter[0].isupper()
            from_suffix = "form of"
            if tpl == "standard spelling of":
                from_suffix = "standard spelling of"
            elif tpl == "alternative spelling of":
                from_suffix = "spelling of"
            elif tpl in (
                "eye dialect of",
                "pronunciation spelling of",
                "pronunciation variant of",
            ):
                ender = italic(f", representing {fromtext} {langs[lang]}")
            if not ender:
                starter = f"{fromtext} {from_suffix}"
                starter = capitalize(starter) if cap else starter

        starter = starter[0].lower() + starter[1:] if data["nocap"] == "1" else starter
        phrase = italic(starter)
        phrase += f" {strong(word)}"
        phrase += gloss_tr_poss(data, gloss)
        if ender:
            phrase += ender
        if template_model["dot"]:
            if data["dot"]:
                phrase += data["dot"]
            elif data["nodot"] != "1":
                phrase += "."
        return phrase

    if tpl in ("zh-l", "zh-m"):
        return chinese(parts, data)

    try:
        return f"{italic(capitalize(tpl))} {strong(parts[1])}"
    except IndexError:
        return capitalize(tpl)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/en
release_description = """\
Words count: {words_count}
Wiktionary dump: {dump_date}

Available files:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Updated on {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"
