from abc import ABC, abstractmethod

from ideal_spot.data import WeatherDataBase, WeatherFeed


class WeatherTarget(ABC):

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    @abstractmethod
    def add_data_to_db(db: WeatherDataBase, new_feed: WeatherFeed) -> WeatherDataBase:
        pass

    @staticmethod
    @abstractmethod
    def calculate_objective(db: WeatherDataBase) -> float:
        pass

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
