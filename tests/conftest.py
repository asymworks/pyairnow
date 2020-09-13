'''pyAirNow pytest Fixtures'''
import pytest
import re

from aioresponses import aioresponses

from .mock_api import mock_airnow_api


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.fixture
def mock_airnowapi(mock_aioresponse):
    url_pattern = re.compile(r'^http://www\.airnowapi\.org/(.*)$')
    mock_aioresponse.get(url_pattern, callback=mock_airnow_api)
