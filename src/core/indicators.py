import pandas as pd

def moving_average(series: pd.Series, window: int) -> pd.Series:
    """Simple moving average"""
    return series.rolling(window=window).mean()

def exponential_moving_average(series: pd.Series, span: int) -> pd.Series:
    """Exponential moving average"""
    return series.ewm(span=span, adjust=False).mean()

def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """Relative Strength Index"""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))