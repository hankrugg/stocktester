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
        self.data = self.validate_data(data.sort_values(by='timestamp'))
        self.current_index = 0

    def __iter__(self):
        """Returns itself"""
        return self

    def __next__(self):
        """Returns the next data point"""
        if self.current_index >= len(self.data):
            raise StopIteration

        row = self.data.iloc[self.current_index]
        self.current_index += 1
        return MarketDataPoint(
            timestamp=row['timestamp'],
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            volume=row['volume']
        )

    @staticmethod
    def validate_data(data: pd.DataFrame) -> pd.DataFrame:
        """Validates the data"""
        if data.empty:
            raise ValueError('Data is empty')

        valid_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        for column in valid_columns:
            if column not in data.columns:
                raise KeyError('Column "{}" is missing'.format(column))

        data = data[valid_columns]  # take only the columns that we want if there were other columns included

        data = data.ffill()  # if there are data missing, fill it with the previous data

        data = data.dropna()   # all the data should be filled, but there is no way to forward fill the
        # first row, this would drop the first row

        data.reset_index(drop=True, inplace=True)  # if the first row was dropped, the index needs to be reset

        data = cast_types(data)  # change the types of the data to what we expect

        return data


def cast_types(data: pd.DataFrame) -> pd.DataFrame:
    """Casts data as correct types"""
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['open'] = data['open'].astype(float)
    data['high'] = data['high'].astype(float)
    data['low'] = data['low'].astype(float)
    data['close'] = data['close'].astype(float)
    data['volume'] = data['volume'].astype(float)
    return data
