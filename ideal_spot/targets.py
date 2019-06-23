from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Set

from pandas import DataFrame

from ideal_spot.feed import ForecastWeatherFeedFactory
from ideal_spot.spots import Spot


class WeatherTarget(ABC):

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.forecast_data = None

    def evaluate_spot(self, spot: Spot):
        metrics = self.get_forecast_metrics()
        feed_data = self.generate_forecast_data(spot, metrics)
        self.set_forecast_data(feed_data)
        spot.set_scores(self.calculate_scores(spot))

    def get_api_key(self) -> str:
        return self.api_key

    def get_forecast_data(self) -> DataFrame:
        return self.forecast_data

    def set_forecast_data(self, forecast_data: DataFrame):
        self.forecast_data = forecast_data

    def get_forecast_metrics(self) -> Set[str]:
        return set()

    def calculate_scores(self, spot: Spot) -> Dict:
        return dict()

    def generate_forecast_data(self, spot: Spot, metrics: Set[str]) -> DataFrame:
        feed = ForecastWeatherFeedFactory(self.get_api_key(), spot.get_lat(), spot.get_long()).generate_feed(metrics)
        feed_data = feed.get_data()
        return feed_data


class WeatherTargetDecorator(WeatherTarget, ABC):

    def __init__(self, target: WeatherTarget, name: str):
        super().__init__(target.get_api_key())
        self.target = target
        self.name = name

    def get_api_key(self) -> str:
        return self.target.get_api_key()

    def get_forecast_data(self) -> DataFrame:
        return self.target.get_forecast_data()

    def set_forecast_data(self, forecast_data: DataFrame):
        self.target.set_forecast_data(forecast_data)

    @abstractmethod
    def get_forecast_metrics(self) -> Set[str]:
        return self.target.get_forecast_metrics()

    def calculate_scores(self, spot: Spot) -> Dict:
        scores = self.target.calculate_scores(spot)
        scores[self.name] = self._calculate_score(spot)
        return scores

    def generate_forecast_data(self, spot: Spot, metrics: Set[str]) -> DataFrame:
        return self.target.generate_forecast_data(spot, metrics)

    @abstractmethod
    def _calculate_score(self, spot: Spot) -> float:
        pass


class RangeTargetDecorator(WeatherTargetDecorator, ABC):

    def __init__(self, target: WeatherTarget, name: str, range_start: datetime, range_end: datetime,
                 value_name: str, max_value: float, min_value: float, operation: str):
        super().__init__(target, name)
        self.range_start = range_start
        self.range_end = range_end
        self.value_name = value_name
        self.max_value = max_value
        self.min_value = min_value
        self.operation = operation

        assert self.max_value > self.min_value, 'Max value %s must be larger than min value %s' % (str(self.max_value),
                                                                                                   str(self.min_value))
        assert self.operation in ['sum', 'mean']

    def _calculate_score(self, spot: Spot) -> float:

        df = self.get_forecast_data()

        df = df[df['datetime'] >= self.range_start]
        df = df[df['datetime'] <= self.range_end]

        cumulative_value = None
        if self.operation == 'sum':
            cumulative_value = df[self.value_name].sum()
        elif self.operation == 'mean':
            cumulative_value = df[self.value_name].mean()

        normalized_cumulative_value = (cumulative_value - self.min_value) / (self.max_value - self.min_value)
        normalized_cumulative_value = max(0.0, normalized_cumulative_value)
        normalized_cumulative_value = min(1.0, normalized_cumulative_value)

        return normalized_cumulative_value


class NewRainTarget(RangeTargetDecorator):

    def __init__(self, target: WeatherTarget, name: str, range_start: datetime, range_end: datetime):
        super().__init__(target, name, range_start, range_end, 'rain', 10.0, 0.0, 'sum')
        # FIXME determine ideal max rain value

    def get_forecast_metrics(self) -> Set[str]:
        metrics = super().get_forecast_metrics()
        metrics.add('rain')
        return metrics


class NewSnowTarget(RangeTargetDecorator):

    def __init__(self, target: WeatherTarget, name: str, range_start: datetime, range_end: datetime):
        super().__init__(target, name, range_start, range_end, 'snow', 10.0, 0.0, 'sum')
        # FIXME determine ideal max snow value

    def get_forecast_metrics(self) -> Set[str]:
        metrics = super().get_forecast_metrics()
        metrics.add('snow')
        return metrics


class IdealValueTargetDecorator(RangeTargetDecorator, ABC):

    def __init__(self, target: WeatherTarget, name: str, range_start: datetime, range_end: datetime,
                 value_name: str, max_value: float, min_value: float, ideal_value: float):
        super().__init__(target, name, range_start, range_end, value_name, max_value, min_value, 'mean')
        self.ideal_value = ideal_value

    def _calculate_score(self, spot: Spot) -> float:

        normalized_value_average = super()._calculate_score(spot)
        value_average = normalized_value_average * (self.max_value - self.min_value) + self.min_value

        score = abs(self.ideal_value - value_average)
        normalized_score = score / (self.max_value - self.min_value)
        normalized_score = 1.0 - normalized_score

        return normalized_score


class IdealTempTarget(IdealValueTargetDecorator):

    def __init__(self, target: WeatherTarget, name: str, range_start: datetime, range_end: datetime, ideal_temp: float):
        super().__init__(target, name, range_start, range_end, 'temp', 400.0, 200.0, ideal_temp)
        # FIXME determine ideal temperature range

    def get_forecast_metrics(self) -> Set[str]:
        metrics = super().get_forecast_metrics()
        metrics.add('temp')
        return metrics


class IdealWindTarget(IdealValueTargetDecorator):

    def __init__(self, target: WeatherTarget, name: str, range_start: datetime, range_end: datetime, ideal_wind: float):
        super().__init__(target, name, range_start, range_end, 'wind', 40.0, 0.0, ideal_wind)

    def get_forecast_metrics(self) -> Set[str]:
        metrics = super().get_forecast_metrics()
        metrics.add('wind')
        return metrics
