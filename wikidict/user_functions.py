"""
Functions that can be used in *templates_multi* of any locale.

Check the "html/wikidict/user_functions.html" file for a user-friendly version.
"""
import re
from collections import defaultdict
from typing import Dict, List, Optional

from .lang import templates_italic


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


def century(parts: List[str], century: str) -> str:
    """
    Format centuries.

        >>> century(["XVI"], "siècle")
        'XVI<sup>e</sup> siècle'
        >>> century(["XVIII", "XIX"], "century")
        'XVIII<sup>e</sup> century - XIX<sup>e</sup> century'
    """
    return " - ".join(f"{p}{superscript('e')} {century}" for p in parts)


def chimy(composition: List[str]) -> str:
    """
    Format chimy notations.

        >>> chimy(["H", "2", "O"])
        'H<sub>2</sub>O'
        >>> chimy(["FeCO", "3", ""])
        'FeCO<sub>3</sub>'
    """
    return "".join(subscript(c) if c.isdigit() else c for c in composition)


def chinese(
    parts: List[str], data: Dict[str, str], laquo: str = "“", raquo: str = "”"
) -> str:
    """
    Format Chinese word or sentence.

        >>> chinese(["餃臺灣／台灣／台湾"], defaultdict(str))
        '餃臺灣／台灣／台湾'
        >>> chinese(["痟", "mad"], defaultdict(str, {"tr": "siáu"}))
        '痟 (<i>siáu</i>, “mad”)'
        >>> chinese(["秦"], defaultdict(str, {"gloss": "Qin"}))
        '秦 (“Qin”)'
        >>> chinese(["餃子／饺子", "jiǎozi"], defaultdict(str))
        '餃子／饺子 (<i>jiǎozi</i>)'
        >>> chinese(["餃子／饺子", "jiǎozi", "jiaozi bouillis"], defaultdict(str), laquo="«&nbsp;", raquo="&nbsp;»")
        '餃子／饺子 (<i>jiǎozi</i>, «&nbsp;jiaozi bouillis&nbsp;»)'
        >>> chinese(["*班長", ""], defaultdict(str, {"tr": "bānzhǎng", "gloss": "team leader"}))
        '*班長 (<i>bānzhǎng</i>, “team leader”)'
        >>> chinese(["木蘭"], defaultdict(str, {"tr": "Mùlán", "lit": "magnolia"}))
        '木蘭 (<i>Mùlán</i>, literally “magnolia”)'
    """  # noqa
    phrase = parts.pop(0).replace("/", "／")
    tr = data["tr"] or (parts.pop(0) if parts else "")
    gl = data["gloss"] or (parts.pop(0) if parts else "")
    if not tr and not gl and not data["lit"]:
        return phrase

    phrase += " ("
    if tr:
        phrase += italic(tr)
    if gl:
        if tr:
            phrase += ", "
        phrase += f"{laquo}{gl}{raquo}"
    if data["lit"]:
        if tr:
            phrase += ", literally "
        phrase += f"{laquo}{data['lit']}{raquo}"
    phrase += ")"
    return phrase


def color(rgb: str) -> str:
    """
    Format a RGB hexadecimal color.

        >>> color("#B0F2B6")
        '[RGB #B0F2B6]'
    """
    return f"[RGB {rgb}]"


def concat(
    parts: List[str],
    sep: str = "",
    last_sep: str = None,
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
        >>> concat(["Mathématique", "Physique", "Chimie"], sep=", ", last_sep=" et ")
        'Mathématique, Physique et Chimie'
        >>> concat(["Physique", "Chimie"], sep=", ", last_sep=" et ")
        'Physique et Chimie'
        >>> concat(["Physique"], sep=", ", last_sep=" et ")
        'Physique'
    """
    if indexes:
        result = [part for index, part in enumerate(parts) if index in indexes]
    else:
        result = list(parts)

    if skip:
        result = [part for part in result if part != skip]
        if parts.count(skip):
            sep = " "
    r = [p for p in result if p]
    if last_sep is None or last_sep == sep or len(r) == 1:
        return sep.join(r)
    else:
        return sep.join(r[:-1]) + last_sep + r[-1] if r else ""


def coord(values: List[str]) -> str:
    """
    Format lon/lat coordinates.

        >>> coord(["04", "39", "N", "74", "03", "O", "type:country"])
        '04°39′N 74°03′O'
    """
    return "{0}°{1}′{2} {3}°{4}′{5}".format(*values)


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
          File "<doctest wikidict.user_functions.eval_expr[0]>", line 1, in <module>
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


def extract_keywords_from(parts: List[str]) -> Dict[str, str]:
    """
    Given a list of strings, extract strings containing an equal sign ("=").

    Return a *defaultdict(str)* with key=value extracted from the original list.

    The left part of the sign is used as the dict key and the right part as the value.
    When a string contains the sign, it is removed from the original list.

        >>> extract_keywords_from([])
        defaultdict(<class 'str'>, {})
        >>> extract_keywords_from(["foo"])
        defaultdict(<class 'str'>, {})
        >>> extract_keywords_from(["foo", "bar=baz"])
        defaultdict(<class 'str'>, {'bar': 'baz'})
        >>> extract_keywords_from(["foo", "bar=baz=ouf"])
        defaultdict(<class 'str'>, {'bar': 'baz=ouf'})
        >>> extract_keywords_from(["foo", "bar = baz=ouf"])
        defaultdict(<class 'str'>, {'bar': 'baz=ouf'})
    """
    data = defaultdict(str)
    for part in parts.copy():
        if "=" in part:
            key, value = part.split("=", 1)
            data[key.strip()] = value.strip()
            parts.pop(parts.index(part))
    return data


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


def lookup_italic(word: str, locale: str, empty_default: bool = False) -> str:
    """
    Find the *word* from the *templates_italic* table of the given *locale*.

    If the *word* is not found, it is returned as-is.

        >>> lookup_italic("", "fr")
        ''
        >>> lookup_italic("absol", "fr")
        'Absolument'
        >>> lookup_italic("inexistant", "fr")
        'inexistant'
        >>> lookup_italic("alagoas", "pt")
        'Alagoas'
        >>> lookup_italic("Antropônimo", "pt")
        'Antropônimo'
    """
    default = "" if empty_default else word
    looking_for = word

    if locale == "pt":
        looking_for = word.lower()
        default = word

    return templates_italic[locale].get(looking_for, default)


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

    # Handle mathematical substract character
    has_math_substract_symbol = number[0] == "−"
    if has_math_substract_symbol:
        number = number.replace("−", "-")

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
    res = res.replace(",", "|").replace(".", fsep).replace("|", tsep)

    if has_math_substract_symbol:
        res = res.replace("-", "−")

    return res


def parenthesis(text: str) -> str:
    """
    Return the *text* surrounded by parenthesis.

        >>> parenthesis("foo")
        '(foo)'
    """
    return f"({text})"


def person(word: str, parts: List[str]) -> str:
    """
    Format a person name.

        >>> person("foo", ["Aldous", "Huxley"])
        'Aldous Huxley'
        >>> person("foo", ["Théodore Agrippa d’", "Aubigné"])
        'Théodore Agrippa d’ Aubigné'
        >>> person("foo", ["Théodore Agrippa d’", "Aubigné", "'=oui"])
        'Théodore Agrippa d’Aubigné'
        >>> person("foo", ["L. L. Zamenhof"])
        'L. L. Zamenhof'
        >>> person("foo", ["lang=en", "Roger", "Adams"])
        'Roger Adams'
        >>> person("foo", ["", "Brantôme", "Brantôme (écrivain)"])
        'Brantôme'

    Source: https://fr.wiktionary.org/wiki/Mod%C3%A8le:nom_w_pc
    """
    data = [p for p in parts if "=" in p]
    parts = [p for p in parts if "=" not in p]
    res = parts.pop(0)

    # First name only
    if not parts:
        return res

    # Last name only or first name + last name
    space = "" if ("'=oui" in data or not res) else " "
    res += space + parts.pop(0)
    return res


def sentence(parts: List[str]) -> str:
    """
    Capitalize the first item in *parts* and concat with the second one.

        >>> sentence(["superlatif de", "petit", "fr"])
        'Superlatif de petit'
        >>> sentence(["variante de", "ranche", "fr"])
        'Variante de ranche'
        >>> sentence(["RFC", "5322"])
        'RFC 5322'
        >>> sentence(["comparatif de", "bien", "fr", "adv"])
        'Comparatif de bien'
    """
    return capitalize(concat(parts, sep=" ", indexes=[0, 1]))


def small(text: str) -> str:
    """
    Return the *text* surrounded by small HTML tags.

        >>> small("foo")
        '<small>foo</small>'
    """
    return f"<small>{text}</small>"


def small_caps(text: str) -> str:
    """
    Return the *text* surrounded by the CSS style to use small capitals.

    Small-caps glyphs typically use the form of uppercase letters but are reduced
    to the size of lowercase letters.

        >>> small_caps("Dupont")
        "<span style='font-variant:small-caps'>Dupont</span>"
    """
    return f"<span style='font-variant:small-caps'>{text}</span>"


def strike(text: str) -> str:
    """
    Return the *text* surrounded by strike HTML tags.

        >>> strike("foo")
        '<s>foo</s>'
    """
    return f"<s>{text}</s>"


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


def tag(parts: List[str]) -> str:
    """
    Get only interesting values from *parts*.

    - values without `=`
    - values starting with `text=`

    Source: https://sv.wiktionary.org/wiki/Mall:tagg

        >>> tag(["historia"])
        'historia'
        >>> tag(["biologi", "allmänt"])
        'biologi, allmänt'
        >>> tag(["politik", "formellt", "språk=tyska"])
        'politik, formellt'
        >>> tag(["kat=nedsättande", "text=något nedsättande"])
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
    return italic(parenthesis(text))


__all__ = (
    "capitalize",
    "century",
    "chimy",
    "chinese",
    "extract_keywords_from",
    "color",
    "concat",
    "coord",
    "eval_expr",
    "int_to_roman",
    "italic",
    "lookup_italic",
    "number",
    "parenthesis",
    "person",
    "sentence",
    "small",
    "small_caps",
    "strike",
    "strong",
    "subscript",
    "superscript",
    "tag",
    "term",
)
