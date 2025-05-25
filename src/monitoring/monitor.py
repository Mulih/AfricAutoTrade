import logging
import time
from typing import Any, Optional, Dict

class TradingMonitor:
    def __init__(self, log_file: str = 'trading_bot.log'):
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

    def log_event(self, level: str, message: str, trade_details: Optional[Dict[str, Any]] =None):
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

    def update_metrics(self, trade_result: Optional[Dict[str, Any]] = None, current_balance: Optional[float] = None):
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


    def send_alert(self, message: str):
        """Sends an alert (e.g., via email, SMS, or Slack)."""
        self.log_event('warning', f"ALERT: {message}")
        # Integrate notification service AWS SNS
        print(f"--- ALERT SENT: {message} ---")

    def get_current_metrics(self):
        return self.performance_metrics

if __name__ == "__main__":
    monitor = TradingMonitor()

    monitor.log_event('info', "Bot started successfully.")
    monitor.log_event('warning', "High volatility detected.")
    monitor.log_event('error', "Failed to connect to market data API.", trade_details={'api': 'example.com'})

    # Simulate trade updates
    monitor.update_metrics(trade_result={'status': 'success', 'profit_loss': 10.50}, current_balance=10010.50)
    monitor.update_metrics(trade_result={'status': 'success', 'profit_loss': -5.00}, current_balance=10005.50)
    monitor.update_metrics(trade_result={'status': 'failed', 'error': 'Insufficient funds'})

    monitor.update_metrics(current_balance=9999.00)

    monitor.send_alert("Low cash balance. Consider pausing trading.")

    print("\nFinal Metrics:", monitor.get_current_metrics())

    # Simulate a loop
    for i in range(3):
        monitor.log_event('info', f"Processing cycle {i+1}")
        time.sleep(1)