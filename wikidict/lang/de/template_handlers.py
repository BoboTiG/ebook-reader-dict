from collections import defaultdict  # noqa
from typing import Dict, List, Tuple

from ...user_functions import extract_keywords_from, italic
from .abk import abk

bibel_names = {
    "Gen": "Genesis",
    "1 Mos": "1. Buch Mose",
    "Ex": "Exodus",
    "2 Mos": "2. Buch Mose",
    "Lev": "Levitikus",
    "3 Mos": "3. Buch Mose",
    "Num": "Numeri",
    "4 Mos": "4. Buch Mose",
    "Dtn": "Deuteronomium",
    "5 Mos": "5. Buch Mose",
    "Jos": "Josua",
    "Ri": "Richter",
    "Rut": "Rut",
    "1 Sam": "1. Buch Samuel",
    "2 Sam": "2. Buch Samuel",
    "1 Kön": "1. Buch der Könige",
    "2 Kön": "2. Buch der Könige",
    "1 Chr": "1. Buch der Chronik",
    "2 Chr": "2. Buch der Chronik",
    "Esr": "Esra",
    "Neh": "Nehemia",
    "2 Esr": "2. Buch Esra ([[Nehemia]])",
    "Tob": "Tobit (Tobias)",
    "Jdt": "Judit",
    "Est": "Ester",
    "1 Makk": "1. Buch der Makkabäer",
    "2 Makk": "2. Buch der Makkabäer",
    "Ijob": "Ijob",
    "Ps": "Psalm",
    "Spr": "Sprichwörter",
    "Koh": "Kohelet",
    "Hld": "Hoheslied",
    "Weish": "Weisheit",
    "Sir": "Jesus Sirach",
    "Jes": "Jesaja",
    "Jer": "Jeremia",
    "Klgl": "Klagelieder",
    "Bar": "Baruch",
    "Ez": "Ezechiel",
    "Dan": "Daniel",
    "Hos": "Hosea",
    "Joel": "Joel",
    "Am": "Amos",
    "Obd": "Obadja",
    "Jona": "Jona",
    "Mi": "Micha",
    "Nah": "Nahum",
    "Hab": "Habakuk",
    "Zef": "Zefanja",
    "Hag": "Haggai",
    "Sach": "Sacharja",
    "Mal": "Maleachi",
    "Mt": "Matthäus",
    "Mk": "Markus",
    "Lk": "Lukas",
    "Joh": "Johannes",
    "Apg": "Apostelgeschichte",
    "Röm": "Römer",
    "1 Kor": "1. Korinther",
    "2 Kor": "2. Korinther",
    "Gal": "Galater",
    "Eph": "Epheser",
    "Phil": "Philipper",
    "Kol": "Kolosser",
    "1 Thess": "1. Thessalonicher",
    "2 Thess": "2. Thessalonicher",
    "1 Tim": "1. Timotheus",
    "2 Tim": "2. Timotheus",
    "Tit": "Titus",
    "Phlm": "Philemon",
    "Hebr": "Hebräer",
    "Jak": "Jakobus",
    "1 Petr": "1. Petrus",
    "2 Petr": "2. Petrus",
    "1 Joh": "1. Johannes",
    "2 Joh": "2. Johannes",
    "3 Joh": "3. Johannes",
    "Jud": "Judas",
    "Offb": "Offenbarung",
}


def render_bibel(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_bibel("Bibel", ["Mt", "1", "1"], defaultdict(str))
    'Matthäus 1,1'
    >>> render_bibel("Bibel", ["Mt", "1", "1-5", "HFA"], defaultdict(str))
    'Matthäus 1,1-5'
    >>> render_bibel("Bibel", ["Mt", "1", "1", "NIV"], defaultdict(str))
    'Matthäus 1,1'
    >>> render_bibel("Bibel", ["Mos", "18", "4", "LUT"], defaultdict(str))
    'Mos 18,4'
    """
    phrase = bibel_names.get(parts[0], parts[0])
    phrase += f" {parts[1]}"
    if len(parts) > 2:
        phrase += f",{parts[2]}"
    return phrase


no_commas = (
    "allg.",
    "allgemein",
    "ansonsten",
    "auch",
    "bei",
    "bes.",
    "besonders",
    "bis",
    "bisweilen",
    "das",
    "der",
    "die",
    "eher",
    "früher",
    "häufig",
    "hauptsächlich",
    "im",
    "in",
    "insbes.",
    "insbesondere",
    "leicht",
    "meist",
    "meistens",
    "mit",
    "mitunter",
    "noch",
    "noch in",
    "nur",
    "nur noch",
    "oder",
    "oft",
    "oftmals",
    "ohne",
    "respektive",
    "sehr",
    "seltener",
    "seltener auch",
    "sonst",
    "sowie",
    "später",
    "speziell",
    "teils",
    "teilweise",
    "über",
    "überwiegend",
    "und",
    "von",
    "vor allem",
    "vor allem in",
    "z. B.",
    "zum Beispiel",
    "z. T.",
    "zum Teil",
)


def render_K(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_K("K", ["Sport"], defaultdict(str))
    '<i>Sport:</i>'
    >>> render_K("K", ["trans."], defaultdict(str))
    '<i>transitiv:</i>'
    >>> render_K("K", ["trans.", "Linguistik", "Wortbildung"], defaultdict(str))
    '<i>transitiv, Linguistik, Wortbildung:</i>'
    >>> render_K("K", ["kPl.", "ugs."], defaultdict(str))
    '<i>kein Plural, umgangssprachlich:</i>'
    >>> render_K("K", ["Astronomie"], defaultdict(str, {"ft": "kurz für"}))
    '<i>Astronomie, kurz für:</i>'
    >>> render_K("K", ["intrans.", "Nautik"], defaultdict(str, {"t7": "_", "ft": "(von Schiffen)"}))
    '<i>intransitiv, Nautik (von Schiffen):</i>'
    >>> render_K("K", ["intrans.", "Nautik"], defaultdict(str, {"t7": "_", "ft": "(von Schiffen)"}))
    '<i>intransitiv, Nautik (von Schiffen):</i>'
    >>> render_K("K", ["test", "Nautik"], defaultdict(str, {"t1": "_"}))
    '<i>test Nautik:</i>'
    >>> render_K("K", ["landschaftlich", ""], defaultdict(str))
    '<i>landschaftlich:</i>'
    >>> render_K("K", ["Süddeutschland", "und", "Österreich", "sonst", "veraltete Schreibweise"], defaultdict(str))
    '<i>Süddeutschland und Österreich, sonst veraltete Schreibweise:</i>'
    """  # noqa
    conjonctions = ("oder", "respektive", "sowie", "und")
    conjonctions_start = (*conjonctions, *no_commas)
    phrase = ""
    parts = [p for p in parts if p]
    for i, p in enumerate(parts, start=1):
        t_index = f"t{i}"
        phrase += abk[p] if p in abk else p
        default_sep = ""
        if i != len(parts):
            default_sep = (
                ","
                if p not in conjonctions_start
                and i < len(parts)
                and parts[i] not in conjonctions
                else " "
            )
            sep = data.get(t_index, default_sep)
            if sep == "_":
                sep = " "
            elif sep.strip():
                sep = f"{sep} "
            phrase += sep

    ft = f"{data['ft']}" if "ft" in data else ""
    if ft:
        spacer = data.get("t7", ", ")
        if spacer == "_":
            spacer = " "
        ft = spacer + ft

    return italic(f"{phrase}{ft}:")


def render_Ut(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_Ut("Üt", ["grc", "διάλογος", "diálogos"], defaultdict(str))
    '<i>διάλογος (diálogos)</i>'
    >>> render_Ut("Üt", ["grc", "διαλέγομαι", "dialégesthai", "διαλέγεσθαι"], defaultdict(str))
    '<i>διαλέγεσθαι (dialégesthai)</i>'
    """
    parts.pop(0)  # language
    phrase = parts[0] if len(parts) < 3 else parts[2]
    if len(parts) > 1:
        phrase += f" ({parts[1]})"
    return italic(phrase)


def render_Uxx4(tpl: str, parts: List[str], data: Dict[str, str]) -> str:
    """
    >>> render_Uxx4("Üxx4", ["ar", "مسجد"], defaultdict(str, {"v":"مَسْجِد", "d":"masğid", "b":"Moschee"}))
    'مَسْجِد (DMG: masğid) ‚Moschee‘'
    >>> render_Uxx4("Üxx4", ["ur"], defaultdict(str, {"2": "فن", "v":"فَنّ", "d":"fann", "b":"Kunst"}))
    'فَنّ (ALA-LC: fann) ‚Kunst‘'
    >>> render_Uxx4("Üxx4", ["he", "שבת"], defaultdict(str, {"v":"שַׁבָּת", "d":"šabāṯ", "b":"Ruhepause"}))
    'שַׁבָּת (CHA: šabāṯ) ‚Ruhepause‘'
    >>> render_Uxx4("Üxx4", ["yi", "רעגן־בױגן"], defaultdict(str, {"d":"regn-boygn", "b":"Regenbogen"}))
    'רעגן־בױגן (YIVO: regn-boygn) ‚Regenbogen‘'
    >>> render_Uxx4("Üxx4", ["syr", "ܡܫܝܚܐ"], defaultdict(str, {"v":"ܡܫܺܝܚܳܐ", "d":"mšiḥāʾ", "b":"Messias"}))
    'ܡܫܺܝܚܳܐ (ALA-LC: mšiḥāʾ) ‚Messias‘'
    >>> render_Uxx4("Üxx4", ["fr", "ܡܫܝܚܐ"], defaultdict(str, {"v":"ܡܫܺܝܚܳܐ", "d":"mšiḥāʾ", "b":"Messias"}))
    'ܡܫܺܝܚܳܐ (mšiḥāʾ) ‚Messias‘'
    """
    language = parts.pop(0)
    phrase = parts.pop(0) if parts else ""
    phrase = data.get("v", data.get("2", phrase))
    if "d" in data:
        if language in ("ar", "fa", "ha", "ota", "pnb"):
            phrase += f" (DMG: {data['d']})"
        elif language in ("he"):
            phrase += f" (CHA: {data['d']})"
        elif language in ("yi"):
            phrase += f" (YIVO: {data['d']})"
        elif language in ("jrb", "ps", "syr", "ur"):
            phrase += f" (ALA-LC: {data['d']})"
        else:
            phrase += f" ({data['d']})"

    if "b" in data:
        phrase += f" ‚{data['b']}‘"
    return phrase


template_mapping = {
    "Bibel": render_bibel,
    "K": render_K,
    "Üt": render_Ut,
    "Üt?": render_Ut,
    "Üxx4": render_Uxx4,
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(template: Tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data)
