import logging
from typing import List
import pandas as pd

logger = logging.getLogger(__name__)

class StrategyBase:
    """
    Abstract base class for trading strategies.
    """
    def generate_signals(self, prices: pd.Series[float | int]) -> List[str]:
        """
        Generate trading signals for a price series.
        :param prices: Series of prices.
        :return: List of signals ('BUY', 'SELL', 'HOLD').
        """
        raise NotImplementedError("Must implement generate_signals method.")

class SimpleMovingAverageStrategy(StrategyBase):
    """
    Simple moving average crossover strategy.
    """
    def __init__(self, short_window: int = 10, long_window: int = 30):
        self.short_window   = short_window
        self.long_window    = long_window

    def generate_signals(self, prices: pd.Series[float | int]) -> List[str]:
        if len(prices) < self.long_window:
            logger.warning("Not enough data for long window.")
            return ['HOLD'] * len(prices)
        short_ma = prices.rolling(window=self.short_window).mean()
        long_ma = prices.rolling(window=self.long_window).mean()
        signals: List[str] = []
        for i in range(len(prices)):
            if i < self.long_window:
                signals.append('HOLD')
            elif short_ma.iloc[i] > long_ma.iloc[i]:
                signals.append('BUY')
            elif short_ma.iloc[i] < long_ma.iloc[i]:
                signals.append('SELL')
            else:
                signals.append('HOLD')
        return signals