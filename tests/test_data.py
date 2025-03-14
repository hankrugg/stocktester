import unittest
import sys
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv('local_path'))

from backtrader.backtesting.data.data_loader import MarketData, MarketDataPoint


class TestMarketData(unittest.TestCase):

    def setUp(self):
        """Set up test data"""
        self.valid_data = pd.DataFrame([
            {"timestamp": datetime(2024, 1, 1, 9, 30), "open": 100, "high": 105, "low": 99, "close": 102,
             "volume": 1000},
            {"timestamp": datetime(2024, 1, 1, 9, 31), "open": 102, "high": 106, "low": 101, "close": 103,
             "volume": 1100}
        ])

        self.missing_column_data = pd.DataFrame([
            {"timestamp": datetime(2024, 1, 1, 9, 30), "open": 100, "high": 105, "low": 99, "close": 102}
        ])  # Missing 'volume'

        self.nan_data = self.valid_data.copy()
        self.nan_data.loc[3, "close"] = None  # Introduce a NaN
        self.nan_data2 = self.valid_data.copy()
        self.nan_data2.loc[0, "close"] = None

    def test_valid_data(self):
        """Test MarketData loads valid data correctly"""
        loader = MarketData(self.valid_data)
        first_point = next(loader)
        self.assertIsInstance(first_point, MarketDataPoint)
        self.assertEqual(first_point.close, 102)

    def test_missing_column_raises_error(self):
        """Ensure missing columns raise an error"""
        with self.assertRaises(KeyError):
            MarketData(self.missing_column_data)

    def test_nan_handling(self):
        """Ensure NaN values are handled properly (should be forward filled)"""
        loader = MarketData(self.nan_data.ffill())  # Forward fill applied
        first_point = next(loader)
        self.assertEqual(first_point.close, 102)  # Should not be None

    def test_chronological_order(self):
        """Ensure data remains sorted"""
        shuffled_data = self.valid_data.sample(frac=1)  # Shuffle rows
        loader = MarketData(shuffled_data)
        timestamps = [next(loader).timestamp for _ in range(len(self.valid_data))]
        self.assertEqual(timestamps, sorted(timestamps))  # Must be sorted

    def test_stop_iteration(self):
        """Ensure StopIteration is raised when data is exhausted"""
        loader = MarketData(self.valid_data)
        list(loader)  # Exhaust iterator
        with self.assertRaises(StopIteration):
            next(loader)

    def test_data_change(self):
        """Ensure the iterator data does not change when the dataframe is changed"""
        loader = MarketData(self.valid_data)
        self.valid_data.iloc[0] = 0
        first_point = next(loader)
        self.assertNotEquals(first_point, 0)

    def test_data_change2(self):
        """Ensure the iterator data does not change when the dataframe is changed"""
        test_point = self.valid_data.iloc[0]
        loader = MarketData(self.valid_data)
        self.valid_data.iloc[0] = 0
        first_point = next(loader)
        self.assertEquals(test_point.timestamp, first_point.timestamp)
        self.assertEquals(test_point.open, first_point.open)
        self.assertEquals(test_point.high, first_point.high)
        self.assertEquals(test_point.low, first_point.low)
        self.assertEquals(test_point.close, first_point.close)
        self.assertEquals(test_point.volume, first_point.volume)



if __name__ == '__main__':
    unittest.main()
