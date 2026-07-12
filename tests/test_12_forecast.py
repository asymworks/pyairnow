import datetime
import pytest

from pyairnow import WebServiceAPI

from .mock_api import MOCK_API_KEY


@pytest.mark.asyncio
async def test_api_forecast_zipcode(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode(90001)

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]['DateIssue'] == '2020-09-01'
    assert data[0]['DateForecast'] == '2020-09-02'
    assert data[0]['ReportingArea'] == 'Los Angeles'
    assert data[0]['StateCode'] == 'CA'
    assert data[0]['ParameterName'] == 'O3'
    assert data[0]['AQI'] == 55
    assert data[0]['Category'] == {'Number': 2, 'Name': 'Moderate'}
    assert data[0]['ActionDay'] is False

    assert data[1]['ParameterName'] == 'PM2.5'
    assert data[1]['AQI'] == 42
    assert data[1]['Category'] == {'Number': 1, 'Name': 'Good'}


@pytest.mark.asyncio
async def test_api_forecast_zipcode_distance(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.warns(DeprecationWarning, match='distance parameter is deprecated'):
        data = await client.forecast.zipCode(90001, distance=100)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['ParameterName'] == 'O3'


@pytest.mark.asyncio
async def test_api_forecast_zipcode_date_str(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode(90001, date='2020-09-01')

    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_api_forecast_zipcode_date_date(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode(
        90001,
        date=datetime.date(2020, 9, 1)
    )

    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_api_forecast_zipcode_date_datetime(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.zipCode(
        90001,
        date=datetime.datetime(2020, 9, 1, 11, 45, 1)
    )

    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_api_forecast_ll(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.latLong(34.053718, -118.244842)

    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]['DateIssue'] == '2020-09-01'
    assert data[0]['DateForecast'] == '2020-09-02'
    assert data[0]['ReportingArea'] == 'Los Angeles'
    assert data[0]['StateCode'] == 'CA'
    assert data[0]['ParameterName'] == 'O3'
    assert data[0]['AQI'] == 55
    assert data[0]['Category'] == {'Number': 2, 'Name': 'Moderate'}


@pytest.mark.asyncio
async def test_api_forecast_ll_distance(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.warns(DeprecationWarning, match='distance parameter is deprecated'):
        data = await client.forecast.latLong(
            34.053718, -118.244842,
            distance=120
        )

    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_api_forecast_ll_date_str(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.latLong(
        34.053718, -118.244842,
        date='2020-09-01'
    )

    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_api_forecast_ll_date_date(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.latLong(
        34.053718, -118.244842,
        date=datetime.date(2020, 9, 1)
    )

    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_api_forecast_ll_date_datetime(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    data = await client.forecast.latLong(
        34.053718, -118.244842,
        date=datetime.datetime(2020, 9, 1, 11, 45, 0)
    )

    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_api_forecast_zipcode_raw_format(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY, legacy_format=False)
    data = await client.forecast.zipCode(90001)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['parameterName'] == 'OZONE'
    assert data[0]['aqi'] == 55
    assert data[0]['categoryName'] == 'Moderate'
    assert 'DateIssue' not in data[0]


@pytest.mark.asyncio
async def test_api_forecast_ll_raw_format(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY, legacy_format=False)
    data = await client.forecast.latLong(34.053718, -118.244842)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['parameterName'] == 'OZONE'
    assert data[0]['aqi'] == 55
    assert 'DateIssue' not in data[0]
