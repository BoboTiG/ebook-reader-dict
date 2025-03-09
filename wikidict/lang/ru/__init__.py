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
etyl_section = ("этимология",)
sections = (
    *etyl_section,
    "значение",
    "{{значение}}",
    "семантические свойства",
    "{{семантические свойства}}",
    "морфологические и синтаксические свойства",
    "как самостоятельный глагол",  # for verbs with aux
    "в значении вспомогательного глагола или связки",  # for verbs with aux
)

# Variants
variant_titles = ("значение",)
variant_templates = ("{{прич.",)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    #
    # Variants
    #
    "прич.",
)

# Some definitions are not good to keep (plural, gender, ... )
templates_ignored = ("??", "gb", "etym-lang", "L", "Lacuna", "l", "lacuna", "unfinished", "семантика", "пример")

# Templates more complex to manage.
templates_multi = {
    # {{"|Сработать по Шеремету}}
    '"': 'f"„{parts[1]}“"',
    # {{===|Атлант}}
    "===": 'f"то же, что {parts[1]}"',
    # {{wikiref|совершенный вид}}
    "wikiref": "parts[-1]",
    # {{кс|Унбегаун, с. 44}}
    "кс": 'f"[{parts[1]}]"',
    # {{t:=|поисковая оптимизация}} →  {{_t_|поисковая оптимизация}} (converted in `render.adjust_wikicode()`)
    "_t_": 'f"то же, что {parts[1]}"',
    "страд.": "italic('страд.') + ' к' + ((' ' + parts[1]) if len(parts) > 1 else '')",
    # {{марр|значение слова или выражения}}
    "марр": 'f"‘{parts[1]}’"',
    # {{этим-2|{{lang|en|AI|ИИ}}|{{lang|en|artificial intelligence|искусственный интеллект}}|[[тренер]]|{{lang|en|trainer|тренер}}}}
    "этим-2": 'f"{parts[1]} + {parts[3]}"',
}

# Templates that will be completed/replaced using custom text.
templates_other = {
    "?": "<small>?</small>",
    "-": "—",
    "--": "—",
    "Ф": "<small>Использованы данные словаря М. Фасмера</small>",
    "Нужен перевод": "<b>Значение этого слова или выражения пока не указано.</b> Вы можете предложить свой вариант.",
    "советск.": "<i>советск.</i>",
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
    *,
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
    *,
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


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    missed_templates: list[tuple[str, str]] | None = None,
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["en"], "ru")
        'Английский'

        >>> last_template_handler(["выдел", "foo"], "ru")
        'foo'

        >>> last_template_handler(["аббр.", "ru"], "ru")
        '<i>сокр.</i>'
        >>> last_template_handler(["аббр.", "ru", "Свободная демократическая партия", "без ссылки=1"], "ru")
        '<i>сокр.</i> от <i>Свободная демократическая партия</i>'
        >>> last_template_handler(["аббр.", "ru", "Свободная демократическая партия", "без ссылки=1", ""], "ru")
        '<i>сокр.</i> от <i>Свободная демократическая партия</i>'

        >>> last_template_handler(["рег."], "ru")
        '<i>рег.</i>'
        >>> last_template_handler(["рег.", "Латвия"], "ru")
        '<i>рег. (Латвия)</i>'

        >>> last_template_handler(["свойство", "абелев"], "ru")
        'свойство по значению прилагательного <i>абелев</i>'
        >>> last_template_handler(["свойство", "погнутый", "состояние=1"], "ru")
        'свойство или состояние по значению прилагательного <i>погнутый</i>'

        >>> last_template_handler(["нареч.", "адекватный"], "ru")
        'наречие к <i>адекватный</i>'
        >>> last_template_handler(["наречие", "адекватный", "в соответствии с чем-либо"], "ru")
        'наречие к <i>адекватный</i>; в соответствии с чем-либо'

        # Labels
        >>> last_template_handler(["зоол.", "ru"], "ru")
        '<i>зоол.</i>'
        >>> last_template_handler(["сленг", "ru"], "ru")
        '<i>сленг</i>'
        >>> last_template_handler(["гипокор.", "ru", "Александр"], "ru")
        '<i>гипокор.</i> к Александр'
        >>> last_template_handler(["эррат.", "ru", "Александр"], "ru")
        '<i>эррат.</i> от Александр'
        >>> last_template_handler(["умласк."], "ru")
        '<i>уменьш.-ласк.</i>'

        >>> last_template_handler(["Унбегаун"], "ru")
        '<i>Унбегаун Б.-О.</i> Русские фамилии. — М. : Прогресс, 1989. — 443 с. — ISBN 5-01-001045-3.'
        >>> last_template_handler(["Унбегаун", "сокр=1"], "ru")
        'Унбегаун'

        #
        # Variants
        #
        >>> last_template_handler(["прич.", "зыбить"], "ru")
        'зыбить'
        >>> last_template_handler(["прич.", "не=1", "зыбить", "наст", "страд"], "ru")
        'зыбить'
    """
    from ...user_functions import extract_keywords_from, italic
    from .. import defaults
    from .labels import labels
    from .langs import langs
    from .template_handlers import lookup_template, render_template

    tpl, *parts = template
    data = extract_keywords_from(parts)

    #
    # Variants
    #
    if tpl == "прич.":
        if (variant := parts[0]) == "<small>?</small>":
            variant = ""
        return variant

    if lookup_template(tpl):
        return render_template(word, template)

    if tpl == "рег.":
        text = tpl
        if parts:
            text += f" ({parts[0]})"
        return italic(text)

    if tpl == "аббр.":
        text = italic("сокр.")
        if len(parts) > 1:
            text += f" от {italic(parts[1])}"
        return text

    if tpl == "выдел":
        return parts[0]

    if tpl in {"наречие", "нареч."}:
        text = f"наречие к {italic(parts[0])}"
        if len(parts) > 1:
            text += f"; {parts[1]}"
        return text

    if tpl == "свойство":
        text = tpl
        if data["состояние"] == "1":
            text += " или состояние"
        return f"{text} по значению прилагательного {italic(parts[0])}"

    if tpl == "Унбегаун":
        if data["сокр"] == "1":
            return tpl
        return f"{italic(tpl + ' Б.-О.')} Русские фамилии. — М. : Прогресс, 1989. — 443 с. — ISBN 5-01-001045-3."

    if label := labels.get(tpl):
        if tpl == "умласк.":
            label = "уменьш.-ласк."
        text = italic(label)
        if len(parts) > 1:
            text += f" {'от' if tpl == 'эррат.' else 'к'} {parts[-1]}"
        return text

    if lang := langs.get(tpl):
        return lang

    return defaults.last_template_handler(template, locale, word=word, missed_templates=missed_templates)
