# https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution
"""Russian language."""
from typing import Tuple

# Regex pour trouver la prononciation
pronunciation = r"(?:transcriptions-ru.)(\w*)"
# TODO need to expand template for russian Произношение (rn just get stem)

# Regexp pour trouver le gender
gender = r"(?:{сущ.ru.)([fmnмжс])|(?:{сущ.ru.*\|)([fmnмжс])"
# https://ru.wiktionary.org/wiki/%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD:%D1%81%D1%83%D1%89-ru

# Séparateur des nombres à virgule
float_separator = ","

# Séparateur des milliers
thousands_separator = " "

# Titre des sections qui sont intéressantes à analyser.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_des_sections_de_types_de_mots
# Pour récupérer la liste complète des sections :
#     python -m wikidict fr --find-templates
# Ensuite il faudra purger la liste et il restera les sections ci-dessous.
# section_patterns = (r"\#", r"\*")
section_level = 1
section_sublevels = (3, 4)
head_sections = "{{-ru-}}"
etyl_section = ("Этимология",)

sections = (
    *etyl_section,
    "Значение",
    "Семантические свойства",
    "{{Значение}}",
    "{{Семантические свойства}}",
    "Морфологические и синтаксические свойства",
)

# Certaines définitions ne sont pas intéressantes à garder (pluriel, genre, ...)
# definitions_to_ignore = (
# Modèles spéciaux
# )

# Malgré tout, même si une définition est sur le point d'être ignorée (via definitions_to_ignore),
# alors ces mots seront tout de même conservés.
# https://fr.wikipedia.org/wiki/Pluriels_irr%C3%A9guliers_en_fran%C3%A7ais
# words_to_keep = ()

# Modèle à ignorer : le texte sera supprimé.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les/Bandeaux
# templates_ignored = ()

# Modèles qui seront remplacés par du texte italique.
# https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_tous_les_mod%C3%A8les
# templates_italic = {}

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
# templates_multi = {}

# Modèles qui seront remplacés par du texte personnalisé.
# templates_other = {}


def last_template_handler(
    template: Tuple[str, ...], locale: str, word: str = ""
) -> str:

    from .langs import langs
    from ..defaults import last_template_handler as default
    from .template_handlers import render_template, lookup_template

    if lookup_template(template[0]):
        return render_template(template)

    tpl, *parts = template

    # This is a country in the current locale
    if tpl in langs:
        return langs[tpl]

    return default(template, locale, word=word)


# Contenu de la release sur GitHub :
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ru
release_description = """\
Количество слов : {words_count}
Экспорт Викисловаря : {dump_date}

Доступные файлы :

- [Kobo]({url_kobo}) (dicthtml-{locale}-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}-{locale}.df.bz2)

<sub>Обновлено по {creation_date}</sub>
"""  # noqa

# Le nom du dictionnaire qui sera affiché en-dessous de chaque définition
wiktionary = "Викисловарь (ɔ) {year}"
