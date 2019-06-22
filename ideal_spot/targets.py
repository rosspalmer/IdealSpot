from abc import ABC, abstractmethod
from typing import Dict, Set

from feed import ForecastWeatherFeedFactory, ForecastWeatherFeed
from optimizer import Spot


class WeatherTarget(ABC):

    def __init__(self):
        self.forecast_feed = None

    def evaluate_spot(self, spot: Spot):
        metrics = self.get_forecast_metrics()
        feed = ForecastWeatherFeedFactory(spot.get_lat(), spot.get_long()).generate_feed(metrics)
        self.set_forecast_feed(feed)
        spot.set_scores(self.calculate_scores(spot))

    def get_forecast_feed(self) -> ForecastWeatherFeed:
        return self.forecast_feed

    def set_forecast_feed(self, forecast_feed: ForecastWeatherFeed):
        self.forecast_feed = forecast_feed

    @abstractmethod
    def get_forecast_metrics(self) -> Set[str]:
        return set()

    @abstractmethod
    def calculate_scores(self, spot: Spot) -> Dict:
        pass


class WeatherTargetDecorator(WeatherTarget, ABC):

    def __init__(self, target: WeatherTarget, name: str):
        super().__init__()
        self.target = target
        self.name = name

    def get_forecast_feed(self) -> ForecastWeatherFeed:
        return self.target.get_forecast_feed()

    def set_forecast_feed(self, forecast_feed: ForecastWeatherFeed):
        self.target.set_forecast_feed(forecast_feed)

    @abstractmethod
    def get_forecast_metrics(self) -> Set[str]:
        return self.target.get_forecast_metrics()

    def calculate_scores(self, spot: Spot) -> Dict:
        scores = self.calculate_scores(spot)
        scores[self.name] = self._calculate_score(spot)
        return scores

    @abstractmethod
    def _calculate_score(self, spot: Spot) -> float:
        pass
