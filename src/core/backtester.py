import pandas as pd
from typing import Dict, Any
from src.core.strategy import trend_following_strategy

class Backtester:
    """
    Backtester runs a strategy over historical data and computes performance metrics.
    """
    def __init__(self, price_series: pd.Series):
        self.prices = price_series
        self.signals = []
        self.returns = []

    def run_backtest(self) -> None:
        # Generate signals
        self.signals = trend_following_strategy(self.prices)

        # Compute returns: assume strategy holds 1 unit per signal
        self.returns = []
        for i in range(1, len(self.prices)):
            prev_price = self.prices.iloc[i-1]
            curr_price = self.prices.iloc[i]
            signal = self.signals[i-1]
            ret = (curr_price - prev_price) / prev_price if signal == 'BUY' else 0
            self.returns.append(ret)

    def get_performance_metrics(self) -> Dict[str, Any]:
        df = pd.Series(self.returns)
        return {
            'total_return': df.sum(),
            'average_return': df.mean(),
            'sharpe_ratio': df.mean() / df.std() * (252**0.5)
        }