from src.monitoring.monitor import TradingMonitor


def test_log_event_and_metrics():
    monitor = TradingMonitor(log_file='test.log')
    monitor.log_event('info', 'Test event')
    monitor.update_metrics(
        trade_result={'status': 'success', 'profit_loss': 10}
    )
    metrics = monitor.get_current_metrics()
    assert 'trades_executed' in metrics
    assert 'total_profit_loss' in metrics


def test_update_order_book_metrics():
    monitor = TradingMonitor(log_file='test.log')
    monitor.update_order_book_metrics(symbol='BTCUSDT', limit=5)
    metrics = monitor.get_current_metrics()
    assert 'order_book_spread' in metrics
    assert 'order_book_imbalance' in metrics
