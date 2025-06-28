"""
Modifiers used to uniformize, and clean-up, POS (Part Of Speech).
"""

import re

# Clean-up POS using regexp(s), they are executed in order
PATTERNS = {
    "da": [
        # `{{verbum}}` → `verbum`
        re.compile(r"\{\{([^|}]+).*").sub,
        # `verbum 1` → `verbum`
        re.compile(r"([^\d]+)\s+.*").sub,
    ],
    "eo": [
        # `{{vortospeco|adverbo, vortgrupo|eo}}` → `adverbo, vortgrupo`
        re.compile(r"\{\{vortospeco\|([^|]+).*").sub,
        # `{{signifoj}}` → `signifoj`
        re.compile(r"\{\{([^}]+).*").sub,
    ],
    "es": {
        # `{{verbo transitivo|es|terciopersonal}}` → `verbo transitivo`
        re.compile(r"\{\{([^|}]+).*").sub,
        # `verbo transitivo` → `verbo`
        re.compile(r"([^\s]+)\s+.*").sub,
    },
    "fr": [
        # `{{s|verbe|fr}}` → `verbe`
        re.compile(r"\{\{s\|([^|}]+).*").sub,
    ],
    "it": [
        # `{{nome}}` → `nome`
        re.compile(r"\{\{([^}]+).*").sub,
    ],
}

# Uniformize POS
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
    },
    "en": {
        "adverbial phrase": "adverb",
        "prepositional phrase": "preposition",
        "verb form": "verb",
        "verb phrase": "verb",
    },
    "eo": {
        "adverbo, vortgrupo": "adverbo",
        "difinoj": "difino",
        "liternomo": "litero",
        "literoparo": "litero",
        "mallongigoj": "mallongigo",
        "signifoj": "signifo",
        "substantiva formo": "substantivo",
        "substantivo, vortgrupo": "substantivo",
        "verba formo": "verbo",
        "verbo, vortgrupo": "verbo",
    },
    "fr": {
        "abréviations": "abréviation",
        "adj": "adjectif",
        "adjectif démonstratif": "adjectif",
        "adjectif exclamatif": "adjectif",
        "adjectif indéfini": "adjectif",
        "adjectif interrogatif": "adjectif",
        "adjectif numéral": "adjectif",
        "adjectif possessif": "adjectif",
        "adjectif relatif": "adjectif",
        "adverbe interrogatif": "adverbe",
        "adverbe relatif": "adverbe",
        "article défini": "article",
        "article indéfini": "article",
        "article partitif": "article",
        "conjonction de coordination": "conjonction",
        "déterminant démonstratif": "déterminant",
        "locution-phrase": "phrase",
        "locution phrase": "phrase",
        "pronom démonstratif": "pronom",
        "pronom indéfini": "pronom",
        "pronom interrogatif": "pronom",
        "pronom personnel": "pronom",
        "pronom possessif": "pronom",
        "pronom relatif": "pronom",
    },
    "it": {
        "acron": "abbreviazione",
        "agg form": "aggettivo",
        "agg": "aggettivo",
        "art": "articolo",
        "avv": "avverbio",
        "cong": "congiunzione",
        "inter": "interiezione",
        "loc nom": "nome",
        "pref": "prefisso",
        "prep": "preposizione",
        "pron pos": "pronome",
        "sost form": "sostantivo",
        "sost": "sostantivo",
        "suff": "suffisso",
        "verb form": "verb",
    },
}
