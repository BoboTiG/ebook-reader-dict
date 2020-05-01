import os
from unittest.mock import patch

import pytest

os.environ["WIKI_LOCALE"] = "fr"

# Must be imported after *WIKI_LOCALE* is set
from scripts import __main__ as entry_point  # noqa


@patch("scripts.convert.main")
@patch("scripts.get.main")
def test_main_snapshot_up_to_date(mocked_get, mocked_convert):
    # https://docs.python.org/3/library/unittest.mock.html#nesting-patch-decorators
    mocked_get.return_value = 1
    mocked_convert.side_effect = RuntimeError  # To be sure this is not called
    assert entry_point.main([]) == 1
    assert mocked_get.called
    assert not mocked_convert.called


@patch("scripts.upload.main")
@patch("scripts.convert.main")
@patch("scripts.get.main")
@pytest.mark.parametrize(
    "args, called_get, called_convert, called_upload",
    [
        ([], True, True, False),
        (["--fetch-only"], True, False, False),
        (["--convert-only"], False, True, False),
        (["--update-release"], False, False, True),
    ],
)
def test_main_args(
    mocked_get,
    mocked_convert,
    mocked_upload,
    args,
    called_get,
    called_convert,
    called_upload,
):
    # https://docs.python.org/3/library/unittest.mock.html#nesting-patch-decorators
    mocked_get.return_value = 0
    mocked_convert.return_value = 0
    mocked_upload.return_value = 0
    entry_point.main(args)
    assert mocked_get.called is called_get
    assert mocked_convert.called is called_convert
    assert mocked_upload.called is called_upload


def test_get_word(capsys):
    # The word exists
    assert entry_point.main(["--get-word", "mutiner"]) == 0

    # The word does not exist
    assert entry_point.main(["--get-word", "mutinerssssssss"]) == 0
