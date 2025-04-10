"""Esperanto language."""

# Float number separator
import re

from ...user_functions import unique

float_separator = ","

# Thousands separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
section_patterns = ("#", r":\[\d+\]", r"\*")
section_sublevels = (3, 4)
head_sections = ("{{lingvo|eo}}", "{{lingvo|mul}}", "esperanto", "multldingva", "translingva")
etyl_section = ("{{deveno}}", "{{etimologio}}")
sections = (
    *etyl_section,
    "adjektivo",
    "adverbo",
    "difinoj",
    "infikso",
    "interjekcio",
    "konjunkcio",
    "malllongigo",
    "mallongigoj",
    "numeralo",
    "prefikso",
    "prepozicio",
    "pronomo",
    "radiko",
    "signifo",
    "signo",
    "subjunkcio",
    "substantivo",
    "sufikso",
    "verba formo",
    "verbo",
    "{{signifoj}",
    "{{vortospeco|adjektiva formo|eo}",
    "{{vortospeco|adjektivo|eo}",
    "{{vortospeco|adverbo|eo}",
    "{{vortospeco|antaŭfiksaĵo|eo}",
    "{{vortospeco|artikolo|eo}",
    "{{vortospeco|demanda adverbo|eo}",
    "{{vortospeco|esprimo|eo}",
    "{{vortospeco|finaĵo|eo}",
    "{{vortospeco|frazo|eo}",
    "{{vortospeco|interjekcio|eo}",
    "{{vortospeco|konjunkcio|eo}",
    "{{vortospeco|liternomo|eo}",
    "{{vortospeco|litero|eo}",
    "{{vortospeco|literoparo|eo}",
    "{{vortospeco|loknomo|eo}",
    "{{vortospeco|mallongigo|eo}",
    "{{vortospeco|mallongigo|mul}",
    "{{vortospeco|mona nomo|eo}",
    "{{vortospeco|nombro|eo}",
    "{{vortospeco|nomo|eo}",
    "{{vortospeco|numeralo|eo}",
    "{{vortospeco|partikulo|eo}",
    "{{vortospeco|persona nomo|eo}",
    "{{vortospeco|persona pronomo|eo}",
    "{{vortospeco|poseda pronomo|eo}",
    "{{vortospeco|postfiksaĵo|eo}",
    "{{vortospeco|prepozicio|eo}",
    "{{vortospeco|pronomo|eo}",
    "{{vortospeco|scienca nomo|mul}",
    "{{vortospeco|signo|mul}",
    "{{vortospeco|simbolo|eo}",
    "{{vortospeco|simbolo|mul}",
    "{{vortospeco|subjunkcio|eo}",
    "{{vortospeco|substantiva formo|eo}",
    "{{vortospeco|substantivo|eo}",
    "{{vortospeco|substantivo|mul}",
    "{{vortospeco|sufikso|eo}",
    "{{vortospeco|verbo ambaŭtransitiva|eo}",
    "{{vortospeco|verba formo|eo}",
    "{{vortospeco|verbo|eo}",
    "{{vortospeco|verbo netransitiva|eo}",
    "{{vortospeco|verbo transitiva|eo}",
    "{{vortospeco|vortgrupo|eo}",
)

# Variants
variant_titles = sections
variant_templates = ("{{form-eo}}",)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (*[variant.lstrip("{") for variant in variant_templates],)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "?",
    "aŭdo",
    "barileto",
    "fundamenta",
    "IFA",
    "N",
    "PRON",
    "quote-book",
    "quote-magazine",
    "ref-AdE",
    "ref-Grabowski",
    "ref-Kalman",
    "ref-PrV",
    "ref-ReVo",
    "radiofoniaj liternomoj",
    "rima",
    "vian",
    "Vd",
    "Vidu ankaŭ",
    "W",
    "X",
)

# Templates more complex to manage.
templates_multi = {
    # {{fina|o}}
    "fina": "parts[1]",
    # {{lite|ŭ}}
    "lite": "parts[1]",
    # {{inte|o}}
    "inte": "parts[1]",
    # {{mems|du}}
    "mems": "parts[1]",
    # {{pref|mis}}
    "pref": "parts[1]",
    # {{radi|vort}}
    "radi": "parts[1]",
    # {{sufi|il}}
    "sufi": "parts[1]",
    # {{Vortospeco|mona nomo|eo}}
    "Vortospeco": "capitalize(parts[1])",
}

# Templates that will be completed/replaced using custom text.
templates_other = {
    "🏠": "🏠 <i>arkitekturo</i>",
    "🌄": "<i>geografio</i>",
    "🍴": "gastronomia",
    "📖": "📖 <i>(presarto kaj libroj)</i>",
    "📷": "📷 <i>fotografio kaj kinotekniko</i>",
    "⏚": "⏚ <i>elektro kaj elektroteĥniko</i>",
    "✞": "✞ <i>kristanismo</i>",
    "❤": "❤ <i>korpostrukturo kaj histologio:</i>",
    "☆": "☆ <i>belartoj<i>",
    "♉": "♉ <i>bestologio</i>",
    "👥": "👥 <i>komunuza senso</i>",
    "🍁": "🍁 <i>herbiko</i>",
    "✈": "✈ <i>aviado</i>",
    "♠": "♠ <i>ludoj</i>",
    "☼": "☼ <i>terscieco (inkl. mineral- kaj rokoscienco)</i>",
    "⚓": "⚓ <i>marnavigado kaj ŝipoj</i>",
    "⚕": "(⚕ <i>kuracscienco kaj kirurgio</i>)",
    "♜": "♜ <i>historio</i>",
    "Λ": "Λ <i>lingv.</i>",
    "⊕": "⊕ <i>terologio (inkl. mineralogio kaj petrologio):</i>",
    "♧": "♧ <i>beletro</i>",
    "Ⓣ": "Ⓣ <i>(teknikoj [inkl. mekanikon kaj metalurgion])</i>",
    "☇": "☇ <i>forkomunikoj (inkl. radioforsonadon, videaĵojn kaj elektrosonsciencon</i>)",
    "Π": "Π <i>prahistorio</i>",
    "Θ": "(<i>Θ religioj</i>)",
    "𝅘𝅥𝅰": "𝅘𝅥𝅰 <i>muziko</i>",
    "⚔": (
        '<img style="height:100%;max-height:0.8em;width:auto;vertical-align:bottom"'
        ' src="data:image/gif;base64,R0lGODlhHgAYAPcAAAAAAAEBAQICAgMDAwQEBAUFBQYGBg'
        "cHBwgICAkJCQoKCgsLCwwMDA0NDQ4ODg8PDxAQEBERERISEhMTExQUFBUVFRYWFhcXFxgYGBkZ"
        "GRoaGhsbGxwcHB0dHR4eHh8fHyAgICEhISIiIiMjIyQkJCUlJSYmJicnJygoKCkpKSoqKisrKy"
        "wsLC0tLS4uLi8vLzAwMDExMTIyMjMzMzQ0NDU1NTY2Njc3Nzg4ODk5OTo6Ojs7Ozw8PD09PT4+"
        "Pj8/P0BAQEFBQUJCQkNDQ0REREVFRUZGRkdHR0hISElJSUpKSktLS0xMTE1NTU5OTk9PT1BQUF"
        "FRUVJSUlNTU1RUVFVVVVZWVldXV1hYWFlZWVpaWltbW1xcXF1dXV5eXl9fX2BgYGFhYWJiYmNj"
        "Y2RkZGVlZWZmZmdnZ2hoaGlpaWpqamtra2xsbG1tbW5ubm9vb3BwcHFxcXJycnNzc3R0dHV1dX"
        "Z2dnd3d3h4eHl5eXp6ent7e3x8fH19fX5+fn9/f4CAgIGBgYKCgoODg4SEhIWFhYaGhoeHh4iI"
        "iImJiYqKiouLi4yMjI2NjY6Ojo+Pj5CQkJGRkZKSkpOTk5SUlJWVlZaWlpeXl5iYmJmZmZqamp"
        "ubm5ycnJ2dnZ6enp+fn6CgoKGhoaKioqOjo6SkpKWlpaampqenp6ioqKmpqaqqqqurq6ysrK2t"
        "ra6urq+vr7CwsLGxsbKysrOzs7S0tLW1tba2tre3t7i4uLm5ubq6uru7u7y8vL29vb6+vr+/v8"
        "DAwMHBwcLCwsPDw8TExMXFxcbGxsfHx8jIyMnJycrKysvLy8zMzM3Nzc7Ozs/Pz9DQ0NHR0dLS"
        "0tPT09TU1NXV1dbW1tfX19jY2NnZ2dra2tvb29zc3N3d3d7e3t/f3+Dg4OHh4eLi4uPj4+Tk5O"
        "Xl5ebm5ufn5+jo6Onp6erq6uvr6+zs7O3t7e7u7u/v7/Dw8PHx8fLy8vPz8/T09PX19fb29vf3"
        "9/j4+Pn5+fr6+vv7+/z8/P39/f7+/v///yH5BAEAAP8ALAAAAAAeABgAAAiQAP8JHEiwoMGDCB"
        "MqXMgQISN4DRuGQwMtIsNeaNJZXMhI00aF6dAc+5jwWMaP8Hr1MnjK48dwpwIE4MOoJiM0Kz/K"
        "ksmzZwCIH9H49CkrXLhjvSouhDe0KU+cCHsxauK0qsxwB61qDYDVoNCtTflEBTtULEKmTTVRDb"
        'sQ2leejP6F9NnkFMm7ePPq3ct3YUAAADs="/> <i>militaferoj</i>'
    ),
    "AGRHOR": "<i>terkulturo</i>",
    "EKON": "<i>ekon.</i>",
    "HOR": "<i>hortikulturo, arbokulturo, arbarkultivo</i>",
    "KRI": "<i>krist.</i>",
    "TRA": "<i>trafiko</i>",
    "figurs.": "<i>figursenca</i>",
    "hist.": "♜ <i>hist.</i>",
    "ĵar.": "<i>ĵar.</i>",
    "lat. tardío": "malfrua latina",
    "lat. vulg.": "vulgara latina",
    "ling.": "Λ <i>lingv.</i>",
    "mar.": "⚓ <i>maraferoj</i>",
    "poe.": (
        '<img style="height:100%;max-height:0.8em;width:auto;vertical-align:bottom"'
        ' src="data:image/gif;base64,R0lGODlhFwAaAPcAAAAAAAEBAQICAgMDAwQEBAUFBQYGB'
        "gcHBwgICAkJCQoKCgsLCwwMDA0NDQ4ODg8PDxAQEBERERISEhMTExQUFBUVFRYWFhcXFxgYGB"
        "kZGRoaGhsbGxwcHB0dHR4eHh8fHyAgICEhISIiIiMjIyQkJCUlJSYmJicnJygoKCkpKSoqKis"
        "rKywsLC0tLS4uLi8vLzAwMDExMTIyMjMzMzQ0NDU1NTY2Njc3Nzg4ODk5OTo6Ojs7Ozw8PD09"
        "PT4+Pj8/P0BAQEFBQUJCQkNDQ0REREVFRUZGRkdHR0hISElJSUpKSktLS0xMTE1NTU5OTk9PT"
        "1BQUFFRUVJSUlNTU1RUVFVVVVZWVldXV1hYWFlZWVpaWltbW1xcXF1dXV5eXl9fX2BgYGFhYW"
        "JiYmNjY2RkZGVlZWZmZmdnZ2hoaGlpaWpqamtra2xsbG1tbW5ubm9vb3BwcHFxcXJycnNzc3R"
        "0dHV1dXZ2dnd3d3h4eHl5eXp6ent7e3x8fH19fX5+fn9/f4CAgIGBgYKCgoODg4SEhIWFhYaG"
        "hoeHh4iIiImJiYqKiouLi4yMjI2NjY6Ojo+Pj5CQkJGRkZKSkpOTk5SUlJWVlZaWlpeXl5iYm"
        "JmZmZqampubm5ycnJ2dnZ6enp+fn6CgoKGhoaKioqOjo6SkpKWlpaampqenp6ioqKmpqaqqqq"
        "urq6ysrK2tra6urq+vr7CwsLGxsbKysrOzs7S0tLW1tba2tre3t7i4uLm5ubq6uru7u7y8vL2"
        "9vb6+vr+/v8DAwMHBwcLCwsPDw8TExMXFxcbGxsfHx8jIyMnJycrKysvLy8zMzM3Nzc7Ozs/P"
        "z9DQ0NHR0dLS0tPT09TU1NXV1dbW1tfX19jY2NnZ2dra2tvb29zc3N3d3d7e3t/f3+Dg4OHh4"
        "eLi4uPj4+Tk5OXl5ebm5ufn5+jo6Onp6erq6uvr6+zs7O3t7e7u7u/v7/Dw8PHx8fLy8vPz8/"
        "T09PX19fb29vf39/j4+Pn5+fr6+vv7+/z8/P39/f7+/v///yH5BAEAAP8ALAAAAAAXABoAAAj"
        "NAP8JHEiwoMGDCBMqXIiwFqiB1RapEwjuYUJlAADYmAgCwIqJNgAsmXgQTEYAa4CdXALupA2E"
        "S04CUHmSZkaLBatZyGjhX0gAFtStOAkIIaCMyv61tFBNIEYAixoCKPpP5RKCGZsePApOICioW"
        "FckNDmwDoCuXgHgNLgCxMC2BG24TQhgrjoAYAZiXMsWgMBaAGoNBDE3oVlg/8ySPCpYYTWwIB"
        'Y4BcrwH+GjANTpxFsZiMyhGdEuNCkTqKrKAoGpXk0StevXsGPLnj0wIAA7"/> <i>poetiko, poezio</i>'
    ),
}
templates_other["Ĵar."] = templates_other["ĵar."]
templates_other["Ling."] = templates_other["ling."]
templates_other["Mar."] = templates_other["mar."]
templates_other["MUZ"] = templates_other["𝅘𝅥𝅰"]
templates_other["Poe."] = templates_other["poe."]


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/eo
release_description = """\
### 🌟 Por esti regule ĝisdatigita, ĉi tiu projekto bezonas subtenon; [Alklaku ĉi tie](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) por donaci. 🌟

<br/>


Vortoj kalkulas: {words_count}
Vikivortaro rubejo: {dump_date}

Plena versio:
{download_links_full}

Etimologio-libera versio:
{download_links_noetym}

<sub>Ĝisdatigita je {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Vikivortaro (ɔ) {year}"


def find_genders(code: str, locale: str) -> list[str]:
    """
    >>> find_genders("", "eo")
    []
    >>> find_genders("{{g|m}}", "eo")
    ['m']
    """
    pattern = re.compile(r"{g\|(\w+)")
    return unique(pattern.findall(code))


def find_pronunciations(code: str, locale: str) -> list[str]:
    """
    >>> find_pronunciations("", "eo")
    []
    >>> find_pronunciations("{{PRON|`luk/o.`}}", "eo")
    ['luk/o']
    >>> find_pronunciations("{{PRON|`[[advent]]•[[o]]`}}", "eo")
    ['advent•o']
    >>> find_pronunciations("{{PRON|`{{radi|vultur}} + o`}}", "eo")
    ['vultur + o']
    >>> find_pronunciations("{{PRON|` {{radi|dekstr}} + {{fina|a}}`}}", "eo")
    ['dekstr + a']
    >>> find_pronunciations("{{IFA|/vitpunkto/}}", "eo")
    ['/vitpunkto/']
    """
    from ...utils import process_templates

    pattern1 = re.compile(r"\{\{PRON\|`([^`]+)`")
    pattern2 = re.compile(r"\{\{IFA\|([^}]+)}}")
    return [
        process_templates("", match.rstrip("."), "eo")
        for match in pattern1.findall(code) or pattern2.findall(code) or []
    ]


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    all_templates: list[tuple[str, str, str]] | None = None,
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["form-eo"], "eo", word="surdaj")
        'surda'
    """
    from .. import defaults
    from .template_handlers import lookup_template, render_template

    if lookup_template(template[0]):
        return render_template(word, template)

    return defaults.last_template_handler(template, locale, word=word, all_templates=all_templates)


random_word_url = "https://eo.wiktionary.org/wiki/Speciala%C4%B5o:RandomRootpage"


def adjust_wikicode(code: str, locale: str) -> str:
    # sourcery skip: inline-immediately-returned-variable
    """
    >>> adjust_wikicode("{{Deklinacio-eo}}", "eo")
    ''

    >>> adjust_wikicode("{{form-eo}}", "eo")
    '# {{form-eo}}'

    >>> adjust_wikicode("{{xxx}}", "eo")
    '==== {{xxx}} ===='
    >>> adjust_wikicode("{{xx-x}}", "eo")
    '==== {{xx-x}} ===='
    >>> adjust_wikicode("===={{Tradukoj}}====", "eo")
    '== {{Tradukoj}} =='

    >>> adjust_wikicode("{{Vorterseparo}}:{{radi|tret}} + {{fina|i}}", "eo")
    '\\n{{PRON|`{{radi|tret}} + {{fina|i}}`}}\\n'
    >>> adjust_wikicode("{{Vorterseparo}}\\n:{{radi|tret}} + {{fina|i}}", "eo")
    '\\n{{PRON|`{{radi|tret}} + {{fina|i}}`}}\\n'
    """
    # Wipe out {{Deklinacio-eo}}
    code = code.replace(f"{{{{Deklinacio-{locale}}}}}", "")

    # Variants
    # {{form-eo}} → # {{form-eo}}
    code = code.replace(f"{{{{form-{locale}}}}}", f"# {{{{form-{locale}}}}}")

    # {{xxx}} → ==== {{xxx}} ====
    # {{xx-x}} → ==== {{xx-x}} ====
    code = re.sub(r"^(\{\{[\w\-]+\}\})", r"==== \1 ====", code, flags=re.MULTILINE)

    # ===={{Tradukoj}}==== → == {{Tradukoj}} ==
    code = re.sub(
        r"====\s*(\{\{(?:Ekzemploj|Derivaĵoj|Referencoj|Sinonimoj|Tradukoj|Vortfaradoj|trad-\w+)\}\})\s*====",
        r"== \1 ==",
        code,
        flags=re.MULTILINE,
    )

    # Easier pronunciation
    code = re.sub(r"==== {{Vorterseparo}} ====\s*:(.+)\s*", r"\n{{PRON|`\1`}}\n", code, flags=re.MULTILINE)

    return code
