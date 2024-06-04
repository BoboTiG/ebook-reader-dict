"""Danish language."""

import re
from typing import List

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{da}}", "dansk", "{{=da=}}")
etyl_section = ("{{etym}}", "Etymologi")
sections = (
    *etyl_section,
    "Adjektiv",
    "Adverbium",
    "Konjugation",
    "Lydord",
    "Personligt prononmen",
    "Possessivt prononmen",
    "Pronomen",
    "Prœposition",
    "Proposition",
    "Substantiv",
    "Ubestemt prononmen",
    "Verbum",
    "{{abbr}}",
    "{{abr}}",
    "{{adj}}",
    "{{adv}}",
    "{{afl}}",
    "{{conj}}",
    "{{interj}}",
    "{{noun}}",
    "{{prep}}",
    "{{pron}}",
    "{{prop}}",
    "{{verb}}",
    "{{car-num}}",
    "-adj-",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    "da-noun-2",
    "da-noun-3",
    "da-noun-4",
    "da-noun-5",
    "da-noun-6",
    "da-noun-7",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "definition mangler",
    "da-v-pres",
    "de",
    "dm",
    "-syn-",
    "etyl",
    "wikipedia",
    "Wikipedia",
    "infl",
)

templates_multi = {
    # {{compound|hjemme|værn}}
    "compound": "' + '.join(parts[1:])",
    # {{confix|cysto|itis|lang=da}}
    "confix": "parts[1] + '- + -' + parts[2]",
    # {{data}}
    "data": "'(' + italic('data') + ')'",
    # {{dublet af|da|boulevard}}
    "dublet af": "'dublet af ' + strong(parts[-1])",
    # {{en}}
    "en": "'Engelsk'",
    # {{form of|imperative form|bjerge|lang=da}}
    "form of": "italic(parts[1] + ' of') + ' ' + strong(parts[2])",
    # {{fysik}}
    "fysik": "'(' + italic('fysik') + ')'",
    # {{l|da|USA}}
    "l": "parts[-1]",
    # {{label|militær|våben}}
    "label": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{prefix|hoved|gade|lang=da}}
    "prefix": "parts[1] + '- + ' + parts[2]",
    # {{suffix|Norden|isk|lang=da}}
    "suffix": "parts[1] + ' + -' + parts[2]",
    # {{term|mouse|lang=en}}
    "term": "parts[1] + superscript('(' + parts[-1].lstrip('=lang') + ')')",
    # {{trad|en|limnology}}
    "trad": "parts[-1] + superscript('(' + parts[1] + ')')",
    # {{u|de|Reis}}
    "u": "parts[-1] + superscript('(' + parts[1] + ')')",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/da
release_description = """\
Ordtælling: {words_count}
Dump Wiktionary: {dump_date}

Tilgængelige filer:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Opdateret den {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_pronunciations(code: str) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{IPA|/bɛ̜ːˀ/|lang=da}}")
    ['/bɛ̜ːˀ/']
    """
    pattern = re.compile(r"\{\{IPA(?:\|(.*?))?\|lang=da\}\}", flags=re.MULTILINE)
    matches = re.findall(pattern, code) or []

    return [item for sublist in matches for item in sublist.split("|") if item]
