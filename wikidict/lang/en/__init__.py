"""English language."""

import re

from ...user_functions import flatten, unique
from .labels import labels

# Float number separator
float_separator = "."

# Thousands separator
thousands_separator = ","

# Markers for sections that contain interesting text to analyse.
head_sections = ("english", "translingual")
section_sublevels = (4, 3)
etyl_section = ("etymology", "etymology 1")
sections = (
    "adjective",
    "adverb",
    "article",
    "conjunction",
    "contraction",
    "determiner",
    *etyl_section,
    "interjection",
    "noun",
    "numeral",
    "particle",
    "prefix",
    "preposition",
    "pronoun",
    "proper noun",
    "suffix",
    "symbol",
    "verb",
)

# Variants
variant_titles = (
    "noun",
    "verb",
)
variant_templates = (
    "{{en-ing",
    "{{en-ipl",
    "{{en-irregular",
    "{{en-past",
    "{{en-simple",
    "{{en-superlative",
    "{{en-third",
    "{{en-tpso",
    "{{infl of",
    "{{plural of",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    "rfdef",
    #
    # Variants
    #
    "en-ing",
    "en-irregular plural of",
    "en-past of",
    "en-simple past of",
    "en-superlative of",
    "en-tpso",
    "en-third-person singular of",
    "en-third person singular of",
    "en-third-person_singular_of",
    "infl of",
    "plural of",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "anchor",
    "attention",
    "c",
    "C",
    "cln",
    "dercat",
    "elements",
    "etymid",
    "etymon",
    "etystub",
    "examples",
    "Image requested",
    "lena",
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
    "rfe",
    "rfex",
    "rfi",
    "rfquote-sense",
    "rfv-etym",
    "rfv-sense",
    "root",
    "slim-wikipedia",
    "senseid",
    "senseno",
    "seeCites",
    "swp",
    "tea room",
    "tea room sense",
    "top",
    "topics",
    "translation only",
    "was wotd",
    "wikipedia",
    "Wikipedia",
    "wikispecies",
    "Wikispecies",
    "wp",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    **labels,
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
    "defdate": "small('[' + parts[1] + (f'–{parts[2]}' if len(parts) > 2 else '') + ']')",
    # {{en-archaic third-person singular of|term}}
    "en-archaic third-person singular of": "italic('(archaic) third-person singular simple present indicative form of') + f' {strong(parts[1])}'",
    # {{en-comparative of|term}}
    "en-comparative of": "italic('comparative form of') + f' {strong(parts[1])}' + ': more ' + parts[1]",
    # {{en-archaic second-person singular of|term}}
    "en-archaic second-person singular of": "italic('(archaic) second-person singular simple present form of') + f' {strong(parts[1])}'",
    # {{en-archaic second-person singular past of|term}}
    "en-archaic second-person singular past of": "italic('(archaic) second-person singular simple past form of') + f' {strong(parts[1])}'",
    # {{gl|liquid H<sub>2</sub>O}}
    "gl": "parenthesis(parts[1])",
    # {{gloss|liquid H<sub>2</sub>O}}
    "gloss": "parenthesis(parts[1])",
    # {{glossary|inflected}}
    "glossary": "parts[-1]",
    # {{i|Used only ...}}
    "i": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{IPAfont|[[ʌ]]}}
    "IPAfont": 'f"⟨{parts[1]}⟩"',
    # {{lang|fr|texte}}
    "lang": "parts[-1]",
    # {{Latn-def|en|name|O|o}}
    "Latn-def": "f'{italic(\"The name of the Latin-script letter\")} {strong(parts[3])}.' if parts[2] == 'name' else ''",
    # {{Latn-def-lite|en|name|O|o}}
    "Latn-def-lite": "f'{italic(\"The name of the Latin-script letter\")} {strong(parts[3])}.' if parts[2] == 'name' else ''",
    # {{monospace|#!}}
    "mono": "f'<span style=\"font-family:monospace\">{parts[1]}</span>'",
    "monospace": "f'<span style=\"font-family:monospace\">{parts[1]}</span>'",
    # {{n-g|Definite grammatical ...}}
    "n-g": "italic(parts[-1].lstrip('1='))",
    # {{n-g-lite|Definite grammatical ...}}
    "n-g-lite": "italic(parts[-1].lstrip('1='))",
    # {{ng|Definite grammatical ...}}
    "ng": "italic(parts[-1].lstrip('1='))",
    # {{ng-lite|Definite grammatical ...}}
    "ng-lite": "italic(parts[-1].lstrip('1='))",
    # {{ngd|Definite grammatical ...}}
    "ngd": "italic(parts[-1].lstrip('1='))",
    # {{nobr|1=[ ...=C=C=C=... ]}}
    "nobr": 'f\'<span style="white-space:nowrap">{parts[1].lstrip("1=")}</span>\'',
    # {{non gloss|Definite grammatical ...}}
    "non gloss": "italic(parts[-1].lstrip('1='))",
    # {{non-gloss|Definite grammatical ...}}
    "non-gloss": "italic(parts[-1].lstrip('1='))",
    # {{non-gloss definition|Definite grammatical ...}}
    "non-gloss definition": "italic(parts[-1].lstrip('1='))",
    # {{non gloss definition|Definite grammatical ...}}
    "non gloss definition": "italic(parts[-1].lstrip('1='))",
    # {{nowrap|1=[ ...=C=C=C=... ]}}
    "nowrap": 'f\'<span style="white-space:nowrap">{parts[1].lstrip("1=")}</span>\'',
    # {{q|Used only ...}}
    "q": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{q-lite|Used only ...}}
    "q-lite": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{qf|Used only ...}}
    "qf": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{qua|Used only ...}}
    "qua": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{qual|Used only ...}}
    "qual": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{qualifier|Used only ...}}
    "qualifier": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{qualifier-lite|Used only ...}}
    "qualifier-lite": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{s|foo}}
    "s": "f'{parenthesis(italic(parts[1]))} :'",
    # {{sense|foo}}
    "sense": "f'{parenthesis(italic(parts[1]))} :'",
    # {{small caps|ce}}
    "small caps": "small_caps(parts[1])",
    # {{smallcaps|ce}}
    "smallcaps": "small_caps(parts[1])",
    # {{smc|ce}}
    "smc": "small_caps(parts[1])",
    # {{sub|KI}}
    "sub": "subscript(parts[1])",
    # {{sup|KI}}
    "sup": "superscript(parts[1])",
    # {{taxfmt|Gadus macrocephalus|species|ver=170710}}
    "taxfmt": "italic(parts[1])",
    # {{taxlink|Gadus macrocephalus|species|ver=170710}}
    "taxlink": "italic(parts[1])",
    #
    # Variants
    #
    # {{en-ing form of|term}}
    "en-ing form of": "parts[1]",
    # {{en-simple past of|term}}
    "en-simple past of": "parts[1]",
    # {{en-irregular plural of|term}}
    "en-irregular plural of": "parts[1]",
    "en-ipl": "parts[1]",
    # {{en-past of|term}}
    "en-past of": "parts[1]",
    # {{en-superlative of|term}}
    "en-superlative of": "parts[1]",
    # {{en-tpso|term}}
    "en-tpso": "parts[1]",
    # {{en-third-person singular of|term}}
    "en-third-person singular of": "parts[1]",
    # {{en-third-person_singular_of|term}}
    "en-third-person_singular_of": "parts[1]",
    # {{en-third person singular of|term}}
    "en-third person singular of": "parts[1]",
    # {{plural of|en|human}}
    "plural of": "parts[2]",
}

# Templates that will be completed/replaced using custom text.
templates_other = {"nbsp": "&nbsp;"}


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/en
release_description = """\
### 🌟 In order to be regularly updated, this project needs support; [click here](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) to donate. 🌟

<br/>


Words count: {words_count}
Wiktionary dump: {dump_date}

Full version:
{download_links_full}

Etymology-free version:
{download_links_noetym}

<sub>Updated on {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_pronunciations(
    code: str,
    *,
    pattern: re.Pattern[str] = re.compile(r"{IPA\|en\|(/[^/]+/)(?:\|(/[^/]+/))*"),
) -> list[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{IPA|en|/ʌs/}}")
    ['/ʌs/']
    >>> find_pronunciations("{{IPA|en|/ʌs/|/ʌs/}}")
    ['/ʌs/']
    >>> find_pronunciations("{{IPA|en|/ʌs/}} {{IPA|en|/ʌs/}}")
    ['/ʌs/']
    >>> find_pronunciations("{{IPA|en|/ʌs/}}, {{IPA|en|/ʌz/}}")
    ['/ʌs/', '/ʌz/']
    >>> find_pronunciations("{{IPA|en|/ʌs/|/ʌz/}}")
    ['/ʌs/', '/ʌz/']
    """
    return unique(flatten(pattern.findall(code)))


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    missed_templates: list[tuple[str, str]] | None = None,
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

        >>> last_template_handler(["initialism of", "en", "w:Shockwave Flash"], "en")
        '<i>Initialism of</i> <b>Shockwave Flash</b>.'
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
        >>> last_template_handler(["cens sp", "en", "bitch"], "en")
        '<i>Censored spelling of</i> <b>bitch</b>.'

        >>> last_template_handler(["pronunciation spelling of", "en", "everything", "from=AAVE"], "en")
        '<i>Pronunciation spelling of</i> <b>everything</b><i>, representing African-American Vernacular English</i>.'

        >>> last_template_handler(["zh-m", "痟", "tr=siáu", "mad"], "en")
        '痟 (<i>siáu</i>, “mad”)'

        #
        # Variants
        #
        >>> last_template_handler(["infl of", "en", "cling", "", "ing-form"], "en")
        'cling'
        >>> last_template_handler(["infl of", "1=en", "2=cling", "3=", "4=ing-form"], "en")
        'cling'

    """

    from ...user_functions import capitalize, chinese, extract_keywords_from, italic, strong
    from .form_of import form_of_templates
    from .langs import langs
    from .template_handlers import gloss_tr_poss, join_names, lookup_template, render_template

    if lookup_template(template[0]):
        return render_template(word, template)

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "infl of":
        return data["2"] or parts[1]

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
            gloss = data["t"] or data["gloss"] or data["5"] or (parts.pop(0) if parts else "")
        else:
            text = data["alt"] or data["3"] or (parts.pop(0) if parts else "")
            gloss = data["t"] or data["gloss"] or data["4"] or (parts.pop(0) if parts else "")
        word = text or word
        if word.startswith("w:"):
            word = word[2:]

        if fromtext := join_names(data, "from", " and "):
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
                ender = italic(f", representing {templates_italic.get(data['from'], fromtext)} {langs[lang]}")
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
            elif data["nodot"] not in ("1", "y", "yes"):
                phrase += "."
        return phrase

    if tpl in ("zh-l", "zh-m"):
        return chinese(parts, data)

    try:
        return f"{italic(capitalize(tpl))} {strong(parts[1])}"
    except IndexError:
        return capitalize(tpl)
