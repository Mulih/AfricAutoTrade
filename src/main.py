import time
import os
import pandas as pd
from dotenv import load_dotenv

from src.data_ingestion import get_market_data, get_realtime_data
from src.ai.models import AIModel
from src.strategies.strategy import TradingStrategy
from src.execution.executor import TradeExecutor
from src.monitoring.monitor import TradingMonitor

def run_trading_bot():
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

    # Main Trading Loop
    try:
        while True:
            monitor.log_event('info', "--- Starting new trading cycle ---")

            # 2. Data Ingestion
            current_market_data = get_realtime_data(symbol='BTCUSD')
            if not current_market_Data or current_market_data.get('price') is None:
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
    except KeyboardInterrupt:
        monitor.log_event('info', "Bot stopped manually (KeyboardInterrupt).")