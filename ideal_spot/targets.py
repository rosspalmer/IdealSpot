from abc import ABC, abstractmethod

from ideal_spot.data import WeatherDataBase, WeatherFeed


class WeatherTarget(ABC):

    @staticmethod
    @abstractmethod
    def calculate_objective(db: WeatherDataBase) -> float:
        pass

    @staticmethod
    @abstractmethod
    def add_data_to_db(db: WeatherDataBase, new_feed: WeatherFeed) -> WeatherDataBase:
        pass
