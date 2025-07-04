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
etyl_section = ("etymology", *[f"etymology {idx}" for idx in range(1, 20)])
sections = (
    *etyl_section,
    "adjective",
    "adverb",
    "article",
    "conjunction",
    "contraction",
    "determiner",
    "interjection",
    "letter",
    "noun",
    "numeral",
    "number",
    "particle",
    "punctuation mark",
    "prefix",
    "preposition",
    "pronoun",
    "proper noun",
    "suffix",
    "symbol",
    "verb",
)

# Variants
variant_titles = sections
variant_templates = (
    "{{active participle of",
    "{{adj form of",
    "{{agent noun of",
    "{{an of",
    "{{alternative plural of",
    "{{en-archaic",
    "{{female equivalent of",
    "{{feminine equivalent of",
    "{{femeq",
    "{{feminine of",
    "{{feminine plural of",
    "{{feminine plural past participle of",
    "{{feminine singular of",
    "{{feminine singular past participle of",
    "{{form of",
    "{{gerund of",
    "{{imperfective form of",
    "{{inflection of",
    "{{infl of",
    "{{masculine plural of",
    "{{masculine plural past participle of",
    "{{neuter plural of",
    "{{neuter singular past participle of",
    "{{noun form of",
    "{{participle of",
    "{{passive of",
    "{{passive participle of",
    "{{past participle form of",
    "{{past participle of",
    "{{perfective form of",
    "{{plural of",
    "{{plural",
    "{{present participle of",
    "{{reflexive of",
    "{{verbal noun of",
    "{{verb form of",
)

# Some definitions are not good to keep
definitions_to_ignore = ("rfdef",)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "#tag",
    "anchor",
    "Anchor",
    "ant",
    "attention",
    "attn",
    "audio",
    "box-bottom",
    "box-top",
    "c",
    "C",
    "catlangname",
    "center bottom",
    "center top",
    "character info",
    "cite-av",
    "cite-book",
    "cite-journal",
    "cite-newsgroup",
    "cite-song",
    "cite-thesis",
    "cite-video game",
    "cite-web",
    "cln",
    "col",
    "col-bottom",
    "col-top",
    "commonscat",
    "def-unc",
    "def-uncertain",
    "dercat",
    "dhub",
    "elements",
    "enum",
    "etymid",
    "etymon",
    "etystub",
    "examples",
    "hot sense",
    "hot word",
    "Image requested",
    "lena",
    "listen",
    "multiple image",
    "multiple images",
    "nonlemma",
    "number box",
    "+obj",
    "pedia",
    "PIE word",
    "picdic",
    "picdicimg",
    "picdiclabel",
    "quote-book",
    "quote-hansard",
    "quote-journal",
    "quote-mailing list",
    "quote-newsgroup",
    "quote-song",
    "quote-us-patent",
    "quote-video game",
    "quote-web",
    "quote-wikipedia",
    "R",
    "ref",
    "reflist",
    "refn",
    "rel-bottom",
    "rel-top",
    "rf-sound example",
    "rfap",
    "rfc",
    "rfc-sense",
    "rfclarify",
    "rfd",
    "rfd-redundant",
    "rfd-sense",
    "rfdate",
    "rfdef",
    "rfe",
    "rfeq",
    "rfetym",
    "rfex",
    "rfi",
    "rfm",
    "rfm-sense",
    "rfp",
    "rfq",
    "rfq-sense",
    "rfquote",
    "rfquote-sense",
    "rfref",
    "rfscript",
    "rfusex",
    "rfv",
    "rfv-etym",
    "rfv-sense",
    "root",
    "see",
    "see desc",
    "slim-wikipedia",
    "senseid",
    "senseno",
    "seeCites",
    "sid",
    "swp",
    "syndiff",
    "synonyms",
    "t-needed",
    "tea room",
    "tea room sense",
    "thub",
    "top",
    "topic",
    "topics",
    "translation only",
    "unsupported",
    "ux",
    "void",
    "was wotd",
    "wikidata",
    "wikipedia",
    "Wikipedia",
    "wikispecies",
    "Wikispecies",
    "word",
    "wp",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    **labels,
    "gentrade": "Genericized trademark",
}

# Templates more complex to manage.
templates_multi = {
    # {{1|interactive}}
    "1": "capitalize(parts[-1])",
    # {{abbrev|en|goodbye}}
    "abbrev": 'f"Abbreviation of {italic(parts[-1])}"',
    # {{C.|21|st}}
    "C.": "parts[1] + (parts[2] if len(parts) > 2 else 'th') + f' c.'",
    # {{caps|discourse}}
    "caps": "parts[-1]",
    # {{circa2|1850s}}
    "circa2": "italic('circa' if 'short=yes' not in parts and 'short=1' not in parts else 'c.') + f' {parts[1]}'",
    "color panel": "color(parts[-1])",
    # {{defdate|from 15th c.}}
    "defdate": "small('[' + parts[1] + (f'–{parts[2]}' if len(parts) > 2 else '') + ']')",
    # {{en:w|Pepe the Frog}} -> {{en|w|Pepe the Frog}}
    "en": "parts[-1]",
    # {{en-comparative of|term}}
    "en-comparative of": "italic('comparative form of') + f' {strong(parts[1])}' + ': more ' + parts[1]",
    # {{en-obsolete past participle of|baptize}}
    "en-obsolete past participle of": "f\"{term('obsolete')} <i>past participle of</i> {strong(parts[1])}\"",
    # {{en-superlative of|Brummie}}
    "en-superlative of": "f\"{italic('superlative form of')} {strong(parts[1])}: most {parts[1]}\"",
    # {{en-early modern spelling of|colour}}
    "en-early modern spelling of": 'f"<i>Early Modern spelling of</i> {strong(parts[1])}"',
    # {{from|en|-er|id=Oxford}}
    "from": "parts[2]",
    # {{gl|liquid H<sub>2</sub>O}}
    "gl": "parenthesis(parts[1])",
    # {{gloss|liquid H<sub>2</sub>O}}
    "gloss": "parenthesis(parts[1])",
    # {{glossary|inflected}}
    "glossary": "parts[-1]",
    # {{i|Used only ...}}
    "i": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{IPAfont|[[ʌ]]}}
    "IPAfont": "f\"&lsaquo;{parts[1].strip('⟨⟩')}&rsaquo;\"",
    # {{italic|Love Island}}
    "italic": "italic(parts[1])",
    # {{ja-def|茨城}}
    "ja-def": 'f"{parts[1]}:"',
    # {{lang|fr|texte}}
    "lang": "parts[-1]",
    # {{less common spelling of|en|African-like}
    "less common spelling of": 'f"<i>rare spelling of</i> <b>{parts[-1]}</b>"',
    # {{lit|eagle killer}}
    "lit": 'f"Literally, “{parts[1]}”"',
    # {{m-self|en|a|b}}
    "m-self": "italic(parts[-1])",
    # {{mention-gloss|silver-bearing}}
    "mention-gloss": 'f"“{parts[-1]}”"',
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
    # {{noitalic|ふうじん}}
    "noitalic": "parts[1]",
    # {{nobr|1=[ ...=C=C=C=... ]}}
    "nobr": 'f\'<span style="white-space:nowrap">{parts[1].lstrip("1=")}</span>\'',
    "nominalization": 'f"Nominalization of {italic(parts[-1])}"',
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
    # {{|&thinsp;𝼊&thinsp;}}
    "orthography": "f'&lsaquo;{parts[1]}&rsaquo;'",
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
    # {{Runr-def|ᛗ}}
    "Runr-def": 'f"The Runic character {parts[1]}."',
    # {{s|foo}}
    "s": "f'{parenthesis(italic(parts[1]))} :'",
    # {{sense|foo}}
    "sense": "f'{parenthesis(italic(parts[1]))} :'",
    # {{shitgibbon|en|arse|muncher}}
    "shitgibbon": 'f"Shitgibbon compound of {italic(parts[2])} + {italic(parts[3])}"',
    # {{small|(kraken)}}
    "small": "small(parts[1])",
    # {{small caps|ce}}
    "small caps": "small_caps(parts[1])",
    # {{smallcaps|ce}}
    "smallcaps": "small_caps(parts[1])",
    # {{smc|ce}}
    "smc": "small_caps(parts[1])",
    # {{speciesabbrev|C|difficile||la}}
    "speciesabbrev": "f'Used, in context, to shorten the name and simplify the pronunciation of a species name with a generic name beginning with {parts[1]} and a specific epithet of {parts[2]}.'",
    # {{staco|Airport station (MTR)|Airport|Hong Kong}}
    "staco": 'f"<i>(rail transport) The station code of</i> <b>{parts[2] or parts[1]}</b> <i>in {parts[3]}</i>."',
    # {{sub|KI}}
    "sub": "subscript(parts[1])",
    # {{sup|KI}}
    "sup": "superscript(parts[1])",
    # {{syc-root|ܪ ܩ ܥ}}
    "syc-root": "parts[-1]",
    # {{taxfmt|Gadus macrocephalus|species|ver=170710}}
    "taxfmt": "italic(parts[1])",
    # {{taxlink|Gadus macrocephalus|species|ver=170710}}
    "taxlink": "italic(parts[1])",
    "taxlink2": "italic(parts[1])",
    # {{IUPAC-1|alanine}}
    "IUPAC-1": 'f"IUPAC 1-letter symbol for {parts[1]}"',
}
templates_multi["angbr"] = templates_multi["IPAfont"]
templates_multi["angbr IPA"] = templates_multi["IPAfont"]
templates_multi["datedef"] = templates_multi["defdate"]
templates_multi["defdt"] = templates_multi["defdate"]
templates_multi["lg"] = templates_multi["glossary"]
templates_multi["m-g"] = templates_multi["mention-gloss"]
templates_multi["nom"] = templates_multi["nominalization"]
templates_multi["orthography"] = templates_multi["IPAfont"]
templates_multi["upright"] = templates_multi["noitalic"]

# Templates that will be completed/replaced using custom text.
templates_other = {
    "--": "&nbsp;—",
    "=": "=",
    ",": ",",
    "Brai-ety": "Invented by Louis Braille, braille cells were arranged in numerical order and assigned to the letters of the French alphabet. Most braille alphabets follow this assignment for the 26 letters of the basic Latin alphabet or, in non-Latin scripts, for the transliterations of those letters. In such alphabets, the first ten braille letters (the first decade: ⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚) are assigned to the Latin letters A to J and to the digits 1 to 9 and 0. (Apart from '2', the even digits all have three dots: ⠃⠙⠋⠓⠚.)<br/><br/>The letters of the first decade are those cells with at least one dot in the top row and at least one in the left column, but none in the bottom row.  The next decade repeat the pattern with the addition of a dot at the lower left, the third decade with two dots in the bottom row, and the fourth with a dot on the bottom right. The fifth decade is like the first, but shifted downward one row. The first decade is supplemented by the two characters with dots in the right column and none in the bottom row, and that supplement is propagated to the other decades using the generation rules above. Finally, there are four characters with no dots in the top two rows. Many languages that use braille letters beyond the 26 of the basic Latin alphabet follow an approximation of the English or French values for additional letters.",
    "corruption": "corruption",
    "epi-def": "<i>Used as a specific epithet</i>",
    "internationalism": "Internationalism",
    "nbsp": "&nbsp;",
    "mdash": "&mdash;",
    "sic": "<sup>[<i>sic</i>]</sup>",
}


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


def find_genders(code: str, locale: str) -> list[str]:
    """
    >>> find_genders("", "en")
    []
    >>> find_genders("{{taxoninfl|i=1|g=f}}", "en")
    ['f']
    """
    pattern = re.compile(r"{taxoninfl\|(?:i=\d+\|)?g=(\w+).*")
    return unique(flatten(pattern.findall(code)))


def find_pronunciations(code: str, locale: str) -> list[str]:
    """
    >>> find_pronunciations("", "en")
    []
    >>> find_pronunciations("{{IPA|en|/ʌs/}}", "en")
    ['/ʌs/']
    >>> find_pronunciations("{{IPA|en|/ʌs/|/ʌs/}}", "en")
    ['/ʌs/']
    >>> find_pronunciations("{{IPA|en|/ʌs/}} {{IPA|en|/ʌs/}}", "en")
    ['/ʌs/']
    >>> find_pronunciations("{{IPA|en|/ʌs/}}, {{IPA|en|/ʌz/}}", "en")
    ['/ʌs/', '/ʌz/']
    >>> find_pronunciations("{{IPA|en|/ʌs/|/ʌz/}}", "en")
    ['/ʌs/', '/ʌz/']
    """
    pattern = re.compile(rf"\{{IPA\|{locale}\|(/[^/]+/)(?:\|(/[^/]+/))*")
    return unique(flatten(pattern.findall(code)))


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    all_templates: list[tuple[str, str, str]] | None = None,
    variant_only: bool = False,
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["eye dialect of", "en" , "ye#Etymology 6", "t=t", "from=from", "from2=from2"], "en")
        '<i>Eye dialect spelling of</i> <b>ye</b> (“t”)<i>, representing from and from2 English</i>'
        >>> last_template_handler(["alternative spelling of", "en" , "ye", "from=from", "from2=from2"], "en")
        '<i>From and from2 spelling of</i> <b>ye</b>'

        >>> last_template_handler(["initialism of", "en", "w:Shockwave Flash"], "en")
        '<i>Initialism of</i> <b>Shockwave Flash</b>'
        >>> last_template_handler(["initialism of", "en", "optical character reader", "dot=&nbsp;(the scanning device)"], "en")
        '<i>Initialism of</i> <b>optical character reader</b>&nbsp;(the scanning device)'
        >>> last_template_handler(["init of", "en", "optical character reader", "tr=tr", "t=t", "ts=ts"], "en")
        '<i>Initialism of</i> <b>optical character reader</b> (<i>tr</i> /ts/, “t”)'
        >>> last_template_handler(["init of", "en", "OCR", "optical character reader", "nodot=1", "nocap=1"], "en")
        '<i>initialism of</i> <b>optical character reader</b>'

        >>> last_template_handler(["standard spelling of", "en", "from=Irish English", "Irish Traveller"], "en")
        '<i>Irish English standard spelling of</i> <b>Irish Traveller</b>'
        >>> last_template_handler(["standard spelling of", "en", "enroll"], "en")
        '<i>Standard spelling of</i> <b>enroll</b>'
        >>> last_template_handler(["cens sp", "en", "bitch"], "en")
        '<i>Censored spelling of</i> <b>bitch</b>'

        >>> last_template_handler(["pronunciation spelling of", "en", "everything", "from=AAVE"], "en")
        '<i>Pronunciation spelling of</i> <b>everything</b><i>, representing African-American Vernacular English</i>'

        >>> last_template_handler(["zh-m", "痟", "tr=siáu", "mad"], "en")
        '痟 (<i>siáu</i>, “mad”)'
    """

    from ...user_functions import capitalize, chinese, extract_keywords_from, italic, strong
    from .. import defaults
    from .form_of import form_of_templates
    from .langs import langs
    from .template_handlers import gloss_tr_poss, join_names, lookup_template, render_template

    tpl, *parts = template

    tpl_variant = f"__variant__{tpl}"
    if variant_only:
        tpl = tpl_variant
        template = tuple([tpl_variant, *parts])
    elif lookup_template(tpl_variant):
        # We are fetching the output of a variant template, we do not want to keep it
        return ""

    if lookup_template(template[0]):
        return render_template(word, template)

    data = extract_keywords_from(parts)

    if tpl in form_of_templates:
        starter = form_of_templates[tpl]
        ender = ""
        lang = data["1"] or (parts.pop(0) if parts else "")
        word = (data["2"] or (parts.pop(0) if parts else "")).split("#", 1)[0]

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

        starter = starter[0].lower() + starter[1:] if data["nocap"] else capitalize(starter)
        phrase = italic(starter)
        phrase += f" {strong(word)}"
        phrase += gloss_tr_poss(data, gloss)
        if ender:
            phrase += ender
        if dot := data["dot"]:
            phrase += dot
        return phrase

    if tpl in ("zh-l", "zh-m"):
        return chinese(parts, data)

    return defaults.last_template_handler(template, locale, word=word, all_templates=all_templates)


# https://en.wiktionary.org/wiki/Wiktionary:Random_page
random_word_url = "https://en.wiktionary.org/wiki/Special:RandomInCategory/English_lemmas#English"


def adjust_wikicode(code: str, locale: str) -> str:
    # sourcery skip: inline-immediately-returned-variable
    """
    >>> adjust_wikicode('{| class="floatright"\\n|-\\n| {{PIE word|en|h₁eǵʰs}}\\n| {{PIE word|en|ḱóm}}\\n|}', "en")
    ''
    >>> adjust_wikicode('{| class="floatright"\\n|-\\n| {{PIE word|en|h₁eǵʰs}}\\n| {{PIE word|en|ḱóm}}\\n|}{{root|en|ine-pro|*(s)ker-|id=cut|*h₃reǵ-}}', "en")
    '{{root|en|ine-pro|*(s)ker-|id=cut|*h₃reǵ-}}'
    >>> adjust_wikicode("<math>\\\\frac{|AP|}{|BP|} = \\\\frac{|AC|}{|BC|}</math>", "en")
    '<math>\\\\frac{|AP|}{|BP|} = \\\\frac{|AC|}{|BC|}</math>'
    """
    # Remove tables (cf issue #2073)
    code = re.sub(r"^\{\|.*?\|\}", "", code, flags=re.DOTALL | re.MULTILINE)

    return code
