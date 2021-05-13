"""Norwegian language."""

# Regex to find the pronunciation
pronunciation = r""

# Float number separator
float_separator = ","

# Thousads separator
thousands_separator = " "

# Markers for sections that contain interesting text to analyse.
head_sections = ("norsk",)
section_sublevels = (3, 4)
etyl_section = ["Etymologi"]
sections = (
    *etyl_section,
    "Substantiv",
)

# Templates to ignore: the text will be deleted.
templates_ignored = ("",)

# Templates more complex to manage.
templates_multi = {
    "": "",
}

# Release content on GitHub
# https://github.com/BoboTiG/ebook-reader-dict/releases/tag/no
release_description = """\
Ord räknas: {words_count}
Dumpa Wiktionary: {dump_date}

Tillgängliga filer:

- [Kobo]({url_kobo}) (dicthtml-{locale}.zip)
- [StarDict]({url_stardict}) (dict-{locale}.zip)
- [DictFile]({url_dictfile}) (dict-{locale}.df)

<sub>Uppdaterad på {creation_date}</sub>
"""  # noqa

# Dictionary name that will be printed below each definition
wiktionary = "Wiktionary (ɔ) {year}"
