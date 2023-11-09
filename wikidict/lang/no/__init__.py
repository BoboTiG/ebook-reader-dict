"""Norwegian language."""

import re

from ...user_functions import flatten, uniq

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("norsk",)
section_sublevels = (3, 4)
etyl_section = ("Etymologi",)
sections = (
    *etyl_section,
    "Adjektiv",
    "Adverb",
    "Substantiv",
    "Verb",
)

# Variants
variant_titles = tuple(section for section in sections if section not in etyl_section)
variant_templates = (
    "{{no-adj-bøyningsform",
    "{{no-sub-bøyningsform",
    "{{no-verbform av",
    "{{no-verb-bøyningsform",
)

# Templates to ignore: the text will be deleted.
definitions_to_ignore = (
    #
    # For variants
    #
    "no-adj-bøyningsform",
    "no-sub-bøyningsform",
    "no-verbform av",
    "no-verb-bøyningsform",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "definisjon mangler",
    "etymologi mangler",
    "mangler definisjon",
    "norm",
)

# Templates more complex to manage.
templates_multi = {
    # {{alternativ skrivemåte|be}}
    "alternativ skrivemåte": "f\"{italic('alternativ skrivemåte av')} {strong(parts[-1])}\"",
    # {{bøyningsform|no|sub|korp}}
    "bøyningsform": "f\"{italic('bøyningsform av')} {strong(parts[-1])}\"",
    # {{feilstaving av|førstvoterende|språk=no}}
    "feilstaving av": 'f"Feilstaving av {parts[1]}."',
    # {{l|lt|duktė}}
    "l": "parts[-1]",
    # {{opphav|norrønt|språk=no}
    "opphav": "parts[1]",
    # {{prefiks|a|biotisk|språk=no}}
    "prefiks": 'f"{italic(parts[1])}- + {italic(parts[2])}"',
    # {{qualifier|idiomatisk}}
    "qualifier": "term(parts[1])",
    # {{suffiks|konsentrere|sjon|språk=no}}
    "suffiks": 'f"{italic(parts[1])} + -{italic(parts[2])}"',
    # {{tidligere bøyningsform|no|sub|jul}}
    "tidligere bøyningsform": "f\"{italic('tidligere bøyningsform av')} {strong(parts[-1])}\"",
    # {{tidligere skriveform|no|kunstnarleg}}
    "tidligere skriveform": "f\"{italic('tidligere skriveform av')} {strong(parts[-1])}\"",
    # {{tidligere skrivemåte|no|naturlig tall}}
    "tidligere skrivemåte": "f\"{italic('tidligere skrivemåte av')} {strong(parts[-1])}\"",
    # {{vokabular|overført}}
    "vokabular": "term(parts[1])",
    #
    # For variants
    #
    # {{no-adj-bøyningsform|b|vis|nb=ja|nrm=ja|nn=ja}}
    "no-adj-bøyningsform": "parts[2]",
    # {{no-verbform av|imperativ|børste|nb=ja}}
    "no-verbform av": "parts[2]",
    # {{no-sub-bøyningsform|be|funn|nb=ja|nrm=ja|nn=ja}}
    "no-sub-bøyningsform": "parts[2]",
    # {{no-verb-bøyningsform|pret|finne|nb=ja|nrm=ja}}
    "no-verb-bøyningsform": "parts[2]",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/no
release_description = """\
Ord räknas: {words_count}
Dumpa Wiktionary: {dump_date}

Tillgängliga filer:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Uppdaterad på {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_genders(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"{{n[bon]-sub\|(\w+)}}"),
) -> list[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("{{no-sub|m}}")
    ['m']
    >>> find_genders("{{no-sub|mf}}")
    ['mf']
    >>> find_genders("{{nn-sub|f}}")
    ['f']
    >>> find_genders("{{nb-sub|m}}")
    ['m']
    """
    return uniq(flatten(pattern.findall(code)))


def last_template_handler(
    template: tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["jus"], "no")
        '<i>(jus)</i>'
        >>> last_template_handler(["jus", "nb"], "no")
        '<i>(jus)</i>'
        >>> last_template_handler(["jus", "nn"], "no")
        '<i>(jus)</i>'
        >>> last_template_handler(["jus", "no"], "no")
        '<i>(jus)</i>'
        >>> last_template_handler(["jus", "no"], "nrm")
        '<i>(jus)</i>'

        >>> last_template_handler(["kontekst", "fobi", "utellelig", "kat=no:Fobier", "kat2=no:Masseord"], "no")
        '<i>(fobi, utellelig)</i>'
        >>> last_template_handler(["tema", "matematikk", "fysikk", "språk=no"], "no")
        '<i>(matematikk, fysikk)</i>'

        >>> last_template_handler(["overslån", "en", "no", "quality of life"], "no")
        'engelsk <i>quality of life</i>'
        >>> last_template_handler(["overslån", "en", "no", "virgin oil", "virgin", "t1=jomfru", "oil", "t2=olje"], "no")
        'engelsk <i>virgin oil</i>, <i>virgin</i> («jomfru») + <i>oil</i> («olje»)'

    """  # noqa
    from ...user_functions import concat, extract_keywords_from, italic, term
    from .codelangs import codelangs

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl in {"kontekst", "tema"}:
        return term(concat(parts, sep=", "))

    if tpl == "overslån":
        phrase = f"{codelangs[parts[0]]} {italic(parts[2])}"
        if rest := parts[3:]:
            phrase += ", "
            for idx, part in enumerate(rest, 1):
                phrase += italic(part)
                if trad := data[f"t{idx}"]:
                    phrase += f" («{trad}»)"
                if part != parts[-1]:
                    phrase += " + "

        return phrase

    if not parts or (len(parts) == 1 and parts[0] in {"nb", "nn", "no", "nrm"}):
        return term(tpl)

    raise ValueError(f"Unhandled template: {word=}, {template=}")
