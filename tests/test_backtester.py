import pandas as pd
from src.core.strategy import SimpleMovingAverageStrategy, RSIStrategy
from src.core.backtester import Backtester
from src.risk.risk_manager import RiskManager, RiskParams

def test_backtester_sma():
    prices = pd.Series([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], dtype=float)
    strategy = SimpleMovingAverageStrategy(short_window=3, long_window=5)
    risk = RiskManager(10000, RiskParams())
    backtester = Backtester(prices, strategy, risk_manager=risk)
    backtester.run()
    assert isinstance(backtester.metrics, dict)
    assert "sharpe_ratio" in backtester.metrics
    assert "max_drawdown" in backtester.metrics

def test_backtester_rsi():
    prices = pd.Series([1,2,3,2,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], dtype=float)
    strategy = RSIStrategy(lower=30, upper=70, window=3)
    risk = RiskManager(10000, RiskParams())
    backtester = Backtester(prices, strategy, risk_manager=risk)
    backtester.run()
    assert isinstance(backtester.metrics, dict)
    assert "sharpe_ratio" in backtester.metrics
    assert "max_drawdown" in backtester.metrics