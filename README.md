# BackTrader  

**BackTrader** is a Python framework for backtesting trading strategies. It provides a flexible and efficient environment for traders, quants, and researchers to simulate and evaluate trading algorithms using historical market data.  

## Features  
- **Fast Execution** – Optimized for large datasets and complex strategies.  
- **Performance Metrics** – Includes Sharpe ratio, drawdown analysis, and trade statistics.  

## Installation  
Create a new Conda environment and install BackTrader:  
```sh
conda create -n BackTrader-env python=3.10 -y  
conda activate BackTrader-env  
pip install BackTrader  
```

To install the latest development version from source:  
```sh
git clone https://github.com/hankrugg/BackTrader.git  
cd BackTrader  
pip install .  
```

## Quick Start  
Run a simple moving average crossover strategy in just a few lines:  
```python
from BackTrader import Backtester, Strategy

class SMACrossover(Strategy):
    def next(self):
        if self.sma(50) > self.sma(200):
            self.buy()
        elif self.sma(50) < self.sma(200):
            self.sell()

backtester = Backtester(data="AAPL.csv", strategy=SMACrossover)
results = backtester.run()
results.plot()
```

## Documentation  
See the full [documentation](https://github.com/hankrugg/BackTrader/wiki) for API details and examples.  

## Contributing  
Contributions are welcome! Open an issue or submit a pull request to improve BackTrader.  

## License  
BackTrader is licensed under the MIT License.  
