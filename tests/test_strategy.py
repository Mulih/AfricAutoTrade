from src.strategies.strategy import TradingStrategy


def test_make_decision_buy():
    class DummyAI:
        def predict(self, features):  # type: ignore
            return 1
    strategy = TradingStrategy(ai_model=DummyAI())
    market_data = {'price': 65000, 'volume': 1000}
    decision = strategy.make_decision(market_data, 1)
    assert decision in ['buy', 'hold']


def test_make_decision_sell():
    class DummyAI:
        def predict(self, features):  # type: ignore
            return 0
    strategy = TradingStrategy(ai_model=DummyAI())
    market_data = {'price': 67000, 'volume': 1000}
    decision = strategy.make_decision(market_data, 0)
    assert decision in ['sell', 'hold']


def test_evaluate_performance():
    strategy = TradingStrategy(ai_model=None)
    trades = [  # type: ignore
        {'type': 'buy', 'entry_price': 100, 'exit_price': 110, 'quantity': 1},
        {'type': 'sell', 'entry_price': 200, 'exit_price': 190, 'quantity': 1},
        {'type': 'buy', 'entry_price': 150, 'exit_price': 140, 'quantity': 1},
    ]
    perf = strategy.evaluate_performance(trades)  # type: ignore
    assert 'profit' in perf
    assert 'win_rate' in perf
