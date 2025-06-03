from typing import Dict, Any, List
from src.data_ingestion import get_order_book_metrics


class TradingStrategy:

    def __init__(self, ai_model: Any):
        self.ai_model = ai_model
        # Placeholder for other strategy parameters

    def make_decision(
        self,
        market_data: Dict[str, Any],
        ai_prediction: int,
        symbol: str = 'BTCUSDT'
    ) -> str:
        """
        Makes a trading decision on current market data and AI prediction.
        :param market_data: dict of current market data
        :param ai_prediction: The output from the AI model
        :return: 'buy', 'sell', or 'hold'
        """
        ob_metrics = get_order_book_metrics(symbol)
        spread = ob_metrics['spread']
        imbalance = ob_metrics['imbalance']
        current_price = market_data.get('price')

        if current_price is None:
            print("Warning: Missing 'price' in market data. Holding.")
            return 'hold'

        # Example production logic: combine AI and order book signals
        if ai_prediction == 1 and current_price < 66000:
            print(
                f"Strategy: AI recommends BUY and "
                f"price is favorable ({current_price}). "
                "Decision: Buy"
            )
            return 'buy'
        elif ai_prediction == 0 and current_price > 64000:
            print(
                f"Strategy: AI recommends SELL "
                f"and price is high ({current_price}). "
                "Decision: SELL"
            )
            return 'sell'
        elif (
            ai_prediction == 1 and spread is not None and spread < 5 and
            imbalance is not None and imbalance > 0
        ):
            print(
                f"Strategy: AI recommends BUY, spread={spread}, "
                f"imbalance={imbalance}. "
                "Decision: BUY"
            )
            return 'buy'
        elif (
            ai_prediction == 0 and spread is not None and spread < 5 and
            imbalance is not None and imbalance < 0
        ):
            print(
                f"Strategy: AI recommends SELL, spread={spread}, "
                f"imbalance={imbalance}. "
                "Decision: SELL"
            )
            return 'sell'
        else:
            print(
                f"Strategy: HOLD. AI={ai_prediction}, spread={spread}, "
                f"imbalance={imbalance}"
            )
            return 'hold'

    def evaluate_performance(
        self, historical_trades: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Evaluates the strategy's performance based on historical trades.
        :param historical_trades: List of executed trades
                                    with entry/exit prices, etc.
        :return: dict with performance metrics (e.g., profit, win_rate)
        """
        total_profit = 0.0
        num_wins = 0
        num_losses = 0
        for trade in historical_trades:
            if (
                trade['type'] == 'buy'
                and trade['exit_price'] > trade['entry_price']
            ):
                total_profit += (
                    (trade['exit_price'] - trade['entry_price'])
                    * trade['quantity']
                )
                num_wins += 1
            elif (
                trade['type'] == 'sell' and
                trade['exit_price'] < trade['entry_price']
            ):
                total_profit += (
                    (trade['entry_price'] - trade['exit_price'])
                    * trade['quantity']
                )  # for short sells
                num_wins += 1
            else:
                num_losses += 1
        win_rate = (
            num_wins / (num_wins + num_losses)
            if (num_wins + num_losses) > 0
            else 0.0
        )
        print(
            f"Strategy Performance: Total Profit: {total_profit:.2f}, "
            f"Win rate: {win_rate:.2%}"
        )
        return {'profit': total_profit, 'win_rate': win_rate}
