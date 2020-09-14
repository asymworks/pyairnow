import pytest

from pyairnow.conv import aqi_to_concentration, concentration_to_aqi


def test_convert_pm25():
    assert aqi_to_concentration(0, 'PM2.5') == 0
    assert aqi_to_concentration(25, 'PM2.5') == 6
    assert aqi_to_concentration(50, 'PM2.5') == 12
    assert aqi_to_concentration(51, 'PM2.5') == 12.1
    assert aqi_to_concentration(86, 'PM2.5') == 28.7
    assert aqi_to_concentration(144, 'PM2.5') == 53.0

    assert concentration_to_aqi(0, 'PM2.5') == 0
    assert concentration_to_aqi(12.0, 'PM2.5') == 50
    assert concentration_to_aqi(12.1, 'PM2.5') == 51
    assert concentration_to_aqi(28.66, 'PM2.5') == 86
    assert concentration_to_aqi(53.0, 'PM2.5') == 144


def test_convert_invalid_negative_aqi():
    with pytest.raises(ValueError):
        aqi_to_concentration(-1, 'PM2.5')


def test_convert_invalid_overrange_aqi():
    with pytest.raises(ValueError):
        aqi_to_concentration(501, 'PM2.5')


def test_convert_invalid_negative_o3():
    with pytest.raises(ValueError):
        concentration_to_aqi(-0.0008, 'O3')


def test_convert_invalid_overrange_o3():
    with pytest.raises(ValueError):
        concentration_to_aqi(0.605, 'O3')
