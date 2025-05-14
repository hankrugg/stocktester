"""
Created May 14



"""

def sharpe_ratio(expected_portfolio_return, risk_free_return, portfolio_std_dev):
    return (expected_portfolio_return - risk_free_return) / portfolio_std_dev
