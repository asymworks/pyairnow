'''Retrieve Historical Air Quality'''
from datetime import date as date_, datetime
from typing import Callable, Coroutine, Optional, Union


class Historical:
    '''
    Class to retrieve historical air quality by zip code or by latitude and
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
        params: dict = dict(zipCode=zipCode)
        '''Airnow  needs T00-0000 appended to the date parameter for historical calls'''
        if date and isinstance(date, str):
            y, m, d = date.split('-')
            params['date'] = date_(int(y), int(m), int(d)).isoformat() + "T00-0000"
        elif date and isinstance(date, datetime):
            params['date'] = date.date().isoformat() + "T00-0000"
        elif date and isinstance(date, date_):
            params['date'] = date.isoformat() + "T00-0000"
        if distance:
            params['distance'] = distance

        return await self._request(
            'aq/observation/zipCode/historical',
            params=params
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
            latitude=str(latitude),
            longitude=str(longitude),
        )
        if date and isinstance(date, str):
            y, m, d = date.split('-')
            params['date'] = date_(int(y), int(m), int(d)).isoformat() + "T00-0000"
        elif date and isinstance(date, datetime):
            params['date'] = date.date().isoformat() + "T00-0000"
        elif date and isinstance(date, date_):
            params['date'] = date.isoformat() + "T00-0000"
        if distance:
            params['distance'] = distance

        return await self._request(
            'aq/observation/latLong/historical',
            params=params
        )
