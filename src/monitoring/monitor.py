import logging
import time

class TradingMonitor:
    def __init__(self, log_file='trading_bot.log'):
        self.log_file = log_file
        self.logger = self._setup_logger()
        self.performance_metrics = {
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
