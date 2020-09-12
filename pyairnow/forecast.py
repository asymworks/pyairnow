'''Retrieve Air Quality Forecasts'''
from datetime import date as date_, datetime
from typing import Callable, Coroutine, Optional, Union

class Forecast:
    '''
    Class to retrieve the air quality forecast by zip code or by latitude and
    longitude.
    '''
    def __init__(self, request: Callable[..., Coroutine]) -> None:
        self._request = request

    async def zipCode(
        self,
        zipCode: str,
        *,
        date: Optional[Union[date_, datetime, str]] = None,
        distance: Optional[int] = None
    ) -> list:
        '''Request current observation for zip code'''
        params: dict = dict(zipCode = zipCode)
        if date and isinstance(date, str):
            params['date'] = date_.fromisoformat(date).isoformat()
        elif date and isinstance(date, datetime):
            params['date'] = date.date().isoformat()
        elif date and isinstance(date, date_):
            params['date'] = date.isoformat()
        if distance:
            params['distance'] = distance

        return await self._request(
            'aq/forecast/zipCode',
            params = params
        )

    async def latLong(
        self,
        latitude: Optional[Union[float, str]] = None,
        longitude: Optional[Union[float, str]] = None,
        *,
        date: Optional[Union[date_, datetime, str]] = None,
        distance: Optional[int] = None,
    ) -> None:
        '''Request current observation for latitude/longitude'''
        params: dict = dict(
            latitude = str(latitude),
            longitude = str(longitude),
        )
        if date and isinstance(date, str):
            params['date'] = date_.fromisoformat(date).isoformat()
        elif date and isinstance(date, datetime):
            params['date'] = date.date().isoformat()
        elif date and isinstance(date, date_):
            params['date'] = date.isoformat()
        if distance:
            params['distance'] = distance

        return await self._request(
            'aq/forecast/latLong',
            params = params
        )
