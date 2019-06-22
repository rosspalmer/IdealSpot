from abc import ABC, abstractmethod

from data import WeatherDataBase
from optimizer import Spot


class WeatherTarget(ABC):

    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def add_data_to_db(self, spot: Spot, db: WeatherDataBase) -> WeatherDataBase:
        pass

    @abstractmethod
    def calculate_objective(self, spot: Spot, db: WeatherDataBase) -> float:
        pass

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
