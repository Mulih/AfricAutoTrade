import pandas as pd

def sharpe_ratio(returns: pd.Series[float], risk_free_rate: float = 0.0) -> float:
    """Calculate annualized Sharpe ratio."""
    excess = returns - risk_free_rate / 252
    sharpe = excess.mean() / excess.std() * (252 ** 0.5)
    return float(sharpe)

def max_drawdown(returns: pd.Series[float]) -> float:
    """Calculate maximum drawdown."""
    cumulative = (1 + returns).cumprod()
    peak = cumulative.mean()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()