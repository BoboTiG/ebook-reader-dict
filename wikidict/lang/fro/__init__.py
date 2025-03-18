"""Old French language."""

import re

from ...user_functions import flatten, unique
from .. import fr

head_sections = ("{{langue|fro}}",)
sections = tuple(section.replace("fr", "fro") for section in fr.sections)
variant_titles = tuple(section.replace("fr", "fro") for section in fr.variant_titles)

float_separator = fr.float_separator
thousands_separator = fr.thousands_separator
definitions_to_ignore = fr.definitions_to_ignore
templates_ignored = fr.templates_ignored
templates_italic = fr.templates_italic
templates_multi = fr.templates_multi
templates_other = fr.templates_other
etyl_section = fr.etyl_section
variant_templates = fr.variant_templates
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
    return unique(flatten(pattern.findall(code)))


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
    if not (match := pattern.search(code)):
        return []

    # There is at least one match, we need to get whole line
    # in order to be able to find multiple pronunciations
    line = code[match.start() : code.find("\n", match.start())]
    return [f"\\{p}\\" for p in unique(pattern.findall(line))]
