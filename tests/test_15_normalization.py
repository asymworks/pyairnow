'''Tests for response normalization from new API format to legacy format'''
from pyairnow.observation import _normalize_observation, CATEGORY_NAME_TO_NUMBER
from pyairnow.forecast import _normalize_forecast


class TestObservationNormalization:
    def test_basic_fields(self):
        raw = {
            'dateObserved': '2024-01-15',
            'hourObserved': '14:00',
            'localTimeZone': 'PST',
            'reportingAreaName': 'San Francisco',
            'parameterName': 'PM2.5',
            'nowcastAQI': 42,
            'aqiCategoryName': 'Good',
        }
        result = _normalize_observation(raw)

        assert result['DateObserved'] == '2024-01-15'
        assert result['HourObserved'] == 14
        assert result['LocalTimeZone'] == 'PST'
        assert result['ReportingArea'] == 'San Francisco'
        assert result['ParameterName'] == 'PM2.5'
        assert result['AQI'] == 42
        assert result['Category'] == {'Number': 1, 'Name': 'Good'}

    def test_ozone_renamed_to_o3(self):
        raw = {
            'parameterName': 'OZONE',
            'nowcastAQI': 30,
            'aqiCategoryName': 'Good',
        }
        result = _normalize_observation(raw)
        assert result['ParameterName'] == 'O3'

    def test_pm10_unchanged(self):
        raw = {'parameterName': 'PM10', 'nowcastAQI': 20, 'aqiCategoryName': 'Good'}
        result = _normalize_observation(raw)
        assert result['ParameterName'] == 'PM10'

    def test_hour_string_parsed(self):
        raw = {'hourObserved': '09:00', 'aqiCategoryName': ''}
        result = _normalize_observation(raw)
        assert result['HourObserved'] == 9

    def test_hour_integer_passthrough(self):
        raw = {'hourObserved': 15, 'aqiCategoryName': ''}
        result = _normalize_observation(raw)
        assert result['HourObserved'] == 15

    def test_all_category_mappings(self):
        for name, expected_number in CATEGORY_NAME_TO_NUMBER.items():
            raw = {'aqiCategoryName': name}
            result = _normalize_observation(raw)
            assert result['Category']['Number'] == expected_number
            assert result['Category']['Name'] == name

    def test_unknown_category_defaults_to_zero(self):
        raw = {'aqiCategoryName': 'Unknown Category'}
        result = _normalize_observation(raw)
        assert result['Category']['Number'] == 0

    def test_missing_fields_default_gracefully(self):
        result = _normalize_observation({})
        assert result['DateObserved'] == ''
        assert result['HourObserved'] == 0
        assert result['LocalTimeZone'] == ''
        assert result['ReportingArea'] == ''
        assert result['StateCode'] == ''
        assert result['Latitude'] is None
        assert result['Longitude'] is None
        assert result['ParameterName'] == ''
        assert result['AQI'] == -1

    def test_null_fields_default_gracefully(self):
        raw = {
            'dateObserved': None,
            'hourObserved': None,
            'localTimeZone': None,
            'reportingAreaName': None,
            'stateCode': None,
            'latitude': None,
            'longitude': None,
            'parameterName': None,
            'nowcastAQI': None,
            'aqiCategoryName': None,
        }
        result = _normalize_observation(raw)
        assert result['DateObserved'] == ''
        assert result['HourObserved'] == 0
        assert result['LocalTimeZone'] == ''
        assert result['ReportingArea'] == ''
        assert result['StateCode'] == ''
        assert result['Latitude'] is None
        assert result['Longitude'] is None
        assert result['ParameterName'] == ''
        assert result['AQI'] == -1
        assert result['Category'] == {'Number': 0, 'Name': ''}

    def test_null_aqi_falls_back_to_aqi_key(self):
        raw = {'nowcastAQI': None, 'aqi': 42, 'aqiCategoryName': 'Good'}
        result = _normalize_observation(raw)
        assert result['AQI'] == 42

    def test_zero_aqi_is_preserved(self):
        raw = {'nowcastAQI': 0, 'aqiCategoryName': 'Good'}
        result = _normalize_observation(raw)
        assert result['AQI'] == 0


class TestForecastNormalization:
    def test_basic_fields(self):
        raw = {
            'dateIssue': '2024-01-15',
            'dateValid': '2024-01-16',
            'reportingArea': 'Los Angeles',
            'stateCode': 'CA',
            'parameterName': 'PM2.5',
            'aqi': 55,
            'categoryNumber': 2,
            'categoryName': 'Moderate',
            'actionDay': True,
            'discussion': 'Expect moderate air quality',
        }
        result = _normalize_forecast(raw)

        assert result['DateIssue'] == '2024-01-15'
        assert result['DateForecast'] == '2024-01-16'
        assert result['ReportingArea'] == 'Los Angeles'
        assert result['StateCode'] == 'CA'
        assert result['ParameterName'] == 'PM2.5'
        assert result['AQI'] == 55
        assert result['Category'] == {'Number': 2, 'Name': 'Moderate'}
        assert result['ActionDay'] is True
        assert result['Discussion'] == 'Expect moderate air quality'

    def test_ozone_renamed_to_o3(self):
        raw = {
            'parameterName': 'OZONE',
            'aqi': 30,
            'categoryNumber': 1,
            'categoryName': 'Good',
        }
        result = _normalize_forecast(raw)
        assert result['ParameterName'] == 'O3'

    def test_missing_fields_default_gracefully(self):
        result = _normalize_forecast({})
        assert result['DateIssue'] == ''
        assert result['DateForecast'] == ''
        assert result['ReportingArea'] == ''
        assert result['StateCode'] == ''
        assert result['ParameterName'] == ''
        assert result['AQI'] == -1
        assert result['Category'] == {'Number': 0, 'Name': ''}
        assert result['ActionDay'] is False
        assert result['Discussion'] == ''

    def test_null_fields_default_gracefully(self):
        raw = {
            'dateIssue': None,
            'dateValid': None,
            'reportingArea': None,
            'stateCode': None,
            'latitude': None,
            'longitude': None,
            'parameterName': None,
            'aqi': None,
            'categoryNumber': None,
            'categoryName': None,
            'actionDay': None,
            'discussion': None,
        }
        result = _normalize_forecast(raw)
        assert result['DateIssue'] == ''
        assert result['DateForecast'] == ''
        assert result['ReportingArea'] == ''
        assert result['StateCode'] == ''
        assert result['Latitude'] is None
        assert result['Longitude'] is None
        assert result['ParameterName'] == ''
        assert result['AQI'] == -1
        assert result['Category'] == {'Number': 0, 'Name': ''}
        assert result['ActionDay'] is False
        assert result['Discussion'] == ''

    def test_null_legacy_category_defaults_gracefully(self):
        result = _normalize_forecast({'Category': None, 'AQI': 20})
        assert result['Category'] == {'Number': 0, 'Name': ''}
        assert result['AQI'] == 20

    def test_legacy_category_still_read(self):
        name = 'Unhealthy for Sensitive Groups'
        result = _normalize_forecast({'Category': {'Number': 3, 'Name': name}})
        assert result['Category']['Number'] == 3
        assert result['Category']['Name'] == name

    def test_action_day_false_is_preserved(self):
        result = _normalize_forecast({'actionDay': False})
        assert result['ActionDay'] is False
