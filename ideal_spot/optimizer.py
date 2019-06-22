from typing import Any, Dict, Set

from ideal_spot.targets import WeatherTarget


class Spot:

    def __init__(self, name: str, lat: float, long: float):
        self.name = name
        self.lat = lat
        self.long = long

        self.scores = dict()
        self.overall_score = 0.0
        self.data = dict()

    def add_data(self, name: str, data: Any):
        self.data[name] = data

    def get_data(self, name: str) -> Any:
        return self.data[name]

    def get_lat(self) -> float:
        return self.lat

    def get_long(self) -> float:
        return self.long

    def get_overall_score(self) -> float:
        return self.overall_score

    def get_scores(self) -> Dict[str, float]:
        return self.scores

    def set_overall_score(self, overall_score: float):
        self.overall_score = overall_score

    def set_scores(self, scores: Dict[str, float]):
        self.scores = scores

    def __eq__(self, other) -> bool:
        return self.lat == other.lat and self.long == other.long

    def __hash__(self) -> int:
        return hash([self.lat, self.long])


class EvaluateSpots:

    @staticmethod
    def score_spots(spots: Set[Spot], target: WeatherTarget, score_weight_map: Dict[str, float] = None) -> Set[Spot]:

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
