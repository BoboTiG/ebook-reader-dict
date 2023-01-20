"""Italian language."""
import re
from typing import Dict, List, Pattern, Tuple

from ...user_functions import uniq

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{-it-}}",)
etyl_section = ("{{etim}}",)
sections = (
    *head_sections,
    *etyl_section,
    "{{acron}",
    "{{agg}",
    "{{avv}",
    "{{art}",
    "{{cong}",
    "{{inter}",
    "{{pref}",
    "{{Pn}",
    "{{prep}",
    "{{pron poss}",
    "{{suff}",
    "{{sost}",
    "{{verb}",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    "{{verb form",
    "{{nome",
    #  "{{agg form",
    "{{sost form",
    "{{-sost form-",
    "{{It-conj",
)

# Templates to ignore: the text will be deleted.
templates_ignored = ("Nodef", "Noetim", "Noref", "Trad1", "Trad2")

# Templates more complex to manage.
templates_multi: Dict[str, str] = {
    # {{context|ecology|lang=it}}
    "Context": "small(term(parts[1]))",
    "context": "small(term(parts[1]))",
    # {{Est|raro|it}}
    "Est": "small(term('per estensione'))",
    "est": "small(term('per estensione'))",
    # {{Etim-link|aggrondare}}
    # {{Etim-link||cervice}}
    "Etim-link": "'vedi ' + parts[2 if len(parts) >= 3 else 1]",
    "etim-link": "'vedi ' + parts[2 if len(parts) >= 3 else 1]",
    # {{Fig}}
    "Fig": "f'{small(italic(\"(senso figurato)\"))}'",
    "fig": "f'{small(italic(\"(senso figurato)\"))}'",
    # {{Glossa|raro|it}}
    "Glossa": "small(term(parts[1]))",
    "glossa": "small(term(parts[1]))",
    # {{Lett|non comune|it}}
    "Lett": "small(term('letteralmente'))",
    "lett": "small(term('letteralmente'))",
    # {{Quote|...}}
    "Quote": "'«' + parts[1] + '» ' + term(parts[2])",
    "quote": "'«' + parts[1] + '» ' + term(parts[2])",
    # {{Tabs|aggrondato|aggrondati|aggrondata|aggrondate}}
    "Tabs": "'Masc. sing. ' + parts[1] + ', masc. plur. ' + parts[2] + ', fem. sing. ' + parts[3] + ', fem. plur. ' + parts[4]",  # noqa
    "tabs": "'Masc. sing. ' + parts[1] + ', masc. plur. ' + parts[2] + ', fem. sing. ' + parts[3] + ', fem. plur. ' + parts[4]",  # noqa
    # {{Taxon|Chromis chromis|Chromis chromis}}
    "Taxon": "'la sua classificazione scientifica è ' + strong(italic(parts[1]))",
    "taxon": "'la sua classificazione scientifica è ' + strong(italic(parts[1]))",
    # {{Term|statistica|it}}
    "Term": "small(term(parts[1]))",
    "term": "small(term(parts[1]))",
    # {{Vd|acre#Italiano|acre}}
    "Vd": "'vedi ' + parts[-1]",
    "vd": "'vedi ' + parts[-1]",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/it
release_description = """\
Numero di parole: {words_count}
Export Wiktionary: {dump_date}

File disponibili:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Aggiornato il {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wikizionario (ɔ) {year}"


def find_genders(
    code: str,
    pattern: Pattern[str] = re.compile(r"{{Pn\|?w?}} ''([fm])[singvol ]*''"),
) -> List[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("{{Pn}} ''m sing''")
    ['m']
    """
    return uniq(pattern.findall(code))


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(r"{IPA\|(/[^/]+/)"),
) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{IPA|/kondiˈvidere/}}")
    ['/kondiˈvidere/']
    """
    return uniq(pattern.findall(code))


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["la"], "it")
        'latino'

        >>> last_template_handler(["Pn"], "it", word="Santissimo")
        '<b>Santissimo</b>'

    """
    from ...user_functions import strong
    from ..defaults import last_template_handler as default
    from .langs import langs

    tpl, *parts = template

    if tpl == "Pn":
        return strong(word)

    # This is a country in the current locale
    if lang := langs.get(tpl, ""):
        return lang

    return default(template, locale, word=word)
