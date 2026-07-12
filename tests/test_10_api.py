import pytest

from aiohttp import ClientSession
from pyairnow import WebServiceAPI

from .mock_api import MOCK_API_KEY


@pytest.mark.asyncio
async def test_api(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode('90001')

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]['ParameterName'] == 'O3'
    assert data[0]['AQI'] == 55
    assert data[0]['Category']['Number'] == 2
    assert data[0]['Category']['Name'] == 'Moderate'


@pytest.mark.asyncio
async def test_api_with_session(mock_airnowapi):
    session = ClientSession()
    client = WebServiceAPI(MOCK_API_KEY, session=session)
    data = await client.forecast.zipCode(90001)

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]['ParameterName'] == 'O3'
    assert data[0]['AQI'] == 55

    await session.close()
