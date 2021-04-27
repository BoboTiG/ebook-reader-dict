from wikidict import get_word


def test_simple():
    # The word exists and contains subsublists.
    assert get_word.main("fr", "base") == 0


def test_word_of_the_day():
    assert get_word.main("fr", "") == 0


def test_subdefinitions():
    assert get_word.main("fr", "mesure") == 0


def test_raw():
    assert get_word.main("fr", "marron", raw=True) == 0


def test_word_with_variants():
    assert get_word.main("fr", "suis") == 0


def test_word_not_found():
    assert get_word.main("fr", "mutinerssssssss") == 0
