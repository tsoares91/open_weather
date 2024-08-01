import os
import pandas as pd
import requests
from datetime import datetime, timezone


class WeatherDataFetcher:
    def __init__(self, api_key, units='metric'):
        self.api_key = api_key
        self.units = units
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'

    def fetch_weather(self, city):
        url = \
            f'{self.base_url}?q={city}&appid={self.api_key}&units={self.units}'
        response = requests.get(url)
        return response.json()


class WeatherDataProcessor:
    def __init__(self, data):
        self.data = data

    def flatten_data(self):
        if self.data["cod"] == "404":
            return None

        # Convert the 'dt' timestamp to a human-readable date format
        date_time = datetime.fromtimestamp(self.data['dt'], tz=timezone.utc)\
                            .strftime('%Y-%m-%d %H:%M:%S')

        flattened_data = {
            'lon': self.data['coord']['lon'],
            'lat': self.data['coord']['lat'],
            'weather_id': self.data['weather'][0]['id'],
            'weather_main': self.data['weather'][0]['main'],
            'weather_description': self.data['weather'][0]['description'],
            'weather_icon': self.data['weather'][0]['icon'],
            'base': self.data['base'],
            'temp': self.data['main']['temp'],
            'feels_like': self.data['main']['feels_like'],
            'temp_min': self.data['main']['temp_min'],
            'temp_max': self.data['main']['temp_max'],
            'pressure': self.data['main']['pressure'],
            'humidity': self.data['main']['humidity'],
            'sea_level': self.data['main']['sea_level'],
            'grnd_level': self.data['main']['grnd_level'],
            'visibility': self.data['visibility'],
            'wind_speed': self.data['wind']['speed'],
            'wind_deg': self.data['wind']['deg'],
            'clouds_all': self.data['clouds']['all'],
            'dt': self.data['dt'],
            'date_time': date_time,
            'sys_type': self.data['sys']['type'],
            'sys_id': self.data['sys']['id'],
            'sys_country': self.data['sys']['country'],
            'sys_sunrise': self.data['sys']['sunrise'],
            'sys_sunset': self.data['sys']['sunset'],
            'timezone': self.data['timezone'],
            'id': self.data['id'],
            'name': self.data['name'],
            'cod': self.data['cod']
        }
        return flattened_data


class WeatherDataSaver:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_to_csv(self, data):
        file_exists = os.path.exists(self.file_path)
        df = pd.DataFrame([data])
        df.to_csv(self.file_path, mode='a', index=False,
                  header=not file_exists)


class WeatherApp:
    def __init__(self, base_csv_file_path, api_key):
        self.base_csv_file_path = base_csv_file_path
        self.api_key = api_key
        self.fetcher = WeatherDataFetcher(api_key)
        self.saver = WeatherDataSaver(os.path.join(base_csv_file_path,
                                                   'weather_data.csv'))
        self.cities = self.load_cities()

    def load_cities(self):
        cities_csv_file_path = os.path.join(self.base_csv_file_path,
                                            'listofcities.csv')
        df_cities = pd.read_csv(cities_csv_file_path, header=None)
        return df_cities[0].tolist()

    def run(self):
        for city in self.cities:
            data = self.fetcher.fetch_weather(city)
            processor = WeatherDataProcessor(data)
            flattened_data = processor.flatten_data()
            if flattened_data:
                self.saver.save_to_csv(flattened_data)
                print(f"{city}: info added to the {self.saver.file_path}")
            else:
                print(f"Erro, {city} not found")


if __name__ == "__main__":
    base_csv_file_path = os.path.dirname("Open_Weather")
    api_key = "a91a96bd7b64f16aba8bfe4eeb4412c8"
    app = WeatherApp(base_csv_file_path, api_key)
    app.run()
