import unittest
from unittest.mock import patch
import pandas as pd

from main_opp import WeatherApp


class TestWeatherApp(unittest.TestCase):
    def setUp(self):
        self.api_key = 'dummy_api_key'
        self.base_csv_file_path = 'dummy_path'
        self.cities = ['London', 'Paris', 'Berlin']
        self.weather_data = {
                'coord': {'lon': 139.6917, 'lat': 35.6895},
                'weather': [{'id': 800,
                             'main': 'Clear',
                             'description': 'clear sky',
                             'icon': '01d'}],
                'base': 'stations',
                'main': {'temp': 30.0,
                         'feels_like': 30.0,
                         'temp_min': 30.0,
                         'temp_max': 30.0,
                         'pressure': 1012,
                         'humidity': 53,
                         'sea_level': 1012,
                         'grnd_level': 1008},
                'visibility': 10000,
                'wind': {'speed': 5.14, 'deg': 60},
                'clouds': {'all': 0},
                'dt': 1600000000,
                'sys': {'type': 2,
                        'id': 200,
                        'country': 'JP',
                        'sunrise': 1600000000,
                        'sunset': 1600040000},
                'timezone': 32400,
                'id': 1850147,
                'name': 'Tokyo',
                'cod': 200
                }

    @patch('main_opp.WeatherDataFetcher.fetch_weather')
    @patch('main_opp.pd.read_csv')
    @patch('main_opp.pd.DataFrame.to_csv')
    def test_weather_app(self, mock_to_csv, mock_read_csv, mock_fetch_weather):
        # Mock the fetch_weather method
        mock_fetch_weather.return_value = self.weather_data

        # Mock the list of cities
        mock_read_csv.return_value = pd.DataFrame(self.cities)

        # Initialize the WeatherApp
        app = WeatherApp(self.base_csv_file_path, self.api_key)

        # Run the app
        app.run()

        # Check that fetch_weather was called for each city
        self.assertEqual(mock_fetch_weather.call_count, len(self.cities))

        # Check that data was saved
        self.assertTrue(mock_to_csv.called)

        # Check that to_csv was called with the correct file path
        mock_to_csv.assert_called_with(app.saver.file_path, mode='a',
                                       index=False, header=True)

    @patch('main_opp.WeatherDataFetcher.fetch_weather')
    @patch('main_opp.pd.read_csv')
    def test_city_not_found(self, mock_read_csv, mock_fetch_weather):
        # Mock an API response for a non-existent city
        mock_fetch_weather.return_value = \
            {"cod": "404", "message": "city not found"}

        # Mock the list of cities
        mock_read_csv.return_value = pd.DataFrame(['NonExistentCity'])

        # Initialize the WeatherApp
        app = WeatherApp(self.base_csv_file_path, self.api_key)

        # Run the app and capture the output
        with patch('builtins.print') as mock_print:
            app.run()
            mock_print.assert_called_with("Erro, NonExistentCity not found")


if __name__ == '__main__':
    unittest.main()
