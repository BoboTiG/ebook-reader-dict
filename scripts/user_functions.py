"""
Functions that can be used in *templates_multi* of any locale.

Check the "html/scripts/user_functions.html" file for a user-friendly version.
"""
import re
from typing import List, Optional, Tuple
from warnings import warn

from .lang import all_langs, templates_italic


def capitalize(text: str) -> str:
    """
    Capitalize the first letter only.

        >>> capitalize("")
        ''
        >>> capitalize("alice")
        'Alice'
        >>> capitalize("BOB")
        'BOB'
        >>> capitalize("alice and bob")
        'Alice and bob'
    """
    if not text:
        return ""
    return f"{text[0].capitalize()}{text[1:]}"


def century(parts: Tuple[str, ...], century: str) -> str:
    """
    Format centuries.

        >>> century(["siècle", "XVI"], "siècle")
        'XVI<sup>e</sup> siècle'
        >>> century(["siècle", "XVIII", "XIX"], "century")
        'XVIII<sup>e</sup> century - XIX<sup>e</sup> century'
    """
    return " - ".join(f"{p}{superscript('e')} {century}" for p in parts[1:])


def chimy(composition: Tuple[str, ...]) -> str:
    """
    Format chimy notations.

        >>> chimy(["H", "2", "O"])
        'H<sub>2</sub>O'
        >>> chimy(["FeCO", "3", ""])
        'FeCO<sub>3</sub>'
    """
    return "".join(subscript(c) if c.isdigit() else c for c in composition)


def color(rgb: str) -> str:
    """
    Format a RGB hexadecimal color.

        >>> color("#B0F2B6")
        '[RGB #B0F2B6]'
    """
    return f"[RGB {rgb}]"


def concat(
    parts: Tuple[str, ...],
    sep: str = "",
    indexes: Optional[List[int]] = None,
    skip: Optional[str] = None,
) -> str:
    """
    Simply concat all *parts* using the *sep* character as glue.

    If *indexes* is set, it must be a list of integers where each of one is the part number to keep.
    If *skip* is set, it must be a string. If a part is equal to *skip* then is it skipped and the
    *sep* become a single space.
    It allowes to filter out some parts while keeping others.

        >>> concat(["92", "%"])
        '92%'
        >>> concat(["O", "M", "G"], sep="!")
        'O!M!G'
        >>> concat(["sport"], sep=" ", indexes=[0, 2])
        'sport'
        >>> concat(["sport", "fr", "collectif"], sep=" ", indexes=[0, 2])
        'sport collectif'
        >>> concat(["marca", "ca", "antigament", "_", "en plural"], sep=" ", indexes=[2, 3, 4, 5], skip="_")
        'antigament en plural'
        >>> concat(["antigament", "_", "en plural"], sep=",", skip="_")
        'antigament en plural'
        >>> concat(["Arte", "", ""], sep=" e ")
        'Arte'
    """
    if indexes:
        result = [part for index, part in enumerate(parts) if index in indexes]
    else:
        result = list(parts)

    if skip:
        result = [part for part in result if part != skip]
        if parts.count(skip):
            sep = " "

    return sep.join(p for p in result if p)


def coord(values: Tuple[str, ...]) -> str:
    """
    Format lon/lat coordinates.

        >>> coord(["04", "39", "N", "74", "03", "O", "type:country"])
        '04°39′N 74°03′O'
    """
    return "{0}°{1}′{2} {3}°{4}′{5}".format(*values)


def etymology(parts: Tuple[str, ...]) -> str:
    """
    Display cross-language etymology.

        >>> etymology("étyl|grc|fr".split("|"))
        'grec ancien'
        >>> etymology("étyl|no|fr|mot=ski".split("|"))
        'norvégien <i>ski</i>'
        >>> etymology("étyl|la|fr|mot=invito|type=verb".split("|"))
        'latin <i>invito</i>'
        >>> etymology("étyl|grc|fr|mot=λόγος|tr=lógos|type=nom|sens=étude".split("|"))
        'grec ancien λόγος, <i>lógos</i> (« étude »)'
        >>> etymology("étyl|grc|fr|λόγος|lógos|étude|type=nom|lien=1".split("|"))
        'grec ancien λόγος, <i>lógos</i> (« étude »)'
        >>> etymology("calque|la|fr".split("|"))
        'latin'
        >>> etymology("calque|en|fr|mot=to date|sens=à ce jour".split("|"))
        'anglais <i>to date</i> (« à ce jour »)'
        >>> etymology("calque|sa|fr|mot=वज्रयान|tr=vajrayāna|sens=véhicule du diamant".split("|"))
        'sanskrit वज्रयान, <i>vajrayāna</i> (« véhicule du diamant »)'

    Source: https://fr.wiktionary.org/wiki/Mod%C3%A8le:%C3%A9tyl

    Source: https://fr.wiktionary.org/wiki/Mod%C3%A8le:calque
    """
    l10n_src = parts[1]
    l10n_dst = parts[2]
    res = all_langs[l10n_dst][l10n_src]
    if len(parts) == 3:
        return res

    data = {}
    for part in parts[3:]:
        if "=" in part:
            key, value = part.split("=")
            data[key] = value
        elif "mot" not in data:
            data["mot"] = part
        elif "tr" not in data:
            data["tr"] = part
        elif "sens" not in data:
            data["sens"] = part

    if "tr" in data:
        res += f" {data['mot']}, <i>{data['tr']}</i>"
    else:
        res += f" <i>{data['mot']}</i>"
    if "sens" in data:
        res += f" (« {data['sens']} »)"

    return res


def eval_expr(expr: str) -> str:
    """
    Compute and return the result of *expr*.

        >>> eval_expr("2 ^ 30")
        '1073741824'

    *expr* is sanitized and only a small range of characters are allowed:

        >>> eval_expr("cat /etc/passwd")  # doctest: +ELLIPSIS
        Traceback (most recent call last):
          File ".../doctest.py", line 1329, in __run
            compileflags, 1), test.globs)
          File "<doctest scripts.user_functions.eval_expr[0]>", line 1, in <module>
          File ".../user_functions.py", line 33, in eval_expr
            raise ValueError(f"Dangerous characters in the expr {expr!r}")
        ValueError: Dangerous characters in the expr 'cat /etc/passwd'

    Allowed characters are digits (0-9), spaces and operators (+-*^).
    """
    # Prevent horrors
    # digits, space and operators (+-*^)
    if re.search(r"[^\d\s\*\-\+\^\.]+", expr):
        raise ValueError(f"Dangerous characters in the expr {expr!r}")

    # Replace signs
    expr = expr.replace("^", "**")

    return f"{eval(expr)}"


def int_to_roman(number: int) -> str:
    """
    Convert an integer to a Roman numeral.

        >>> int_to_roman(12)
        'XII'
        >>> int_to_roman(2020)
        'MMXX'

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


def italic(text: str) -> str:
    """
    Return the *text* surrounded by italic HTML tags.

        >>> italic("foo")
        '<i>foo</i>'
    """
    return f"<i>{text}</i>"


def lookup_italic(word: str, locale: str) -> str:
    """
    Find the *word* from the *templates_italic* table of the given *locale*.

    If the *word* is not found, it is returned as-is.

        >>> lookup_italic("", "fr")
        ''
        >>> lookup_italic("absol", "fr")
        'Absolument'
        >>> lookup_italic("inexistant", "fr")
        'inexistant'
    """
    return templates_italic[locale].get(word, word)


def number(number: str, fsep: str, tsep: str) -> str:
    """
    Format a number using the provided float and thousands separators.

        >>> number("1 000 000 000 000", ",", " ")
        '1 000 000 000 000'
        >>> number("1000000", ",", " ")
        '1 000 000'
        >>> number("1000000", ".", "")
        '1000000'
        >>> number("1000000", ".", ",")
        '1,000,000'
        >>> number("-1000000", ",", " ")
        '-1 000 000'
        >>> number("-1000000", "", "")
        '-1000000'
        >>> number("-1000000", ".", ",")
        '-1,000,000'
        >>> number("4.54609", "," , " ")
        '4,54609'
        >>> number("4.54609", "." , ",")
        '4.54609'
        >>> number("22905", "," , ".")
        '22.905'
    """
    # Remove superfluous spaces
    number = number.replace(" ", "")

    try:
        # Integer
        res = f"{int(number):,}"
    except ValueError:
        # Float
        res = f"{float(number):,}"

    # Replace the current thousands separator with "|";
    # then replace the dot with the float separator;
    # and lastly replace the "|" with the deisred thousands separator.
    # This 3-steps-replacement is needed for when separators are replacing each other.
    return res.replace(",", "|").replace(".", fsep).replace("|", tsep)


def person(parts: Tuple[str, ...]) -> str:
    """
    Format a person name.

        >>> person(["Aldous", "Huxley"])
        "Aldous <span style='font-variant:small-caps'>Huxley</span>"
        >>> person(["Théodore Agrippa d’", "Aubigné"])
        "Théodore Agrippa d’ <span style='font-variant:small-caps'>Aubigné</span>"
        >>> person(["Théodore Agrippa d’", "Aubigné", "'=oui"])
        "Théodore Agrippa d’<span style='font-variant:small-caps'>Aubigné</span>"
        >>> person(["L. L. Zamenhof"])
        'L. L. Zamenhof'

    Source: https://fr.wiktionary.org/wiki/Mod%C3%A8le:nom_w_pc
    """
    res = parts[0]
    if len(parts) > 1:
        if parts[-1] != "'=oui":
            res += " "
        res += small_caps(parts[1])
    else:
        warn(f"Malformed template in the Wikicode (parts={parts})")
    return res


def sentence(parts: Tuple[str, ...]) -> str:
    """
    Capitalize the first item in *parts* and concat with the second one.

        >>> sentence("superlatif de|petit|fr".split("|"))
        'Superlatif de petit'
        >>> sentence("variante de|ranche|fr".split("|"))
        'Variante de ranche'
        >>> sentence("RFC|5322".split("|"))
        'RFC 5322'
        >>> sentence("comparatif de|bien|fr|adv".split("|"))
        'Comparatif de bien'
    """
    return capitalize(concat(parts, sep=" ", indexes=[0, 1]))


def small_caps(text: str) -> str:
    """
    Return the *text* surrounded by the CSS style to use small capitals.

    Small-caps glyphs typically use the form of uppercase letters but are reduced
    to the size of lowercase letters.

        >>> small_caps("Dupont")
        "<span style='font-variant:small-caps'>Dupont</span>"
    """
    return f"<span style='font-variant:small-caps'>{text}</span>"


def strong(text: str) -> str:
    """
    Return the *text* surrounded by strong HTML tags.

        >>> strong("foo")
        '<b>foo</b>'
    """
    return f"<b>{text}</b>"


def subscript(text: str) -> str:
    """
    Return the *text* surrounded by subscript HTML tags.

    Subscript text appears half a character below the normal line,
    and is sometimes rendered in a smaller font.
    Subscript text can be used for chemical formulas.

        >>> subscript("foo")
        '<sub>foo</sub>'
    """
    return f"<sub>{text}</sub>"


def superscript(text: str) -> str:
    """
    Return the *text* surrounded by superscript HTML tags.

    Superscript text appears half a character above the normal line,
    and is sometimes rendered in a smaller font.

        >>> superscript("foo")
        '<sup>foo</sup>'
    """
    return f"<sup>{text}</sup>"


def tag(parts: Tuple[str, ...]) -> str:
    """
    Get only interesting values from *parts*.

    - values without `=`
    - values starting with `text=`

    Source: https://sv.wiktionary.org/wiki/Mall:tagg

        >>> tag(["historia"])
        'historia'
        >>> tag(["biologi", "allmänt"])
        'biologi, allmänt'
        >>> tag("politik|formellt|språk=tyska".split("|"))
        'politik, formellt'
        >>> tag("kat=nedsättande|text=något nedsättande".split("|"))
        'något nedsättande'
    """
    words = []

    for part in parts:
        if "=" not in part:
            words.append(part)
        elif part.startswith("text="):
            words.append(part.split("=")[1])

    return ", ".join(words)


def term(text: str) -> str:
    """
    Format a "term", e.g. return the *text* in italic and surrounded by parenthesis.

    If the *text* is already in such style, it will not be processed again.

        >>> term("")
        ''
        >>> term("foo")
        '<i>(foo)</i>'
        >>> term("Foo")
        '<i>(Foo)</i>'
        >>> term("<i>(Foo)</i>")
        '<i>(Foo)</i>'
    """
    if not text:
        return ""
    elif text.startswith("<i>("):
        return text
    return italic(f"({text})")


__all__ = (
    "capitalize",
    "century",
    "chimy",
    "color",
    "concat",
    "coord",
    "etymology",
    "eval_expr",
    "int_to_roman",
    "italic",
    "lookup_italic",
    "number",
    "person",
    "sentence",
    "small_caps",
    "strong",
    "subscript",
    "superscript",
    "tag",
    "term",
)
