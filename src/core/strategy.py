from typing import List
import pandas as pd
from src.core.indicators import moving_average, rsi

def trend_following_strategy(prices: pd.Series) -> List[str]:
    """
    Simple trend-following: buy when price > MA(50). sell when price < MA(50).
    Returns a list of 'BUY', 'SELL', or 'HOLD' signals.
    """
    signals = []
    ma50 = moving_average(prices, window=50)
    for price, ma in zip(prices, ma50):
        if pd.isna(ma):
            signals.append('HOLD')
        elif price > ma:
            signals.append('BUY')
        elif price < ma:
            signals.append('SELL')
        else:
            signals.append('HOLD')
    return signals

def rsi_strategy(prices: pd.Series) -> List[str]:
    """
    RSI-based strategy: buy when RSI < 30 (oversold). sell when RSI > 70 (overbought).
    """
    signals = []
    rsi_vals = rsi(prices)
    for val in rsi_vals:
        if pd.isna(val):
            signals.append('HOLD')
        elif val < 30:
            signals.append('BUY')
        else:
            signals.append('HOLD')
    return signals