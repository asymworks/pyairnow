'''Retrieve a list of Current Observations'''
import warnings
from typing import Callable, Coroutine, Optional, Union

from pyairnow.util import coalesce


CATEGORY_NAME_TO_NUMBER = {
    'Good': 1,
    'Moderate': 2,
    'Unhealthy for Sensitive Groups': 3,
    'Unhealthy': 4,
    'Very Unhealthy': 5,
    'Hazardous': 6,
}


PARAMETER_NAME_MAP = {
    'OZONE': 'O3',
}


def _normalize_observation(raw: dict) -> dict:
    '''Transform new API response format to legacy format for compatibility.'''
    hour_raw = coalesce(raw, 'hourObserved', default=0)
    if isinstance(hour_raw, str):
        hour = int(hour_raw.split(':')[0])
    else:
        hour = int(hour_raw)

    cat_name = coalesce(raw, 'aqiCategoryName', default='')
    cat_number = CATEGORY_NAME_TO_NUMBER.get(cat_name, 0)

    param = coalesce(raw, 'parameterName', default='')
    param = PARAMETER_NAME_MAP.get(param, param)

    return {
        'DateObserved': coalesce(raw, 'dateObserved', default=''),
        'HourObserved': hour,
        'LocalTimeZone': coalesce(raw, 'localTimeZone', default=''),
        'ReportingArea': coalesce(raw, 'reportingAreaName', default=''),
        'StateCode': coalesce(raw, 'stateCode', default=''),
        'Latitude': coalesce(raw, 'latitude'),
        'Longitude': coalesce(raw, 'longitude'),
        'ParameterName': param,
        'AQI': coalesce(raw, 'nowcastAQI', 'aqi', default=-1),
        'Category': {
            'Number': cat_number,
            'Name': cat_name,
        },
    }


class Observations:
    '''
    Class to retrieve the current air quality observations by zip code or by
    latitude and longitude.
    '''
    def __init__(
        self, request: Callable[..., Coroutine], *,
        legacy_format: bool = True
    ) -> None:
        self._request = request
        self._legacy_format = legacy_format

    async def zipCode(
        self,
        zipCode: str,
        *,
        distance: Optional[int] = None
    ) -> list:
        '''Request current observation for zip code'''
        params: dict = dict(zipCode=zipCode)
        if distance is not None:
            warnings.warn(
                'The distance parameter is deprecated and ignored by the '
                'AirNow 2026 API. It will be removed in a future version.',
                DeprecationWarning,
                stacklevel=2,
            )

        data = await self._request(
            'aq/observation/current/ziplatlong',
            params=params
        )
        if self._legacy_format:
            return [_normalize_observation(o) for o in data]
        return data

    async def latLong(
        self,
        latitude: Optional[Union[float, str]] = None,
        longitude: Optional[Union[float, str]] = None,
        *,
        distance: Optional[int] = None,
    ) -> list:
        '''Request current observation for latitude/longitude'''
        params: dict = dict(
            latitude=str(latitude),
            longitude=str(longitude),
        )
        if distance is not None:
            warnings.warn(
                'The distance parameter is deprecated and ignored by the '
                'AirNow 2026 API. It will be removed in a future version.',
                DeprecationWarning,
                stacklevel=2,
            )

        data = await self._request(
            'aq/observation/current/ziplatlong',
            params=params
        )
        if self._legacy_format:
            return [_normalize_observation(o) for o in data]
        return data
