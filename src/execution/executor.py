import os
import pandas as pd
from typing import Dict, Any
from dotenv import load_dotenv


try:
    from binance.client import Client as BinanceClient
    from binance.enums import *
    from binance.exceptions import BinanceAPIException, BinanceRequestException
except ImportError:
    print("Warning: 'python-binance' library not found. Live trading functionality will be simulated.")
    BinanceClient = None

load_dotenv() # Load environment variables from .env file

class TradeExecutor:
    def __init__(self, api_key: str, api_secret: str, mode: str = 'paper'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.mode = mode # 'live' or 'paper'
        self.broker_client = None

        print(f"TradeExecutor initialized in {self.mode} mode.")

        if self.mode == 'live':
            if BinanceClient:
                try:
                    self.broker_client = BinanceClient(api_key, api_secret)
                    # Test connection by getting server time
                    server_time = self.broker_client.get_server_time()
                    print(f"Connected to Binance API. Server time: {server_time['serverTime']}")
                except (BinanceAPIException, BinanceRequestException) as e:
                    print(f"ERROR: Could not connect to Binance API in live mode: {e}")
                    print("Falling back to paper trading mode due to API connection failure.")
                    self.mode = 'paper' # Fallback if live connection fails
                except Exception as e:
                    print(f"An unexpected error occurred Binance client initialization: {e}")
                    print("Falling back to paper trading mode.")
                    self.mode = 'paper'
            else:
                print("Binance client not available. Live trading functionality cannot be used.")
                print("Falling back to paper trading mode.")
                self.mode = 'paper'

        # Initialize paper trading account state
        self.paper_cash = float(os.getenv('PAPER_STARTING_CASH', 100000.0))
        self.paper_holdings: Dict[str, float] = {}


    def execute_trade(self, symbol: str, order_type: str, quantity: float) -> Dict[str, Any]:
        """
        Executes a trade order with the brokerage.
        :param symbol: Trading pair (e.g., 'BTC/USD')
        :param order_type: 'buy' or 'sell'
        :param quantity: Amount to trade
        :return: dict with trade details or success status
        """
        print(f"Attempting to execute {order_type} order for {quantity} of {symbol} in {self.mode} mode...")

        if self.mode == 'paper':
            # Simulate trade execution for paper trading
            print(f"[PAPER TRADE] Successfully simulated {order_type} {quantity} of {symbol}.")
            return {
                'status': 'success',
                'order_id': f"sim_order_{os.urandom(4).hex()}",
                'symbol': symbol,
                'type': order_type,
                'quantity': quantity,
                'price': 65000.0 if order_type == 'buy' else 64950.0, # Mock price
                'timestamp': pd.Timestamp.now().isoformat()
            }
        elif self.mode == 'live':
            # call binance API here
            # try:
            #     order = self.broker_client.create_order(symbol, order_type, quantity)
            #     print(f"LIVE TRADE: Order {order.id} placed for {symbol}")
            #     return {'status': 'success', 'order_id': order.id, ...}
            # except Exception as e:
            #     print(f"LIVE TRADE ERROR: {e}")
            #     return {'status': 'failed', 'error': str(e)}
            print("LIVE TRADING IS NOT YET IMPLEMENTED. Running in paper mode.")
            # fallback to paper mode simulation
            original_mode = self.mode
            self.mode = 'paper'
            result = self.execute_trade(symbol, order_type, quantity)
            self.mode = original_mode
            return result
        else:
            print(f"Invalid mode: {self.mode}")
            return {'status': 'failed', 'error': 'Invalid execution mode'}

    def get_account_balance(self) -> Dict[str, Any]:
        """Fetches current account balance."""
        if self.mode == 'paper':
            return {'cash': 100000.0, 'asset_holdings': {'BTC': 1.0}}
        else:
            # return self.broker_client.get_balance()
            return {'cash': 0.0, 'asset_holdings': {}} # placehoder for live


if __name__ == "__main__":
    # ensure there is a .ev file with dummy API keys for local testing
    executor = TradeExecutor(
        api_key=os.getenv('BINANCE_API_KEY', 'dummy_key'),
        api_secret=os.getenv('BINANCE_API_SECRET', 'dummy_secret'),
        mode='paper' # starting with paper for safety
    )

    # Simulate a buy order
    buy_result = executor.execute_trade('BTCUSD', 'buy', 0.001)
    print("Buy Order Result:", buy_result)

    # Simulate a sell order
    sell_result = executor.execute_trade('ETHUSD', 'sell', 0.005)
    print("Sell Order Result:", sell_result)

    balance = executor.get_account_balance()
    print("Current Account Balance:", balance)