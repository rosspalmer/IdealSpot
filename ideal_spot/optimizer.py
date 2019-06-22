from typing import Dict, Set

from ideal_spot.targets import WeatherTarget


class Spot:

    def __init__(self, name: str, lat: float, long: float):
        self.name = name
        self.lat = lat
        self.long = long

        self.scores = dict()
        self.overall_score = 0.0

    def calculate_overall_score(self):
        self.overall_score = 0.0
        for score in self.scores.values():
            self.overall_score += score

    def set_score(self, name: str, score: float):
        self.scores[name] = score

    def get_overall_score(self) -> float:
        return self.overall_score

    def __eq__(self, other) -> bool:
        return self.lat == other.lat and self.long == other.long

    def __hash__(self) -> int:
        return hash([self.lat, self.long])


class EvaluateSpots:

    @staticmethod
    def score_spots(spots: Set[Spot], target_weight_map: Dict[WeatherTarget, float]) -> Set[Spot]:

        for spot in spots:

            for target, weight in target_weight_map.items():
                score = target.calculate_objective(spot)
                spot.set_score(target.get_name(), score * weight)

            spot.calculate_overall_score()

        return spots
