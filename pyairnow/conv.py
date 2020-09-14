'''Convert AQI to and from Pollutant Concentrations'''

EPA_TABLE = [
    {
        'iL': 0,
        'iH': 50,
        'breakpoints': {
            'O3':       { 'bL': 0.000,    'bH': 0.054   },
            'PM2.5':    { 'bL': 0.0,      'bH': 12.0    },
            'PM10':     { 'bL': 0,        'bH': 54      },
            'CO':       { 'bL': 0.0,      'bH': 4.4     },
            'SO2':      { 'bL': 0,        'bH': 35      },
            'NO2':      { 'bL': 0,        'bH': 53      },
        },
    },
    {
        'iL': 51,
        'iH': 100,
        'breakpoints': {
            'O3':       { 'bL': 0.055,    'bH': 0.070   },
            'PM2.5':    { 'bL': 12.1,     'bH': 35.4    },
            'PM10':     { 'bL': 55,       'bH': 154     },
            'CO':       { 'bL': 4.5,      'bH': 9.4     },
            'SO2':      { 'bL': 36,       'bH': 75      },
            'NO2':      { 'bL': 54,       'bH': 100     },
        },
    },
    {
        'iL': 101,
        'iH': 150,
        'breakpoints': {
            'O3':       { 'bL': 0.071,    'bH': 0.085   },
            'PM2.5':    { 'bL': 35.5,     'bH': 55.4    },
            'PM10':     { 'bL': 155,      'bH': 254     },
            'CO':       { 'bL': 9.5,      'bH': 12.4    },
            'SO2':      { 'bL': 76,       'bH': 185     },
            'NO2':      { 'bL': 101,      'bH': 360     },
        },
    },
    {
        'iL': 151,
        'iH': 200,
        'breakpoints': {
            'O3':       { 'bL': 0.086,    'bH': 0.105   },
            'PM2.5':    { 'bL': 55.5,     'bH': 150.4   },
            'PM10':     { 'bL': 255,      'bH': 354     },
            'CO':       { 'bL': 12.5,     'bH': 15.4    },
            'SO2':      { 'bL': 186,      'bH': 304     },
            'NO2':      { 'bL': 361,      'bH': 649     },
        },
    },
    {
        'iL': 201,
        'iH': 300,
        'breakpoints': {
            'O3':       { 'bL': 0.106,    'bH': 0.200   },
            'PM2.5':    { 'bL': 150.5,    'bH': 250.4   },
            'PM10':     { 'bL': 355,      'bH': 424     },
            'CO':       { 'bL': 15.5,     'bH': 30.4    },
            'SO2':      { 'bL': 305,      'bH': 604     },
            'NO2':      { 'bL': 650,      'bH': 1249    },
        },
    },
    {
        'iL': 301,
        'iH': 400,
        'breakpoints': {
            # Ozone here changes from 8h to 1h reporting
            'O3':       { 'bL': 0.405,    'bH': 0.504   },
            'PM2.5':    { 'bL': 250.5,    'bH': 350.4   },
            'PM10':     { 'bL': 425,      'bH': 504     },
            'CO':       { 'bL': 30.5,     'bH': 40.4    },
            'SO2':      { 'bL': 605,      'bH': 804     },
            'NO2':      { 'bL': 1250,     'bH': 1649    },
        },
    },
    {
        'iL': 401,
        'iH': 500,
        'breakpoints': {
            'O3':       { 'bL': 0.505,    'bH': 0.604   },
            'PM2.5':    { 'bL': 350.5,    'bH': 500.4   },
            'PM10':     { 'bL': 505,      'bH': 604     },
            'CO':       { 'bL': 40.5,     'bH': 50.4    },
            'SO2':      { 'bL': 805,      'bH': 1004    },
            'NO2':      { 'bL': 1650,     'bH': 2049    },
        },
    },
]

EPA_ROUND_FNS = {
    'O3':       lambda c: round(c, 3),
    'PM2.5':    lambda c: round(c, 1),
    'PM10':     lambda c: int(round(c, 0)),
    'CO':       lambda c: round(c, 1),
    'SO2':      lambda c: int(round(c, 0)),
    'NO2':      lambda c: int(round(c, 0)),
}


def aqi_to_concentration(aqi, pollutant):
    '''Convert AQI (0-500) to Pollutant Concentration'''
    if aqi < 0 or aqi > 500:
        raise ValueError('AQI must be between 0 and 500')

    for row in EPA_TABLE:
        iL = row['iL']
        iH = row['iH']
        if iL <= aqi and iH >= aqi:
            bL = row['breakpoints'][pollutant]['bL']
            bH = row['breakpoints'][pollutant]['bH']
            cp = float(aqi - iL) * (bH - bL) / (iH - iL) + bL
            return EPA_ROUND_FNS[pollutant](cp)

    raise RuntimeError('No matching row found in EPA_TABLE')


def concentration_to_aqi(conc, pollutant):
    '''Convert Pollutant Concentration to AQI'''
    if conc < 0:
        raise ValueError('Concentration must be positive')

    rounded = EPA_ROUND_FNS[pollutant](conc)
    for row in EPA_TABLE:
        bL = row['breakpoints'][pollutant]['bL']
        bH = row['breakpoints'][pollutant]['bH']
        if bL <= rounded and bH >= rounded:
            iL = row['iL']
            iH = row['iH']

            return int(round(float(iH - iL) / (bH - bL) * (conc - bL) + iL, 0))

    raise ValueError(
        f'Invalid concentration {rounded} for pollutant {pollutant}'
    )
