"""
Interacts with the portfolio to buy and sell positions.
"""

from backtesting.portfolio.portfolio import Portfolio

class Broker(Portfolio):

    def buy(self, portfolio_pct: float, price: float) -> None:
        """
        Buys a percentage of the portfolio at the given price.
        """
        if portfolio_pct <= 0 or portfolio_pct > 1:
            raise ValueError("Portfolio percentage must be between 0 and 1.")
        
        cost = portfolio_pct * self.liquidity
        stock_count = cost / price
        
        if stock_count <= 0:
            raise ValueError("Cannot buy zero or negative stock count.")
        
        self.stock_count += stock_count
        self.liquidity -= cost


    def sell(self, portfolio_pct: float, price: float) -> None:
        """
        Sells a percentage of the portfolio at the given price.
        """
        if portfolio_pct <= -1 or portfolio_pct > 0:
            raise ValueError("Portfolio percentage must be between -1 and 0.")
        
        portfolio_pct = abs(portfolio_pct)
        if portfolio_pct > 1:
            raise ValueError("Portfolio percentage cannot exceed 1.")
        
        stock_count_to_sell = self.stock_count * portfolio_pct
        
        if stock_count_to_sell <= 0:
            raise ValueError("Cannot sell zero or negative stock count.")
        
        self.stock_count -= stock_count_to_sell
        self.liquidity += stock_count_to_sell * price


