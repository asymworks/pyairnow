import pytest

from aiohttp import ClientSession
from pyairnow import WebServiceAPI

from .mock_api import MOCK_API_KEY


@pytest.mark.asyncio
async def test_api(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode('90001')

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'zipCode'
    assert data[0]['when'] is None

    assert 'zipCode' in data[0]['query']
    assert data[0]['query']['zipCode'] == '90001'


@pytest.mark.asyncio
async def test_api_with_session(mock_airnowapi):
    session = ClientSession()
    client = WebServiceAPI(MOCK_API_KEY, session=session)
    data = await client.forecast.zipCode(90001)

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'zipCode'
    assert data[0]['when'] is None

    assert 'zipCode' in data[0]['query']
    assert data[0]['query']['zipCode'] == '90001'
