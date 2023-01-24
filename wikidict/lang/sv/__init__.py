"""Swedish language."""
import re
from typing import List, Pattern, Tuple

from ...user_functions import uniq

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
# https://sv.wiktionary.org/wiki/Wiktionary:Stilguide#Ordklassrubriken
head_sections = ("==Svenska==", "svenska")
sections = (
    "Adjektiv",
    "Adverb",
    "Affix",
    "Artikel",
    "Efterled",
    "Förkortning",
    "Förled",
    "Interjektion",
    "Konjunktion",
    "Possessivt pronomen",
    "Postposition",
    "Prefix",
    "Preposition",
    "Pronomen",
    "Substantiv",
    "Suffix",
    "Verbpartikel",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "?",
    "citat",
    "inget uppslag",
    "struktur",
    "synonymer",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "oböjl": "oböjligt",
    "oräkn": "oräknebart",
}

# Templates more complex to manage.
templates_multi = {
    # {{böjning|sv|subst|boll}}
    "böjning": "italic('böjningsform av') + ' ' + parts[-1]",
    # {{färg|#80FF80|light green}}
    "färg": "color(parts[1])",
    # {{länka|etansyra}}
    "länka": "parts[1]",
    # {{led|sv|f|gata}}
    "led": "italic(('förled' if parts[2] == 'f' else 'efterled') + ' tillhörigt ordet') + ' ' + parts[-1]",
    # {{n}}
    "n": "italic('n')",
    # {{ö|en|test}}
    "ö": "parts[-1]",
    # {{ö+|en|test}}
    "ö+": "f\"{parts[-1]} {superscript('(' + parts[1] + ')')}\"",
    # {{ö-inte|en|test}}
    "ö-inte": "f\"{strong('inte')} {italic(strike(parts[-1]))}\"",
    # {{uttal|sv|ipa=mɪn}}
    "uttal": "f\"{strong('uttal:')} /{parts[-1].lstrip('ipa=')}/\"",
}

# Templates that will be completed/replaced using custom style.
templates_other = {
    "dödform": "†",
}


_avledning = {
    "aktpart": "aktiv particip",
    "passpart": "passiv particip",
    "perfpart": "perfektparticip",
    "presger": "presens gerundium",
    "prespart": "presensparticip",
    "prespartakt": "presens particip aktiv",
    "prespartpass": "presens particip passiv",
    "pretger": "preteritum gerundium",
    "pretpartakt": "preteritum particip aktiv",
    "pretpartpass": "preteritum particip passiv",
}

_gammalstavning = {
    "hv": "genom stavningsreformen 1906 ",
    "dt": "genom stavningsreformen 1906 ",
    "f": "genom stavningsreformen 1906 ",
    "fv": "genom stavningsreformen 1906 ",
    "eä": "genom sjätte upplagan av SAOL (1889) ",
    "gk": "genom sjunde upplagan av SAOL (1900) ",
    "w": "vid övergången från fraktur till antikva ",
    "aa": "genom rättskrivningsreformen 1948 ",
    "dl": "genom rättskrivningsreformen 1948 ",
    "ld": "genom rättskrivningsreformen 1948 ",
    "ss": "genom rättskrivningsreformen 1996 ",
    "ff": "genom rättskrivningsreformen 1996 ",
    "äe": "genom rättskrivningsreformen 1996 ",
    "sär": "genom rättskrivningsreformen 1996 ",
    "auh": "genom rättskrivningsreformen 1996 ",
    "zs": "genom stavningsreformen 1973 ",
}


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/sv
release_description = """\
Ord räknas: {words_count}
Dumpa Wiktionary: {dump_date}

Tillgängliga filer:

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Uppdaterad på {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_pronunciations(
    code: str,
    pattern: Pattern[str] = re.compile(r"{uttal\|sv\|(?:[^\|]+\|)?ipa=([^}]+)}"),
) -> List[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{uttal|sv|ipa=eːn/, /ɛn/, /en}}")
    ['/eːn/, /ɛn/, /en/']
    """
    return [f"/{p}/" for p in uniq(pattern.findall(code))]


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["foo"], "sv")
        '##opendoublecurly##foo##closedoublecurly##'

        >>> last_template_handler(["avledning", "sv", "tråkig"], "sv")
        '<i>avledning till</i> tråkig'
        >>> last_template_handler(["avledning", "sv", "seende", "adj"], "sv")
        '<i>avledning till adjektivet</i> seende'
        >>> last_template_handler(["avledning", "sv", "mälta", "ordform=prespart"], "sv")
        '<i>presensparticip av</i> mälta'
        >>> last_template_handler(["avledning", "sv", "lada", "partikel=till", "ordform=perfpart"], "sv")
        '<i>perfektparticip av</i> lada till <i>och</i> tillada'
        >>> last_template_handler(["avledning", "sv", "rikta", "partikel=in", "ordform=prespart"], "sv")
        '<i>presensparticip av</i> rikta in <i>och</i> inrikta'

        >>> last_template_handler(["gammalstavning", "fv", "brev"], "sv")
        '<i>genom stavningsreformen 1906 ersatt av</i> brev'
        >>> last_template_handler(["gammalstavning", "m", "Dalarna"], "sv")
        '<i>ersatt av</i> Dalarna'

        >>> last_template_handler(["tagg", "historia"], "sv")
        '<i>(historia)</i>'
        >>> last_template_handler(["tagg", "biologi", "allmänt"], "sv")
        '<i>(biologi, allmänt)</i>'
        >>> last_template_handler(["tagg", "politik", "formellt", "språk=tyska"], "sv")
        '<i>(politik, formellt)</i>'
        >>> last_template_handler(["tagg", "kat=nedsättande", "text=något nedsättande"], "sv")
        '<i>(något nedsättande)</i>'
        >>> last_template_handler(["tagg", "text=substantivistiskt slutled", "samhällsvetenskap"], "sv")
        '<i>(samhällsvetenskap, substantivistiskt slutled)</i>'

    """  # noqa
    from ...user_functions import extract_keywords_from, italic, term
    from ..defaults import last_template_handler as default

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "avledning":
        if not data["ordform"]:
            phrase = "avledning till"
            if len(parts) == 3:
                cat = parts.pop(2)
                phrase += " "
                phrase += (
                    "adjektivet"
                    if cat == "adj"
                    else "substantiv"
                    if cat == "subst"
                    else cat
                )
        else:
            phrase = _avledning[data["ordform"]] + " av"
        phrase = italic(phrase)

        if data["partikel"]:
            partikel = data["partikel"]
            phrase += f" {parts[-1]} {partikel} {italic('och')}"
            word = partikel + parts[-1]
            # Delete superfluous letters (till + lada = tilllada, but we need tillada)
            word = re.sub(r"(.)(?:\1){2,}", r"\1\1", word)
        else:
            word = parts[-1]

        return f"{phrase} {word}"

    if tpl == "gammalstavning":
        cat = _gammalstavning.get(parts[0], "") + "ersatt av"
        return f"{italic(cat)} {parts[-1]}"

    if tpl == "tagg":
        words = parts
        if data["text"]:
            words.append(data["text"])
        return term(", ".join(words))

    return default(template, locale, word=word)
