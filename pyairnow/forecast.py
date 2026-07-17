'''Retrieve Air Quality Forecasts'''
import warnings
from datetime import date as date_, datetime
from typing import Callable, Coroutine, Optional, Union

from pyairnow.util import coalesce


PARAMETER_NAME_MAP = {
    'OZONE': 'O3',
}


def _normalize_forecast(raw: dict) -> dict:
    '''Transform new API response format to legacy format for compatibility.'''
    legacy_cat = coalesce(raw, 'Category', default={})
    cat_number = coalesce(raw, 'categoryNumber')
    if cat_number is None:
        cat_number = coalesce(legacy_cat, 'Number', default=0)
    cat_name = coalesce(raw, 'categoryName')
    if cat_name is None:
        cat_name = coalesce(legacy_cat, 'Name', default='')

    param = coalesce(raw, 'parameterName', 'ParameterName', default='')
    param = PARAMETER_NAME_MAP.get(param, param)

    return {
        'DateIssue': coalesce(raw, 'dateIssue', default=''),
        'DateForecast': coalesce(raw, 'dateValid', 'DateForecast', default=''),
        'ReportingArea': coalesce(
            raw, 'reportingArea', 'ReportingArea', default=''
        ),
        'StateCode': coalesce(raw, 'stateCode', 'StateCode', default=''),
        'Latitude': coalesce(raw, 'latitude', 'Latitude'),
        'Longitude': coalesce(raw, 'longitude', 'Longitude'),
        'ParameterName': param,
        'AQI': coalesce(raw, 'aqi', 'AQI', default=-1),
        'Category': {
            'Number': cat_number,
            'Name': cat_name,
        },
        'ActionDay': coalesce(raw, 'actionDay', 'ActionDay', default=False),
        'Discussion': coalesce(raw, 'discussion', 'Discussion', default=''),
    }


class Forecast:
    '''
    Class to retrieve the air quality forecast by zip code or by latitude and
    longitude.
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
        date: Optional[Union[date_, datetime, str]] = None,
        distance: Optional[int] = None
    ) -> list:
        '''Request forecast for zip code'''
        params: dict = dict(zipCode=zipCode)
        if date and isinstance(date, str):
            y, m, d = date.split('-')
            params['date'] = date_(int(y), int(m), int(d)).isoformat()
        elif date and isinstance(date, datetime):
            params['date'] = date.date().isoformat()
        elif date and isinstance(date, date_):
            params['date'] = date.isoformat()
        if distance is not None:
            warnings.warn(
                'The distance parameter is deprecated and ignored by the '
                'AirNow 2026 API. It will be removed in a future version.',
                DeprecationWarning,
                stacklevel=2,
            )

        data = await self._request(
            'aq/forecast/current',
            params=params
        )
        if self._legacy_format:
            return [_normalize_forecast(f) for f in data]
        return data

    async def latLong(
        self,
        latitude: Optional[Union[float, str]] = None,
        longitude: Optional[Union[float, str]] = None,
        *,
        date: Optional[Union[date_, datetime, str]] = None,
        distance: Optional[int] = None,
    ) -> list:
        '''Request forecast for latitude/longitude'''
        params: dict = dict(
            latitude=str(latitude),
            longitude=str(longitude),
        )
        if date and isinstance(date, str):
            y, m, d = date.split('-')
            params['date'] = date_(int(y), int(m), int(d)).isoformat()
        elif date and isinstance(date, datetime):
            params['date'] = date.date().isoformat()
        elif date and isinstance(date, date_):
            params['date'] = date.isoformat()
        if distance is not None:
            warnings.warn(
                'The distance parameter is deprecated and ignored by the '
                'AirNow 2026 API. It will be removed in a future version.',
                DeprecationWarning,
                stacklevel=2,
            )

        data = await self._request(
            'aq/forecast/current',
            params=params
        )
        if self._legacy_format:
            return [_normalize_forecast(f) for f in data]
        return data
