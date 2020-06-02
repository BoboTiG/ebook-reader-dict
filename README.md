# eBook Reader Dictionaries

Finally descent dictionaries based on [Wiktionary](https://www.wiktionary.org/) for your lovely Kobo.

## Dictionaries

[![Update dictionaries](https://github.com/BoboTiG/ebook-reader-dict/workflows/Update%20dictionaries/badge.svg)](https://github.com/BoboTiG/ebook-reader-dict/actions?query=workflow%3A%22Update+dictionaries%22)

- [Catalan](https://github.com/BoboTiG/ebook-reader-dict/releases/tag/ca)
- [Français](https://github.com/BoboTiG/ebook-reader-dict/releases/tag/fr)

## Updating Dictionaries

If you do not fin a word or if a translation is not good for you, there is nothing to do here.
Everything should be changed on [Wiktionary](https://www.wiktionary.org/) directly.

All dictionaries are automatically re-generated **every day** at midnight. Your changes will likely be included in the next Wiktionary dump, so when it will come, at most 24h later the new dictionary will contain your stuff :)

The `dicthml-LOCALE.zip` file is updated inplace so that the download link never changes.

## Adding a new Dictionary

[Pull requests](https://github.com/BoboTiG/ebook-reader-dict/pulls) are very welcome. It is quite straithforward to add a new locale:

1. Copy the reference file [lang/fr.py](scripts/lang/fr.py) into `lang/$LOCALE.py`. And apply changes to fit the new locale.
2. Update [lang/\_\_init__.py](scripts/lang/__init__.py) accordingly.
3. Test it:
   ```shell
   # Install dependencies
   python -m pip install -r requirements.txt
   python -m pip install -r requirements-tests.txt

   # Run the command that will fetch the data and convert it into dicthtml-$LOCALE.zip
   # /!\ This command will take some time (from 15 to 45 minutes)
   python -m scripts --locale $LOCALE
4. Optional, but highly advisable: add [tests](tests/).

That's it! Thanks a lot for your contribution :heart:

---

When done, a maintainer will:

- Test on his/her side.
- Create a new release with the tag `$LOCALE`. This is where the dictionary will be uploaded.
- Update that [README](#) to include the new locale in the [Dictionaries](#Dictionaries) section.
  Keep it alphabetically sorted please, and use the original locale for the language name, not english.
