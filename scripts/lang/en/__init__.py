"""English language."""
from typing import Tuple

# Regex to find the pronunciation
pronunciation = r"{IPA\|en\|/([^/]+)/"

# Float number separator
float_separator = "."

# Thousads separator
thousands_separator = ","

# Markers for sections that contain interesting text to analyse.
head_sections = ("english",)
section_sublevels = (4, 3)
etyl_section = ["Etymology", "Etymology 1"]
sections = (
    "Adjective",
    "Adverb",
    "Article",
    "Conjunction",
    "Contraction",
    "Determiner",
    *etyl_section,
    "Interjection",
    "Noun",
    "Numeral",
    "Particle",
    "Prefix",
    "Preposition",
    "Pronoun",
    "Proper noun",
    "Suffix",
    "Symbol",
    "Verb",
)

# Some definitions are not good to keep (plural, genre, ... )
definitions_to_ignore = (
    "en-past of",
    "en-simple past of",
    "infl of",
    "inflection of",
    "plural of",
    "rfdef",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "c",
    "C",
    "cln",
    "multiple images",
    "+obj",
    "picdic",
    "picdiclabel",
    "rel-bottom",
    "rel-top",
    "rfex",
    "root",
    "senseid",
    "tea room",
    "tea room sense",
    "top",
    "topics",
    "was wotd",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "AAVE": "African-American Vernacular",
    "American": "US",
    "Early ME": "Early Middle English",
}

# Templates more complex to manage.
templates_multi = {
    # {{abbr of|en|abortion}}
    "abbr of": "italic('Abbreviation of') + ' ' + strong(parts[-1])",
    # {{alt case|en|angstrom}}
    "alt case": "italic('Alternative letter-case form of') + ' ' + strong(parts[-1])",
    # {{defdate|from 15th c.}}
    "defdate": "small('[' + parts[1] + ']')",
    # {{eye dialect of|en|is}}
    "eye dialect of": "italic('Eye dialect spelling of') + ' ' + strong(parts[-1])",
    # {{form of|en|obsolete emphatic|ye}}
    "form of": "italic(parts[2] + ' of') + ' ' + strong(parts[-1])",
    # {{gloss|liquid H<sub>2</sub>O}}
    "gloss": "parenthesis(parts[1])",
    # {{IPAchar|[tʃ]|lang=en}})
    "IPAchar": "parts[1]",
    # {{IPAfont|[[ʌ]]}}
    "IPAfont": 'f"⟨{parts[1]}⟩"',
    # {{n-g|Definite grammatical ...}}
    "n-g": "italic(parts[-1].lstrip('1='))",
    # {{ngd|Definite grammatical ...}}
    "ngd": "italic(parts[-1].lstrip('1='))",
    # {{non-gloss definition|Definite grammatical ...}}
    "non-gloss definition": "italic(parts[-1].lstrip('1='))",
    # {{q|Used only ...}}
    "q": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{qual|Used only ...}}
    "qual": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{qualifier|Used only ...}}
    "qualifier": "'(' + concat([italic(p) for p in parts[1:]], ', ') + ')'",
    # {{taxlink|Gadus macrocephalus|species|ver=170710}}
    "taxlink": "italic(parts[1])",
    # {{vern|Pacific cod}}
    "vern": "parts[-1]",
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be call in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["alternative form of", "enm" , "theen"], "en")
        '<i>Alternative form of</i> <b>theen</b>'
        >>> last_template_handler(["alt form", "enm" , "a", "pos=indefinite article"], "en")
        '<i>Alternative form of</i> <b>a</b> (indefinite article)'
        >>> last_template_handler(["alt form", "enm" , "worth", "t=to become"], "en")
        '<i>Alternative form of</i> <b>worth</b> (“to become”)'
        >>> last_template_handler(["alt form", "en" , "ess", "nodot=1"], "en")
        '<i>Alternative form of</i> <b>ess</b>'

        >>> last_template_handler(["bor", "en", "ar", "الْعِرَاق", "", "Iraq"], "en")
        'Arabic <i>الْعِرَاق</i> (<i>ālʿrāq</i>, “Iraq”)'
        >>> last_template_handler(["der", "en", "fro", "-"], "en")
        'Old French'
        >>> last_template_handler(["etyl", "enm", "en"], "en")
        'Middle English'
        >>> last_template_handler(["inh", "en", "enm", "water"], "en")
        'Middle English <i>water</i>'
        >>> last_template_handler(["inh", "en", "ang", "wæter", "", "water"], "en")
        'Old English <i>wæter</i> (“water”)'
        >>> last_template_handler(["inh", "en", "ang", "etan", "t=to eat"], "en")
        'Old English <i>etan</i> (“to eat”)'
        >>> last_template_handler(["inh", "en", "ine-pro", "*werdʰh₁om", "*wr̥dʰh₁om"], "en")
        'Proto-Indo-European <i>*wr̥dʰh₁om</i>'
        >>> last_template_handler(["noncog", "fro", "livret", "t=book, booklet"], "en")
        'Old French <i>livret</i> (“book, booklet”)'
        >>> last_template_handler(["noncog", "xta", "I̱ta Ita", "lit=flower river"], "en") #xochopa
        'Alcozauca Mixtec <i>I̱ta Ita</i> (literally “flower river”)'
        >>> last_template_handler(["noncog", "egy", "ḫt n ꜥnḫ", "", "grain, food", "lit=wood/stick of life"], "en")
        'Egyptian <i>ḫt n ꜥnḫ</i> (“grain, food”, literally “wood/stick of life”)'


        >>> last_template_handler(["doublet", "en" , "fire"], "en")
        'Doublet of <i>fire</i>'
        >>> last_template_handler(["doublet", "es" , "directo", "notext=1"], "en")
        '<i>directo</i>'
        >>> last_template_handler(["doublet", "en" , "advoke", "avouch", "avow"], "en")
        'Doublet of <i>advoke</i>, <i>avouch</i> and <i>avow</i>'
        >>> last_template_handler(["doublet", "ja" , "tr1=Mosukō", "モスコー", "nocap=1"], "en")
        'doublet of <i>モスコー</i> (<i>Mosukō</i>)'
        >>> last_template_handler(["doublet", "ja" , "ヴィエンヌ", "tr1=Viennu", "t1=Vienne", "ウィーン", "tr2=Wīn"], "en")
        'Doublet of <i>ヴィエンヌ</i> (<i>Viennu</i>, “Vienne”) and <i>ウィーン</i> (<i>Wīn</i>)'
        >>> last_template_handler(["doublet", "ru" , "ру́сский", "tr1=rúkij", "t1=R", "g1=m", "pos1=n", "lit1=R"], "en")
        'Doublet of <i>ру́сский</i> <i>m</i> (<i>rúkij</i>, “R”, n, literally “R”)'

        >>> last_template_handler(["suffix", "en", "do", "ing"], "en")
        '<i>do</i>&nbsp;+&nbsp;<i>-ing</i>'
        >>> last_template_handler(["prefix", "en", "un", "do"], "en")
        '<i>un-</i>&nbsp;+&nbsp;<i>do</i>'
        >>> last_template_handler(["suffix", "en", "toto", "lala", "t1=t1", "tr1=tr1", "alt1=alt1", "pos1=pos1" ], "en")
        '<i>alt1</i> (<i>tr1</i>, “t1”, pos1)&nbsp;+&nbsp;<i>-lala</i>'
        >>> last_template_handler(["prefix", "en", "toto", "lala", "t1=t1", "tr1=tr1", "alt1=alt1", "pos1=pos1" ], "en")
        '<i>alt1-</i> (<i>tr1-</i>, “t1”, pos1)&nbsp;+&nbsp;<i>lala</i>'
        >>> last_template_handler(["suffix", "en", "toto", "lala", "t2=t2", "tr2=tr2", "alt2=alt2", "pos2=pos2" ], "en")
        '<i>toto</i>&nbsp;+&nbsp;<i>-alt2</i> (<i>-tr2</i>, “t2”, pos2)'
        >>> last_template_handler(["prefix", "en", "toto", "lala", "t2=t2", "tr2=tr2", "alt2=alt2", "pos2=pos2" ], "en")
        '<i>toto-</i>&nbsp;+&nbsp;<i>alt2</i> (<i>tr2</i>, “t2”, pos2)'
        >>> last_template_handler(["confix", "en", "neuro", "genic"], "en")
        '<i>neuro-</i>&nbsp;+&nbsp;<i>-genic</i>'
        >>> last_template_handler(["confix", "en", "neuro", "gene", "tr2=genic"], "en")
        '<i>neuro-</i>&nbsp;+&nbsp;<i>-gene</i> (<i>-genic</i>)'
        >>> last_template_handler(["confix", "en", "be", "dew", "ed"], "en")
        '<i>be-</i>&nbsp;+&nbsp;<i>dew</i>&nbsp;+&nbsp;<i>-ed</i>'
        >>> last_template_handler(["compound", "fy", "fier", "lj", "t1=far", "t2=leap", "pos1=adj", "pos2=v"], "en")
        '<i>fier</i> (“far”, adj)&nbsp;+&nbsp;<i>lj</i> (“leap”, v)'
        >>> last_template_handler(["blend", "he", "תַּשְׁבֵּץ", "tr1=tashbéts", "t1=crossword", "חֵץ", "t2=arrow", "tr2=chets"], "en")  # noqa
        'Blend of <i>תַּשְׁבֵּץ</i> (<i>tashbéts</i>, “crossword”)&nbsp;+&nbsp;<i>חֵץ</i> (<i>chets</i>, “arrow”)'
        >>> last_template_handler(["blend", "en"], "en")
        'Blend'
        >>> last_template_handler(["blend", "en", "notext=1", "scratch", "t1=money", "bill", "alt2=bills", ""], "en")
        '<i>scratch</i> (“money”)&nbsp;+&nbsp;<i>bills</i>'

        >>> last_template_handler(["l", "cs", "háček"], "en")
        'háček'
        >>> last_template_handler(["l", "en", "go", "went"], "en")
        'went'
        >>> last_template_handler(["l", "en", "God be with you"], "en")
        'God be with you'
        >>> last_template_handler(["l", "la", "similis", "t=like"], "en")
        'similis (“like”)'
        >>> last_template_handler(["l", "la", "similis", "", "like"], "en")
        'similis (“like”)'
        >>> last_template_handler(["l", "mul", "☧", ""], "en")
        '☧'
        >>> last_template_handler(["l", "ru", "ру́сский", "", "Russian", "g=m"], "en")
        'ру́сский <i>m</i> (<i>russkij</i>, “Russian”)'
        >>> last_template_handler(["link", "en", "water vapour"], "en")
        'water vapour'
        >>> last_template_handler(["ll", "en", "cod"], "en")
        'cod'

        >>> last_template_handler(["m", "en", "more"], "en")
        '<b>more</b>'
        >>> last_template_handler(["m", "enm", "us"], "en")
        '<i>us</i>'
        >>> last_template_handler(["m", "ine-pro", "*h₁ed-", "t=to eat"], "en")
        '<i>*h₁ed-</i> (“to eat”)'
        >>> last_template_handler(["m", "ar", "عِرْق", "", "root"], "en")
        '<i>عِرْق</i> (<i>ʿrq</i>, “root”)'
        >>> last_template_handler(["m", "pal", "tr=ˀl'k'", "ts=erāg", "t=lowlands"], "en")
        "(<i>ˀl'k'</i>, <i>/erāg/</i>, “lowlands”)"
        >>> last_template_handler(["m", "ar", "عَرِيق", "", "deep-rooted"], "en")
        '<i>عَرِيق</i> (<i>ʿrīq</i>, “deep-rooted”)'

        >>> last_template_handler(["label", "en" , "Australia", "slang", "nocat=1"], "en")
        '<i>(Australia, slang)</i>'
        >>> last_template_handler(["lb", "en" , "Australia"], "en")
        '<i>(Australia)</i>'
        >>> last_template_handler(["lb", "en" , "Australia", "or", "foobar"], "en")
        '<i>(Australia or foobar)</i>'
        >>> last_template_handler(["lb", "en" , "foobar", "and", "Australia", "or", "foobar"], "en")
        '<i>(foobar and Australia or foobar)</i>'
        >>> last_template_handler(["lb", "en" , "foobar", "_", "Australia", "foobar"], "en")
        '<i>(foobar Australia, foobar)</i>'
        >>> # last_template_handler(["lb", "en" , "roa-lor"], "en")
        >>> # '<i>(Lorrain)</i>'
        >>> last_template_handler(["lbl", "en" , "transitive"], "en")
        '<i>(transitive)</i>'

        >>> last_template_handler(["place", "en", "A country in the Middle East"], "en")
        'A country in the Middle East'
        >>> last_template_handler(["place", "en", "A country", "modern=Iraq"], "en")
        'A country; modern Iraq'
        >>> last_template_handler(["place", "en", "village", "co/Fulton County", "s/Illinois"], "en")
        'a village in Fulton County, Illinois'
        >>> last_template_handler(["place", "en", "city/county seat", "co/Lamar County", "s/Texas"], "en")
        'a city, the county seat of Lamar County, Texas'
        >>> last_template_handler(["place", "en", "small town/and/unincorporated community"], "en")
        'a small town and unincorporated community'
        >>> last_template_handler(["place", "en", "town", "s/New York", ";", "named after Paris"], "en")
        'a town in New York; named after Paris'
        >>> last_template_handler(["place", "en", "s"], "en")
        'a state'
        >>> last_template_handler(["place", "en", "state", "c/USA"], "en")
        'a state of the United States'
        >>> last_template_handler(["place", "en", "city", "c/Republic of Ireland"], "en")
        'a city in Ireland'
        >>> last_template_handler(["place", "en", "city", "s/Georgia", "c/United States"], "en")
        'a city in Georgia, United States'

        >>> last_template_handler(["standard spelling of", "en", "from=Irish English", "Irish Traveller"], "en")
        '<i>Irish English standard spelling of</i> <b>Irish Traveller</b>.'
        >>> last_template_handler(["standard spelling of", "en", "enroll"], "en")
        '<i>Standard spelling of</i> <b>enroll</b>.'

        >>> last_template_handler(["surname", "en"], "en")
        '<i>A surname.</i>'
        >>> last_template_handler(["surname", "en", "nodot=1"], "en")
        '<i>A surname</i>'
        >>> last_template_handler(["surname", "en", "rare"], "en")
        '<i>A rare surname.</i>'
        >>> last_template_handler(["surname", "en", "A=An", "occupational"], "en")
        '<i>An occupational surname.</i>'
        >>> last_template_handler(["surname", "en", "from=Latin", "dot=,"], "en")
        '<i>A surname,</i>'
    """
    from itertools import zip_longest

    from .langs import langs
    from .places import (
        recognized_placetypes,
        recognized_placenames,
        recognized_qualifiers,
        placetypes_aliases,
    )
    from ...transliterator import transliterate
    from ...user_functions import (
        capitalize,
        concat,
        extract_keywords_from,
        italic,
        lookup_italic,
        strong,
        term,
    )

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl in ("alt form", "alternative form of"):
        res = italic("Alternative form of")
        word = parts[1] if len(parts) > 1 else data.get("2", "")
        res += f" {strong(word)}"
        if data["t"]:
            res += f" (“{data['t']}”)"
        if data["pos"]:
            res += f" ({data['pos']})"
        return res

    # Short path for the {{m|en|WORD}} template
    if tpl == "m" and len(parts) == 2 and parts[0] == "en" and not data:
        return strong(parts[1])

    if tpl in (
        "bor",
        "cog",
        "der",
        "etyl",
        "inh",
        "l",
        "link",
        "ll",
        "mention",
        "m",
        "noncog",
    ):
        mentions = ("l", "link", "ll", "mention", "m")
        if tpl not in ("cog", "etyl", "noncog", *mentions):
            parts.pop(0)  # Remove the destination language

        dst_locale = parts.pop(0)

        if tpl == "etyl":
            parts.pop(0)

        lang = langs.get(dst_locale, "")
        phrase = lang if tpl not in mentions else ""

        if parts:
            word = parts.pop(0)

        if word == "-":
            return phrase

        word = data["alt"] or word
        gloss = data["t"] or data["gloss"]

        if parts:
            word = parts.pop(0) or word  # 4, alt=

        trans = ""
        if tpl in ("bor", *mentions):
            if phrase:
                phrase += " "
            if tpl in ("l", "link", "ll"):
                phrase += word
            elif word:
                phrase += italic(word)
            if data["g"]:
                phrase += f" {italic(data['g'])}"
            trans = transliterate(dst_locale, word)
        elif word:
            phrase += f" {italic(word)}"

        if parts:
            gloss = parts.pop(0)  # 5, t=, gloss=

        local_phrase = []
        if data["tr"]:
            local_phrase.append(f"{italic(data['tr'])}")
        if data["ts"]:
            local_phrase.append(f"{italic('/' + data['ts'] + '/')}")
        if trans:
            local_phrase.append(f"{italic(trans)}")
        if gloss:
            local_phrase.append(f"“{gloss}”")
        if data["lit"]:
            local_phrase.append(f"{'literally “' + data['lit'] + '”'}")
        if local_phrase:
            phrase += " ("
            phrase += concat(local_phrase, ", ")
            phrase += ")"

        return phrase.lstrip()

    def add_dash(tpl: str, index: int, parts_count: int, chunk: str) -> str:
        if tpl in ["prefix", "confix"] and i == 1:
            chunk += "-"
        if tpl == "suffix" and i == 2:
            chunk = "-" + chunk
        if tpl == "confix" and i == parts_count:
            chunk = "-" + chunk
        return chunk

    compound = ["af", "affix", "prefix", "suffix", "confix", "compound", "blend"]
    with_start_text = ["doublet", "piecewise doublet", "blend"]
    if tpl in ["doublet", "piecewise doublet", *compound]:
        lang = parts.pop(0)  # language code
        phrase = ""
        if data["notext"] != "1" and tpl in with_start_text:
            starter = tpl
            if parts:
                starter += " of "
            phrase = starter if data["nocap"] else starter.capitalize()
        a_phrase = []
        i = 1
        parts_count = len(parts)
        while parts:
            si = str(i)
            chunk = parts.pop(0)
            chunk = data["alt" + si] or chunk
            chunk = add_dash(tpl, i, parts_count, chunk)
            if not chunk:
                continue
            chunk = italic(chunk)
            if data["g" + si]:
                chunk += " " + italic(data["g" + si])
            local_phrase = []
            if data["tr" + si]:
                result = data["tr" + si]
                result = add_dash(tpl, i, parts_count, result)
                local_phrase.append(italic(result))
            if data["t" + si]:
                local_phrase.append(f"{'“' + data['t'+si] + '”'}")
            if data["pos" + si]:
                local_phrase.append(data["pos" + si])
            if data["lit" + si]:
                local_phrase.append(f"{'literally “' + data['lit'+si] + '”'}")
            if local_phrase:
                chunk += " (" + concat(local_phrase, ", ") + ")"
            a_phrase.append(chunk)
            i += 1

        sep = ", "
        last_sep = " and "
        if tpl in compound:
            sep = "&nbsp;+&nbsp;"
            last_sep = sep

        phrase += concat(a_phrase, sep, last_sep)
        return phrase

    if tpl in ("label", "lb", "lbl"):
        if len(parts) == 2:
            return term(parts[1])

        res = ""
        for word1, word2 in zip_longest(parts[1:], parts[2:]):
            if word1 in ("_", "and", "or"):
                continue

            res += lookup_italic(word1, locale)

            if word2 == "_":
                res += " "
            elif word2 == "and":
                res += " and "
            elif word2 == "or":
                res += " or "
            elif word2:
                res += ", "

        return term(res.rstrip(", "))

    if tpl == "place":
        parts.pop(0)  # Remove the language
        phrase = ""
        i = 1
        parts_count = len(parts)
        while parts:
            si = str(i)
            part = parts.pop(0)
            subparts = part.split("/")
            if i == 1:
                no_article = False
                for j, subpart in enumerate(subparts):
                    if subpart == "and":
                        phrase = phrase[:-2] + " and"
                        no_article = True
                        continue
                    subpart = placetypes_aliases.get(subpart, subpart)
                    s = recognized_placetypes.get(subpart, {})
                    qualifier = ""
                    if not s:
                        q_array = subpart.split(" ")
                        qualifier = q_array[0]
                        if qualifier in recognized_qualifiers:
                            qualifier = recognized_qualifiers[qualifier]
                            subpart = " ".join(q_array[1:])
                        else:
                            qualifier = ""
                        subpart = placetypes_aliases.get(subpart, subpart)
                        s = recognized_placetypes.get(subpart, {})
                    if s:
                        phrase += "" if no_article else s["article"]
                        phrase += f" {qualifier}" if qualifier else ""
                        phrase += " " + s["display"]
                        no_article = False
                        if j == len(subparts) - 1:
                            phrase += f" {s['preposition']} " if parts else ""
                        else:
                            phrase += ", "
                    else:
                        phrase += part
            elif len(subparts) > 1:
                phrase += ", " if i > 2 else ""
                subpart = subparts[0]
                subpart = placetypes_aliases.get(subpart, subpart)
                placename_key = subpart + "/" + subparts[1]
                placename = recognized_placenames.get(placename_key, {})
                if (
                    placename
                    and placename["display"]
                    and placename["display"] in recognized_placenames
                ):
                    placename_key = placename["display"]
                    placename = recognized_placenames[placename_key]
                if placename:
                    if placename["article"] and i < 3:
                        phrase += placename["article"] + " "
                    if placename["display"]:
                        phrase += placename["display"].split("/")[1]
                    else:
                        phrase += placename_key.split("/")[1]
                else:
                    phrase += subparts[1]
            elif part == ";":
                phrase += "; "
            else:
                phrase += part

            modern_key = "modern" + "" if i == 1 else si
            if data[modern_key]:
                phrase += "; modern " + data[modern_key]
            i += 1
        return phrase

    if tpl == "standard spelling of":
        if data["from"]:
            phrase = italic(f"{data['from']} {tpl}")
        else:
            phrase = italic("Standard spelling of")
        return f"{phrase} {strong(parts[1])}."

    if tpl == "surname":
        parts.pop(0)  # Remove the lang

        art = data["A"] or "A"
        dot = data["dot"] or ("" if data["nodot"] else ".")
        if not parts:
            return italic(f"{art} {tpl}{dot}")
        return italic(f"{art} {parts[0]} {tpl}{dot}")

    try:
        return f"{italic(capitalize(tpl))} {strong(parts[1])}"
    except IndexError:
        return capitalize(tpl)


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/en
release_description = """\
Words count: {words_count}
Wiktionary dump: {dump_date}

Installation:

1. Copy the [dicthtml-{locale}.zip <sup>:floppy_disk:</sup>]({url}) file into the `.kobo/custom-dict/` folder of the reader.
2. **Restart** the reader.

<sub>Updated on {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"
