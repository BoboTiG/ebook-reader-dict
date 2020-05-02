"""Utilities."""
import re
from typing import List

from .lang import templates, templates_ignored, templates_multi
from . import constants as C


def capitalize(text: str) -> str:
    """Capitalize the first letter only."""
    return f"{text[0].capitalize()}{text[1:]}"


def fmt_chimy(composition: List[str]) -> str:
    """Format chimy notations."""
    return "".join(f"<sub>{c}</sub>" if c.isdigit() else c for c in composition)


def int_to_roman(number: int) -> str:
    """
    Convert an integer to a Roman numeral.
    Source: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html
    """

    # if not 0 < number < 4000:
    #     raise ValueError("Argument must be between 1 and 3999")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
    result = []
    for i in range(len(ints)):
        count = int(number / ints[i])
        result.append(nums[i] * count)
        number -= ints[i] * count
    return "".join(result)


def clean(text: str) -> str:
    """Cleans up the provided wikicode.
    Removes templates, tables, parser hooks, magic words, HTML tags and file embeds.
    Keeps links.
    Source: https://github.com/macbre/mediawiki-dump/blob/3f1553a/mediawiki_dump/tokenizer.py#L8
    """
    # Speed-up lookup
    sub = re.sub

    # basic formatting
    text = sub(r"'''?([^']+)'''?", "\\1", text)

    # Parser hooks
    text = sub(r"<[^>]+>[^<]+</[^>]+>", "", text)  # <ref>foo</ref> -> ''

    # HTML
    text = sub(r"<[^>]+/?>", " ", text)  # <br> / <br />
    text = text.replace("&nbsp;", " ")

    # Templates
    # {{foo}} -> 'foo'
    # {{foo|bar}} -> foo, or bar if foo == w
    # {{foo|{{test}}|123}} -> ''
    while "{{" in text:
        start = text.find("{{")
        level = 1
        pos = start + 2
        subtext = ""

        while pos < len(text):
            # print(f"> {text[pos:pos+2]} <")

            if text[pos : pos + 2] == "{{":
                # Nested template - enter next level
                level += 1
                pos += 1
            elif text[pos : pos + 2] == "}}":
                # Nested template - leave this level
                pos += 1
                level -= 1
            else:
                subtext += text[pos]

            # The template is now completed
            if level == 0:
                # print(repr(text), start, pos, repr(text[start : pos + 1]))

                # Handle he data inside the template
                if "|" in subtext:
                    parts = subtext.split("|")
                    tpl = parts[0]
                    if tpl == "w":
                        # Ex: {{w|ISO 639-3}} -> ISO 639-3
                        subtext = parts[1]
                    elif tpl == "fchim":
                        # Ex: {{fchim|H|2|O}} -> H2O
                        subtext = fmt_chimy(parts[1:])
                    elif tpl == "term":
                        # Ex: {{term|ne … guère que}} -> (Ne … guère que)
                        subtext = f"({capitalize(parts[1])})"
                    elif tpl in templates_ignored[C.LOCALE]:
                        subtext = ""
                    elif tpl in templates_multi[C.LOCALE]:
                        subtext = eval(templates_multi[C.LOCALE][tpl])
                    elif tpl in templates[C.LOCALE]:
                        subtext = templates[C.LOCALE][tpl]
                    elif len(parts) == 2:
                        # Ex: {{grammaire|fr}} -> (Grammaire)
                        subtext = f"({capitalize(tpl)})"
                    else:
                        # Ex: {{trad+|af|gebruik}} -> ''
                        # Ex: {{conj|grp=1|fr}} -> ''
                        subtext = ""
                elif subtext in templates_ignored[C.LOCALE]:
                    subtext = ""
                elif subtext in templates[C.LOCALE]:
                    subtext = templates[C.LOCALE][subtext]
                else:
                    # May need custom handling in lang/$LOCALE.py
                    subtext = f"({capitalize(subtext)})"

                text = f"{text[:start]}{subtext}{text[pos + 1 :]}"
                break

            # Check the next character
            pos += 1

        # The template is not well balanced, leave the endless loop
        if level != 0:  # pragma: nocover
            break

    # Tables
    text = sub(r"{\|[^}]+\|}", "", text)  # {|foo..|}

    # Headings
    text = sub(
        r"^=+\s?([^=]+)\s?=+",
        lambda matches: matches.group(1).strip(),
        text,
        flags=re.MULTILINE,
    )  # == a == -> a

    # Files and other links with namespaces
    text = sub(r"\[\[[^:\]]+:[^\]]+\]\]", "", text)  # [[foo:b]] -> ''

    # Local links
    text = sub(r"\[\[([^|\]]+)\]\]", "\\1", text)  # [[a]] -> a
    text = sub(r"\[\[[^|]+\|([^\]]+)\]\]", "\\1", text)  # [[a|b]] -> b

    text = text.replace("[[", "").replace("]]", "")

    # External links
    text = sub(
        r"\[http[^\s]+ ([^\]]+)\]", "\\1", text
    )  # [[http://example.com foo]] -> foo
    text = sub(r"https?://[^\s]+", "", text)  # remove http://example.com

    # Lists
    text = sub(r"^\*+\s?", "", text, flags=re.MULTILINE)

    # Magic words
    text = sub(r"__\w+__", "", text)  # __TOC__

    # Remove extra quotes left
    text = text.replace("''", "")

    # Remove extra spaces
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s{1,}\.", ".", text)

    return text.strip()


def is_ignored(word: str) -> bool:
    """Helper to filter out words from the final dictionary."""
    # Filter out "small" words and numbers
    return len(word) < 3 or word.isnumeric()
