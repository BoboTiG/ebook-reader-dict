# eBook Reader Dictionaries

Finally descent dictionaries based on [Wiktionary](https://www.wiktionary.org/) for your lovely Kobo.

## Dictionaries

![Update dictionaries](https://github.com/BoboTiG/ebook-reader-dict/workflows/Update%20dictionaries/badge.svg)

Note: small words (with less than 3 characters) and numbers are not included.

Latest versions can be downloaded just here:

- [Français](https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr)

## Updating Dictionaries

If you do not fin a word or if a translation is not good for you, there is nothing to do here.
Everything should be changed on [Wiktionary](https://www.wiktionary.org/) directly.

All dictionaries are automatically re-generated every Sunday at midnight.
The `dicthml-LOCALE.zip` file is updated inplace so that the download link never changes.

## Adding a new Dictionary

[Pull requests](https://github.com/BoboTiG/ebook-reader-dict/pulls) are very welcome. It is quite straithforward to add a new locale:

0. Keep everything alphabetically sorted please.
1. Copy the reference file [lang/fr.py](scripts/lang/fr.py) into `lang/$LOCALE.py`. And apply changes to fit the new locale.
2. Update [lang/\_\_init__.py](scripts/lang/__init__.py) accordingly.
3. Create **empty** files:
   - `data/$LOCALE/words.count`
   - `data/$LOCALE/words.list`
   - `data/$LOCALE/words.snapshot`

That's it!
