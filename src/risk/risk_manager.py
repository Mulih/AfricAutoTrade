import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RiskParams:
    """
    Parameters for risk management
    """
    def __init__(
        self,
        max_position_size: float = 0.1,     # Max 10% capital per trade
        max_daily_loss: float = 0.05,       # Max 5% daily loss
        max_open_trades: int = 5,
        stop_loss_pct: float = 0.02,        # 2% stop loss
        take_profit_pct: float = 0.04       # 4% take profit
    ):
        self.max_position_size = max_position_size
        self.max_daily_loss = max_daily_loss
        self.max_open_trades = max_open_trades
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct

class RiskManager:
    """
    Enforces risk management rules for trading.
    """
    def __init__(self, capital: float, params: RiskParams):
        """
        :param capital: Total trading capital.
        :param params: RiskParams instance.
        """
        self.capital = capital
        self.params = params
        self.open_trades: Dict[str, Dict[str, Any]] = {}
        self.daily_loss = 0.0

    def check_position_size(self, symbol: str, order_size: float) -> bool:
        """
        Check if the order size is within allowed risk limits.
        """
        max_allowed = self.capital * self.params.max_position_size
        if order_size > max_allowed:
            logger.warning(f"Order size {order_size} exceeds max allowed {max_allowed} for {symbol}")
            return False
        return True

    def check_daily_loss(self, loss: float) -> bool:
        """
        Check if the daily loss limit has been breached.
        """
        self.daily_loss += loss
        if self.daily_loss > self.capital * self.params.max_daily_loss:
            logger.error("Daily loss limit breached. Trading halted for the day.")
            return False
        return True

    def can_open_trade(self) -> bool:
        """
        Check if a new trade can be opened based on max open trades.
        """
        if len(self.open_trades) >= self.params.max_open_trades:
            logger.warning("Max open trades reached.")
            return False
        return True

    def register_trade(self, symbol: str, trade_info: Dict[str, Any]) -> None:
        """
        Register a new open trade.
        """
        self.open_trades[symbol] = trade_info
        logger.info(f"Registered trade for {symbol}: {trade_info}")

    def close_trade(self, symbol: str) -> None:
        """
        Remove a trade from open trades.
        """
        if symbol in self.open_trades:
            logger.info(f"Closing trade for {symbol}")
            del self.open_trades[symbol]

    def check_stop_loss_take_profit(self, entry_price: float, current_price: float) -> str:
        """
        Check if stop loss or take profit is triggered.
        Returns 'stop_loss', 'take_profit', or ''.
        """
        change_pct = (current_price - entry_price) / entry_price
        if change_pct <= -self.params.stop_loss_pct:
            logger.info(f"Stop loss triggered: {change_pct:.2%}")
            return 'stop_loss'
        elif change_pct >= self.params.take_profit_pct:
            logger.info(f"Take profit triggered: {change_pct:.2%}")
            return 'take_profit'
        return ''

    def reset_daily_loss(self) -> None:
        """
        Reset daily loss counter (call at start of new trading day).
        """
        logger.info("Resetting daily loss counter.")
        self.daily_loss = 0.0