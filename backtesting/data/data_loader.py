"""
This class is responsible for loading and validating data that the user provides.
This class is designed to strictly prohibit any form of data leakage so the user can fully trust
the results of their analysis.

Accepts a pandas data frame to allow users to specify where the want to retrieve their data from.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

import pandas as pd


@dataclass
class MarketDataPoint:
    """This class represents the datapoints that will be iterated over"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class MarketData(Iterator[MarketDataPoint]):

    def __init__(self, data: pd.DataFrame):
        """Initialize with dataframe that requires timestamp, open, high, low, close, and volume."""
        self.data = data.sort_values(by='timestamp')
        self.current_index = 0

    def __iter__(self):
        """Returns itself"""
        return self

    def __next__(self):
        """Returns the next data point"""
        if self.current_index >= len(self.data):
            raise StopIteration

        row = self.data[self.current_index]
        self.current_index += 1
        return MarketDataPoint(
            timestamp=row['timestamp'],
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            volume=row['volume']
        )

