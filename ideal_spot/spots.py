from typing import Any, Dict


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

    def get_name(self) -> str:
        return self.name

    def get_overall_score(self) -> float:
        return self.overall_score

    def get_scores(self) -> Dict[str, float]:
        return self.scores

    def set_overall_score(self, overall_score: float):
        self.overall_score = overall_score

    def set_scores(self, scores: Dict[str, float]):
        self.scores = scores

    def __eq__(self, other) -> bool:
        return self.get_name() == other.get_name()

    def __hash__(self) -> int:
        return hash(self.get_name())
