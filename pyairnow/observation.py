'''Retrieve a list of Current Observations'''
from typing import Callable, Coroutine, Optional, Union

class Observation:
    '''
    Class to retrieve the current air quality observations by zip code or by
    latitude and longitude.
    '''
    def __init__(self, request: Callable[..., Coroutine]) -> None:
        self._request = request

    async def zipCode(
        self,
        zipCode: str,
        *,
        distance: Optional[int] = None
    ) -> list:
        '''Request current observation for zip code'''
        params: dict = dict(zipCode = zipCode)
        if distance:
            params['distance'] = distance

        return await self._request(
            'aq/observation/zipCode/current',
            params = params
        )

    async def latLong(
        self,
        latitude: Optional[Union[float, str]] = None,
        longitude: Optional[Union[float, str]] = None,
        *,
        distance: Optional[int] = None,
    ) -> None:
        '''Request current observation for latitude/longitude'''
        params: dict = dict(
            latitude = str(latitude),
            longitude = str(longitude),
        )
        if distance:
            params['distance'] = distance

        return await self._request(
            'aq/observation/latLong/current',
            params = params
        )
