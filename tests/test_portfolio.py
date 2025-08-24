import unittest
import sys
import os

import numpy as np
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.getenv('local_path'))

from backtrader.backtesting.portfolio.portfolio import Portfolio

class TestPortfolio(unittest.TestCase):

    def test_initial_values(self):
        p = Portfolio()
        self.assertEqual(p.initial_investment, 25000)
        self.assertEqual(p.liquidity, 25000)
        self.assertEqual(p.stock_count, 0)

    def test_custom_initial_investment(self):
        p = Portfolio(initial_investment=100000)
        self.assertEqual(p.initial_investment, 100000)
        self.assertEqual(p.liquidity, 100000)
        self.assertEqual(p.stock_count, 0)

    def test_set_liquidity(self):
        p = Portfolio()
        p.liquidity = 10000
        self.assertEqual(p.liquidity, 10000)

    def test_set_liquidity_negative_raises(self):
        p = Portfolio()
        with self.assertRaises(ValueError):
            p.liquidity = -1

    def test_set_stock_count(self):
        p = Portfolio()
        p.stock_count = 5
        self.assertEqual(p.stock_count, 5)

    def test_set_stock_count_negative_raises(self):
        p = Portfolio()
        with self.assertRaises(ValueError):
            p.stock_count = -10

    def test_multiple_updates(self):
        p = Portfolio(initial_investment=5000)
        p.liquidity = 4000
        p.stock_count = 3
        self.assertEqual(p.liquidity, 4000)
        self.assertEqual(p.stock_count, 3)