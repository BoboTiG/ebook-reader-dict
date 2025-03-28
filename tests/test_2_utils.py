import pytest
import responses

from wikidict import constants, utils


@responses.activate
def test_convert_chem_error(caplog: pytest.LogCaptureFixture) -> None:
    responses.add(responses.POST, constants.WIKIMEDIA_URL_MATH_CHECK.format(type="chem"), status=404)
    utils.convert_chem("bad formula", "word")
    assert caplog.records[0].getMessage() == "<chem> ERROR with 'bad formula' in [word]"


@responses.activate
def test_convert_math_error(caplog: pytest.LogCaptureFixture) -> None:
    responses.add(responses.POST, constants.WIKIMEDIA_URL_MATH_CHECK.format(type="math"), status=404)
    utils.convert_math("bad formula", "word")
    assert caplog.records[0].getMessage() == "<math> ERROR with 'bad formula' in [word]"
