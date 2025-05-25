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