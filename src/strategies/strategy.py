from typing import Dict, Any
class TradingStrategy:
    def __init__(self, ai_model):
        self.ai_model = ai_model
        # place holder for other strategy parameters

    def make_decision(self, market_data, ai_prediction):
        """
        Makes a trading decision on current market data and AI prediction.
        :param maraket_data: dict of current market data (e.g., {'price': X, 'volume': Y})
        :param ai_prediction: The output from the AI model (e.g., 0 for 'sell/hold', 1 for 'buy')
        :return: 'buy', 'sell', or 'hold'
        """
        current_price = market_data.get('price')

        if current_price is None:
            print("Warning: Missing 'price' in market data. Holding.")
            return 'hold'

        # simple logic
        if ai_prediction == 1 and current_price < 66000: # Buy signal from AI and price below a threshold
            print(f"Strategy: AI recommends BUY and price is favorable ({current_price}). Decision: Buy")
            return 'buy'
        elif ai_prediction == 0 and current_price > 64000: # Sell signal from AI and price above a threshold
            print(f"Strategy: AI recommends SELL and price is high ({current_price}). Decision: SELL")
            return 'sell'
        else:
            print(f"Strategy: AI prediction: {ai_prediction}, Current Price: {current_price}. Decision: HOLD")
            return 'hold'


    def evaluate_performance(self, historical_trades):
        """
        Evaluates the strategy's performance based on historical trades.
        (Will be more complex in future)
        :param historical_trades: List of executed trades with entry/exit prices, etc.
        :return: dict with performance metrics (e.g., profit, win_rate)
        """
        # placeholder for actual performance evaluation
        total_profit = 0
        num_wins = 0
        num_losses = 0

        for trade in historical_trades:
            if trade['type'] == 'buy' and trade['exit_price'] > trade['entry_price']:
                total_profit += (trade['exit_price'] - trade['entry_price']) * trade['quantity']
                num_wins += 1
            elif trade['type'] == 'sell' and trade['exit_price'] < trade['entry_price']:
                total_profit += (trade['entry_price'] - trade['exit_price']) * trade['quantity'] # for short sells
                num_wins += 1
            else:
                num_losses += 1

        win_rate = num_wins / (num_wins + num_losses) if (num_wins + num_losses) > 0 else 0

        print(f"Strategy Performance: Total Profit: {total_profit:.2f}, Win rate: {win_rate:.2%}")
        return {'profit': total_profit, 'win_rate': win_rate}


if __name__ == "__main__":
    from src.ai.models import AIModel

    # Mock AI Model for testing strategy independently
    class MockAIModel:
        # Simulate a prediction based on a 'dummy_indicator' in features
        if 'dummy_indicator' in features and features['dummy_indicator'] > 0.5:
            return 1 # Simulate buy signal
        return 0 # simulate sell/hold signal

    mock_ai = MockAIModel()
    strategy = TradingStrategy(ai_model=mock_ai)

    # Test cases for decision making
    print("\n--- Decision Making Tests ---")
    market_data_buy = {'price': 65500, 'volume': 1000}
    # For mock_ai, let's assume market_data is also used to generate AI features
    ai_features_buy = {'dummy_indicator': 0.7, 'price_change': 0.01, 'volume_change': 0.1}
    ai_pred_buy = mock_ai.predict(ai_features_buy)
    decision_buy = strategy.make_decision(market_data_buy, ai_pred_buy)
    print(f"Market Data: {market_data_buy}, AI Prediction: {ai_pred_buy} -> Decision: {decision_buy}")

    market_data_sell = {'price': 64500, 'volume': 500}
    ai_features_sell = {'dummy_indicator': 0.3, 'price_change': -0.005, 'volume_change': -0.05}
    ai_pred_sell = mock_ai.predict(ai_features_sell)
    decision_sell = strategy.make_decision(market_data_sell, ai_pred_sell)
    print(f"Market Data: {market_data_sell}, AI Prediction: {ai_pred_sell} -> Decision: {decision_sell}")

    market_data_hold = {'price': 65000, 'volume': 700}
    ai_features_hold = {'dummy_indicator': 0.45, 'price_change': 0.001, 'volume_change': 0.01}
    ai_pred_hold = mock_ai.predict(ai_features_hold)
    decision_hold = strategy.make_decision(market_data_hold, ai_pred_hold)
    print(f"Market Data: {market_data_hold}, AI Prediction: {ai_pred_hold} -> Decision: {decision_hold}")

    # Test performance evaluation (mock historical trades)
    print("\n--- Performance Evaluation Test ---")
    historical_trades = [
        {'type': 'buy', 'entry_price': 100, 'exit_price': 105, 'quantity': 1},
        {'type': 'sell', 'entry_price': 200, 'exit_price': 190, 'quantity': 0.5}, # Short sell
        {'type': 'buy', 'entry_price': 150, 'exit_price': 145, 'quantity': 2}, # Loss
    ]
    strategy.evaluate_performance(historical_trades)