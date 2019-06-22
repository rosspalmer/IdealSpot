from collections import defaultdict

from pandas import DataFrame

from optimizer import Spot


class WeatherDataBase:

    def __init__(self):
        self.tables = defaultdict(dict)

    def get_table(self, spot: Spot, table_name: str) -> DataFrame:
        return self.tables[spot][table_name]

    def set_table(self, spot: Spot, table_name: str, df: DataFrame):
        self.tables[spot][table_name] = df
