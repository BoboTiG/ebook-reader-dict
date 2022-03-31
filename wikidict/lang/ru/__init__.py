#https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution
"""Russian language."""
from typing import Tuple

# Regex pour trouver la prononciation
pronunciation = r"(?:transcriptions-ru.)(\w*)" #TODO need to expand template for russian Произношение (rn just get stem)

# Regexp pour trouver le gender
gender = r"(?:{сущ.ru.)([fmnмжс])|(?:{сущ.ru.*\|)([fmnмжс])" #works after applying filter to code via Морфологические и синтаксические свойства https://ru.wiktionary.org/wiki/%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD:%D1%81%D1%83%D1%89-ru

# Séparateur des nombres à virgule
float_separator = ","

# Séparateur des milliers
thousands_separator = " "

# Titre des sections qui sont intéressantes à analyser.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_des_sections_de_types_de_mots
# Pour récupérer la liste complète des sections :
#     python -m wikidict fr --find-templates
# Ensuite il faudra purger la liste et il restera les sections ci-dessous.
#section_patterns = (r"\#", r"\*")
section_level = 1
section_sublevels = (3,4)
head_sections = ("{{-ru-}}")
etyl_section = ("Этимология",)

sections = (
    *etyl_section,
    "Значение",
    "Семантические свойства",
    "{{Значение}}",
    "{{Семантические свойства}}",
    "Морфологические и синтаксические свойства"
)

# Certaines définitions ne sont pas intéressantes à garder (pluriel, genre, ...)
definitions_to_ignore = (
     # Modèles spéciaux
 )

# Malgré tout, même si une définition est sur le point d'être ignorée (via definitions_to_ignore),
# alors ces mots seront tout de même conservés.
# https://fr.wikipedia.org/wiki/Pluriels_irr%C3%A9guliers_en_fran%C3%A7ais
words_to_keep = (
)

# Modèle à ignorer : le texte sera supprimé.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les/Bandeaux
templates_ignored = (
)

# Modèles qui seront remplacés par du texte italique.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les
templates_italic = {
}

# Modèles un peu plus complexes à gérer, leur prise en charge demande plus de travail.
# Le code de droite sera passer à une fonction qui l'exécutera. Il est possible d'utiliser
# n'importe quelle fonction Python et celles définies dans user_functions.py.
#
# # Les arguments disponibles sont :
#   - *tpl* (texte) qui contient le nom du modèle.
#   - *parts* (liste de textes) qui contient les toutes parties du modèle.
#
# Exemple avec le modèle complet "{{comparatif de|bien|fr|adv}}" :
#   - *tpl* contiendra le texte "comparatif de".
#   - *parts* contiendra la liste ["comparatif de", "bien", "fr", "adv"].
#
# L'accès à *tpl* et *parts* permet ensuite de modifier assez aisément le résultat souhaité.
#
# Un documentation des fonctions disponibles se trouve dans le fichier HTML suivant :
#   html/wikidict/user_functions.html
templates_multi = {
}

# Modèles qui seront remplacés par du texte personnalisé.
templates_other = {
}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:
 
    from .langs import langs
    from ..defaults import last_template_handler as default
    from ...user_functions import (
        chinese,
        extract_keywords_from,
        italic,
        person,
        term,
    )
    from .template_handlers import render_template, lookup_template

    if lookup_template(template[0]):
        return render_template(template)

    tpl, *parts = template
    data = extract_keywords_from(parts)

    if tpl.startswith("Citation/"):
        parts = tpl.split("/")[1:]
        author = person(word, parts.pop(0).split(" ", 1))
        book = parts.pop(0) if parts else ""
        date = parts.pop(0) if parts else ""
        if "|" in date:
            date, page = date.split("|")
        else:
            page = ""
        if not date and not book:
            return author
        if not date:
            return italic(book)
        if not page:
            return f"{author}, {italic(book)}, {date}"
        return f"{author}, {italic(book)}, {date}, page {page}"

    if tpl == "Citation bloc":
        return f"<br/>«&nbsp;{parts[0]}&nbsp;»<br/>"

    if tpl == "code langue":
        lang = parts[0]
        for code, l10n in langs.items():
            if l10n == lang:
                return code
        return ""

    if tpl in ("ellipse", "par ellipse"):
        return (
            term("Par ellipse")
            if not data["de"]
            else f'{italic("(Ellipse de")} {data["de"]}{italic(")")}'
        )

    if tpl == "R:DAF6":
        w = parts[0] if parts else word
        return f"«&nbsp;{w}&nbsp;», dans <i>Dictionnaire de l’Académie française, sixième édition</i>, 1832-1835"

    if tpl == "R:TLFi":
        w = parts[0] if parts else word
        return f"«&nbsp;{w}&nbsp;», dans <i>TLFi, Le Trésor de la langue française informatisé</i>, 1971–1994"

    if tpl == "fr-verbe-flexion":
        return data.get("1", parts[0] if parts else "")

    if tpl.startswith(("fr-accord-", "fr-rég")):
        singular = data["s"] or data["ms"]
        if tpl == "fr-accord-eau":
            singular = parts[0] + "eau"
        elif tpl == "fr-accord-eux":
            singular = parts[0] + "eux"
        elif tpl == "fr-accord-mf-al":
            singular = parts[0] + "al"
        elif not singular:
            singular = word.rstrip("s")
        if data["inv"]:
            singular += f" {data['inv']}"
        return singular

    if tpl == "Légifrance":
        return data["texte"]

    if tpl in ("langue", "nom langue"):
        phrase = langs[parts[0]]
        if tpl == "langue":
            phrase = phrase[0].capitalize() + phrase[1:]
        return phrase

    if tpl in ("ar-mot", "ar-terme"):
        return f'<span style="line-height: 0px;"><span style="font-size:larger">{arabiser(parts[0])}</span></span> <small>({parts[0]})</small>'  # noqa
    if tpl == "ar-ab":
        return f'<span style="line-height: 0px;"><span style="font-size:larger">{arabiser(parts[0])}</span></span>'

    if tpl == "rouge":
        prefix_style = "background-" if data["fond"] == "1" else ""
        phrase = parts[0] if parts else data["texte"] or data["1"]
        return f'<span style="{prefix_style}color:red">{phrase}</span>'

    if tpl in ("Wikipedia", "Wikipédia", "wikipédia", "wp", "WP"):
        start = ""
        if parts:
            start = parts[1] if len(parts) > 1 else parts[0]
        elif word:
            start = word
        phrase = "sur l’encyclopédie Wikipédia"
        if data["lang"]:
            l10n = langs[data["lang"]]
            phrase += f" (en {l10n})"
        return f"{start} {phrase}" if start else phrase

    if tpl in ("zh-l", "zh-m"):
        return chinese(parts, data, laquo="«&nbsp;", raquo="&nbsp;»")

    # This is a country in the current locale
    if tpl in langs:
        return langs[tpl]

    return default(template, locale, word=word)


# Contenu de la release sur GitHub :
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr
release_description = """\
Nombre de mots : {words_count}
Export Wiktionnaire : {dump_date}

Fichiers disponibles :

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Mis à jour le {creation_date}</sub>
"""  # noqa

# Le nom du dictionnaire qui sera affiché en-dessous de chaque définition
wiktionary = "Wiktionnaire (ɔ) {year}"
