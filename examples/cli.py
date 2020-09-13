'''Test Script/CLI Interface to pyairnow'''
import argparse
import asyncio

from pyairnow import WebServiceAPI


def optionalArgs(args):
    '''Load optional keyword arguments (date and dict)'''
    kwargs = dict()
    if args.date is not None:
        kwargs['date'] = args.date
    if args.distance is not None:
        kwargs['distance'] = args.distance

    return kwargs


def llArgs(args):
    '''Load latitude and longitude from the location argument'''
    try:
        lat, long = args.split(',')
    except ValueError:
        raise ValueError(
            'Invalid location string, expected <latitude>,<longitude>'
        )

    return [float(lat.strip()), float(long.strip())]


async def get_forecast_zip(args: argparse.Namespace) -> None:
    '''Print forecast information for a zip code'''
    client = WebServiceAPI(args.api_key)
    data = await client.forecast.zipCode(args.zipcode, **optionalArgs(args))
    print(data)


async def get_forecast_ll(args: argparse.Namespace) -> None:
    '''Print forecast information for a latitude and longitude'''
    client = WebServiceAPI(args.api_key)
    data = await client.forecast.latLong(*llArgs(args), **optionalArgs(args))
    print(data)


async def get_current_zip(args: argparse.Namespace) -> None:
    '''Print current observation information for a zip code'''
    client = WebServiceAPI(args.api_key)
    data = await client.observations.zipCode(
        args.zipcode,
        **optionalArgs(args),
    )
    print(data)


async def get_current_ll(args: argparse.Namespace) -> None:
    '''Print current observation information for a latitude and longitude'''
    client = WebServiceAPI(args.api_key)
    data = await client.observations.latLong(
        *llArgs(args),
        **optionalArgs(args),
    )
    print(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='CLI Client for pyAirNow, which obtains current and '
                    'forecasted air quality information from AirNow. The '
                    'returned JSON data is printed to stdout.',
        epilog='To obtain an API key, visit https://docs.airnowapi.org/login',
    )
    parser.add_argument(
        '-k', '--api-key',
        required=True,
        help='AirNow API Key (required)',
    )

    location_group = parser.add_mutually_exclusive_group(required=True)
    location_group.add_argument(
        '-z', '--zipcode',
        help='Zip Code for Observations or Forecast. May not be used with '
             '--location.',
    )
    location_group.add_argument(
        '-l', '--location',
        help='Latitude and Longitude for Observations or Forecast (must be '
             'formatted as "<latitude>,<longitude>" with an optional space '
             'before the longitude value. May not be used with --zipcode.'
    )

    parser.add_argument(
        '-r', '--distance',
        help='If no reporting area is associated with the zip code or '
             'latitude and longitude, return data from a station within this '
             'distance (in miles)'
    )
    parser.add_argument(
        '-d', '--date',
        help='Desired forecast date. If omitted, the current day forecast is '
             'returned. Format as yyyy-mm-dd'
    )
    parser.add_argument(
        'type', choices=['forecast', 'observations'],
        help='Look up either the forecast or the current observations for the '
             'given location'
    )
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    if args.type == 'forecast':
        if args.zipcode is not None:
            loop.run_until_complete(get_forecast_zip(args))
        else:
            loop.run_until_complete(get_forecast_ll(args))
    else:
        if args.zipcode is not None:
            loop.run_until_complete(get_current_zip(args))
        else:
            loop.run_until_complete(get_current_ll(args))
