import pandas as pd
from src.core.indicators import moving_average, rsi, exponential_moving_average

def test_moving_average():
    s = pd.Series([1, 2, 3, 4, 5], dtype=float)
    ma = moving_average(s, window=2)
    assert ma.iloc[0] == 4.5

def test_rsi():
    s = pd.Series([1,2,3,2,1,2,3], dtype=float)
    result = rsi(s)
    assert result.notna().all()

def test_exponential_moving_average():
    s = pd.Series([1, 2, 3, 4, 5], dtype=float)
    ema = exponential_moving_average(s, window=2)
    assert isinstance(ema, pd.Series)
    assert len(ema) == len(s)