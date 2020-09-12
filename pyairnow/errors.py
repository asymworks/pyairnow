'''AirNow API Error Classes'''

class AirNowError(Exception):
    '''Base AirNow Error Class'''
    pass

class EmptyResponseError(Exception):
    '''Empty Response Error'''
    pass

class InvalidJsonError(Exception):
    '''Invalid JSON Data Error'''
    pass

class InvalidKeyError(Exception):
    '''Invalid API Key Error'''
    pass
