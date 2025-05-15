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

class RSIStrategy(StrategyBase):
    """
    RSI-based mean reversion strategy.
    """
    def __init__(self, lower: float = 30, upper: float = 70, window: int = 14):
        self.lower = lower
        self.upper = upper
        self.window = window

    def generate_signals(self, prices: pd.Series[float | int]) -> List[str]:
        delta = prices.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=self.window, min_periods=1).mean()
        avg_loss = loss.rolling(window=self.window, min_periods=1).mean()
        rs = avg_gain / (avg_loss + 1e-9)
        rsi = 100 - (100 / (1 + rs))
        signals: List[str] = []
        for val in rsi:
            if val < self.lower:
                signals.append('BUY')
            elif val > self.upper:
                signals.append('SELL')
            else:
                signals.append('HOLD')
        return signals


from typing import Any

def get_Strategy(name: str, **kwargs: Any) -> StrategyBase:
    """
    Factory to get a strategy by name.
    :param name: Name of the strategy ("sma" or "rsi")
    :param kwargs: Parameters for the strategy.
    :return: instance of a StrategyBase subclass
    """
    if name == "sma":
        return SimpleMovingAverageStrategy(**kwargs)
    elif name == "rsi":
        return RSIStrategy(**kwargs)
    else:
        raise ValueError(f"Unknown strategy: {name}")