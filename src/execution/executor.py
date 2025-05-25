import os
import time
import pandas as pd
from typing import Dict, Any, Optional
from dotenv import load_dotenv


try:
    from binance.client import Client as BinanceClient
    from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC, ORDER_TYPE_MARKET
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


    def _simulate_trade(self, symbol: str, order_type: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Simulates a trade for paper trading mode.
        Calculates impact on paper cash and holdings.
        """
        timestamp = pd.Timestamp.now().isoformat()
        cost = quantity * price

        if order_type == 'buy':
            if self.paper_cash >= cost:
                self.paper_cash -= cost
                self.paper_holdings[symbol] = self.paper_holdings.get(symbol, 0.0) + quantity
                status = 'success'
                message = f"[PAPER TRADE] Successfully simulated BUY {quantity} of {symbol} at {price:.2f}. Remaining cash: {self.paper_cash:.2f}"
            else:
                status = 'failed'
                message = f"[PAPER TRADE] Failed to BUY {quantity} of {symbol} at {price:.2f}: Insufficient cash. Current cash: {self.paper_cash:.2f}"
        elif order_type == 'sell':
            if self.paper_holdings.get(symbol, 0.0) >= quantity:
                self.paper_cash += cost # Selling adds cash
                self.paper_holdings[symbol] = self.paper_holdings.get(symbol, 0.0) - quantity
                status = 'success'
                message = f"[PAPER TRADE] Successfully simulated SELL {quantity} of {symbol} at {price:.2f}. Current cash: {self.paper_cash:.2f}"
            else:
                status = 'failed'
                message = f"[PAPER TRADE] Failed to SELL {quantity} of {symbol} at {price:.2f}: Insufficient {symbol} holdings. Current holdings: {self.paper_holdings.get(symbol, 0.0):.4f}"
        else:
            status = 'failed'
            message = f"[PAPER TRAADE] Invalid order type: {order_type}"

        print(message)
        return {
            'status': status,
            'order_id': f"sim_order_{os.urandom(4).hex()}",
            'symbol': symbol,
            'type': order_type,
            'quantity': quantity,
            'price': price,
            'timestamp': timestamp,
            'message': message
        }


    def execute_trade(self, symbol: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
        """
        Executes a trade order with the brokeragec or simulates it.
        :param symbol: Trading pair (e.g., 'BTC/USD')
        :param order_type: 'buy' or 'sell'
        :param quantity: Amount to trade
        :param price: Optional. The price at which to place a LIMIT order. If None, a MARKET order is attempted.
        :return: dict with trade details or success status
        """
        print(f"Attempting to execute {order_type} order for {quantity} of {symbol} in {self.mode} mode...")

        if self.mode == 'paper':
            # For paper trading, A mock price is needed if not provided
            mock_price = price if price is not None else (65000.0 if order_type == 'buy' else 64950.0)
            return self._simulate_trade(symbol, order_type, quantity, mock_price)
        elif self.mode == 'live':
            if not self.broker_client:
                print("ERROR: Live trading client not initialized. Falling back to paper mode.")
                return self._simulate_trade(symbol, order_type, quantity, price or 65000.0)

            try:
                order_params = {
                    'symbol': symbol,
                    'side': SIDE_BUY if order_type == 'buy' else SIDE_SELL,
                    'quantity': quantity
                }

                if price is not None:
                    order_params['type'] = ORDER_TYPE_LIMIT
                    order_params['price'] = f"{price:.2f}" # Binance API expects price as string
                    order_params['timeInForce'] = TIME_IN_FORCE_GTC # Good Till Cancelled
                    print(f"Placing LIVE LIMIT {order_type.upper()} order for {quantity} {symbol}...")
                    order = self.broker_client.create_order(**order_params)
                else:
                    order_params['type'] = ORDER_TYPE_MARKET
                    print(f"Placing LIVE MARKET {order_type.upper()} order for {quantity} {symbol}...")
                    order = self.broker_client.create_order(**order_params)

                print(f"LIVE TRADE: Order {order['orderId']} placed. Status: {order['status']}")
                # Wait a bit and check order status for market orders to getfilled price
                if order['type'] == 'MARKET' and order['status'] == 'NEW':
                    # For market orders, sometimes the fill details are not immediate.
                    # Will implement poll or use WebSockets. For now, using wait.
                    time.sleep(2) # Gite it a moment to fill
                    filled_order = self.broker_client.get_order(symbol=symbol, orderId=order['orderId'])
                    filled_price = float(filled_order['fills'][0]['price']) if filled_order['fills'] else 0.0
                    print(f"LIVE TRADE: MArket order {order['orderId']} filled at approx. {filled_price:.2f}")
                    return {
                        'status': 'success',
                        'order_id': order['orderId'],
                        'symbol': order['symbol'],
                        'type': order_type,
                        'quantity': float(order['executedQty']),
                        'price': filled_price,
                        'timestamp': pd.to_datetime(order['updateTime'], unit='ms').isoformat(),
                        'raw_response': filled_order
                    }
                return {
                    'status': 'success',
                    'order_id': order['orderId'],
                    'symbol': order['symbol'],
                    'type': order_type,
                    'quantity': float(order['origQty']),
                    'price': float(order.get('price', '0.0')),
                    'timestamp': pd.to_datetime(order['transactTime'], unit='ms').isoformat(),
                    'raw_response': order
                }


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