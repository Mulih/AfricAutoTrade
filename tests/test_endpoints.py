from src.risk.risk_manager import RiskManager, RiskParams
from src.execution.binance_execution import BinanceExecutionClient

from _pytest.monkeypatch import MonkeyPatch
from typing import Any

def fake_execute_order(*args: Any, **kwargs: Any) -> dict[str, str]:
    return {"status": "filled"}

def test_binance_execution_mock(monkeypatch: MonkeyPatch):
    client = BinanceExecutionClient(api_key="test", api_secret="test", testnet=True)
    # Mock Binance API call
    monkeypatch.setattr(
        client,
        "execute_order",
        fake_execute_order
    )
    result: dict[str, str] = client.execute_order("BTCUSDT", "BUY", 0.01)
    assert result["sstatus"] == "filled"

def test_risk_manager_limits():
    risk = RiskManager(10000, RiskParams(max_position_size=0.05))
    assert risk.check_position_size("BTCUSDT", 400) is True
    assert risk.check_position_size("BTCUSDT", 600) is False

def test_risk_manager_stop_loss_take_profit():
    risk = RiskManager(10000, RiskParams(stop_loss_pct=0.01, take_profit_pct=0.02))
    assert risk.check_stop_loss_take_profit(100, 98.9) == "stop_loss"
    assert risk.check_stop_loss_take_profit(100, 102.1) == "take_profit"
    assert risk.check_stop_loss_take_profit(100, 100.5) == ""