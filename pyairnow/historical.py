'''Retrieve Historical Air Quality'''
from datetime import date as date_, datetime, timezone, timedelta
from typing import Callable, Coroutine, Optional, Union
from .errors import AirNowError


class Historical:
    '''
    Class to retrieve historical air quality by zip code or by latitude and
    longitude.
    '''
    def __init__(self, request: Callable[..., Coroutine]) -> None:
        self._request = request

    '''If date is given as string, must be in yyyy-mm-d format. '''
    async def zipCode(
        self,
        zipCode: str,
        *,
        date: Union[date_, datetime, str],
        distance: Optional[int] = None
    ) -> list:
        '''Request current observation for zip code'''
        params: dict = dict(zipCode=zipCode)
        '''Airnow  needs T00-0000 appended to the date parameter for historical calls'''
        if isinstance(date, str):
            y, m, d = date.split('-')
            '''create a timezone object with no utc offset'''
            tz = timezone(timedelta())
            params['date'] = datetime(int(y), int(m), int(d), tzinfo=tz).strftime("%Y-%m-%dT%H%z")
        elif isinstance(date, datetime):
            tz = timezone(timedelta())
            date = date.replace(tzinfo=tz)
            params['date'] = date.strftime("%Y-%m-%dT%H%z")
        elif isinstance(date, date_):
            tz=timezone(timedelta())
            params['date'] = datetime(date.year, date.month, date.day, tzinfo=tz).strftime("%Y-%m-%dT%H%z")
        else:
            raise AirNowError("Bad date type. Date parameter is either date, datetime, or a string.")

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
        date: Union[date_, datetime, str],
        distance: Optional[int] = None,
    ) -> None:
        '''Request current observation for latitude/longitude'''
        params: dict = dict(
            latitude=str(latitude),
            longitude=str(longitude),
        )

        if isinstance(date, str):
            y, m, d = date.split('-')
            '''create a timezone object with no utc offset'''
            tz = timezone(timedelta())
            params['date'] = datetime(int(y), int(m), int(d), tzinfo=tz).strftime("%Y-%m-%dT%H%z")
        elif isinstance(date, datetime):
            tz = timezone(timedelta())
            date = date.replace(tzinfo=tz)
            params['date'] = date.strftime("%Y-%m-%dT%H%z")
        elif isinstance(date, date_):
            tz=timezone(timedelta())
            params['date'] = datetime(date.year, date.month, date.day, tzinfo=tz).strftime("%Y-%m-%dT%H%z")
        else:
            raise AirNowError("Bad date type. Date parameter is either date, datetime, or a string.")

        if distance:
            params['distance'] = distance

        return await self._request(
            'aq/observation/latLong/historical',
            params=params
        )

