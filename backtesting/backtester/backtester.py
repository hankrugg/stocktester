from abc import ABC, abstractmethod
from typing import List, Iterable
from backtesting.portfolio.portfolio import Portfolio
from backtesting.portfolio.broker import Broker
from backtesting.data.data_loader import MarketDataPoint

class Backtester(ABC):
    def __init__(self, market_data: Iterable[MarketDataPoint]):
        """
        Accepts an iterable of MarketDataPoint, such as an instance of MarketData.
        """
        self.market_data = market_data
        self.portfolio_value_history = []
        self.past_data = []
        self.MAX_BUY_PCT = 1
        self.MAX_SELL_PCT = -1


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
            decision = self.make_decision(data_point)
            decision = max(min(self.MAX_BUY_PCT, decision), self.MAX_SELL_PCT) # clip range between -1,1
            return decision
        except Exception as e:
            print(f"Error in decision for {data_point.timestamp}. {e}. Holding position.")
            return 0



    def run_simulation(self, initial_investment) -> List[float]:
        """
        Runs through all market data and simulates trading.
        """
        portfolio = Portfolio(initial_investment=initial_investment)
        broker = Broker(portfolio)
        for data_point in self.market_data:
            decision = self._make_decision_wrapper(data_point)

            price = data_point.close
            if decision > 0: # buy
                broker.buy(portfolio_pct=decision, price=price)
 
            elif decision < 0: # sell
                broker.sell(portfolio_pct=decision, price=price)

            # Record portfolio value
            current_value = portfolio.liquidity + portfolio.stock_count * price
            self.portfolio_value_history.append(current_value)
            self.past_data.append(data_point)

        return self.portfolio_value_history
