"""Utilities."""
import re
from typing import List

from .lang import templates_italic, templates_ignored, templates_multi, templates_other
from . import constants as C


def capitalize(text: str) -> str:
    """Capitalize the first letter only."""
    return f"{text[0].capitalize()}{text[1:]}"


def fmt_chimy(composition: List[str]) -> str:
    """Format chimy notations."""
    return "".join(f"<sub>{c}</sub>" if c.isdigit() else c for c in composition)


def handle_sport(tpl: str, parts: List[str]) -> str:
    """Handle the 'sport' template."""
    res = f"<i>({capitalize(tpl)}"
    if len(parts) >= 3:
        # {{sport|fr|collectif}}
        res += f" {parts[2]}"
    res += ")</i>"
    return res


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

    # Basic formatting
    text = sub(r"'''?([^']+)'''?", "\\1", text)

    # Clean some HTML tags: we want to keep the data for some of them
    # Ex: <span style="color:black">[[foo]]</span> -> '[[foo]]'
    text = sub(r"<span[^>]+>([^<]+)</span>", "\\1", text)

    # Parser hooks
    text = sub(r"<[^>]+>[^<]+</[^>]+>", "", text)  # <ref>foo</ref> -> ''

    # HTML
    text = sub(r"<[^>]+/?>", " ", text)  # <br> / <br />
    text = text.replace("&nbsp;", " ")

    # Files
    # [[File:picture.svg|vignette|120px|'''Base''' d’or ''(sens héraldique)'']] -> ''
    text = sub(r"\[\[[^|\]]+(?:\|[^\]]+){2,}\]\]", "", text)

    # Local links
    text = sub(r"\[\[([^|\]]+)\]\]", "\\1", text)  # [[a]] -> a
    text = sub(r"\[\[[^|]+\|([^\]]+)\]\]", "\\1", text)  # [[a|b]] -> b

    text = text.replace("[[", "").replace("]]", "")

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

    # Templates
    # {{foo}}
    # {{foo|bar}}
    # {{foo|{{bar}}|123}}
    # {{foo|{{bar|baz}}|123}}

    # Simplify the parsing logic: this line will return a list of nested templates.
    for tpl in set(re.findall(r"({{[^{}]*}})", text)):
        # Transform the nested template.
        # This will remove any nested templates from the original text.
        text = text.replace(tpl, transform(tpl[2:-2]))

    # Now that all nested templates are done, we can process top-level ones
    while "{{" in text:
        start = text.find("{{")
        pos = start + 2
        subtext = ""

        while pos < len(text):
            if text[pos : pos + 2] == "}}":
                # We hit the end of the template
                pos += 1
                break

            # Save the template contents
            subtext += text[pos]
            pos += 1

        # The template is now completed
        transformed = transform(subtext)
        text = f"{text[:start]}{transformed}{text[pos + 1 :]}"

    # Remove extra spaces
    text = sub(r"\s{2,}", " ", text)
    text = sub(r"\s{1,}\.", ".", text)

    return text.strip()


def transform(tpl: str) -> str:
    """Handle the data inside the *text* template."""
    if "|" in tpl:
        parts = tpl.split("|")
        tpl = parts[0]
    else:
        parts = []

    if tpl in templates_ignored[C.LOCALE]:
        return ""

    # {{w|ISO 639-3}} -> ISO 639-3
    if tpl == "w":
        return parts[1]

    # {{fchim|H|2|O}} -> H2O
    if tpl == "fchim":
        return fmt_chimy(parts[1:])

    # {{term|ne … guère que}} -> (Ne … guère que)
    if tpl == "term":
        if parts[1].startswith("<i>("):
            return parts[1]
        elif not parts[1]:
            return ""
        return f"<i>({capitalize(parts[1])})</i>"

    if tpl in templates_multi[C.LOCALE]:
        res: str = eval(templates_multi[C.LOCALE][tpl])
        return res

    if tpl in templates_italic[C.LOCALE]:
        return f"<i>({templates_italic[C.LOCALE][tpl]})</i>"

    if tpl in templates_other[C.LOCALE]:
        return templates_other[C.LOCALE][tpl]

    # {{grammaire|fr}} -> (Grammaire)
    if len(parts) == 2:
        return f"<i>({capitalize(tpl)})</i>"

    # {{conj|grp=1|fr}} -> ''
    if len(parts) > 2:
        return ""

    # May need custom handling in lang/$LOCALE.py
    return f"<i>({capitalize(tpl)})</i>" if tpl else ""
