import datetime
import pytest

from pyairnow import WebServiceAPI

from .mock_api import MOCK_API_KEY


@pytest.mark.asyncio
async def test_api_forecast_zipcode(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode(90001)

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'zipCode'
    assert data[0]['when'] is None

    assert 'zipCode' in data[0]['query']
    assert data[0]['query']['zipCode'] == '90001'


@pytest.mark.asyncio
async def test_api_forecast_zipcode_distance(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode(90001, distance=100)

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'zipCode'
    assert data[0]['when'] is None

    assert 'zipCode' in data[0]['query']
    assert data[0]['query']['zipCode'] == '90001'

    assert 'distance' in data[0]['query']
    assert data[0]['query']['distance'] == '100'


@pytest.mark.asyncio
async def test_api_forecast_zipcode_date_str(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode(90001, date='2020-09-01')

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'zipCode'
    assert data[0]['when'] is None

    assert 'zipCode' in data[0]['query']
    assert data[0]['query']['zipCode'] == '90001'

    assert 'date' in data[0]['query']
    assert data[0]['query']['date'] == '2020-09-01'


@pytest.mark.asyncio
async def test_api_forecast_zipcode_date_date(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode(
        90001,
        date=datetime.date(2020, 9, 1)
    )

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'zipCode'
    assert data[0]['when'] is None

    assert 'zipCode' in data[0]['query']
    assert data[0]['query']['zipCode'] == '90001'

    assert 'date' in data[0]['query']
    assert data[0]['query']['date'] == '2020-09-01'


@pytest.mark.asyncio
async def test_api_forecast_zipcode_date_datetime(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode(
        90001,
        date=datetime.datetime(2020, 9, 1, 11, 45, 1)
    )

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'zipCode'
    assert data[0]['when'] is None

    assert 'zipCode' in data[0]['query']
    assert data[0]['query']['zipCode'] == '90001'

    assert 'date' in data[0]['query']
    assert data[0]['query']['date'] == '2020-09-01'


@pytest.mark.asyncio
async def test_api_forecast_ll(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.latLong(34.053718, -118.244842)

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'latLong'
    assert data[0]['when'] is None

    assert 'latitude' in data[0]['query']
    assert data[0]['query']['latitude'] == '34.053718'
    assert 'longitude' in data[0]['query']
    assert data[0]['query']['longitude'] == '-118.244842'


@pytest.mark.asyncio
async def test_api_forecast_ll_distance(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.latLong(
        34.053718, -118.244842,
        distance=120
    )

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'latLong'
    assert data[0]['when'] is None

    assert 'latitude' in data[0]['query']
    assert data[0]['query']['latitude'] == '34.053718'
    assert 'longitude' in data[0]['query']
    assert data[0]['query']['longitude'] == '-118.244842'

    assert 'distance' in data[0]['query']
    assert data[0]['query']['distance'] == '120'


@pytest.mark.asyncio
async def test_api_forecast_ll_date_str(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.latLong(
        34.053718, -118.244842,
        date='2020-09-01'
    )

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'latLong'
    assert data[0]['when'] is None

    assert 'latitude' in data[0]['query']
    assert data[0]['query']['latitude'] == '34.053718'
    assert 'longitude' in data[0]['query']
    assert data[0]['query']['longitude'] == '-118.244842'

    assert 'date' in data[0]['query']
    assert data[0]['query']['date'] == '2020-09-01'


@pytest.mark.asyncio
async def test_api_forecast_ll_date_date(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.latLong(
        34.053718, -118.244842,
        date=datetime.date(2020, 9, 1)
    )

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'latLong'
    assert data[0]['when'] is None

    assert 'latitude' in data[0]['query']
    assert data[0]['query']['latitude'] == '34.053718'
    assert 'longitude' in data[0]['query']
    assert data[0]['query']['longitude'] == '-118.244842'

    assert 'date' in data[0]['query']
    assert data[0]['query']['date'] == '2020-09-01'


@pytest.mark.asyncio
async def test_api_forecast_ll_date_datetime(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.latLong(
        34.053718, -118.244842,
        date=datetime.datetime(2020, 9, 1, 11, 45, 0)
    )

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]['type'] == 'forecast'
    assert data[0]['mode'] == 'latLong'
    assert data[0]['when'] is None

    assert 'latitude' in data[0]['query']
    assert data[0]['query']['latitude'] == '34.053718'
    assert 'longitude' in data[0]['query']
    assert data[0]['query']['longitude'] == '-118.244842'

    assert 'date' in data[0]['query']
    assert data[0]['query']['date'] == '2020-09-01'
