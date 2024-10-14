from pathlib import Path
from unittest.mock import patch

from wikidict import check_word, check_words, render


def test_errors() -> None:
    word_count = 39
    return_value = 42
    with patch.object(check_words, "local_check", return_value=return_value):
        assert check_words.main("fr", word_count, True, "", "") == return_value * word_count


def test_simple() -> None:
    with patch.object(check_word, "check_word", return_value=0):
        assert check_words.main("fr", 1, True, "", "") == 0


def test_get_words_to_tackle_no_json_file() -> None:
    with patch.object(render, "get_latest_json_file", return_value=None):
        assert not check_words.get_words_to_tackle("fr", count=1, is_random=True)


def test_get_words_to_tackle_all(tmp_path: Path) -> None:
    file = tmp_path / "test.json"
    file.write_text('{"base":""}')
    with patch.object(render, "get_latest_json_file", return_value=file):
        assert check_words.get_words_to_tackle("fr", count=-1) == ["base"]


def test_get_words_to_tackle_word_offset(tmp_path: Path) -> None:
    file = tmp_path / "test.txt"
    file.write_text("base\na\naa\nb")
    assert check_words.get_words_to_tackle("fr", offset="a", input_file=f"{tmp_path}/test.txt") == ["a", "aa", "b"]


def test_get_words_to_tackle_numeric_offset(tmp_path: Path) -> None:
    file = tmp_path / "test.txt"
    file.write_text("base\na\naa\nb\nc\nd\ne")
    assert check_words.get_words_to_tackle("fr", offset="5", input_file=f"{tmp_path}/test.txt") == ["d", "e"]


def test_get_words_to_tackle_random(tmp_path: Path) -> None:
    # Note using "letters" rather than "words", just to keep the test simple and try the logic.
    unwanted_letters = "abcd"
    wanted_letters = "efgh"
    all_letters = sorted(wanted_letters + unwanted_letters)

    file = tmp_path / "test.txt"
    file.write_text("\n".join(all_letters))

    picked_letters = check_words.get_words_to_tackle("fr", count=-1, is_random=True, input_file=f"{tmp_path}/test.txt")
    assert sorted(picked_letters) == all_letters


def test_get_words_to_tackle_random_with_count(tmp_path: Path) -> None:
    # Note using "letters" rather than "words", just to keep the test simple and try the logic.
    unwanted_letters = "abcd"
    wanted_letters = "efgh"
    all_letters = sorted(wanted_letters + unwanted_letters)

    file = tmp_path / "test.txt"
    file.write_text("\n".join(all_letters))

    picked_letters = check_words.get_words_to_tackle("fr", count=4, is_random=True, input_file=f"{tmp_path}/test.txt")
    assert any(letter in wanted_letters for letter in picked_letters)


def test_get_words_to_tackle_random_with_offset(tmp_path: Path) -> None:
    # Note using "letters" rather than "words", just to keep the test simple and try the logic.
    unwanted_letters = "abcd"
    wanted_letters = "efgh"
    all_letters = sorted(wanted_letters + unwanted_letters)

    file = tmp_path / "test.txt"
    file.write_text("\n".join(all_letters))

    picked_letters = check_words.get_words_to_tackle(
        "fr", is_random=True, offset="4", input_file=f"{tmp_path}/test.txt"
    )
    assert "".join(sorted(picked_letters)) == wanted_letters


def test_get_words_to_tackle_random_with_offset_and_count(tmp_path: Path) -> None:
    # Note using "letters" rather than "words", just to keep the test simple and try the logic.
    unwanted_letters = "abcd"
    wanted_letters = "efgh"
    all_letters = sorted(wanted_letters + unwanted_letters)

    file = tmp_path / "test.txt"
    file.write_text("\n".join(all_letters))

    picked_letters = check_words.get_words_to_tackle(
        "fr", count=1, is_random=True, offset="4", input_file=f"{tmp_path}/test.txt"
    )
    assert picked_letters[0] in wanted_letters
