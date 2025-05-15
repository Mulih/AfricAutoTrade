import pandas as pd

def moving_average(series: pd.Series[float], window: int) -> pd.Series[float]:
    """
    Calculate the simple moving average.

    :param series: Price series.
    :param window: Window size.
    :return: Moving average series.
    """
    return series.rolling(window=window, min_periods=1).mean()

def rsi(series: pd.Series[float], window: int = 14) -> pd.Series[float]:
    """
    Calculate the Relative Strength Index (RSI).

    :param series: Price series.
    :param window: RSI window.
    :return: RSI values as a pandas Series.
    """
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = delta.clip(upper=0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / (avg_loss +1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def exponential_moving_average(series: pd.Series[float], window: int) -> pd.Series[float]:
    """
    Calculate the exponential moving average.

    :param series: Price series.
    :param window: Window size.
    :return: EMA series.
    """
    return series.ewm(span=window, adjust=False).mean()