from dataclasses import dataclass

@dataclass
class Portfolio:
    initial_investment: float = 25000
    liquidity: float = 25000
    stock_count: int = 0
