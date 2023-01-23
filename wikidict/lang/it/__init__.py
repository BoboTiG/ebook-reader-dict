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
    "{{nome}",
    "{{pref}",
    "{{Pn}",
    "{{prep}",
    "{{pron poss}",
    "{{suff}",
    "{{sost}",
    "{{verb}",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "Clear",
    "clear",
    "Colori_RAL",
    "Colori_Ral",
    "mid",
    "Nodef",
    "Noetim",
    "Noref",
    "Tabs",
    "Trad1",
    "Trad2",
)

# Templates more complex to manage.
templates_multi: Dict[str, str] = {
    # {{Accr}}
    "Accr": "small(f'({italic(\"accrescitivo\")})')",
    "accr": "small(f'({italic(\"accrescitivo\")})')",
    # {{Anal}}
    "Anal": "small('per analogia')",
    "anal": "small('per analogia')",
    # {{Ant}}
    "Ant": "small(f'({italic(\"per antonomasia\")})')",
    "ant": "small(f'({italic(\"per antonomasia\")})')",
    # {{Botanic|statistica|it}}
    "Botanic": "small(term('botanica'))",
    "botanic": "small(term('botanica'))",
    # {{Coll}}
    "Coll": "small(f'({italic(\"colloquiale\")})')",
    "coll": "small(f'({italic(\"colloquiale\")})')",
    # {{Cum|congiuntivo}}
    "Cum": "small(f'{italic(\"seguito da\")} {strong(parts[1])}')",
    "cum": "small(f'{italic(\"seguito da\")} {strong(parts[1])}')",
    # {{context|ecology|lang=it}}
    "Context": "small(term(parts[1]))",
    "context": "small(term(parts[1]))",
    # {{Dim}}
    "Dim": "small(f'({italic(\"diminutivo\")})')",
    "dim": "small(f'({italic(\"diminutivo\")})')",
    # {{Est}}
    "Est": "small(f'({italic(\"per estensione\")})')",
    "est": "small(f'({italic(\"per estensione\")})')",
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
    # {{Ind pres}}
    "Ind pres": "small(f'{italic(\"ind pres \")}')",
    "ind pres": "small(f'{italic(\"ind pres \")}')",
    # {{inf}}
    "inf": "small(f'{italic(\"inf\")}')",
    # {{IPA|/pi dˈdue/}}
    "IPA": 'f"IPA: {parts[1]}"',
    # {{Lett}}
    "Lett": "small(f'({italic(\"letteralmente\")})')",
    "lett": "small(f'({italic(\"letteralmente\")})')",
    # {{Narr}}
    "Narr": "small(f'({italic(\"narrativa\")})')",
    "narr": "small(f'({italic(\"narrativa\")})')",
    # {{Obs}}
    "Obs": "small(f'({italic(\"obsoleto\")})')",
    "obs": "small(f'({italic(\"obsoleto\")})')",
    # {{P pass}}
    "P pass": "small(f'{italic(\"p.pass.\")}')",
    "p pass": "small(f'{italic(\"p.pass.\")}')",
    # {{P pres}}
    "P pres": "small(f'{italic(\"p.pres.\")}')",
    "p pres": "small(f'{italic(\"p.pres.\")}')",
    # {{Pegg}}
    "Pegg": "small(f'({italic(\"peggiorativo\")})')",
    "pegg": "small(f'({italic(\"peggiorativo\")})')",
    # {{Polytonic|ἐπιστάζω}}
    "Polytonic": "parts[1]",
    # {{Pop}}
    "Pop": "small(f'({italic(\"popolare\")})')",
    "pop": "small(f'({italic(\"popolare\")})')",
    # {{Pers}}
    "Pers": "small(f'({italic(\"riferito solo a persone\")})')",
    "pers": "small(f'({italic(\"riferito solo a persone\")})')",
    # {{Quote|...}}
    "Quote": "'«' + parts[1] + '» ' + term(parts[2])",
    "quote": "'«' + parts[1] + '» ' + term(parts[2])",
    # {{Sndc}}
    "Sndc": "small(f'({italic(\"per sineddoche\")})')",
    "sndc": "small(f'({italic(\"per sineddoche\")})')",
    # {{Soltanto plurali}}
    "Soltanto plurali": "small(f'({italic(\"soltanto plurali\")})')",
    "soltanto plurali": "small(f'({italic(\"soltanto plurali\")})')",
    # {{Spec pl}}
    "Spec pl": "small(f'({italic(\"specialmente al plurale\")})')",
    "spec pl": "small(f'({italic(\"specialmente al plurale\")})')",
    # {{Spreg}}
    "Spreg": "small(f'({italic(\"spregiativo\")})')",
    "spreg": "small(f'({italic(\"spregiativo\")})')",
    # {{Taxon|Chromis chromis|Chromis chromis}}
    "Taxon": "'la sua classificazione scientifica è ' + strong(italic(parts[1]))",
    "taxon": "'la sua classificazione scientifica è ' + strong(italic(parts[1]))",
    # {{Teen}}
    "Teen": "small(f'({italic(\"linguaggio giovanile\")})')",
    "teen": "small(f'({italic(\"linguaggio giovanile\")})')",
    # {{Term|statistica|it}}
    "Term": "small(term(parts[1]))",
    "term": "small(term(parts[1]))",
    # {{Vd|acre#Italiano|acre}}
    "Vd": "'vedi ' + parts[-1]",
    "vd": "'vedi ' + parts[-1]",
    # {{Vezz}}
    "Vezz": "small(f'({italic(\"vezzeggiativo\")})')",
    "vezz": "small(f'({italic(\"vezzeggiativo\")})')",
    # {{Volg}}
    "Volg": "small(f'({italic(\"volgare\")})')",
    "volg": "small(f'({italic(\"volgare\")})')",
    # {{Vulg}}
    "Vulg": "small(f'({italic(\"volgare\")})')",
    "vulg": "small(f'({italic(\"volgare\")})')",
    # {{Yprb}}
    "Yprb": "small(f'({italic(\"per iperbole\")})')",
    "yprb": "small(f'({italic(\"per iperbole\")})')",
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

        >>> last_template_handler(["grc"], "it")
        'greco antico'
        >>> last_template_handler(["la"], "it")
        'latino'

        >>> last_template_handler(["Linkf", "gatta"], "it")
        '(<i>f.:</i> <b>gatta</b>)'
        >>> last_template_handler(["Linkf", "inv"], "it")
        '(<i>invariabile</i>)'
        >>> last_template_handler(["linkf", "invariabile"], "it")
        '(<i>invariabile</i>)'

        >>> last_template_handler(["Linkp", "gatti"], "it")
        '(<i>pl.:</i> <b>gatti</b>)'
        >>> last_template_handler(["Linkp", "inv"], "it")
        '(<i>invariabile</i>)'
        >>> last_template_handler(["linkp", "invariabile"], "it")
        '(<i>invariabile</i>)'

        >>> last_template_handler(["Pn"], "it", word="Santissimo")
        '<b>Santissimo</b>'

    """
    from ...user_functions import italic, parenthesis, strong
    from ..defaults import last_template_handler as default
    from .codelangs import codelangs

    tpl, *parts = template
    tpl = tpl.lower()

    if tpl == "linkf":
        return parenthesis(
            italic("invariabile")
            if parts[0] in ("inv", "invariabile")
            else f"{italic('f.:')} {strong(parts[0])}"
        )

    if tpl == "linkp":
        return parenthesis(
            italic("invariabile")
            if parts[0] in ("inv", "invariabile")
            else f"{italic('pl.:')} {strong(parts[0])}"
        )

    if tpl == "pn":
        return strong(word)

    # This is a country in the current locale
    if codelang := codelangs.get(tpl, ""):
        return codelang

    return default(template, locale, word=word)
