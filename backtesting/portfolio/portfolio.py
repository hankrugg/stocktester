"""
Created on Mon Mar 31 2024
"""

from dataclasses import dataclass, field

@dataclass
class Portfolio():
    initial_investment: float = 25000.0
    _liquidity: float = field(init=False)
    _stock_count: int = field(init=False)

    def __post_init__(self):
        self._liquidity = self.initial_investment
        self._stock_count = 0

    @property
    def liquidity(self) -> float:
        return self._liquidity

    @liquidity.setter
    def liquidity(self, value: float):
        if value < 0:
            raise ValueError("Liquidity cannot be negative")
        self._liquidity = value

    @property
    def stock_count(self) -> int:
        return self._stock_count

    @stock_count.setter
    def stock_count(self, value: int):
        if value < 0:
            raise ValueError("Stock count cannot be negative")
        self._stock_count = value
