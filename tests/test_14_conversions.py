import pytest

from pyairnow.conv import aqi_to_concentration, concentration_to_aqi


def test_convert_pm25():
    assert aqi_to_concentration(0, 'PM2.5') == 0
    assert aqi_to_concentration(25, 'PM2.5') == 4.5
    assert aqi_to_concentration(50, 'PM2.5') == 9.0
    assert aqi_to_concentration(51, 'PM2.5') == 9.1
    assert aqi_to_concentration(86, 'PM2.5') == 27.9
    assert aqi_to_concentration(144, 'PM2.5') == 53.0
    assert aqi_to_concentration(500, 'PM2.5') == 325.4
    assert aqi_to_concentration(501, 'PM2.5') == 325.9

    assert concentration_to_aqi(0, 'PM2.5') == 0
    assert concentration_to_aqi(9.0, 'PM2.5') == 50
    assert concentration_to_aqi(9.1, 'PM2.5') == 51
    assert concentration_to_aqi(27.9, 'PM2.5') == 86
    assert concentration_to_aqi(53.0, 'PM2.5') == 144
    assert concentration_to_aqi(325.4, 'PM2.5') == 500
    assert concentration_to_aqi(325.9, 'PM2.5') == 501


def test_convert_invalid_negative_aqi():
    with pytest.raises(ValueError):
        aqi_to_concentration(-1, 'PM2.5')


def test_convert_invalid_negative_o3():
    with pytest.raises(ValueError):
        concentration_to_aqi(-0.0008, 'O3')
