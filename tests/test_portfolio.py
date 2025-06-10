import unittest
from backtesting.portfolio.portfolio import Portfolio

class TestPortfolio(unittest.TestCase):
    
    def setUp(self):
        self.portfolio = Portfolio(initial_investment=10000)

    def test_initial_values(self):
        self.assertEqual(self.portfolio.initial_investment, 10000)
        self.assertEqual(self.portfolio.liquidity, 10000)
        self.assertEqual(self.portfolio.stock_count, 0)

    def test_set_valid_liquidity(self):
        self.portfolio.liquidity = 5000
        self.assertEqual(self.portfolio.liquidity, 5000)

    def test_set_invalid_liquidity(self):
        with self.assertRaises(ValueError):
            self.portfolio.liquidity = -100

    def test_set_valid_stock_count(self):
        self.portfolio.stock_count = 20
        self.assertEqual(self.portfolio.stock_count, 20)

    def test_set_invalid_stock_count(self):
        with self.assertRaises(ValueError):
            self.portfolio.stock_count = -5

if __name__ == '__main__':
    unittest.main()
