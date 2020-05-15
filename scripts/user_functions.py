"""Functions that can be used in *templates_multi*."""
from typing import Tuple
from warnings import warn

from .lang.fr.langs import langs as FR

all_langs = {
    "fr": FR,
}


def capitalize(text: str) -> str:
    """Capitalize the first letter only.

        >>> capitalize("alice")
        'Alice'
        >>> capitalize("BOB")
        'BOB'
        >>> capitalize("alice and bob")
        'Alice and bob'
    """
    return f"{text[0].capitalize()}{text[1:]}"


def format_chimy(composition: Tuple[str, ...]) -> str:
    """Format chimy notations.

        >>> format_chimy(["H", "2", "O"])
        'H<sub>2</sub>O'
        >>> format_chimy(["FeCO", "3", ""])
        'FeCO<sub>3</sub>'
    """
    return "".join(f"<sub>{c}</sub>" if c.isdigit() else c for c in composition)


def handle_century(parts: Tuple[str, ...], century: str) -> str:
    """Handle different century templates.

        >>> handle_century(["siècle", "XVI"], "siècle")
        'XVI<sup>e</sup> siècle'
        >>> handle_century(["siècle", "XVIII", "XIX"], "century")
        'XVIII<sup>e</sup> century - XIX<sup>e</sup> century'
    """
    return " - ".join(f"{p}<sup>e</sup> {century}" for p in parts[1:])


def handle_etyl(parts: Tuple[str, ...]) -> str:
    """Handle the 'etyl' (etymological language) template.
    Source: https://fr.wiktionary.org/wiki/Mod%C3%A8le:%C3%A9tyl

        >>> handle_etyl("étyl|grc|fr".split("|"))
        'grec ancien'
        >>> handle_etyl("étyl|no|fr|mot=ski".split("|"))
        'norvégien <i>ski</i>'
        >>> handle_etyl("étyl|la|fr|mot=invito|type=verb".split("|"))
        'latin <i>invito</i>'
        >>> handle_etyl("étyl|grc|fr|mot=λόγος|tr=lógos|type=nom|sens=étude".split("|"))
        'grec ancien λόγος, <i>lógos</i> (« étude »)'
        >>> handle_etyl("étyl|grc|fr|λόγος|lógos|étude|type=nom|lien=1".split("|"))
        'grec ancien λόγος, <i>lógos</i> (« étude »)'
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


def handle_name(parts: Tuple[str, ...]) -> str:
    """Handle the 'name' template to display writers/authors or any full name person.
    Source: https://fr.wiktionary.org/wiki/Mod%C3%A8le:nom_w_pc

        >>> handle_name(["nom w pc", "Aldous", "Huxley"])
        "Aldous <span style='font-variant:small-caps'>Huxley</span>"
        >>> handle_name(["nom w pc", "L. L. Zamenhof"])
        'L. L. Zamenhof'
        >>> handle_name(["nom w pc", "Théodore Agrippa d’", "Aubigné"])
        "Théodore Agrippa d’ <span style='font-variant:small-caps'>Aubigné</span>"
        >>> handle_name(["nom w pc", "Théodore Agrippa d’", "Aubigné", "'=oui"])
        "Théodore Agrippa d’<span style='font-variant:small-caps'>Aubigné</span>"
    """
    res = parts[1]
    if len(parts) > 2:
        if parts[-1] != "'=oui":
            res += " "
        res += f"<span style='font-variant:small-caps'>{parts[2]}</span>"
    else:
        warn(f"Malformed template in the Wikicode (parts={parts})")
    return res


def handle_sport(tpl: str, parts: Tuple[str, ...]) -> str:
    """Handle the 'sport' template.

        >>> handle_sport("sport", [""])
        '<i>(Sport)</i>'
        >>> handle_sport("sport", ["sport", "fr", "collectif"])
        '<i>(Sport collectif)</i>'
    """
    res = f"<i>({capitalize(tpl)}"
    if len(parts) >= 3:
        # {{sport|fr|collectif}}
        res += f" {parts[2]}"
    res += ")</i>"
    return res


def handle_term(text: str) -> str:
    """Format a term.

        >>> handle_term("")
        ''
        >>> handle_term("foo")
        '<i>(Foo)</i>'
        >>> handle_term("Foo")
        '<i>(Foo)</i>'
        >>> handle_term("<i>(Foo)</i>")
        '<i>(Foo)</i>'
    """
    if text.startswith("<i>("):
        return text
    elif not text:
        return ""
    return f"<i>({capitalize(text)})</i>"


def handle_unit(parts: Tuple[str, ...]) -> str:
    """Pretty format a 'unit'.

        >>> handle_unit(["92", "%"])
        '92%'
    """
    return "".join(parts)


def int_to_roman(number: int) -> str:
    """
    Convert an integer to a Roman numeral.
    Source: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html

        >>> int_to_roman(12)
        'XII'
        >>> int_to_roman(19)
        'XIX'
        >>> int_to_roman(2020)
        'MMXX'
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


__all__ = (
    "capitalize",
    "format_chimy",
    "handle_century",
    "handle_etyl",
    "handle_name",
    "handle_sport",
    "handle_term",
    "handle_unit",
    "int_to_roman",
)
