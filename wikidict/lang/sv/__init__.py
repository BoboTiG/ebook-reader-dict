"""Swedish language."""

import re

from ...user_functions import uniq

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
# https://sv.wiktionary.org/wiki/Wiktionary:Stilguide#Ordklassrubriken
head_sections = ("==svenska==", "svenska")
sections = (
    "adjektiv",
    "adverb",
    "affix",
    "artikel",
    "efterled",
    "förkortning",
    "förled",
    "interjektion",
    "konjunktion",
    "possessivt pronomen",
    "postposition",
    "prefix",
    "preposition",
    "pronomen",
    "substantiv",
    "suffix",
    "verb",
    "verbpartikel",
)

# Variants
variant_titles = (
    "adjektiv",
    "adverb",
    "substantiv",
    "verb",
)
variant_templates = (
    "{{avledning",
    "{{böjning",
)

# Some definitions are not good to keep (plural, gender, ... )
definitions_to_ignore = (
    #
    # Variants
    #
    "avledning",
    "böjning",
)

# Templates to ignore: the text will be deleted.
templates_ignored = (
    "?",
    "citat",
    "inget uppslag",
    "fakta",
    "källa-so",
    "konstr",
    "struktur",
    "sv-adj-alt-okomp",
    "synonymer",
)

# Templates that will be completed/replaced using italic style.
templates_italic = {
    "oböjl": "oböjligt",
    "oräkn": "oräknebart",
}

# Templates more complex to manage.
templates_multi = {
    # {{f}}
    "f": "italic('f')",
    # {{färg|#80FF80|light green}}
    "färg": "color(parts[1])",
    # {{fpl}}
    "fpl": "italic('f pl')",
    # {{ipa|/f/}}
    "ipa": "parts[-1]",
    # {{länk|sv|alfa, beta}}
    "länk": "parts[-1]",
    # {{länk-ar|عَنَى}}
    "länk-ar": "parts[-1]",
    # {{länka|etansyra}}
    "länka": "parts[1]",
    # {{led|sv|f|gata}}
    "led": "italic(('förled' if parts[2] == 'f' else 'efterled') + ' tillhörigt ordet') + ' ' + parts[-1]",
    # {{m}}
    "m": "italic('m')",
    # {{n}}
    "n": "italic('n')",
    # {{npl}}
    "npl": "italic('n pl')",
    # {{ö|en|test}}
    "ö": "parts[-1]",
    # {{ö+|en|test}}
    "ö+": "f\"{parts[-1]} {superscript('(' + parts[1] + ')')}\"",
    # {{ö-inte|en|test}}
    "ö-inte": "f\"{strong('inte')} {italic(strike(parts[-1]))}\"",
    # {{övrigatecken|kolon|:}}
    "övrigatecken": 'f\'"<code>{parts[-1].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</code>"\'',
    # {{övrigauppslagsord|n:te}}
    "övrigauppslagsord": "parts[-1]",
    # {{p}}
    "p": "italic('pl')",
    # {{u}}
    "u": "italic('u')",
    # {{uttal|sv|ipa=mɪn}}
    "uttal": "f\"{strong('uttal:')} /{parts[-1].lstrip('ipa=')}/\"",
    #
    # Variants
    #
    # {{böjning|sv|subst|boll}}
    "böjning": "parts[-1]",
}

# Templates that will be completed/replaced using custom style.
templates_other = {
    "=": "=",
    "dödform": "†",
}

_gammalstavning = {
    "aa": "genom rättskrivningsreformen 1948",
    "auh": "genom rättskrivningsreformen 1996",
    "äe": "genom rättskrivningsreformen 1996",
    "dl": "genom rättskrivningsreformen 1948",
    "dt": "genom stavningsreformen 1906",
    "eä": "genom sjätte upplagan av SAOL (1889)",
    "f": "genom stavningsreformen 1906",
    "ff": "genom rättskrivningsreformen 1996",
    "fv": "genom stavningsreformen 1906",
    "gk": "genom sjunde upplagan av SAOL (1900)",
    "hv": "genom stavningsreformen 1906",
    "ld": "genom rättskrivningsreformen 1948",
    "qv": "genom sjätte upplagan av SAOL (1889)",
    "sär": "genom rättskrivningsreformen 1996",
    "ss": "genom rättskrivningsreformen 1996",
    "th": "genom förenklingen under 1800-talet",
    "w": "vid övergången från fraktur till antikva",
    "wv": "genom övergången från fraktur till antikva",
    "zs": "genom stavningsreformen 1973",
}


# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/sv
release_description = """\
Ord räknas: {words_count}
Dumpa Wiktionary: {dump_date}

Full version:
{download_links_full}

Etymology-Free Version:
{download_links_noetym}

<sub>Uppdaterad på {creation_date}</sub>
"""

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"


def find_pronunciations(
    code: str,
    *,
    pattern: re.Pattern[str] = re.compile(r"{uttal\|sv\|(?:[^\|]+\|)?ipa=([^}|]+)}?\|?"),
) -> list[str]:
    """
    >>> find_pronunciations("")
    []
    >>> find_pronunciations("{{uttal|sv|ipa=eːn/, /ɛn/, /en}}")
    ['/eːn/, /ɛn/, /en/']
    >>> find_pronunciations("{{uttal|sv|ipa=en|uttalslänk=-|tagg=vissa dialekter}}")
    ['/en/']
    >>> find_pronunciations("{{uttal|sv|ipa=ɛn|uttalslänk=-}}")
    ['/ɛn/']
    """
    return [f"/{p}/" for p in uniq(pattern.findall(code))]


def last_template_handler(
    template: tuple[str, ...],
    locale: str,
    *,
    word: str = "",
    missed_templates: list[tuple[str, str]] | None = None,
) -> str:
    """
    Will be called in utils.py::transform() when all template handlers were not used.

        >>> last_template_handler(["foo"], "sv")
        '##opendoublecurly##foo##closedoublecurly##'

        >>> last_template_handler(["avledning", "sv", "tråkig"], "sv")
        'tråkig'
        >>> last_template_handler(["avledning", "sv", "seende", "adj"], "sv")
        'seende'
        >>> last_template_handler(["avledning", "sv", "mälta", "ordform=prespart"], "sv")
        'mälta'
        >>> last_template_handler(["avledning", "sv", "lada", "partikel=till", "ordform=perfpart"], "sv")
        'tillada'
        >>> last_template_handler(["avledning", "sv", "rikta", "partikel=in", "ordform=prespart"], "sv")
        'inrikta'
        >>> last_template_handler(["avledning", "sv", "beriktiga", "verb"], "sv")
        'beriktiga'
        >>> last_template_handler(["avledning", "sv", "bero", "prespart"], "sv")
        'bero'

        >>> last_template_handler(["belagt", "sv", "2025"], "sv")
        'Belagt i språket sedan 2025.'
        >>> last_template_handler(["belagt", "sv", "2025", "n"], "sv")
        'belagt i språket sedan 2025'
        >>> last_template_handler(["belagt", "sv", "2025", "nt"], "sv")
        'belagt i språket sedan 2025-talet'

        >>> last_template_handler(["gammalstavning", "sv", "fv", "brev"], "sv")
        '<i>(ålderdomligt) genom stavningsreformen 1906 ersatt av</i> brev'
        >>> last_template_handler(["gammalstavning", "sv", "m", "Dalarna"], "sv")
        '<i>(ålderdomligt) ersatt av</i> Dalarna'
        >>> last_template_handler(["gammalstavning", "ejtagg=1", "sv", "fv", "övergiva"], "sv")
        '<i>genom stavningsreformen 1906 ersatt av</i> övergiva'

        >>> last_template_handler(["härledning", "sv", "gmq-fsv", "nokot sin, nokon sin"], "sv")
        'fornsvenska <i>nokot sin, nokon sin</i>'
        >>> last_template_handler(["härledning", "sv", "grc", "ἱππόδρομος", "kapplöpningsbana, rännarbana"], "sv")
        'klassisk grekiska <i>ἱππόδρομος</i> (”kapplöpningsbana, rännarbana”)'
        >>> last_template_handler(["härledning", "sv", "grc", "ἱππόδρομος", "tr=hippodromos", "kapplöpningsbana, rännarbana"], "sv")
        'klassisk grekiska <i>ἱππόδρομος</i> (<i>hippodromos</i>, ”kapplöpningsbana, rännarbana”)'

        >>> last_template_handler(["kognat", "en", "hippodrome"], "sv")
        'engelska <i>hippodrome</i>'
        >>> last_template_handler(["kognat", "gmq-bot", "tíðend"], "sv")
        'okänt språk <i>tíðend</i>'

        >>> last_template_handler(["tagg", "historia", ""], "sv")
        '<i>(historia)</i>'
        >>> last_template_handler(["tagg", "biologi", "allmänt"], "sv")
        '<i>(biologi, allmänt)</i>'
        >>> last_template_handler(["tagg", "politik", "formellt", "språk=tyska"], "sv")
        '<i>(politik, formellt)</i>'
        >>> last_template_handler(["tagg", "kat=nedsättande", "text=något nedsättande"], "sv")
        '<i>(något nedsättande)</i>'
        >>> last_template_handler(["tagg", "text=substantivistiskt slutled", "samhällsvetenskap"], "sv")
        '<i>(samhällsvetenskap, substantivistiskt slutled)</i>'
        >>> last_template_handler(["tagg", "reflexivt"], "sv", word="försäga")
        '<i>(reflexivt: <b>försäga sig</b>)</i>'
        >>> last_template_handler(["tagg", "bildligt", "reflexivt"], "sv", word="etsa")
        '<i>(bildligt, reflexivt: <b>etsa sig</b>)</i>'

        >>> last_template_handler(["tr", "ru", "Пётр Ильи́ч Чайко́вский"], "sv")
        'Pjotr Iljítj Tjajkóvskij'

    """
    from ...user_functions import extract_keywords_from, italic, strong, term
    from .. import defaults
    from .langs import langs
    from .transliterator import transliterate

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl == "avledning":
        if len(parts) == 3:
            parts.pop(2)
        if data["partikel"]:
            # Delete superfluous letters (till + lada = tilllada, but we need tillada)
            return re.sub(r"(.)(?:\1){2,}", r"\1\1", f"{data['partikel']}{parts[-1]}")
        return parts[-1]

    if tpl == "belagt":
        year = parts[1]
        if len(parts) > 2:
            first_letter = "b"
            suffix = "-talet" if "t" in parts[2] else ""
        else:
            first_letter = "B"
            suffix = "."
        return f"{first_letter}elagt i språket sedan {year}{suffix}"

    if tpl == "gammalstavning":
        phrase = "" if data["ejtagg"] == "1" else "(ålderdomligt) "
        cat = f"{phrase}{_gammalstavning.get(parts[1], '')} ersatt av"
        return f"{italic(cat)} {parts[-1]}".replace("  ", " ")

    if tpl == "härledning":
        parts.pop(0)  # Remove the source lang
        phrase = langs[parts.pop(0)]
        phrase += f" {italic(parts.pop(0))}"
        if (tr := data["tr"]) or parts:
            phrase += " ("
            if tr:
                phrase += italic(tr)
            if parts:
                phrase += ", " if tr else ""
                phrase += f"”{parts.pop(0)}”"
            phrase += ")"
        return phrase

    if tpl == "kognat":
        return f"{langs[parts[0]]} {italic(parts[1])}"

    if tpl == "tagg":
        words = [
            f"{part}: {strong(f'{word} sig')}" if part == "reflexivt" else part
            for part in filter(lambda p: bool(p), parts)
        ]
        if data["text"]:
            words.append(data["text"])
        return term(", ".join(words))

    if tpl == "tr":
        return transliterate(parts[0], parts[1])

    return defaults.last_template_handler(template, locale, word=word, missed_templates=missed_templates)
