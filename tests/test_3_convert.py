import os
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

import pytest
from marisa_trie import Trie

from wikidict import constants, convert
from wikidict.constants import ASSET_CHECKSUM_ALGO
from wikidict.stubs import Variants, Word, Words

EXPECTED_INSTALL_TXT_FR = """### 🌟 Afin d'être régulièrement mis à jour, ce projet a besoin de soutien ; [cliquez ici](https://github.com/BoboTiG/ebook-reader-dict/issues/2339) pour faire un don. 🌟

<br/>


Nombre de mots : 46
Export Wiktionnaire : 2020-12-17

Version complète :
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dictorg-fr-fr.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.mobi.zip)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-fr.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr.zip)

Version sans étymologies :
- [DICT.org](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dictorg-fr-fr-noetym.zip)
- [DictFile](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr-noetym.df.bz2)
- [Kindle](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr-noetym.mobi.zip)
- [Kobo](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dicthtml-fr-fr-noetym.zip)
- [StarDict](https://github.com/BoboTiG/ebook-reader-dict/releases/download/fr/dict-fr-fr-noetym.zip)

Mis à jour le"""

WORDS = {
    "empty": Word([], [], [], {}, []),
    "foo": Word(["pron"], ["gender"], ["etyl"], {"Noun": ["def 1", ("sdef 1",)]}, []),
    "foos": Word(["pron"], ["gender"], ["etyl"], {"Noun": ["def 1", ("sdef 1", ("ssdef 1",))]}, ["baz"]),
    "baz": Word(["pron"], ["gender"], ["etyl"], {"Noun": ["def 1", ("sdef 1",)]}, ["foobar"]),
    "empty1": Word([], [], [], {}, ["foo"]),
    "empty2": Word([], [], [], {}, ["empty1"]),
    "Multiple Etymologies": Word(
        ["pron"],
        ["gender"],
        ["etyl 1", ("setyl 1",)],
        {"Noun": ["def 1", ("sdef 1",)]},
        [],
    ),
    "Multiple Etymology": Word(
        ["pron0"],
        ["gender0"],
        ["etyl0"],
        {"Noun": ["def 0"]},
        ["Multiple Etymologies"],
    ),
    "GIF": Word(
        ["pron"],
        ["gender"],
        ["etyl"],
        {
            "Noun": [
                '<img style="height:100%;max-height:0.8em;width:auto;vertical-align:bottom"'
                ' src="data:image/gif;base64,R0lGODdhNwAZAIEAAAAAAP///wAAAAAAACwAAAAANwAZAE'
                "AIwwADCAwAAMDAgwgTKlzIUKDBgwUZFnw4cGLDihEvOjSYseFEigQtLhSpsaNGiSdTQgS5kiVG"
                "lwhJeuRoMuHHkDBH1pT4cKdKmSpjUjT50efGnEWTsuxo9KbQnC1TFp051KhNpUid8tR6EijPkC"
                "V3en2J9erLoBjRXl1qVS1amTWn6oSK1WfGpnjDQo1q1Wvbs125PgX5l6zctW1JFgas96/FxYwv"
                'RnQsODHkyXuPDt5aVihYt5pBr9woGrJktmpNfxUYEAA7"/>'
            ]
        },
        ["gif"],
    ),
}


def test_simple() -> None:
    assert convert.main("fr") == 0

    # Check for all dictionaries
    output_dir = Path(os.environ["CWD"]) / "data" / "fr" / "fr" / "output"

    # DictFile
    assert (output_dir / "dict-fr-fr.df").is_file()
    assert (output_dir / f"dict-fr-fr.df.{ASSET_CHECKSUM_ALGO}").is_file()
    assert (output_dir / "dict-fr-fr-noetym.df").is_file()
    assert (output_dir / f"dict-fr-fr-noetym.df.{ASSET_CHECKSUM_ALGO}").is_file()

    # DictFile bz2
    assert (output_dir / "dict-fr-fr.df.bz2").is_file()
    assert (output_dir / f"dict-fr-fr.df.bz2.{ASSET_CHECKSUM_ALGO}").is_file()
    assert (output_dir / "dict-fr-fr-noetym.df.bz2").is_file()
    assert (output_dir / f"dict-fr-fr-noetym.df.bz2.{ASSET_CHECKSUM_ALGO}").is_file()

    # DICT.org
    assert (output_dir / "dictorg-fr-fr.zip").is_file()
    assert (output_dir / f"dictorg-fr-fr.zip.{ASSET_CHECKSUM_ALGO}").is_file()
    assert (output_dir / "dictorg-fr-fr-noetym.zip").is_file()
    assert (output_dir / f"dictorg-fr-fr-noetym.zip.{ASSET_CHECKSUM_ALGO}").is_file()

    # Kobo
    assert (output_dir / "dicthtml-fr-fr-noetym.zip").is_file()
    assert (output_dir / f"dicthtml-fr-fr-noetym.zip.{ASSET_CHECKSUM_ALGO}").is_file()
    dicthtml = output_dir / "dicthtml-fr-fr.zip"
    assert dicthtml.is_file()
    assert (output_dir / f"dicthtml-fr-fr.zip.{ASSET_CHECKSUM_ALGO}").is_file()

    # Mobi
    assert (output_dir / "dict-fr-fr.mobi.zip").is_file()
    assert (output_dir / f"dict-fr-fr.mobi.zip.{ASSET_CHECKSUM_ALGO}").is_file()
    assert (output_dir / "dict-fr-fr-noetym.mobi.zip").is_file()
    assert (output_dir / f"dict-fr-fr-noetym.mobi.zip.{ASSET_CHECKSUM_ALGO}").is_file()

    # StarDict
    stardict = output_dir / "dict-fr-fr.zip"
    assert stardict.is_file()
    assert (output_dir / f"dict-fr-fr.zip.{ASSET_CHECKSUM_ALGO}").is_file()
    assert (output_dir / "dict-fr-fr-noetym.zip").is_file()
    assert (output_dir / f"dict-fr-fr-noetym.zip.{ASSET_CHECKSUM_ALGO}").is_file()

    # Check the Kobo ZIP content
    expected_files = [
        "11.html",
        constants.ZIP_INSTALL,
        "aa.html",
        "ac.html",
        "ba.html",
        "bo.html",
        "ch.html",
        "co.html",
        "de.html",
        "dj.html",
        "du.html",
        "ef.html",
        "em.html",
        "en.html",
        "ge.html",
        "gr.html",
        "gè.html",
        "ic.html",
        "ko.html",
        "mi.html",
        "mu.html",
        "na.html",
        "pi.html",
        "pr.html",
        "ra.html",
        "sa.html",
        "si.html",
        "sl.html",
        "su.html",
        "te.html",
        "tu.html",
        "ve.html",
        "words",
        constants.ZIP_WORDS_COUNT,
        constants.ZIP_WORDS_SNAPSHOT,
        "ép.html",
        "œc.html",
        "πa.html",
    ]
    expected_trie_keys = [
        "-aux",
        "-eresse",
        "42",
        "5E",
        "Bogotanais",
        "DES",
        "Slovène",
        "Turgeon",
        "a",
        "accueil",
        "acrologie",
        "barbe à papa",
        "base",
        "bath",
        "chacune",
        "colligeait",
        "colliger",
        "corollaires",
        "corps portant",
        "djed",
        "dubitatif",
        "effluve",
        "employer",
        "en",
        "encyclopædie",
        "geler",
        "greffier",
        "gèlent",
        "ich",
        "koro",
        "minute",
        "minuter",
        "minutes",
        "mutiner",
        "naguère",
        "pinyin",
        "précepte",
        "rance",
        "sapristi",
        "silicone",
        "suis",
        "tests-definitions",
        "venoient",
        "éperon",
        "œcuménique",
        "π",
    ]
    with ZipFile(dicthtml) as fh:
        assert sorted(fh.namelist()) == expected_files

        # testfile returns the name of the first corrupt file, or None
        errors = fh.testzip()
        assert errors is None

        # Check content of INSTALL.txt
        install_txt = fh.read(constants.ZIP_INSTALL).decode()
        print(install_txt)
        assert install_txt.startswith(EXPECTED_INSTALL_TXT_FR)

        # Check the trie
        trie = Trie()
        trie.map(fh.read("words"))
        assert sorted(trie.keys()) == expected_trie_keys

    # Check the StarDict ZIP content
    expected_files = [
        "dict-data.dict.dz",
        "dict-data.idx",
        "dict-data.ifo",
        "dict-data.syn",
        "res/db28a816.gif",
    ]
    with ZipFile(stardict) as fh:
        assert sorted(fh.namelist()) == expected_files

        # testfile returns the name of the first corrupt file, or None
        errors = fh.testzip()
        assert errors is None


def test_no_json_file() -> None:
    with patch.object(convert, "get_latest_json_file", return_value=None):
        assert convert.main("fr") == 1


@pytest.mark.dependency()
@pytest.mark.parametrize(
    "formatter, filename, include_etymology",
    [
        (convert.DictFileFormat, "dict-fr-fr.df", True),
        (convert.DictFileFormat, "dict-fr-fr-noetym.df", False),
        (convert.KoboFormat, "dicthtml-fr-fr.zip", True),
        (convert.KoboFormat, "dicthtml-fr-fr-noetym.zip", False),
    ],
)
def test_generate_primary_dict(formatter: type[convert.BaseFormat], filename: str, include_etymology: bool) -> None:
    output_dir = Path(os.environ["CWD"]) / "data" / "fr" / "fr"
    variants = convert.make_variants(WORDS)
    convert.run_formatter(
        formatter,
        "fr",
        output_dir,
        WORDS,
        variants,
        "20201218",
        include_etymology=include_etymology,
    )

    assert (output_dir / filename).is_file()


@pytest.mark.parametrize(
    "formatter, filename, include_etymology",
    [
        (convert.BZ2DictFileFormat, "dict-fr-fr.df.bz2", True),
        (convert.BZ2DictFileFormat, "dict-fr-fr-noetym.df.bz2", False),
        (convert.DictOrgFormat, "dictorg-fr-fr.zip", True),
        (convert.DictOrgFormat, "dictorg-fr-fr-noetym.zip", False),
        (convert.MobiFormat, "dict-fr-fr.mobi", True),
        (convert.MobiFormat, "dict-fr-fr-noetym.mobi", False),
        (convert.StarDictFormat, "dict-fr-fr.zip", True),
        (convert.StarDictFormat, "dict-fr-fr-noetym.zip", False),
    ],
)
@pytest.mark.dependency(
    depends=[
        "test_generate_primary_dict[DictFileFormat-dict-fr-fr.df]",
        "test_generate_primary_dict[DictFileFormat-dict-fr-fr-noetym.df]",
    ]
)
def test_generate_secondary_dict(formatter: type[convert.BaseFormat], filename: str, include_etymology: bool) -> None:
    output_dir = Path(os.environ["CWD"]) / "data" / "fr" / "fr"
    convert.run_formatter(
        formatter,
        "fr",
        output_dir,
        {},
        {},
        "20201218",
        include_etymology=include_etymology,
    )
    assert (output_dir / filename).is_file()


FORMATTED_WORD_KOBO = """\
<w><p><a name="Multiple Etymologies"/><b>Multiple Etymologies</b> pron <i>gender</i>.<br/><br/><b>Noun</b><ol><li>def 1</li><ol style="list-style-type:lower-alpha"><li>sdef 1</li></ol></ol><p>etyl 1</p><ol><li>setyl 1</li></ol><br/></p><var><variant name="multiple etymology"/></var></w>
"""
FORMATTED_WORD_KOBO_NO_ETYMOLOGY = """\
<w><p><a name="Multiple Etymologies"/><b>Multiple Etymologies</b> pron <i>gender</i>.<br/><br/><b>Noun</b><ol><li>def 1</li><ol style="list-style-type:lower-alpha"><li>sdef 1</li></ol></ol></p><var><variant name="multiple etymology"/></var></w>
"""
FORMATTED_WORD_DICTFILE = """\
@ Multiple Etymologies
: pron <i>gender</i>.
& Multiple Etymology
<html><b>Noun</b><ol><li>def 1</li><ol style="list-style-type:lower-alpha"><li>sdef 1</li></ol></ol><p>etyl 1</p><ol><li>setyl 1</li></ol><br/></html>\


"""
FORMATTED_WORD_DICTFILE_NO_ETYMOLOGY = """\
@ Multiple Etymologies
: pron <i>gender</i>.
& Multiple Etymology
<html><b>Noun</b><ol><li>def 1</li><ol style="list-style-type:lower-alpha"><li>sdef 1</li></ol></ol></html>\


"""


@pytest.mark.parametrize(
    "formatter, include_etymology, expected",
    [
        (convert.KoboFormat, True, FORMATTED_WORD_KOBO),
        (convert.KoboFormat, False, FORMATTED_WORD_KOBO_NO_ETYMOLOGY),
        (convert.DictFileFormat, True, FORMATTED_WORD_DICTFILE),
        (convert.DictFileFormat, False, FORMATTED_WORD_DICTFILE_NO_ETYMOLOGY),
    ],
)
def test_word_rendering(
    formatter: type[convert.BaseFormat],
    include_etymology: bool,
    expected: str,
) -> None:
    output_dir = Path(os.environ["CWD"]) / "data" / "fr" / "fr"
    cls = formatter(
        "fr",
        output_dir,
        WORDS,
        convert.make_variants(WORDS),
        "20221212",
        include_etymology=include_etymology,
    )

    content = next(cls.handle_word("Multiple Etymologies", WORDS))
    assert content == expected


WORDS_VARIANTS_FR = words = {
    "estre": Word(
        pronunciations=["\\ɛtʁ\\"],
        genders=[],
        etymology=[],
        definitions={"Verbe": ["Définition de 'estre'."]},
        variants=[],
    ),
    "être": Word(
        pronunciations=["\\ɛtʁ\\"],
        genders=["m"],
        etymology=[],
        definitions={
            "Verbe": [
                "Définition de 'être'.",
            ]
        },
        variants=[],
    ),
    "suis": Word(
        pronunciations=["\\sɥi\\"],
        genders=[],
        etymology=[],
        definitions={},
        variants=["suivre", "être", "estre"],
    ),
    "suivre": Word(
        pronunciations=["\\sɥivʁ\\"],
        genders=[],
        etymology=[],
        definitions={"Verbe": ["Définition de 'suivre'."]},
        variants=[],
    ),
}
WORDS_VARIANTS_ES = {
    "gastadan": Word(pronunciations=[], genders=[], etymology=[], definitions={}, variants=["gastada"]),
    "gastada": Word(pronunciations=[], genders=[], etymology=[], definitions={}, variants=["gastado"]),
    "gastado": Word(pronunciations=[], genders=[], etymology=[], definitions={}, variants=["gastar"]),
    "gastar": Word(
        pronunciations=[],
        genders=[],
        etymology=[],
        definitions={"Verb": ["Definition of 'gastar'."]},
        variants=[],
    ),
}


def test_make_variants() -> None:
    assert convert.make_variants(WORDS_VARIANTS_FR) == {"suivre": ["suis"], "estre": ["suis"], "être": ["suis"]}
    assert convert.make_variants(WORDS_VARIANTS_ES) == {
        "gastada": ["gastadan"],
        "gastado": ["gastada"],
        "gastar": ["gastado"],
    }


def test_kobo_format_variants_different_prefix(tmp_path: Path) -> None:
    words = WORDS_VARIANTS_FR
    variants = convert.make_variants(words)
    formatter = convert.KoboFormat("fr", tmp_path, words, variants, "20250322")

    assert formatter.make_groups(words) == {
        "es": {"estre": words["estre"]},
        "êt": {"être": words["être"]},
        "su": {"suis": words["suis"], "suivre": words["suivre"]},
    }

    estre = "".join(formatter.handle_word("estre", words))
    être = "".join(formatter.handle_word("être", words))
    suis = "".join(formatter.handle_word("suis", words))
    suivre = "".join(formatter.handle_word("suivre", words))
    assert suis.count('<a name="suis"/>') == 3
    assert "<b>estre</b>" in suis
    assert "<b>suivre</b>" in suis
    assert "<b>être</b>" in suis
    assert "variant" not in estre  # Because group prefixes are differents
    assert "variant" not in suis  # Because variant == word
    assert "variant" not in être  # Because group prefixes are differents
    assert '<var><variant name="suis"/></var>' in suivre  # Because group prefixes are the same


def test_kobo_format_variants_empty_variant_level_1(tmp_path: Path) -> None:
    words = WORDS_VARIANTS_ES
    variants = convert.make_variants(words)
    formatter = convert.KoboFormat("es", tmp_path, words, variants, "20250322")

    assert formatter.make_groups(words) == {
        "ga": {
            "gastada": words["gastada"],
            "gastadan": words["gastadan"],
            "gastado": words["gastado"],
            "gastar": words["gastar"],
        }
    }

    gastadan = "".join(formatter.handle_word("gastadan", words))
    gastada = "".join(formatter.handle_word("gastada", words))
    gastado = "".join(formatter.handle_word("gastado", words))
    gastar = "".join(formatter.handle_word("gastar", words))
    assert not gastadan
    assert not gastada
    assert not gastado
    assert '<var><variant name="gastada"/><variant name="gastado"/></var>' in gastar


def test_df_format(tmp_path: Path) -> None:
    words = WORDS_VARIANTS_FR
    variants = convert.make_variants(words)
    formatter = convert.DictFileFormat("fr", tmp_path, words, variants, "20250323")
    formatter.process()
    output = formatter.dictionary_file(formatter.output_file)

    assert (
        output.read_text(encoding="utf-8")
        == r"""@ estre
: \ɛtʁ\
<html><b>Verbe</b><ol><li>Définition de 'estre'.</li></ol></html>

@ être
: \ɛtʁ\ <i>m</i>.
<html><b>Verbe</b><ol><li>Définition de 'être'.</li></ol></html>

@ suis
: <b>estre</b> \ɛtʁ\
<html><b>Verbe</b><ol><li>Définition de 'estre'.</li></ol></html>

@ suis
: <b>suivre</b> \sɥivʁ\
<html><b>Verbe</b><ol><li>Définition de 'suivre'.</li></ol></html>

@ suis
: <b>être</b> \ɛtʁ\ <i>m</i>.
<html><b>Verbe</b><ol><li>Définition de 'être'.</li></ol></html>

@ suivre
: \sɥivʁ\
& suis
<html><b>Verbe</b><ol><li>Définition de 'suivre'.</li></ol></html>

"""
    )


def test_df_format_variants_different_prefix(tmp_path: Path) -> None:
    words = WORDS_VARIANTS_FR
    variants = convert.make_variants(words)
    formatter = convert.DictFileFormat("fr", tmp_path, words, variants, "20250323")

    estre = "".join(formatter.handle_word("estre", words))
    être = "".join(formatter.handle_word("être", words))
    suis = "".join(formatter.handle_word("suis", words))
    suivre = "".join(formatter.handle_word("suivre", words))
    assert suis.count("@ suis") == 3
    assert ": <b>estre</b>" in suis
    assert ": <b>suivre</b>" in suis
    assert ": <b>être</b>" in suis
    assert "&" not in estre  # Because group prefixes are differents
    assert "&" not in suis  # Because variant == word
    assert "&" not in être  # Because group prefixes are differents
    assert "& suis" in suivre  # Because group prefixes are the same


def test_df_format_variants_empty_variant_level_1(tmp_path: Path) -> None:
    words = WORDS_VARIANTS_ES
    variants = convert.make_variants(words)
    formatter = convert.DictFileFormat("es", tmp_path, words, variants, "20250323")

    gastadan = "".join(formatter.handle_word("gastadan", words))
    gastada = "".join(formatter.handle_word("gastada", words))
    gastado = "".join(formatter.handle_word("gastado", words))
    gastar = "".join(formatter.handle_word("gastar", words))
    assert not gastadan
    assert not gastada
    assert not gastado
    assert "& gastada" in gastar
    assert "& gastado" in gastar


@pytest.mark.parametrize(
    "locale, lang_src, lang_dst",
    [
        ("fr", "fr", "fr"),
        ("fro", "fr", "fro"),
        ("fr:fro", "fr", "fro"),
        ("fr:it", "fr", "it"),
        ("it:fr", "it", "fr"),
    ],
)
def test_sublang(locale: str, lang_src: str, lang_dst: str, tmp_path: Path) -> None:
    snapshot = "20250401"
    pages = Path(f"data-{snapshot}.json")
    words: Words = {}
    variants: Variants = {}

    with (
        patch.dict("os.environ", {"CWD": str(tmp_path)}),
        patch.object(convert, "get_latest_json_file") as mocked_gljf,
        patch.object(convert, "load") as mocked_l,
        patch.object(convert, "make_variants") as mocked_mv,
        patch.object(convert, "distribute_workload") as mocked_dw,
        patch.object(convert, "run_mobi_formatter") as mocked_rmf,
    ):
        mocked_gljf.return_value = pages
        mocked_l.return_value = words
        mocked_mv.return_value = variants
        source_dir = tmp_path / "data" / lang_dst / lang_src

        convert.main(locale)
        mocked_gljf.assert_called_once_with(source_dir)
        mocked_l.assert_called_once_with(pages)
        mocked_mv.assert_called_once_with(words)

        args = (source_dir / "output", pages, locale, words, variants)
        for include_etymology in [False, True]:
            mocked_dw.assert_any_call(convert.get_primary_formatters(), *args, include_etymology=include_etymology)
            mocked_dw.assert_any_call(convert.get_secondary_formatters(), *args, include_etymology=False)
            mocked_rmf.assert_any_call(*args, include_etymology=False)
        assert mocked_dw.call_count == 4
        assert mocked_rmf.call_count == 2
