import logging
import time
from typing import Any

class TradingMonitor:
    def __init__(self, log_file='trading_bot.log'):
        self.log_file = log_file
        self.logger = self._setup_logger()
        self.performance_metrics: dict[str, Any] = {
            'trades_executed': 0,
            'profitable_trades': 0,
            'total_profit_loss': 0.0,
            'current_balance': 0.0
        }

    def _setup_logger(self):
        logger = logging.getLogger('TradingBot')
        logger.setLevel(logging.INFO)

        # File handler
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add handlers
        if not logger.handlers: # prevent adding handlers multiple times
            logger.addHandler(fh)
            logger.addHandler(ch)
        return logger

    def log_event(self, level: str, message: str, trade_details=None):
        """Logs an event with specified level."""
        if trade_details:
            message += f" Details: {trade_details}"
        if level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)
        else:
            self.logger.debug(message) # Default to debug for unknown levels

    def update_metrics(self, trade_result=None, current_balance=None):
        """Updates internal performance metrics."""
        if trade_result:
            self.performance_metrics['trades_executed'] += 1
            if trade_result.get('status') == 'success':
                # logic will be more complex for real P&L calculation
                # For now ill assume a successful trade implies profit or loss
                self.performance_metrics['total_profit_loss'] += trade_result.get('profit_loss', 0)
                if trade_result.get('profit_loss', 0) > 0:
                    self.performance_metrics['profitable_trades'] += 1

            if current_balance is not None:
                self.performance_metrics['current_balance'] = current_balance

            self.log_event('info', f"Metrics Updated: {self.performance_metrics}")