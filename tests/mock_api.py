'''Mocked AirNow API'''
import re

from aioresponses import CallbackResult

MOCK_API_KEY = '01234567-89AB-CDEF-0123-456789ABCDEF'
RE_ENDPOINTS = re.compile(
    '^/?aq/(forecast|observation)/(zipCode|latLong)(/(current|historical))?/?$'
)


def mock_airnow_api(url, **kwargs):
    '''
    Mock the AirNow API
    '''
    m = RE_ENDPOINTS.match(url.path)
    if m is None:
        return CallbackResult(status=404)

    # Parse URL path
    ep_type = m.group(1)
    ep_mode = m.group(2)
    ep_when = m.group(4)

    # Check API Key
    if 'API_KEY' not in url.query:
        return CallbackResult(status=401, payload=dict(
            WebServiceError=[
                dict(
                    Message='Request not authenticated'
                ),
            ],
        ))

    if url.query['API_KEY'] != MOCK_API_KEY:
        return CallbackResult(status=401, payload=dict(
            WebServiceError=[
                dict(
                    Message='Invalid API key'
                ),
            ],
        ))

    # A zip code with value "empty" will return an empty list
    if 'zipCode' in url.query and url.query['zipCode'] == 'empty':
        return CallbackResult(payload=[])

    # A zip code with value "bad_json" will return invalid json
    if 'zipCode' in url.query and url.query['zipCode'] == 'bad_json':
        return CallbackResult(body='Bad JSON Test')

    # A zip code with value "error" will return a JSON error message
    if 'zipCode' in url.query and url.query['zipCode'] == 'error':
        return CallbackResult(status=400, payload=dict(
            WebServiceError=[
                dict(
                    Message='Client Error'
                ),
            ],
        ))

    # A zip code with value "error1" will return a JSON error message
    if 'zipCode' in url.query and url.query['zipCode'] == 'error1':
        return CallbackResult(status=400, payload=dict(
            WebServiceError=[
                'Client Error'
            ],
        ))

    # A zip code with value "error2" will return a non-structured error message
    if 'zipCode' in url.query and url.query['zipCode'] == 'error2':
        return CallbackResult(status=500, payload=dict(
            WebServiceError='Internal Server Error'
        ))

    # A zip code with value "dict" will return a JSON dictionary instead of
    # an array
    if 'zipCode' in url.query and url.query['zipCode'] == 'dict':
        return CallbackResult(payload=dict(status='OK'))

    # Return JSON with the endpoint and query information
    payload = dict(
        type=ep_type,
        mode=ep_mode,
        when=ep_when,
        query=dict(url.query),
    )
    return CallbackResult(payload=[payload])
