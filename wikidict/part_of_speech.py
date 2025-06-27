"""
Modifiers used to unifomize, and clean-up, POS (Part Of Speech).
"""

import re

# Clean-up POS using regexp(s), they are executed in order
PATTERNS = {
    "da": [
        # `{{verbum}}` → `verbum`
        re.compile(r"\{\{([^|}]+).*").sub,
        # `verbum 1` → `verbum`
        re.compile(r"([^\d]+).*").sub,
    ],
    "fr": [
        # `{{s|verbe|fr}}` → `verbe`
        re.compile(r"\{\{s\|([^|}]+).*").sub,
    ],
}

# Unifomize POS
MERGE = {
    "da": {
        "abbr": "forkortelsf",
        "abr": "forkortelsf",
        "ad": "adjektiv",
        "adj": "adjektiv",
        "adjektive": "adjektiv",
        "adv": "adverbium",
        "art": "artikel",
        "car-num": "mængdetal",
        "conj": "konjunktion",
        "dem-pronom": "demonstrativt pronomen",
        "end": "endelse",
        "frase": "sætning",
        "interj": "interjektion",
        "lyd": "lydord",
        "noun": "substantiv",
        "num": "talord",
        "part": "mærke",
        "pers-pronom": "personligt pronomen",
        "phr": "sætning",
        "possessivt pronomen (ejestedord)": "possessivt pronomen",
        "pp": "possessivt pronomen",
        "pref": "prefix",
        "prep": "præposition",
        "pron": "pronomen",
        "prop": "proprium",
        "prov": "ordsprog",
        "seq-num": "ordenstal",
        "substantivisk ordforbindelse": "substantiv",
        "symb": "symbol",
        "ubest-pronon": "ubestemt pronomen",
        "verb": "verbum",
    }
}
