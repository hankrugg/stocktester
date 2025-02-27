"""
This class is responsible for loading and validating data that the user provides.
This class is designed to strictly prohibit any form of data leakage so the user can fully trust
the results of their analysis.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class DataLoader:
    ticker: str
    start_date: datetime.date
    end_date: datetime.date