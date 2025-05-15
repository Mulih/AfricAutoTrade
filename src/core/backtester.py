import logging
from typing import List, Optional, Dict, Any
import pandas as pd
from src.core.strategy import StrategyBase
from src.risk.risk_manager import RiskManager
from src.core.metrics import sharpe_ratio, max_drawdown

logger = logging.getLogger(__name__)

class Backtester:
    """
    Backtesting engine for trading strategies.
    """
    def __init__(
            self,
            prices: pd.Series[float],
            strategy: StrategyBase,
            risk_manager: Optional[RiskManager] = None,
            slippage: float = 0.001,
            commission: float = 0.0005,
            walk_forward: Optional[int] = None
    ):
        """
        :param prices: Price series,
        :param strategy: Strategy instance.
        :param risk_manager: RiskManager instance.
        :param slippage: Slippage per trade (fractional).
        :param commission: Commission per trade (fractional).
        :param walk_forward: Window size for walk-forward testing.
        """
        self.prices         = prices
        self.strategy       = strategy
        self.risk_manager   = risk_manager
        self.slippage       = slippage
        self.commission     = commission
        self.walk_forward   = walk_forward
        self.signals:       List[str] = []
        self.returns:       List[float] = []
        self.metrics:       Dict[str, Any] = {}

    def run(self) -> None:
        """
        Run the backtest, applying strategy, risk, slippage and commission.
        """
        self.signals    = self.strategy.generate_signals(self.prices)
        self.returns    = []
        position        = 0 # 1 for long, 0 for flat
        entry_price     = None


        for i in range(1, len(self.prices)):
            signal = self.signals[i - 1]
            curr_price = self.prices.iloc[i]
            trade_return = 0

            if signal == 'BUY' and position == 0:
                position = 1
                entry_price = curr_price
                logger.info(f"Enter long at {curr_price}")
            elif signal == 'SELL' and position == 1 and entry_price is not None:
                # Exit position
                gross_return = (curr_price - entry_price) / entry_price
                net_return = gross_return - self.slippage - self.commission
                self.returns.append(net_return)
                logger.info(f"Exit long at {curr_price}, return: {net_return:.4f}")
                position = 0
                entry_price = None

            # Risk management: check stop loss/take profit if in position
            if self.risk_manager and position == 1 and entry_price is not None:
                risk_action = self.risk_manager.check_stop_loss_take_profit(entry_price, curr_price)
                if risk_action == 'stop_loss' or risk_action == 'take_profit':
                    gross_return = (curr_price - entry_price) / entry_price
                    net_return = gross_return - self.slippage - self.commission
                    trade_return = net_return
                    logger.info(f"Risk exit ({risk_action}) at {curr_price}, net_return")
                    position = 0
                    entry_price = None

            self.returns.append(trade_return)

        self.metrics = self.compute_metrics()

    def compute_metrics(self) -> Dict[str, Any]:
        """
        Compute performance metrics for the backseat.
        """
        returns_series = pd.Series(self.returns)
        metrics: Dict[str, Any] = {
            "sharpe_ratio": sharpe_ratio(returns_series),
            "max_drawdown": max_drawdown(returns_series),
            "total_return": returns_series.sum(),
            "num_trades": sum(1 for r in self.returns if r != 0)
        }
        logger.info(f"Backtest metrics: {metrics}")
        return metrics

    def walk_forward_test(self) -> List[Dict[str, Any]]:
        """
        Perform walk-forward testing if walk_forward is set.
        Returns a list of metrics for wach window.
        """
        if not self.walk_forward:
            return []
        results: List[Dict[str, Any]] = []
        n = len(self.prices)
        for start in range(0, n - self.walk_forward, self.walk_forward):
            end = start + self.walk_forward
            window_prices = self.prices.iloc[start:end]
            self.__init__(
                prices=window_prices,
                strategy=self.strategy,
                risk_manager=self.risk_manager,
                slippage=self.slippage,
                commission=self.commission,
                walk_forward=None
            )
            self.run()
            results.append(self.metrics)
        return results