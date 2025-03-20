"""Romanian language."""

import re

from ...user_functions import flatten, unique

# Float number separator
float_separator = ","

# Thousands separator
thousands_separator = "."

# Markers for sections that contain interesting text to analyse.
head_sections = ("{{limba|ron}}", "{{limba|ro}}", "{{limba|conv}}")
section_sublevels = (3,)
etyl_section = ("{{etimologie}}",)
sections = (
    "{{abr}}",
    "{{abreviere}",
    "{{adjectiv}",
    "{{adjective}",
    "{{adverb}",
    "{{articol}",
    "{{conjuncție}",
    "{{cuvânt compus}",
    *etyl_section,
    "{{expr}}",
    "{{expresie}",
    "{{expresie|ro",
    "{{interjecție}",
    "{{locuțiune adjectivală}",
    "{{locuțiune adverbială}",
    "{{locuțiune}",
    "{{numeral colectiv}",
    "{{numeral}",
    "{{nume propriu}",
    "{{nume propriu|ro",
    "{{nume taxonomic|conv}",
    "{{participiu}",
    "{{prefix}",
    "{{prepoziție}",
    "{{pronume}",
    "{{pronume|ro",
    "{{substantiv}",
    "{{sufix}",
    "{{simbol|conv}",
    "{{unități}}",
    "{{verb auxiliar}",
    "{{verb copulativ}",
    "{{verb predicativ}",
    "{{verb tranzitiv}",
    "{{verb}",
)

# Variantes
variant_titles = tuple(section for section in sections if section not in etyl_section)
variant_templates = (
    "{{adj form of",
    "{{forma de",
)

# All forms of a words (for variants)
forma_de = (
    "forma de acuzativ feminin la plural pentru",
    "forma de articulat singular pentru",
    "forma de dativ feminin la plural pentru",
    "forma de dativ feminin la singular pentru",
    "forma de dativ-genitiv și de vocativ plural articulat pentru",
    "forma de enitiv-dativ singular articulat pentru",
    "forma de feminin neutru și plural pentru",
    "forma de feminin pentru",
    "forma de feminin plural pentru",
    "forma de feminin singular articulat pentru",
    "forma de feminin singular nearticulat în nominativ-acuzativ pentru",
    "forma de feminin singular nehotărât pentru",
    "forma de feminin singular pentru",
    "forma de feminin și neutru plural pentru",
    "forma de genitiv dativ singular pentru",
    "forma de genitiv singular articulat pentru",
    "forma de genitiv-dativ plural articulat pentru",
    "forma de genitiv-dativ singular articulat pentru",
    "forma de genitiv-dativ și vocativ plural articulat pentru",
    "forma de gerunziu pentru",
    "forma de maculin plural pentr",
    "forma de maculin plural pentru",
    "forma de mascuklin plural pentru",
    "forma de masculin feminin singular pentru",
    "forma de masculin plural pentru",
    "forma de masculin plural singular pentru",
    "forma de masculin pluralpentru",
    "forma de masculin plurl pentru",
    "forma de masculin și feminin plural genitiv-dativ pentru",
    "forma de masculin, neutru și feminin plural pentru",
    "forma de neutru plural pentru",
    "forma de nominativ-acuzativ plural articulat pentru",
    "forma de nominativ-acuzativ plural pentru",
    "forma de participiu pentru",
    "forma de participiu trecut pentru",
    "forma de persoana a I-a plural la conjunctiv prezent pentru",
    "forma de persoana a I-a plural la imperfect pentru",
    "forma de persoana a I-a plural la mai mult ca perfect pentru",
    "forma de persoana a I-a plural la perfect simplu pentru",
    "forma de persoana a I-a plural la prezent pentru",
    "forma de persoana a I-a singular la conjunctiv prezent pentru",
    "forma de persoana a I-a singular la imperfect pentru",
    "forma de persoana a I-a singular la mai mult ca perfect pentru",
    "forma de persoana a I-a singular la perfect simplu pentru",
    "forma de persoana a I-a singular la prezent pentru",
    "forma de persoana a II-a plural la conjunctiv prezent pentru",
    "forma de persoana a II-a plural la imperativ entru",
    "forma de persoana a II-a plural la imperativ pentru",
    "forma de persoana a II-a plural la imperfect pentru",
    "forma de persoana a II-a plural la mai mult ca perfect pentru",
    "forma de persoana a II-a plural la perfect simplu pentru",
    "forma de persoana a II-a plural la prezent pentru",
    "forma de persoana a II-a singular la conjunctiv prezent pentru",
    "forma de persoana a II-a singular la imperativ pentru",
    "forma de persoana a II-a singular la imperfect pentru",
    "forma de persoana a II-a singular la indicativ prezent pentru",
    "forma de persoana a II-a singular la mai mult ca perfect pentru",
    "forma de persoana a II-a singular la perfect simplu pentru",
    "forma de persoana a II-a singular la prezent indicativ pentru",
    "forma de persoana a II-a singular la prezent pentru",
    "forma de persoana a II-a singular la subjonctiv prezent pentru",
    "forma de persoana a III-a plural la conjunctiv prezent pentru",
    "forma de persoana a III-a plural la imperfect pentru",
    "forma de persoana a III-a plural la mai mult ca perfect pentru",
    "forma de persoana a III-a plural la perfect simplu pentru",
    "forma de persoana a III-a plural la prezent indicativ pentru",
    "forma de persoana a III-a plural la prezent pentru",
    "forma de persoana a III-a plural la timpul condițional-optativ pentru",
    "forma de persoana a III-a singular la conjunctiv prezent pentru",
    "forma de persoana a III-a singular la imperfect indicativ pentru",
    "forma de persoana a III-a singular la imperfect pentru",
    "forma de persoana a III-a singular la mai mult ca perfect pentru",
    "forma de persoana a III-a singular la perfect simplu pentru",
    "forma de persoana a III-a singular la perfect simplu pentru",
    "forma de persoana a III-a singular la prezent indicativ pentru",
    "forma de persoana a III-a singular la prezent pentru",
    "forma de persoana a III-a singular la timpul condițional-optativ pentru",
    "forma de plural articulat pentru",
    "forma de plural la feminin și neutru pentru",
    "forma de plural masculin pentru",
    "forma de plural nearticulat în nominativ-acuzativ și genitiv-dativ pentru",
    "forma de plural nearticulat pentru",
    "forma de plural neatriculat pentru",
    "forma de plural pentru",
    "forma de singulaar articulat pentru",
    "forma de singular articulat",
    "forma de singular articulat pentru",
    "forma de singular articulată pentru",
    "forma de singular nearticulat în genitiv-dativ pentru",
    "forma de singular nearticulat pentru",
    "forma de singular vocativ pentru",
    "forma de singular și plural genitiv nearticulat pentru",
    "forma de singulat articulat pentru",
    "forma de vocativ plural articulat pentru",
    "forma de vocativ plural pentru",
    "forma de vocativ singular articulat pentru",
    "forma de vocativ singular pentru",
)

# Templates to ignore: the text will be deleted.
definitions_to_ignore = ("adj form of", *forma_de)

# Templates more complex to manage.
templates_multi = {
    # {{adj form of|ro|frumos||m|p}}
    "adj form of": "parts[2]",
    # {{format de ...|word}}
    **{fd: "parts[-1]" for fd in forma_de},
    # {{n}}
    "n": "italic('n.')",
    # {{p}}
    "p": "italic('pl.')",
    # {{trad|el|παρα}}
    "trad": "parts[-1]",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ro
release_description = """\
### 🌟 Pentru a fi actualizat periodic, acest proiect are nevoie de sprijin; [faceți clic aici](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) pentru a dona. 🌟

<br/>


Număr de cuvinte: {words_count}
Extragerea datelor din Wikționar: {dump_date}

Versiunea completă:
{download_links_full}

Versiune fără etimologie:
{download_links_noetym}

<sub>Ultima actualizare în {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wikționar (ɔ) {year}"


def find_genders(
    code: str,
    *,
    pattern: re.Pattern[str] = re.compile(r"gen={{([fmsingp]+)(?: \?\|)*}"),
) -> list[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("{{substantiv-ron|gen={{m}}|nom-sg=câine|nom-pl=câini")
    ['m']
    >>> find_genders("{{substantiv-ron|gen={{n}}}}")
    ['n']
    """
    return unique(flatten(pattern.findall(code)))


def find_pronunciations(code: str) -> list[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{AFI|/ka.priˈmulg/}}")
    ['/ka.priˈmulg/']
    >>> find_pronunciations("{{IPA|ro|[fruˈmoʃʲ]}}")
    ['[fruˈmoʃʲ]']
    """
    res = []
    for pattern in (
        re.compile(r"{AFI\|(/[^/]+/)(?:\|(/[^/]+/))*"),
        re.compile(r"{IPA\|ro\|([^}]+)"),
    ):
        res.extend(pattern.findall(code))

    return unique(flatten(res))


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    missed_templates: list[tuple[str, str]] | None = None,
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> from random import choice
        >>> last_template_handler([choice(forma_de), "foo"], "ro")
        'foo'

    """
    tpl, *parts = template

    if tpl.startswith("forma de"):
        # Lets error in case of unhandled "forma de" template, it will be easier to support new forms then
        assert tpl in forma_de, tpl
        return parts[-1]

    # Given the tiny number of used templates, it's easier to raise an error instead of relying on the default handler
    raise ValueError(f"Unhandled {template=} {word=}")
