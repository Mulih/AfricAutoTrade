import time
import os
import pandas as pd
from dotenv import load_dotenv
import threading
from typing import Optional

from src.data_ingestion import get_market_data, get_realtime_data
from src.ai.models import AIModel
from src.strategies.strategy import TradingStrategy
from src.execution.executor import TradeExecutor
from src.monitoring.monitor import TradingMonitor

# Global stop event for graceful shutdown
bot_stop_event = threading.Event()


def run_trading_bot(stop_event: Optional[threading.Event] = None):
    # 1. Initialize Components
    monitor = TradingMonitor(log_file='trading_bot_run.log')
    monitor.log_event('info', "Initializing trading bot components...")

    ai_model = AIModel()
    # In production, I'll load the pre-trained model
    ai_model.load_model()

    try:
        # example of dummy training data
        X_dummy = pd.DataFrame([[0.01, 0.1], [-0.005, -0.5], [0.02, 0.2]])
        y_dummy = pd.Series([1, 0, 1])
        ai_model.train(X_dummy, y_dummy)
    except Exception as e:
        monitor.log_event('error', f"Failed to train or load AI model: {e}")
        monitor.log_event('critical', "Exiting due to AI model failure.")
        return

    strategy = TradingStrategy(ai_model=ai_model)

    # Configure executor mode based on environment variable
    execution_mode = os.getenv('EXECUTION_MODE', 'paper')
    executor = TradeExecutor(
        api_key=os.getenv('BINANCE_API_KEY', 'dummy_key'),
        api_secret=os.getenv('BINANCE_API_SECRET', 'dummy_secret'),
        mode=execution_mode
    )

    monitor.log_event('info', "Trading bot components initialized successfully.")

    # Example: Use get_market_data for initial historical data (optional, for feature engineering or backtesting)
    historical_data = get_market_data(symbol='BTCUSD', limit=100)
    monitor.log_event('info', f"Fetched {len(historical_data)} rows of historical market data for BTCUSD.")

    # Main Trading Loop
    try:
        while True:
            if stop_event and stop_event.is_set():
                monitor.log_event('info', "Stop event received. Exiting trading loop.")
                break

            monitor.log_event('info', "--- Starting new trading cycle ---")

            # 2. Data Ingestion
            current_market_data = get_realtime_data(symbol='BTCUSD')
            if not current_market_data or current_market_data.get('price') is None:
                monitor.log_event('error', "Failed to get current market. Skipping cycle.")
                time.sleep(60)
                continue

            # Prepare features for AI model( crucial and depends on AI model's training)
            # For this simple example, let's derive some simple features
            price_change = (current_market_data.get('price', 0) - 64000) / 64000 # dummy calculation
            volume_change = (current_market_data.get('volume', 0) - 1000) / 1000 # dummy calculation
            ai_features = {'price_change': price_change,'volume_change': volume_change}

            # 3. AI Prediction
            ai_prediction = ai_model.predict(ai_features)
            monitor.log_event('info', f"AI predicted: {ai_prediction} for market data: {current_market_data}")

            # 4. Trading Strategy Decision
            decision = strategy.make_decision(current_market_data, ai_prediction)
            monitor.log_event('info', f"Strategy decision: {decision}")

            # 5. Trade Execution
            if decision == 'buy':
                quantity_to_buy = 0.0001 # example
                trade_result = executor.execute_trade('BTCUSD', 'buy', quantity_to_buy)
                monitor.log_event('info', "Buy order executed.", trade_details=trade_result)
                monitor.update_metrics(trade_result=trade_result)
            elif decision == 'sell':
                quantity_to_sell = 0.0001 # example
                trade_result = executor.execute_trade('BTCUSD', 'sell', quantity_to_sell)
                monitor.log_event('info', "Sell order executed.", trade_details=trade_result)
                monitor.update_metrics(trade_result=trade_result)
            else:
                monitor.log_event('info', "Holding. No trade excecuted this cycle.")

            # 6. Monitoring and Metrics Update
            current_balance = executor.get_account_balance().get('cash')
            monitor.update_metrics(current_balance=current_balance)
            # Fetch and log order book metrics for monitoring
            monitor.update_order_book_metrics(symbol='BTCUSDT', limit=10)

            # Simulate historical trades for performance evaulation (optional, done in backtesting)
            # historical_trades_mock = [{'type': 'buy', 'entry_price': 6500, 'exit_price': 65100, 'quantity': 0.001, 'profit_loss': 0.1}]
            # strategy.evaluate_performance(historical_trades_mock)

            monitor.log_event('info', f"Current Bot Metrics: {monitor.get_current_metrics()}")

            # 7. Pause before next cycle
            sleep_time = int(os.getenv('TRADING_CYCLE_INTERVAL_SECONDS', 300)) # Default to 5 minutes
            monitor.log_event('info', f"Sleeping for {sleep_time} seconds...")
            for _ in range(sleep_time):
                if stop_event and stop_event.is_set():
                    monitor.log_event('info', "Stop event received during sleep. Exiting trading loop.")
                    break
                time.sleep(1)
            if stop_event and stop_event.is_set():
                break

    except KeyboardInterrupt:
        monitor.log_event('info', "Bot stopped manually (KeyboardInterrupt).")
    except Exception as e:
        monitor.log_event('critical', f"An unexpected error occured: {e}")
        monitor.send_alert(f"Critical error in trading bot: {e}")
    finally:
        monitor.log_event('info', "Trading bot finished.")


if __name__ == "__main__":
    # TRADING_CYCLE_INTERVAL_SECONDS=60
    # EXECUTION_MODE=paper
    # BROKER_API_KEY=dummy_key
    # BROKER_API_SECRET=dummy_secret
    run_trading_bot(stop_event=bot_stop_event)