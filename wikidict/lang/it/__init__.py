"""Italian language."""

import re

from ...user_functions import unique

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
    "{{agg form}",
    "{{avv}",
    "{{art}",
    "{{cong}",
    "{{inter}",
    "{{loc nom}",
    "{{nome}",
    "{{pref}",
    "{{Pn}",
    "{{prep}",
    "{{pron poss}",
    "{{suff}",
    "{{sost}",
    "{{sost form}",
    "{{verb}",
    "{{verb form}",
)

# Variants
variant_titles = (
    "{{agg form",
    "{{sost",
    "{{suff",
    "{{verb form",
)
variant_templates = (
    "{{flexion",
    "{{Tabs",
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
    "Riflessivo",
    "Trad1",
    "Trad2",
)

# Templates more complex to manage.
templates_multi: dict[str, str] = {
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
    # {{Comparativo di|buono|it}}
    "Comparativo di": 'f"comparativo di {parts[1]}"',
    "comparativo di": 'f"comparativo di {parts[1]}"',
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
### 🌟 Per poter essere aggiornato regolarmente, questo progetto ha bisogno di sostegno; [cliccare qui](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) per fare una donazione. 🌟

<br/>


Numero di parole: {words_count}
Export Wiktionary: {dump_date}

Versione completa:
{download_links_full}

Versione senza etimologia:
{download_links_noetym}

<sub>Aggiornato il {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wikizionario (ɔ) {year}"


def find_genders(code: str, locale: str) -> list[str]:
    """
    >>> find_genders("", "it")
    []
    >>> find_genders("{{Pn}} ''m sing''", "it")
    ['m']
    """
    pattern = re.compile(r"{{Pn\|?w?}} ''([fm])[singvol ]*''")
    return unique(pattern.findall(code))


def find_pronunciations(code: str, locale: str) -> list[str]:
    """
    >>> find_pronunciations("", "it")
    []
    >>> find_pronunciations("{{IPA|/kondiˈvidere/}}", "it")
    ['/kondiˈvidere/']
    >>> find_pronunciations("{{IPA|/əˈtʃì:vəb<sup>lə</sup>/}}", "it")
    ['/əˈtʃì:vəb<sup>lə</sup>/']
    """
    pattern = re.compile(r"{IPA\|(/(.+)/)}")
    return [prons[0][0]] if (prons := pattern.findall(code)) else []


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

        >>> last_template_handler(["grc"], "it")
        'greco antico'
        >>> last_template_handler(["la"], "it")
        'latino'
        >>> last_template_handler(["pie"], "it")
        'proto-indoeuropeo'

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

        >>> last_template_handler(["Sup2", "assoluto", "f sing", "it"], "it", word="massima")
        'superlativo assoluto, femminile singolare di'
    """
    from ...user_functions import italic, parenthesis, strong
    from .. import defaults
    from .codelangs import codelangs
    from .langs import langs
    from .template_handlers import lookup_template, render_template

    tpl, *parts = template
    tpl = tpl.lower()

    if variant_only:
        tpl = f"__variant__{tpl}"
        template = tuple([tpl, *parts])
    elif locale == "it" and lookup_template(f"__variant__{tpl}"):
        # We are fetching the output of a variant template for the original lang, we do not want to keep it
        return ""

    if lookup_template(template[0]):
        return render_template(word, template)

    if tpl == "fonte":
        match parts[0]:
            case "trec":
                return "AA.VV., <i>Vocabolario Treccani</i> edizione online su <i>treccani.it</i>, Istituto dell'Enciclopedia Italiana"
            case _:
                raise ValueError(f"Unhandled fonte: {parts[0]!r}")

    if tpl == "linkf":
        return parenthesis(
            italic("invariabile") if parts[0] in ("inv", "invariabile") else f"{italic('f.:')} {strong(parts[0])}"
        )

    if tpl == "linkp":
        return parenthesis(
            italic("invariabile") if parts[0] in ("inv", "invariabile") else f"{italic('pl.:')} {strong(parts[0])}"
        )

    if tpl == "pn":
        return strong(word)

    if tpl == "sup2":
        gender = {
            "f sing": "femminile singolare",
            "f pl": "femminile plurale",
            "m sing": "maschile singolare",
            "m pl": "maschile plurale",
        }[parts[1]]
        return f"superlativo {parts[0]}, {gender} di"

    # This is a country in the current locale
    if codelang := codelangs.get(tpl):
        return codelang
    if lang := langs.get(tpl):
        return lang

    return defaults.last_template_handler(template, locale, word=word, all_templates=all_templates)


random_word_url = "https://it.wiktionary.org/wiki/Speciale:RandomRootpage"


def adjust_wikicode(code: str, locale: str) -> str:
    # sourcery skip: inline-immediately-returned-variable
    """
    >>> adjust_wikicode("[[w:A|B]]", "it")
    '[[A|B]]'

    >>> adjust_wikicode("[[en:foo]]", "it")
    ''

    >>> adjust_wikicode("{{-verb form-}}", "it")
    '=== {{verb form}} ==='

    >>> adjust_wikicode("{{-avv-|it}}", "it")
    '=== {{avv}} ==='

    >>> adjust_wikicode("{{-avv-|ANY}}", "it")
    '=== {{avv|ANY}} ==='

    >>> adjust_wikicode("{{-avv-}}", "it")
    '=== {{avv}} ==='

    >>> adjust_wikicode("# plurale di [[-ectomia]]", "it")
    '# {{flexion|-ectomia}}'
    >>> adjust_wikicode("# plurale di [[-ectomia]]", "fr")
    '# plurale di [[-ectomia]]{{flexion|-ectomia}}'

    >>> adjust_wikicode("#participio presente di [[amare]]", "it")
    '# {{flexion|amare}}'
    >>> adjust_wikicode("#participio passato di [[amare]]", "it")
    '# {{flexion|amare}}'
    >>> adjust_wikicode("# participio presente di [[amare]]", "it")
    '# {{flexion|amare}}'
    >>> adjust_wikicode("#2ª pers. singolare indicativo presente del verbo [[amare]]", "it")
    '# {{flexion|amare}}'
    >>> adjust_wikicode("# {{3}} singolare imperativo presente del verbo [[amare]]", "it")
    '# {{flexion|amare}}'
    >>> adjust_wikicode("# {{1}}, 2ª pers. e {{3}} singolare congiuntivo presente del verbo [[amare]]", "it")
    '# {{flexion|amare}}'
    """
    # [[w:A|B]] → [[A|B]]
    code = code.replace("[[w:", "[[")

    # [[en:foo]] → ''
    code = re.sub(r"(\[\[\w+:\w+\]\])", "", code)

    # {{-verb form-}} → === {{verb form}} ===
    code = re.sub(r"^\{\{-(.+)-\}\}", r"=== {{\1}} ===", code, flags=re.MULTILINE)

    # {{-avv-|it}} → === {{avv}} ===
    code = re.sub(rf"^\{{\{{-(.+)-\|{locale}\}}\}}", r"=== {{\1}} ===", code, flags=re.MULTILINE)

    # {{-avv-|ANY}} → === {{avv|ANY}} ===
    code = re.sub(r"^\{\{-(.+)-\|(\w+)\}\}", r"=== {{\1|\2}} ===", code, flags=re.MULTILINE)

    # {{-avv-}} → === {{avv}} ===
    code = re.sub(r"^\{\{-(\w+)-\}\}", r"=== {{\1}} ===", code, flags=re.MULTILINE)

    #
    # Variants
    #

    # `# plurale di [[-ectomia]]` → `{{flexion|-ectomia}}`
    # `# terza persona plurale del congiuntivo presente di [[brillantare]]` → `{{flexion|brillantare}}`
    code = re.sub(
        r"^#\s*(.+(?:femminile|singolare|plurale).+\[\[([^\]]+)\]\])",
        r"# {{flexion|\2}}" if locale == "it" else r"#\1{{flexion|\2}}",
        code,
        flags=re.MULTILINE,
    )

    # `# participio presente di [[amare]] → `{{flexion|amare}}`
    # `# participio passato di [[amare]] → `{{flexion|amare}}`
    code = re.sub(
        r"^#\s*(participio (?:passato|presente) di \[\[([^\]]+)\]\])",
        r"# {{flexion|\2}}" if locale == "it" else r"# \1{{flexion|\2}}",
        code,
        flags=re.MULTILINE,
    )

    return code
