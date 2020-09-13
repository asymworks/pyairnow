import pytest

from aiohttp import ClientSession
from pyairnow import WebServiceAPI
from pyairnow.errors import AirNowError, EmptyResponseError, InvalidJsonError, \
    InvalidKeyError

from .mock_api import MOCK_API_KEY


@pytest.mark.asyncio
async def test_api_not_authenticated(mock_airnowapi):
    client = WebServiceAPI('')
    with pytest.raises(InvalidKeyError) as exc_info:
        await client.forecast.zipCode(90001)
        assert 'not authenticated' in str(exc_info.value)


@pytest.mark.asyncio
async def test_api_invalid_key(mock_airnowapi):
    client = WebServiceAPI('123ABC')
    with pytest.raises(InvalidKeyError) as exc_info:
        await client.forecast.zipCode(90001)
        assert 'Invalid API key' in str(exc_info.value)


@pytest.mark.asyncio
async def test_api_bad_json(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.raises(InvalidJsonError) as exc_info:
        await client.forecast.zipCode('bad_json')


@pytest.mark.asyncio
async def test_api_bad_json_2(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.raises(InvalidJsonError) as exc_info:
        await client.forecast.zipCode('dict')


@pytest.mark.asyncio
async def test_api_empty_response(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.raises(EmptyResponseError) as exc_info:
        await client.forecast.zipCode('empty')


@pytest.mark.asyncio
async def test_api_unexpected_error(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.raises(AirNowError) as exc_info:
        await client.forecast.zipCode('error')
        assert 'Client Error' in str(exc_info.value)


@pytest.mark.asyncio
async def test_api_unexpected_error_1(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.raises(AirNowError) as exc_info:
        await client.forecast.zipCode('error1')
        assert 'Internal Server Error' in str(exc_info.value)


@pytest.mark.asyncio
async def test_api_unexpected_error_2(mock_airnowapi):
    client = WebServiceAPI(MOCK_API_KEY)
    with pytest.raises(AirNowError) as exc_info:
        await client.forecast.zipCode('error2')
        assert 'Internal Server Error' in str(exc_info.value)
