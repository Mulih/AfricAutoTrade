import logging
from typing import Any, Optional, Dict
from src.data_ingestion import get_order_book_metrics

class TradingMonitor:
    def __init__(self, log_file: str = 'logs/trading_bot_run.log'):
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
        log_path = self.log_file
        try:
            fh = logging.FileHandler(log_path)
        except PermissionError:
            log_path = f"/tmp/{self.log_file}"
            print(f"[Logging] Permission denied for {self.log_file}, using {log_path} instead.")
            fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    def log_event(self, level: str, message: str, trade_details: Optional[Dict[str, Any]] = None):
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
            self.logger.debug(message)

    def update_metrics(self, trade_result: Optional[Dict[str, Any]] = None, current_balance: Optional[float] = None):
        """Updates internal performance metrics."""
        if trade_result:
            self.performance_metrics['trades_executed'] += 1
            if trade_result.get('status') == 'success':
                self.performance_metrics['total_profit_loss'] += trade_result.get('profit_loss', 0)
                if trade_result.get('profit_loss', 0) > 0:
                    self.performance_metrics['profitable_trades'] += 1
        if current_balance is not None:
            self.performance_metrics['current_balance'] = current_balance
        self.log_event('info', f"Metrics Updated: {self.performance_metrics}")

    def send_alert(self, message: str):
        """Sends an alert (e.g., via email, SMS, or Slack)."""
        self.log_event('warning', f"ALERT: {message}")
        # Integrate notification service AWS SNS or other provider here
        print(f"--- ALERT SENT: {message} ---")

    def get_current_metrics(self):
        return self.performance_metrics

    def update_order_book_metrics(self, symbol: str = 'BTCUSDT', limit: int = 10):
        """Fetch and log order book metrics for monitoring and analytics."""
        metrics = get_order_book_metrics(symbol, limit)
        self.performance_metrics.update({
            'order_book_spread': metrics['spread'],
            'order_book_imbalance': metrics['imbalance'],
            'order_book_vwap_bid': metrics['vwap_bid'],
            'order_book_vwap_ask': metrics['vwap_ask'],
            'order_book_bid_qty': metrics['bid_qty'],
            'order_book_ask_qty': metrics['ask_qty']
        })
        self.log_event('info', f"Order book metrics: {metrics}")