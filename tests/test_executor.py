from src.execution.executor import TradeExecutor


def test_paper_trade_execution():
    executor = TradeExecutor(api_key='dummy', api_secret='dummy', mode='paper')
    result = executor.execute_trade('BTCUSD', 'buy', 0.01, price=65000.0)
    assert result['status'] == 'success'
    assert result['type'] == 'buy'
    assert result['symbol'] == 'BTCUSD'


def test_get_account_balance():
    executor = TradeExecutor(api_key='dummy', api_secret='dummy', mode='paper')
    balance = executor.get_account_balance()
    assert 'cash' in balance
    assert 'asset_holdings' in balance
