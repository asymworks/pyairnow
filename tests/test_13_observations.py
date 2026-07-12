import pytest

from pyairnow import WebServiceAPI

from .mock_api import MOCK_API_KEY


@pytest.mark.asyncio
async def test_api_observations_zipcode(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.observations.zipCode(90001)

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]['DateObserved'] == '2020-09-01'
    assert data[0]['HourObserved'] == 15
    assert data[0]['LocalTimeZone'] == 'PDT'
    assert data[0]['ReportingArea'] == 'Los Angeles'
    assert data[0]['ParameterName'] == 'PM2.5'
    assert data[0]['AQI'] == 55
    assert data[0]['Category'] == {'Number': 2, 'Name': 'Moderate'}

    assert data[1]['ParameterName'] == 'O3'
    assert data[1]['AQI'] == 42
    assert data[1]['Category'] == {'Number': 1, 'Name': 'Good'}


@pytest.mark.asyncio
async def test_api_observations_zipcode_distance(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.warns(DeprecationWarning, match='distance parameter is deprecated'):
        data = await client.observations.zipCode(90001, distance=100)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['ParameterName'] == 'PM2.5'


@pytest.mark.asyncio
async def test_api_observations_ll(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.observations.latLong(34.053718, -118.244842)

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]['DateObserved'] == '2020-09-01'
    assert data[0]['HourObserved'] == 15
    assert data[0]['LocalTimeZone'] == 'PDT'
    assert data[0]['ReportingArea'] == 'Los Angeles'
    assert data[0]['ParameterName'] == 'PM2.5'
    assert data[0]['AQI'] == 55
    assert data[0]['Category'] == {'Number': 2, 'Name': 'Moderate'}


@pytest.mark.asyncio
async def test_api_observations_ll_distance(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.warns(DeprecationWarning, match='distance parameter is deprecated'):
        data = await client.observations.latLong(
            34.053718, -118.244842,
            distance=120
        )

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['ParameterName'] == 'PM2.5'


@pytest.mark.asyncio
async def test_api_observations_zipcode_raw_format(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY, legacy_format=False)
    data = await client.observations.zipCode(90001)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['parameterName'] == 'PM2.5'
    assert data[0]['nowcastAQI'] == 55
    assert data[0]['aqiCategoryName'] == 'Moderate'
    assert 'DateObserved' not in data[0]


@pytest.mark.asyncio
async def test_api_observations_ll_raw_format(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY, legacy_format=False)
    data = await client.observations.latLong(34.053718, -118.244842)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['parameterName'] == 'PM2.5'
    assert data[0]['nowcastAQI'] == 55
    assert 'DateObserved' not in data[0]
