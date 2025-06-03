from abc import ABC, abstractmethod
from typing import List, Iterable
from backtrader.backtesting.portfolio.portfolio import Portfolio
from backtrader.backtesting.data.data_loader import MarketDataPoint

class Backtester(ABC):
    def __init__(self, market_data: Iterable[MarketDataPoint]):
        """
        Accepts an iterable of MarketDataPoint, such as an instance of MarketData.
        """
        self.market_data = market_data
        self.portfolio_value_history = []

    @abstractmethod
    def make_decision(self, data_point: MarketDataPoint) -> int:
        """
        Must be implemented by the user.
        Returns the number of stocks to buy (>0) or sell (<0).
        """
        pass

    def _make_decision_wrapper(self, data_point):
        """
        Adds validation to make_decision function
        """
        try:
            self.make_decision(data_point)
        except:
            Warning(f"Error in decision for {data_point.timestamp}. Holding position")
            return 0



    def run_simulation(self) -> List[float]:
        """
        Runs through all market data and simulates trading.
        """
        portfolio = Portfolio()
        for data_point in self.market_data:
            decision = self._make_decision_wrapper(data_point)

            # THIS IS WRONG. DECISION IS BASED ON THE AMOUNT OF LIQUID CASH IN THE PORTFOLIO NOT THE AMOUNT OF STOCKS TO BUY

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
