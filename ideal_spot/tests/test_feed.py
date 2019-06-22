
import pytest

from ideal_spot.feed import ForecastWeatherFeed, ForecastWeatherFeedFactory

# OpenWeatherMap free API key
TEST_API_KEY = '79094518408cb847574557c958eeec91'


class TestForecastWeatherFeed:

    def test_generate_data(self):

        feed = ForecastWeatherFeed(TEST_API_KEY, 40.0, 104.0)

        data = feed.get_data()

        assert len(data.index) == 40
        assert set(data.columns) == {'datetime'}


class TestTemperatureForecastDecorator:

    def test_generate_data(self):

        feed = ForecastWeatherFeedFactory(TEST_API_KEY, 40.0, 104.0).generate_feed({'temp'})

        data = feed.get_data()

        assert len(data.index) == 40
        assert set(data.columns) == {'datetime', 'temp', 'temp_min', 'temp_max'}


class TestRainForecastDecorator:

    def test_generate_data(self):

        feed = ForecastWeatherFeedFactory(TEST_API_KEY, 40.0, 104.0).generate_feed({'rain'})

        data = feed.get_data()

        assert len(data.index) == 40
        assert set(data.columns) == {'datetime', 'rain'}


class TestSnowForecastDecorator:

    def test_generate_data(self):

        feed = ForecastWeatherFeedFactory(TEST_API_KEY, 40.0, 104.0).generate_feed({'snow'})

        data = feed.get_data()

        assert len(data.index) == 40
        assert set(data.columns) == {'datetime', 'snow'}


class TestCloudForecastDecorator:

    def test_generate_data(self):

        feed = ForecastWeatherFeedFactory(TEST_API_KEY, 40.0, 104.0).generate_feed({'cloud'})

        data = feed.get_data()

        assert len(data.index) == 40
        assert set(data.columns) == {'datetime', 'cloud'}


class TestWindForecastDecorator:

    def test_generate_data(self):

        feed = ForecastWeatherFeedFactory(TEST_API_KEY, 40.0, 104.0).generate_feed({'wind'})

        data = feed.get_data()

        assert len(data.index) == 40
        assert set(data.columns) == {'datetime', 'wind'}


class TestForecastWeatherFeedFactory:

    def test_generate_data_all_metrics(self):

        feed = ForecastWeatherFeedFactory(TEST_API_KEY, 40.0, 104.0).generate_feed({'temp', 'rain', 'snow',
                                                                                    'cloud', 'wind'})

        data = feed.get_data()

        assert len(data.index) == 40
        assert set(data.columns) == {'datetime', 'temp', 'temp_min', 'temp_max',
                                     'rain', 'snow', 'cloud', 'wind'}


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
