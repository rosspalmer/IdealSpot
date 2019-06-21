
from abc import ABC, abstractmethod
from json import loads
from typing import Dict

from pandas import DataFrame
from requests import get


class WeatherDataBase:

    def __init__(self, tables: Dict[str, DataFrame] = None):
        self.tables = tables
        if self.tables is None:
            self.tables = dict()

    def get_table(self, table_name: str) -> DataFrame:
        return self.tables[table_name]

    def set_table(self, table_name: str, df: DataFrame):
        self.tables[table_name] = df


class WeatherFeed(ABC):

    def __init__(self, name: str):
        self.name = name

    def get_data(self) -> DataFrame:
        api_data = get(self._get_api_call()).content
        data = self._generate_data(api_data)
        return data

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def _get_api_call(self) -> str:
        pass

    @abstractmethod
    def _generate_data(self, api_data: str) -> DataFrame:
        pass

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class CoordinateWeatherFeed(WeatherFeed, ABC):

    def __init__(self, name: str, lat: float, long: float):
        super().__init__(name)
        self.lat = lat
        self.long = long

    def get_lat(self) -> float:
        return self.lat

    def get_long(self) -> float:
        return self.long


class ForecastWeatherFeed(CoordinateWeatherFeed):

    def __init__(self, name: str, lat: float, long: float):
        super().__init__(name, lat, long)

    def _get_api_call(self) -> str:
        'api.openweathermap.org/data/2.5/forecast/hourly?lat=%s&lon=%s' % (str(self.lat), str(self.long))

    def _generate_data(self, api_data: str) -> DataFrame:

        json_data = loads(api_data)
        data = list()

        for hour_forecast_data in json_data['list']:
            data.append(self._add_hourly_metrics(hour_forecast_data))

        df = DataFrame(data)

        return df

    @abstractmethod
    def _add_hourly_metrics(self, hour_forecast_data: Dict) -> Dict:
        return dict()


class ForecastWeatherFeedDecorator(ABC, ForecastWeatherFeed):

    def __init__(self, feed: ForecastWeatherFeed):
        super().__init__(feed.get_name(), feed.get_lat(), feed.get_long())
        self.feed = feed

    def get_name(self) -> str:
        return self.feed.name

    def get_lat(self) -> float:
        return self.lat

    def get_long(self) -> float:
        return self.long
