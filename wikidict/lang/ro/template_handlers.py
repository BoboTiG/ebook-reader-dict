from collections import defaultdict

from ...user_functions import extract_keywords_from, italic, strong


def render_forma_de(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_forma_de("forma de singular articulat pentru", ["aventurier"], defaultdict(str))
    '<i>forma de singular articulat pentru</i> <b>aventurier</b>'
    """
    return f"{italic(tpl)} {strong(parts[0])}"


def render_variant(tpl: str, parts: list[str], data: defaultdict[str, str], *, word: str = "") -> str:
    """
    >>> render_variant("adj form of", ["ro", "frumos", "", "m", "p"], defaultdict(str))
    'frumos'
    >>> render_variant("forma de vocativ singular pentru", ["a", "word"], defaultdict(str))
    'word'
    """
    return parts[1] if "adj form of" in tpl else parts[-1]


forma_de = (
    "forma de acuzativ feminin la plural pentru",
    "forma de articulat singular pentru",
    "forma de dativ feminin la plural pentru",
    "forma de dativ feminin la singular pentru",
    "forma de dativ-genitiv și de vocativ plural articulat pentru",
    "forma de enitiv-dativ singular articulat pentru",
    "forma de feminin neutru și plural pentru",
    "forma de feminin pentru",
    "forma de feminin plural pentru",
    "forma de feminin singular articulat pentru",
    "forma de feminin singular nearticulat în nominativ-acuzativ pentru",
    "forma de feminin singular nehotărât pentru",
    "forma de feminin singular pentru",
    "forma de feminin și neutru plural pentru",
    "forma de feminin și plural pentru",
    "forma de genitiv dativ singular pentru",
    "forma de genitiv singular articulat pentru",
    "forma de genitiv-dativ plural articulat pentru",
    "forma de genitiv-dativ singular articulat pentru",
    "forma de genitiv-dativ și vocativ plural articulat pentru",
    "forma de gerunziu pentru",
    "forma de maculin plural pentr",
    "forma de maculin plural pentru",
    "forma de mascuklin plural pentru",
    "forma de masculin feminin singular pentru",
    "forma de masculin plural pentru",
    "forma de masculin plural singular pentru",
    "forma de masculin pluralpentru",
    "forma de masculin plurl pentru",
    "forma de masculin și feminin plural genitiv-dativ pentru",
    "forma de masculin, neutru și feminin plural pentru",
    "forma de neutru plural pentru",
    "forma de nominativ-acuzativ plural articulat pentru",
    "forma de nominativ-acuzativ plural pentru",
    "forma de participiu pentru",
    "forma de participiu trecut pentru",
    "forma de persoana a I-a plural la conjunctiv prezent pentru",
    "forma de persoana a I-a plural la imperfect pentru",
    "forma de persoana a I-a plural la mai mult ca perfect pentru",
    "forma de persoana a I-a plural la perfect simplu pentru",
    "forma de persoana a I-a plural la prezent pentru",
    "forma de persoana a I-a singular la conjunctiv prezent pentru",
    "forma de persoana a I-a singular la imperfect pentru",
    "forma de persoana a I-a singular la mai mult ca perfect pentru",
    "forma de persoana a I-a singular la perfect simplu pentru",
    "forma de persoana a I-a singular la prezent pentru",
    "forma de persoana a II-a plural la conjunctiv prezent pentru",
    "forma de persoana a II-a plural la imperativ entru",
    "forma de persoana a II-a plural la imperativ pentru",
    "forma de persoana a II-a plural la imperfect pentru",
    "forma de persoana a II-a plural la mai mult ca perfect pentru",
    "forma de persoana a II-a plural la perfect simplu pentru",
    "forma de persoana a II-a plural la prezent pentru",
    "forma de persoana a II-a singular la conjunctiv prezent pentru",
    "forma de persoana a II-a singular la imperativ pentru",
    "forma de persoana a II-a singular la imperfect pentru",
    "forma de persoana a II-a singular la indicativ prezent pentru",
    "forma de persoana a II-a singular la mai mult ca perfect pentru",
    "forma de persoana a II-a singular la perfect simplu pentru",
    "forma de persoana a II-a singular la prezent indicativ pentru",
    "forma de persoana a II-a singular la prezent pentru",
    "forma de persoana a II-a singular la subjonctiv prezent pentru",
    "forma de persoana a III-a plural la conjunctiv prezent pentru",
    "forma de persoana a III-a plural la imperfect pentru",
    "forma de persoana a III-a plural la mai mult ca perfect pentru",
    "forma de persoana a III-a plural la perfect simplu pentru",
    "forma de persoana a III-a plural la prezent indicativ pentru",
    "forma de persoana a III-a plural la prezent pentru",
    "forma de persoana a III-a plural la timpul condițional-optativ pentru",
    "forma de persoana a III-a singular la conjunctiv prezent pentru",
    "forma de persoana a III-a singular la imperfect indicativ pentru",
    "forma de persoana a III-a singular la imperfect pentru",
    "forma de persoana a III-a singular la mai mult ca perfect pentru",
    "forma de persoana a III-a singular la perfect simplu pentru",
    "forma de persoana a III-a singular la perfect simplu pentru",
    "forma de persoana a III-a singular la prezent indicativ pentru",
    "forma de persoana a III-a singular la prezent pentru",
    "forma de persoana a III-a singular la timpul condițional-optativ pentru",
    "forma de plural articulat pentru",
    "forma de plural la feminin și neutru pentru",
    "forma de plural masculin pentru",
    "forma de plural nearticulat în nominativ-acuzativ și genitiv-dativ pentru",
    "forma de plural nearticulat pentru",
    "forma de plural neatriculat pentru",
    "forma de plural pentru",
    "forma de singulaar articulat pentru",
    "forma de singular articulat",
    "forma de singular articulat pentru",
    "forma de singular articulată pentru",
    "forma de singular nearticulat în genitiv-dativ pentru",
    "forma de singular nearticulat pentru",
    "forma de singular vocativ pentru",
    "forma de singular și plural genitiv nearticulat pentru",
    "forma de singulat articulat pentru",
    "forma de vocativ plural articulat pentru",
    "forma de vocativ plural pentru",
    "forma de vocativ singular articulat pentru",
    "forma de vocativ singular pentru",
)

template_mapping = {
    # **{fd: render_forma_de for fd in forma_de},
    #
    # Variants
    #
    "__variant__adj form of": render_variant,
    **{f"__variant__{fd}": render_variant for fd in forma_de},
}


def lookup_template(tpl: str) -> bool:
    return tpl in template_mapping


def render_template(word: str, template: tuple[str, ...]) -> str:
    tpl, *parts = template
    data = extract_keywords_from(parts)
    return template_mapping[tpl](tpl, parts, data, word=word)
