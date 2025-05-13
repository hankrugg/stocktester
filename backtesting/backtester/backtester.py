"""
This is the class where all the work will be done.
"""

from abc import ABC, abstractmethod
from typing import List

class Backtester(ABC):
    def __init__(self, market_data):
        self.market_data = market_data
        self.portfolio_value_history = []

    @abstractmethod
    def make_decision(self, data_point):
        """
        Must be implemented by the user.
        Returns the number of stocks to buy (>0) or sell (<0).
        """
        pass

    def run_simulation(self):
        """
        Runs through all market data and simulates trading.
        """
        portfolio = Portfolio()
        for data_point in self.market_data:
            decision = self.make_decision(data_point)

            # Assume simple logic: buy/sell at the current close price
            price = data_point.close
            if decision > 0:
                cost = decision * price
                if portfolio.liquidity >= cost:
                    portfolio.stock_count += decision
                    portfolio.liquidity -= cost
            elif decision < 0:
                sell_amount = min(-decision, portfolio.stock_count)
                portfolio.stock_count -= sell_amount
                portfolio.liquidity += sell_amount * price

            # Record portfolio value
            current_value = portfolio.liquidity + portfolio.stock_count * price
            self.portfolio_value_history.append(current_value)

        return self.portfolio_value_history
