'''Mocked AirNow API'''
import re

from aioresponses import CallbackResult

MOCK_API_KEY = '01234567-89AB-CDEF-0123-456789ABCDEF'

RE_FORECAST_CURRENT = re.compile(r'^/?aq/forecast/current/?$')
RE_OBS_ZIPLATLONG = re.compile(r'^/?aq/observation/current/ziplatlong/?$')

MOCK_OBSERVATION_RESPONSE = [
    {
        'dateObserved': '2020-09-01',
        'hourObserved': '15:00',
        'localTimeZone': 'PDT',
        'reportingAreaName': 'Los Angeles',
        'siteID': '060371103',
        'siteName': 'Los Angeles - N Main',
        'parameterName': 'PM2.5',
        'nowcastAQI': 55,
        'aqiCategoryName': 'Moderate',
        'reportingAgency': 'South Coast AQMD',
        'lookupBehavior': 'Closest Reading By Pollutant',
        'consideredMonitors': 'All',
        'lookupBoundary': '25 Miles',
    },
    {
        'dateObserved': '2020-09-01',
        'hourObserved': '15:00',
        'localTimeZone': 'PDT',
        'reportingAreaName': 'Los Angeles',
        'siteID': '060371103',
        'siteName': 'Los Angeles - N Main',
        'parameterName': 'OZONE',
        'nowcastAQI': 42,
        'aqiCategoryName': 'Good',
        'reportingAgency': 'South Coast AQMD',
        'lookupBehavior': 'Closest Reading By Pollutant',
        'consideredMonitors': 'All',
        'lookupBoundary': '25 Miles',
    },
]

MOCK_FORECAST_RESPONSE = [
    {
        'dateIssue': '2020-09-01',
        'dateValid': '2020-09-02',
        'reportingArea': 'Los Angeles',
        'reportingAreaCode': 'ca060',
        'stateCode': 'CA',
        'parameterName': 'OZONE',
        'aqi': 55,
        'forecastAgency': 'South Coast AQMD',
        'categoryNumber': 2,
        'categoryName': 'Moderate',
        'actionDay': False,
        'discussion': '',
    },
    {
        'dateIssue': '2020-09-01',
        'dateValid': '2020-09-02',
        'reportingArea': 'Los Angeles',
        'reportingAreaCode': 'ca060',
        'stateCode': 'CA',
        'parameterName': 'PM2.5',
        'aqi': 42,
        'forecastAgency': 'South Coast AQMD',
        'categoryNumber': 1,
        'categoryName': 'Good',
        'actionDay': False,
        'discussion': '',
    },
]


def mock_airnow_api(url, **kwargs):
    '''
    Mock the AirNow API
    '''
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

    # Route to appropriate mock response
    if RE_OBS_ZIPLATLONG.match(url.path):
        return CallbackResult(payload=MOCK_OBSERVATION_RESPONSE)

    if RE_FORECAST_CURRENT.match(url.path):
        return CallbackResult(payload=MOCK_FORECAST_RESPONSE)

    return CallbackResult(status=404)
