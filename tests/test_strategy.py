import pandas as pd
from src.core.strategy import SimpleMovingAverageStrategy, RSIStrategy

def test_simple_moving_average_strategy():
    prices = pd.Series([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], dtype=float)
    strategy = SimpleMovingAverageStrategy(short_window=3, long_window=5)
    signals = strategy.generate_signals(prices)
    assert len(signals) == len(prices)
    assert all(signal in ['BUY', 'SELL', 'HOLD'] for signal in signals)

def test_rsi_strategy():
    prices = pd.Series([1,2,3,4,5,6,7,8,9,10,11], dtype=float)
    strategy = RSIStrategy(lower=30, upper=70, window=3)
    signals = strategy.generate_signals(prices)
    assert len(signals) == len(prices)
    assert all(signal in ['BUY', 'SELL', 'HOLD'] for signal in signals)