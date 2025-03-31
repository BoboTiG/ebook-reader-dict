"""Old French language."""

import re

from .. import fr

section_patterns = fr.section_patterns
head_sections = tuple(section.replace("fr", "fro") for section in fr.head_sections)
sections = tuple(section.replace("fr", "fro") for section in fr.sections)
variant_titles = tuple(section.replace("fr", "fro") for section in fr.variant_titles)
variant_templates = tuple(section.replace("fr", "fro") for section in fr.variant_templates)

float_separator = fr.float_separator
thousands_separator = fr.thousands_separator
definitions_to_ignore = fr.definitions_to_ignore
templates_ignored = fr.templates_ignored
templates_italic = fr.templates_italic
templates_multi = fr.templates_multi
templates_other = fr.templates_other
etyl_section = fr.etyl_section
release_description = fr.release_description
wiktionary = fr.wiktionary
last_template_handler = fr.last_template_handler


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
