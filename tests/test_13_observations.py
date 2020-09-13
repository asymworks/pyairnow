import datetime
import pytest

from aiohttp import ClientSession
from pyairnow import WebServiceAPI

from .mock_api import MOCK_API_KEY


@pytest.mark.asyncio
async def test_api_observations_zipcode(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.observations.zipCode(90001)

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'observation'
    assert data[0]['mode'] == 'zipCode'
    assert data[0]['when'] == 'current'

    assert 'zipCode' in data[0]['query']
    assert data[0]['query']['zipCode'] == '90001'


@pytest.mark.asyncio
async def test_api_observations_zipcode_distance(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.observations.zipCode(90001, distance=100)

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'observation'
    assert data[0]['mode'] == 'zipCode'
    assert data[0]['when'] == 'current'

    assert 'zipCode' in data[0]['query']
    assert data[0]['query']['zipCode'] == '90001'

    assert 'distance' in data[0]['query']
    assert data[0]['query']['distance'] == '100'


@pytest.mark.asyncio
async def test_api_observations_ll(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.observations.latLong(34.053718, -118.244842)

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'observation'
    assert data[0]['mode'] == 'latLong'
    assert data[0]['when'] == 'current'

    assert 'latitude' in data[0]['query']
    assert data[0]['query']['latitude'] == '34.053718'
    assert 'longitude' in data[0]['query']
    assert data[0]['query']['longitude'] == '-118.244842'


@pytest.mark.asyncio
async def test_api_observations_ll_distance(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.observations.latLong(
        34.053718, -118.244842,
        distance=120
    )

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'observation'
    assert data[0]['mode'] == 'latLong'
    assert data[0]['when'] == 'current'

    assert 'latitude' in data[0]['query']
    assert data[0]['query']['latitude'] == '34.053718'
    assert 'longitude' in data[0]['query']
    assert data[0]['query']['longitude'] == '-118.244842'

    assert 'distance' in data[0]['query']
    assert data[0]['query']['distance'] == '120'
