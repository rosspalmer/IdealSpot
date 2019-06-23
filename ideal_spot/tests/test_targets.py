from datetime import datetime
from typing import Set

from pandas import DataFrame
import pytest

from targets import RangeTargetDecorator, WeatherTarget, IdealValueTargetDecorator


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


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
