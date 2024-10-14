"""Russian language."""

import re

from ...user_functions import flatten, uniq

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
section_level = 1
section_sublevels = (3, 4)
head_sections = "{{-ru-}}"
etyl_section = ("Этимология",)
sections = (
    *etyl_section,
    "Значение",
    "Семантические свойства",
    "{{Значение}}",
    "{{Семантические свойства}}",
    "Морфологические и синтаксические свойства",
    "Как самостоятельный глагол",  # for verbs with aux
    "В значении вспомогательного глагола или связки",  # for verbs with aux
)

# Variants
variant_titles = ("Значение",)
variant_templates = ("{{прич.",)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    #
    # For variants
    #
    "прич.",
)

# Some definitions are not good to keep (plural, gender, ... )
templates_ignored = ("семантика", "unfinished")

# Templates more complex to manage.
templates_multi = {
    # {{зоол.|ru}}
    "зоол.": "italic('зоол.')",
    # {{сленг|ru}}
    "сленг": "italic('сленг')",
    #
    # For variants
    #
    "прич.": "parts[1]",
}


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ru
release_description = """\
Количество слов : {words_count}
Экспорт Викисловаря : {dump_date}

Полные версии :
{download_links_full}

Версии без этимологии :
{download_links_noetym}

<sub>Обновлено по {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Викисловарь (ɔ) {year}"


def find_genders(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"(?:{сущ.ru.)([fmnмжс])|(?:{сущ.ru.*\|)([fmnмжс])"),
) -> list[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("{{сущ ru f ina 5a|основа=страни́ц|слоги={{по-слогам|стра|ни́|ца}}}}")
    ['f']
    """
    # https://ru.wiktionary.org/wiki/%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD:%D1%81%D1%83%D1%89-ru
    return uniq(flatten(pattern.findall(code)))


def find_pronunciations(
    code: str,
    pattern: re.Pattern[str] = re.compile(r"(?:transcriptions-ru.)(\w*)"),
) -> list[str]:
    """
    >>> find_pronunciations("")
    []
    >>> # Expected behaviour after #1376: ['[strɐˈnʲit͡sə]']
    >>> find_pronunciations("{{transcriptions-ru|страни́ца|страни́цы|Ru-страница.ogg}}")
    ['страни']
    """
    return uniq(pattern.findall(code))


def last_template_handler(template: tuple[str, ...], locale: str, word: str = "") -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["en"], "ru")
        'Английский '

        >>> last_template_handler(["выдел", "foo"], "ru")
        'foo'
    """
    from .. import defaults
    from .langs import langs
    from .template_handlers import lookup_template, render_template

    tpl, *parts = template

    if lookup_template(tpl):
        return render_template(word, template)

    if tpl == "выдел":
        return parts[0]

    if lang := langs.get(tpl):
        return lang

    return defaults.last_template_handler(template, locale, word=word)
