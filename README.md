# eBook Reader Dictionaries

[![Update dictionaries](https://github.com/BoboTiG/ebook-reader-dict/actions/workflows/auto-updates.yml/badge.svg)](https://github.com/BoboTiG/ebook-reader-dict/actions/workflows/auto-updates.yml)
[![Update locale-specific data](https://github.com/BoboTiG/ebook-reader-dict/actions/workflows/auto-update-data.yml/badge.svg)](https://github.com/BoboTiG/ebook-reader-dict/actions/workflows/auto-update-data.yml)
[![Word of the day](https://github.com/BoboTiG/ebook-reader-dict/actions/workflows/daily.yml/badge.svg)](https://github.com/BoboTiG/ebook-reader-dict/actions/workflows/daily.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Features

- (*Kobo devices only*) When selecting a plural word, **its singular form** will be displayed.
- (*Kobo devices only*) When selecting a conjugated verb, **its infinitive version** will be displayed.
- (*Kobo devices only*) When a word is the plural form of another, and also a form of a verb, **all versions** are displayed.
- If a word contains **several pronunciations, or genders**, all are available.
- **Chemical formulas** are converted to SVG.
- **Mathematic formulas** are converted to SVG.
- **Hieroglyphs** are supported.
- **Tables** are supported.

## Downloads

1. <small>`[CA]`</small> [Catalan](../../releases/tag/ca)
1. <small>`[DA]`</small> [Danish](../../releases/tag/da)
1. <small>`[DE]`</small> [German](../../releases/tag/de)
1. <small>`[EL]`</small> [Greek](../../releases/tag/el)
1. <small>`[EN]`</small> [English](../../releases/tag/en)
1. <small>`[EO]`</small> [Esperanto](../../releases/tag/eo)
1. <small>`[ES]`</small> [Spanish](../../releases/tag/es)
1. <small>`[FR]`</small> [French](../../releases/tag/fr) ([news](https://www.mobileread.com/forums/showthread.php?t=330223&page=2))
1. <small>`[IT]`</small> [Italian](../../releases/tag/it)
1. <small>`[NO]`</small> [Norway](../../releases/tag/no)
1. <small>`[PT]`</small> [Portuguese](../../releases/tag/pt)
1. <small>`[RO]`</small> [Romanian](../../releases/tag/ro)
1. <small>`[RU]`</small> [Russian](../../releases/tag/ru)
1. <small>`[SV]`</small> [Swedish](../../releases/tag/sv)

## Installation

### Kobo

Copy the dictionary inside the `.kobo/custom-dict/` folder on your eBook reader.

## Development

Set up a virtual environment:

```bash
python3.13 -m venv venv

# For Linux and Mac users
. venv/bin/activate

# For Windows users
. venv/Scripts/activate
```

Install, or update, dependencies:

```bash
python -m pip install -U pip
python -m pip install -r requirements-tests.txt
```

Run tests:

```bash
# All tests
python -m pytest --doctest-modules wikidict tests

# Skip those requiring a working internet connection
python -m pytest --doctest-modules wikidict tests -m "not webtest"
```

Run linters, and quality checkers, before submitting a pull-request:

```bash
./check.sh
```

## Contributors 💖

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-15-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Thanks go to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="16.66%"><a href="https://www.tiger-222.fr"><img src="https://avatars.githubusercontent.com/u/2033598?v=4?s=100" width="100px;" alt="Mickaël Schoentgen"/><br /><sub><b>Mickaël Schoentgen</b></sub></a><br /><a href="https://github.com/BoboTiG/ebook-reader-dict/issues?q=author%3ABoboTiG" title="Bug reports">🐛</a> <a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=BoboTiG" title="Code">💻</a> <a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=BoboTiG" title="Documentation">📖</a> <a href="#projectManagement-BoboTiG" title="Project Management">📆</a></td>
      <td align="center" valign="top" width="16.66%"><a href="http://lasconic.com"><img src="https://avatars0.githubusercontent.com/u/234271?v=4?s=100" width="100px;" alt="Nicolas Froment"/><br /><sub><b>Nicolas Froment</b></sub></a><br /><a href="https://github.com/BoboTiG/ebook-reader-dict/issues?q=author%3Alasconic" title="Bug reports">🐛</a> <a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=lasconic" title="Code">💻</a> <a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=lasconic" title="Documentation">📖</a> <a href="#projectManagement-lasconic" title="Project Management">📆</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/atti84it"><img src="https://avatars.githubusercontent.com/u/817905?v=4?s=100" width="100px;" alt="Attilio"/><br /><sub><b>Attilio</b></sub></a><br /><a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=atti84it" title="Code">💻</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/chopinesque"><img src="https://avatars.githubusercontent.com/u/10416842?v=4?s=100" width="100px;" alt="chopinesque"/><br /><sub><b>chopinesque</b></sub></a><br /><a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=chopinesque" title="Code">💻</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/ilius"><img src="https://avatars.githubusercontent.com/u/197648?v=4?s=100" width="100px;" alt="Saeed Rasooli"/><br /><sub><b>Saeed Rasooli</b></sub></a><br /><a href="#infra-ilius" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/Moonbase59"><img src="https://avatars.githubusercontent.com/u/3706922?v=4?s=100" width="100px;" alt="Matthias C. Hormann"/><br /><sub><b>Matthias C. Hormann</b></sub></a><br /><a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=Moonbase59" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/tjaderxyz"><img src="https://avatars.githubusercontent.com/u/81907?v=4?s=100" width="100px;" alt="tjader"/><br /><sub><b>tjader</b></sub></a><br /><a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=tjaderxyz" title="Code">💻</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/victornove"><img src="https://avatars.githubusercontent.com/u/10910369?v=4?s=100" width="100px;" alt="Victor"/><br /><sub><b>Victor</b></sub></a><br /><a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=victornove" title="Code">💻</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/drkoll"><img src="https://avatars.githubusercontent.com/u/128939759?v=4?s=100" width="100px;" alt="John Koll"/><br /><sub><b>John Koll</b></sub></a><br /><a href="#translation-drkoll" title="Translation">🌍</a></td>
      <td align="center" valign="top" width="16.66%"><a href="http://www.linkedin.com/in/martamalberti/"><img src="https://avatars.githubusercontent.com/u/129286939?v=4?s=100" width="100px;" alt="Marta Malberti"/><br /><sub><b>Marta Malberti</b></sub></a><br /><a href="#translation-MartaMalb" title="Translation">🌍</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/g1r0"><img src="https://avatars.githubusercontent.com/u/17737200?v=4?s=100" width="100px;" alt="Arsenii Chaplinskii"/><br /><sub><b>Arsenii Chaplinskii</b></sub></a><br /><a href="#translation-g1r0" title="Translation">🌍</a></td>
      <td align="center" valign="top" width="16.66%"><a href="http://and4po.github.io"><img src="https://avatars.githubusercontent.com/u/94716615?v=4?s=100" width="100px;" alt="Ander Romero"/><br /><sub><b>Ander Romero</b></sub></a><br /><a href="#translation-and4po" title="Translation">🌍</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="16.66%"><a href="http://blog.yue-dongchen.xyz"><img src="https://avatars.githubusercontent.com/u/38829129?v=4?s=100" width="100px;" alt="Dongchen Yue &#124; 岳东辰"/><br /><sub><b>Dongchen Yue &#124; 岳东辰</b></sub></a><br /><a href="#translation-yue-dongchen" title="Translation">🌍</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://larssonjohan.com"><img src="https://avatars.githubusercontent.com/u/13087841?v=4?s=100" width="100px;" alt="Johan Larsson"/><br /><sub><b>Johan Larsson</b></sub></a><br /><a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=jolars" title="Code">💻</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/kyxap"><img src="https://avatars.githubusercontent.com/u/3080529?v=4?s=100" width="100px;" alt="kyxap"/><br /><sub><b>kyxap</b></sub></a><br /><a href="https://github.com/BoboTiG/ebook-reader-dict/commits?author=kyxap" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Stars ✨

<picture>
  <source
    media="(prefers-color-scheme: dark)"
    srcset="
      https://api.star-history.com/svg?repos=BoboTIG/ebook-reader-dict&type=Date&theme=dark
    "
  />
  <source
    media="(prefers-color-scheme: light)"
    srcset="
      https://api.star-history.com/svg?repos=BoboTIG/ebook-reader-dict&type=Date
    "
  />
  <img
    alt="Star History Chart"
    src="https://api.star-history.com/svg?repos=BoboTIG/ebook-reader-dict&type=Date"
  />
</picture>
