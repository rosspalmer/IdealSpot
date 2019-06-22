from datetime import datetime
from typing import Set

from pandas import DataFrame
import pytest

from feed import ForecastWeatherFeed
from spots import Spot
from targets import RangeTargetDecorator, WeatherTarget, IdealValueTargetDecorator, IdealTempTarget, EvaluateSpots


class _DummyRangeTargetDecorator(RangeTargetDecorator):

    def get_forecast_metrics(self) -> Set[str]:
        pass


class TestRangeTargetDecorator:

    def test_calculate_score(self):

        df = DataFrame([
            {'datetime': datetime(2019, 1, 1, 1), 'value': 1.0},
            {'datetime': datetime(2019, 1, 1, 8), 'value': 2.1},
            {'datetime': datetime(2019, 1, 1, 14), 'value': 3.2},
            {'datetime': datetime(2019, 1, 1, 20), 'value': 4.3},
            {'datetime': datetime(2019, 1, 2, 1), 'value': 5.4},
        ])

        target = WeatherTarget('not used')
        target.set_forecast_data(df)

        sum_target = _DummyRangeTargetDecorator(target, 'sum_test', datetime(2019, 1, 1, 6), datetime(2019, 1, 1, 20),
                                                'value', 10.0, 0.0, 'sum')
        sum_score = sum_target.calculate_scores(None)

        assert len(sum_score) == 1
        assert round(sum_score['sum_test'], 5) == 0.96

        mean_target = _DummyRangeTargetDecorator(target, 'mean_test', datetime(2019, 1, 1, 6), datetime(2019, 1, 1, 20),
                                                 'value', 10.0, 0.0, 'mean')
        mean_score = mean_target.calculate_scores(None)

        assert len(mean_score) == 1
        assert round(mean_score['mean_test'], 5) == 0.32


class _DummyIdealValueTargetDecorator(IdealValueTargetDecorator):

    def get_forecast_metrics(self) -> Set[str]:
        pass


class TestIdealValueTargetDecorator:

    def test_calculate_score(self):

        df = DataFrame([
            {'datetime': datetime(2019, 1, 1, 1), 'value': 1.0},
            {'datetime': datetime(2019, 1, 1, 8), 'value': 2.1},
            {'datetime': datetime(2019, 1, 1, 14), 'value': 3.2},
            {'datetime': datetime(2019, 1, 1, 20), 'value': 4.3},
            {'datetime': datetime(2019, 1, 2, 1), 'value': 5.4},
        ])

        target = WeatherTarget('not used')
        target.set_forecast_data(df)

        ideal_target = _DummyIdealValueTargetDecorator(target, 'ideal_test',
                                                       datetime(2019, 1, 1, 6), datetime(2019, 1, 1, 20),
                                                       'value', 10.0, 0.0, 5.0)
        scores = ideal_target.calculate_scores(None)

        assert len(scores) == 1
        assert round(scores['ideal_test'], 5) == 0.82

        ideal_target = _DummyIdealValueTargetDecorator(target, 'ideal_test',
                                                       datetime(2019, 1, 1, 6), datetime(2019, 1, 1, 20),
                                                       'value', 10.0, 0.0, 0.0)
        scores = ideal_target.calculate_scores(None)

        assert len(scores) == 1
        assert round(scores['ideal_test'], 5) == 0.68


class _DummyDataWeatherTarget(WeatherTarget):

    def generate_forecast_data(self, spot: Spot, metrics: Set[str]) -> ForecastWeatherFeed:

        print(spot.get_lat())
        print(spot.get_long())

        if spot.get_lat() == 78.0 and spot.get_long() == 104.0:

            df = DataFrame([
                {'datetime': datetime(2019, 1, 1, 1), 'temp': 210.0},
                {'datetime': datetime(2019, 1, 1, 8), 'temp': 254.2},
                {'datetime': datetime(2019, 1, 1, 14), 'temp': 304.2},
                {'datetime': datetime(2019, 1, 1, 20), 'temp': 298.0},
                {'datetime': datetime(2019, 1, 2, 1), 'temp': 301.0},
            ])

        elif spot.get_lat() == 2.3 and spot.get_long() == 101.2:

            df = DataFrame([
                {'datetime': datetime(2019, 1, 1, 1), 'temp': 242.0},
                {'datetime': datetime(2019, 1, 1, 8), 'temp': 244.2},
                {'datetime': datetime(2019, 1, 1, 14), 'temp': 224.2},
                {'datetime': datetime(2019, 1, 1, 20), 'temp': 233.0},
                {'datetime': datetime(2019, 1, 2, 1), 'temp': 301.5},
            ])

        else:
            raise AssertionError('Spot coordinates are not supported')

        return df


class TestEvaluateSpots:

    def test_score_spots_ideal_temp(self):

        spot_a = Spot('spot_a', 78.0, 104.0)
        spot_b = Spot('spot_b', 2.3, 101.2)
        spots = {spot_a, spot_b}

        target = _DummyDataWeatherTarget('not used')
        target = IdealTempTarget(target, 'ideal_temp', datetime(2019, 1, 1, 6), datetime(2019, 1, 1, 20), 220.0)

        spots = EvaluateSpots.score_spots(spots, target)

        for spot in spots:

            if spot.get_name() == 'spot_a':
                assert len(spot.get_scores()) == 1
                assert round(spot.get_scores()['ideal_temp'], 4) == 0.6727
            elif spot.get_name() == 'spot_b':
                assert len(spot.get_scores()) == 1
                assert round(spot.get_scores()['ideal_temp'], 4) == 0.931

            else:
                raise AssertionError('Did not expect spot %s' % spot.get_name())


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
