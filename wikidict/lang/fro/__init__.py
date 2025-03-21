"""Old French language."""

import re

from .. import fr

head_sections = tuple(section.replace("fr", "fro") for section in fr.head_sections)
sections = tuple(section.replace("fr", "fro") for section in fr.sections)
variant_titles = tuple(section.replace("fr", "fro") for section in fr.variant_titles)
variant_templates = tuple(section.replace("fr", "fro") for section in fr.variant_templates)
definitions_to_ignore = tuple(d for d in fr.definitions_to_ignore if d.startswith("{"))

float_separator = fr.float_separator
thousands_separator = fr.thousands_separator
templates_ignored = fr.templates_ignored
templates_italic = fr.templates_italic
templates_multi = fr.templates_multi
templates_other = fr.templates_other
etyl_section = fr.etyl_section
release_description = fr.release_description
wiktionary = fr.wiktionary


def find_genders(
    code: str,
    *,
    pattern: re.Pattern[str] = re.compile(r"{([fmsingp]+)(?: \?\|fro)*}"),
) -> list[str]:
    """
    >>> find_genders("")
    []
    >>> find_genders("'''-eresse''' {{pron|(ə).ʁɛs|fro}} {{f}}")
    ['f']
    >>> find_genders("'''42''' {{msing}}")
    ['msing']
    """
    return fr.find_genders(code, pattern=pattern)


def find_pronunciations(
    code: str,
    *,
    pattern: re.Pattern[str] = re.compile(r"{pron(?:\|lang=fro)?\|([^}\|]+)"),
) -> list[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{pron|ɑ|fro}}")
    ['\\\\ɑ\\\\']
    >>> find_pronunciations("{{pron|ɑ|fro}}, {{pron|a|fro}}")
    ['\\\\ɑ\\\\', '\\\\a\\\\']
    """
    return fr.find_pronunciations(code, pattern=pattern)


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    missed_templates: list[tuple[str, str]] | None = None,
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["fro-accord-ain", "a.me.ʁi.k"], "fro", word="américain")
        'américain'
        >>> last_template_handler(["fro-accord-rég", "a.ta.ʃe də pʁɛs", "ms=attaché", "inv=de presse"], "fro")
        'attaché de presse'
        >>> last_template_handler(["fro-rég", "ka.ʁɔt"], "fro", word="carottes")
        'carotte'
        >>> last_template_handler(["fro-verbe-flexion", "colliger", "ind.i.3s=oui"], "fro")
        'colliger'

    """
    if (tpl := template[0]).startswith(
        (
            "fro-verbe-flexion",
            "fro-accord-rég",
            "fro-rég",
            "fro-accord-",
        )
    ):
        template = tuple([tpl.replace("fro-", "fr-"), *template[1:]])

    return fr.last_template_handler(template, "fr", word=word, missed_templates=missed_templates)
