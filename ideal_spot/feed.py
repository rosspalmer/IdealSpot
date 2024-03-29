
from abc import ABC, abstractmethod
import datetime
from json import loads
from typing import Dict, Set

from pandas import DataFrame
from requests import get


class WeatherFeed(ABC):

    def __init__(self, api_key: str, lat: float, long: float):
        self.api_key = api_key
        self.lat = lat
        self.long = long

    def get_api_key(self) -> str:
        return self.api_key

    def get_data(self) -> DataFrame:
        api_data = get(self._get_api_call()).content
        data = self._generate_data(api_data)
        return data

    def get_lat(self) -> float:
        return self.lat

    def get_long(self) -> float:
        return self.long

    @abstractmethod
    def _get_api_call(self) -> str:
        pass

    @abstractmethod
    def _generate_data(self, api_data: str) -> DataFrame:
        pass


class ForecastWeatherFeed(WeatherFeed):

    def __init__(self, api_key: str, lat: float, long: float):
        super().__init__(api_key, lat, long)

    def _get_api_call(self) -> str:

        api_call = f'http://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.long}' \
            + f'&appid={self.api_key}'

        return api_call

    def _generate_data(self, api_data: str) -> DataFrame:

        json_data = loads(api_data)
        data = list()

        for hour_forecast_data in json_data['list']:
            data.append(self._add_hourly_metrics(hour_forecast_data))

        df = DataFrame(data)

        return df

    def _add_hourly_metrics(self, hour_forecast_data: Dict) -> Dict:
        data = dict()
        timestamp_int = hour_forecast_data['dt']
        data['datetime'] = datetime.datetime.fromtimestamp(timestamp_int)
        return data


class ForecastWeatherFeedDecorator(ForecastWeatherFeed, ABC):

    def __init__(self, feed: ForecastWeatherFeed):
        super().__init__(feed.get_api_key(), feed.get_lat(), feed.get_long())
        self.feed = feed

    def get_api_key(self) -> str:
        return self.feed.get_api_key()

    def get_lat(self) -> float:
        return self.feed.get_lat()

    def get_long(self) -> float:
        return self.feed.get_long()

    @abstractmethod
    def _add_hourly_metrics(self, hour_forecast_data: Dict) -> Dict:
        return self.feed._add_hourly_metrics(hour_forecast_data)


class TemperatureForecastDecorator(ForecastWeatherFeedDecorator):

    def _add_hourly_metrics(self, hour_forecast_data: Dict) -> Dict:
        data = super()._add_hourly_metrics(hour_forecast_data)
        data['temp'] = hour_forecast_data['main']['temp']
        data['temp_min'] = hour_forecast_data['main']['temp_min']
        data['temp_max'] = hour_forecast_data['main']['temp_max']
        return data


class RainForecastDecorator(ForecastWeatherFeedDecorator):

    def _add_hourly_metrics(self, hour_forecast_data: Dict) -> Dict:
        data = super()._add_hourly_metrics(hour_forecast_data)
        rain_amount = 0.0
        if 'rain' in hour_forecast_data and '3h' in hour_forecast_data['rain']:
            rain_amount = hour_forecast_data['rain']['3h']
        data['rain'] = rain_amount
        return data


class SnowForecastDecorator(ForecastWeatherFeedDecorator):

    def _add_hourly_metrics(self, hour_forecast_data: Dict) -> Dict:
        data = super()._add_hourly_metrics(hour_forecast_data)
        snow_amount = 0.0
        if 'snow' in hour_forecast_data and '3h' in hour_forecast_data['snow']:
            snow_amount = hour_forecast_data['snow']['3h']
        data['snow'] = snow_amount
        return data


class CloudForecastDecorator(ForecastWeatherFeedDecorator):

    def _add_hourly_metrics(self, hour_forecast_data: Dict) -> Dict:
        data = super()._add_hourly_metrics(hour_forecast_data)
        data['cloud'] = hour_forecast_data['clouds']['all']
        return data


class WindForecastDecorator(ForecastWeatherFeedDecorator):

    def _add_hourly_metrics(self, hour_forecast_data: Dict) -> Dict:
        data = super()._add_hourly_metrics(hour_forecast_data)
        data['wind'] = hour_forecast_data['wind']['speed']
        return data


class ForecastWeatherFeedFactory:

    def __init__(self, api_key: str, lat: float, long: float):
        self.api_key = api_key
        self.lat = lat
        self.long = long

        self.forecast_decorators = {
            'temp': TemperatureForecastDecorator,
            'rain': RainForecastDecorator,
            'snow': SnowForecastDecorator,
            'cloud': CloudForecastDecorator,
            'wind': WindForecastDecorator
        }

    def generate_feed(self, forecast_metrics: Set[str]) -> ForecastWeatherFeed:

        forecast_feed = ForecastWeatherFeed(self.api_key, self.lat, self.long)

        for forecast_metric in forecast_metrics:
            assert forecast_metric in self.forecast_decorators, 'Forecast metric %s is not supported' % forecast_metric
            forecast_feed = self.forecast_decorators[forecast_metric](forecast_feed)

        return forecast_feed
