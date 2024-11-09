"""Chinses language."""

# Float number separator
import re

from ...user_functions import uniq

float_separator = ","

# Thousads separator
thousands_separator = ","

# Markers for sections that contain interesting text to analyse.
head_sections = ("漢語", "汉语", "{{漢}}")
etyl_section = ()
sections = (
    *etyl_section,
    "動詞",
    "副詞",
    "形容詞",
)

# Variants
variant_titles = sections
variant_templates = ("{{異體}}",)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    #
    # For variants
    #
    "異體",
)

# Templates to ignore: the text will be deleted.
templates_ignored = ("rfdef",)

# Templates more complex to manage.
templates_multi = {
    # {{abbreviation of|zh|留名}}
    "abbreviation of": "f'{parts[2]}之縮寫。'",
    # {{gloss|對患者}}
    "gloss": "f'（{parts[1]}）'",
    # {{misspelling of|zh|稍候}}
    "misspelling of": "f'{parts[2]}的拼寫錯誤。'",
    # {{non-gloss definition|用來表示全範圍}}
    "non-gloss definition": "parts[1]",
    # {{qualifier|前句常有“一方面”……}}
    "qualifier": "parenthesis(parts[1])",
}
templates_multi["gl"] = templates_multi["gloss"]
templates_multi["n-g"] = templates_multi["non-gloss definition"]
templates_multi["qual"] = templates_multi["qualifier"]

# Templates that will be completed/replaced using custom text.
# templates_other = {}


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/zh
release_description = """\
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


# def find_genders(
#     code: str,
#     pattern: re.Pattern[str] = re.compile(r"{g\|(\w+)"),
# ) -> list[str]:
#     """
#     >>> find_genders("")
#     []
#     >>> find_genders("{{g|m}}")
#     ['m']
#     """
#     return uniq(pattern.findall(code))


# {{zh-pron\n|mn=xm,twt,ph:chhit-kóng#-poeh-kóng/twk:chhit-kóng#-peh-kóng\n|w=sh:7chiq kaon paq kaon\n|cat=v\n}}
# def find_pronunciations(
#     code: str,
#     pattern1: re.Pattern[str] = re.compile(r"\{\{PRON\|`([^`]+)`"),
#     pattern2: re.Pattern[str] = re.compile(r"\{\{IFA\|([^}]+)}}"),
# ) -> list[str]:
#     """
#     >>> find_pronunciations("")
#     []
#     >>> find_pronunciations("{{PRON|`luk/o.`}}")
#     ['luk/o']
#     >>> find_pronunciations("{{PRON|`[[advent]]•[[o]]`}}")
#     ['advent•o']
#     >>> find_pronunciations("{{PRON|`{{radi|vultur}} + o`}}")
#     ['vultur + o']
#     >>> find_pronunciations("{{PRON|` {{radi|dekstr}} + {{fina|a}}`}}")
#     ['dekstr + a']
#     >>> find_pronunciations("{{IFA|/vitpunkto/}}")
#     ['/vitpunkto/']
#     """
#     from ...utils import process_templates

#     return [
#         process_templates("", match.rstrip("."), "eo")
#         for match in pattern1.findall(code) or pattern2.findall(code) or []
#     ]


def last_template_handler(template: tuple[str, ...], locale: str, word: str = "") -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["label", "zh", "internet slang"], "zh")
        '(網路用語)'
        >>> last_template_handler(["lb", "zh", "internet slang", "very rare", "&", "Kashkai"], "zh")
        '(網路用語，非常罕用和Qashqai)'
    """
    from ...user_functions import extract_keywords_from, parenthesis
    from .. import defaults
    from .labels import labels
    from .template_handlers import lookup_template, render_template

    tpl, *parts = template
    extract_keywords_from(parts)
    tpl = tpl.lower()

    if lookup_template(tpl):
        return render_template(word, template)

    if tpl in {"lb", "label"}:
        text = ""
        sep = "，"
        for label in parts[1:]:
            if label == "&":
                sep = "和"
            else:
                if text:
                    text += sep
                text += labels.get(label, label)
        return parenthesis(text)

    return defaults.last_template_handler(template, locale, word=word)
