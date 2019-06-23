from typing import Set, Dict

from pandas import DataFrame

from ideal_spot.spots import Spot
from ideal_spot.targets import WeatherTarget


class EvaluateSpots:
    """
    EvaluateSpots is a functional class with main static
    methods for processing Spots and data
    """

    @staticmethod
    def generate_spots(df: DataFrame, name_column: str, lat_column: str, long_column: str) -> Set[Spot]:
        """
        Convert pandas DataFrame into set of Spot classes

        Parameters
        ----------
        df : DataFrame
            pandas DataFrame with spot data for each row, requires three columns below
        name_column : str
            Name of column for string spot name
        lat_column : str
            Name of column for latitude float value
        long_column : str
            Name of column for longitude float value

        Returns
        -------
        Set[Spot]
            Set of configured Spot classes
        """

        spots_data = df[[name_column, lat_column, long_column]].to_dict('records')

        spots = set()
        for spot_data in spots_data:
            spot = Spot(spot_data[name_column], spot_data[lat_column], spot_data[long_column])
            spots.add(spot)

        return spots

    @staticmethod
    def score_spots(spots: Set[Spot], target: WeatherTarget, score_weight_map: Dict[str, float] = None) -> Set[Spot]:
        """
        Apply scoring to a set of Spots using a configured WeatherTarget.
        An weight map may be used to adjust the individual weight of the
        WeatherTarget decorators. The string keys are based on the names
        specified for the individual decorator.

        Parameters
        ----------
        spots : Set[Spot]
            Set of un-scored spots
        target : WeatherTarget
            Configure WeatherTarget class used to generate scores
        score_weight_map : Dict[str, float]
            Optional weight map for WeatherClass decorators

        Returns
        -------
        Set[Spot]
            Set of Spots with scores and overall score set
        """

        for spot in spots:

            target.evaluate_spot(spot)

            overall_score = 0.0
            for score_name, score in spot.get_scores().items():

                weight = 1.0
                if score_weight_map is not None and score_name in score_weight_map:
                    weight = score_weight_map[score_name]
                overall_score += score * weight

            spot.set_overall_score(overall_score)

        return spots
