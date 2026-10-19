'''Client to interact with AirNow Air Quality API'''
from json.decoder import JSONDecodeError
from typing import Optional, cast

from aiohttp import ClientResponse, ClientSession, ClientTimeout

from .errors import AirNowError, EmptyResponseError, InvalidJsonError, \
    InvalidKeyError
from .forecast import Forecast
from .observation import Observations

API_BASE_URL: str = 'https://www.airnowapi.org'
API_DEFAULT_TIMEOUT: int = 10


def _status_message(resp: ClientResponse) -> str:
    '''Describe an HTTP error status, e.g. "HTTP 504 Gateway Time-out"'''
    if resp.reason:
        return f'HTTP {resp.status} {resp.reason}'
    return f'HTTP {resp.status}'


class WebServiceAPI:
    '''Client to interact with AirNow API'''
    def __init__(
        self, api_key: str, *, session: Optional[ClientSession] = None,
        legacy_format: bool = True
    ) -> None:
        '''Initialize with Client Session and API Key'''
        self._api_key: Optional[str] = api_key
        self._session: Optional[ClientSession] = session

        self.forecast = Forecast(self._get, legacy_format=legacy_format)
        self.observations = Observations(self._get, legacy_format=legacy_format)

    async def _get(
        self, endpoint: str, *, base_url: str = API_BASE_URL, **kwargs
    ) -> list:
        '''Run a Request against the API'''
        kwargs.setdefault('params', {})
        kwargs['params']['API_KEY'] = self._api_key
        kwargs['params']['format'] = 'application/json'

        use_running_session = self._session and not self._session.closed

        session: ClientSession
        if use_running_session:
            session = cast(ClientSession, self._session)
        else:
            session = ClientSession(
                timeout=ClientTimeout(total=API_DEFAULT_TIMEOUT)
            )

        try:
            async with session.get(
                f'{base_url}/{endpoint}', **kwargs
            ) as resp:
                try:
                    data = await resp.json(content_type=None)
                except JSONDecodeError:
                    # An error status says more than the body, which is
                    # usually an HTML page from a proxy or gateway in front
                    # of the API.
                    if resp.status >= 400:
                        raise InvalidJsonError(_status_message(resp))

                    # The response can't be parsed as JSON, so we'll use its
                    # body text in an error:
                    response_text = await resp.text()
                    raise InvalidJsonError(response_text)

                # json() returns None for an empty body
                if data is None and resp.status >= 400:
                    raise InvalidJsonError(_status_message(resp))

        finally:
            if not use_running_session:
                await session.close()

        if isinstance(data, dict) and 'WebServiceError' in data:
            # Process an Error Message from the API server
            wsErr = data['WebServiceError']
            if isinstance(wsErr, list) and len(wsErr) > 0:
                if 'Message' in wsErr[0]:
                    if wsErr[0]['Message'] == 'Invalid API key':
                        raise InvalidKeyError(wsErr[0]['Message'])
                    elif wsErr[0]['Message'] == 'Request not authenticated':
                        raise InvalidKeyError(wsErr[0]['Message'])
                    else:
                        raise AirNowError(wsErr[0]['Message'])
                else:
                    raise AirNowError(str(wsErr[0]))
            else:
                raise AirNowError(str(wsErr))

        elif not isinstance(data, list):
            # We should get a list of Observation or Forecast objects
            raise InvalidJsonError(
                'Unexpected response type: %s' % (type(data))
            )

        elif len(data) == 0:
            # No objects were returned
            raise EmptyResponseError('No data was returned')

        # Return list of objects for further processing
        return data
