from datetime import datetime
from typing import Set

import pytest
from pandas import DataFrame

from ideal_spot.evaluate import EvaluateSpots
from ideal_spot.feed import ForecastWeatherFeed
from ideal_spot.spots import Spot
from ideal_spot.targets import IdealTempTarget, WeatherTarget


class _DummyDataWeatherTarget(WeatherTarget):

    def generate_forecast_data(self, spot: Spot, metrics: Set[str]) -> ForecastWeatherFeed:

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

    def test_generate_spots(self):

        df = DataFrame([
            {'spot_name': 'spot_a', 'spot_lat': 78.0, 'spot_long': 104.0},
            {'spot_name': 'spot_b', 'spot_lat': 2.3, 'spot_long': 101.2},
        ])

        spots = EvaluateSpots.generate_spots(df, 'spot_name', 'spot_lat', 'spot_long')

        assert isinstance(spots, set)
        assert len(spots) == 2

        for spot in spots:

            assert isinstance(spot, Spot)

            if spot.get_name() == 'spot_a':
                assert round(spot.get_lat(), 4) == 78.0
                assert round(spot.get_long(), 4) == 104.0
            elif spot.get_name() == 'spot_b':
                assert round(spot.get_lat(), 4) == 2.3
                assert round(spot.get_long(), 4) == 101.2

            else:
                raise AssertionError('Did not expect spot')

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
