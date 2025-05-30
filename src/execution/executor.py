import os
import time
import pandas as pd
from typing import Dict, Any, Optional
from dotenv import load_dotenv


try:
    from binance.client import Client as BinanceClient # type: ignore
    from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC, ORDER_TYPE_MARKET  # type: ignore
    from binance.exceptions import BinanceAPIException, BinanceRequestException # type: ignore
except ImportError:
    print("Warning: 'python-binance' library not found. Live trading functionality will be simulated.")
    BinanceClient = None
    SIDE_BUY = SIDE_SELL = ORDER_TYPE_LIMIT = TIME_IN_FORCE_GTC = ORDER_TYPE_MARKET = None  # type: ignore
    BinanceAPIException = BinanceRequestException = Exception  # type: ignore

load_dotenv() # Load environment variables from .env file

class TradeExecutor:
    def __init__(self, api_key: str, api_secret: str, mode: str = 'paper') -> None:
        """
        Initializes the TradeExecutor instance.
        :param api_key: Binance API key
        :param api_secret: Binance API secret
        :param mode: Trading mode - 'paper' for simulated trading, 'live' for real trading
        """
        self.api_key: str = api_key
        self.api_secret: str = api_secret
        self.mode: str = mode  # 'live' or 'paper'
        self.broker_client: Optional[Any] = None
        self.paper_cash: float = float(os.getenv('PAPER_STARTING_CASH', 100000.0))
        self.paper_holdings: Dict[str, float] = {}
        print(f"TradeExecutor initialized in {self.mode} mode.")
        if self.mode == 'live':
            if BinanceClient:
                try:
                    self.broker_client = BinanceClient(api_key, api_secret)
                    server_time = self.broker_client.get_server_time()
                    print(f"Connected to Binance API. Server time: {server_time['serverTime']}")
                except (BinanceAPIException, BinanceRequestException) as e:  # type: ignore
                    print(f"ERROR: Could not connect to Binance API in live mode: {e}")
                    print("Falling back to paper trading mode due to API connection failure.")
                    self.mode = 'paper'
            else:
                print("Binance client not available. Live trading functionality cannot be used.")
                print("Falling back to paper trading mode.")
                self.mode = 'paper'

    def _simulate_trade(self, symbol: str, order_type: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Simulates a trade execution in paper trading mode.
        :param symbol: Trading pair symbol (e.g., 'BTCUSD')
        :param order_type: 'buy' or 'sell'
        :param quantity: Amount to trade
        :param price: Price at which to simulate the trade
        :return: dict with simulated trade result/status
        """
        timestamp: str = pd.Timestamp.now().isoformat()
        cost: float = quantity * price
        status: str
        message: str
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
                self.paper_cash += cost
                self.paper_holdings[symbol] = self.paper_holdings.get(symbol, 0.0) - quantity
                status = 'success'
                message = f"[PAPER TRADE] Successfully simulated SELL {quantity} of {symbol} at {price:.2f}. Current cash: {self.paper_cash:.2f}"
            else:
                status = 'failed'
                message = f"[PAPER TRADE] Failed to SELL {quantity} of {symbol} at {price:.2f}: Insufficient {symbol} holdings. Current holdings: {self.paper_holdings.get(symbol, 0.0):.4f}"
        else:
            status = 'failed'
            message = f"[PAPER TRADE] Invalid order type: {order_type}"
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
        Executes a trade (buy/sell) for the given symbol and quantity.
        :param symbol: Trading pair symbol (e.g., 'BTCUSD')
        :param order_type: 'buy' or 'sell'
        :param quantity: Amount to trade
        :param price: Optional limit price for the order (market price used if None)
        :return: dict with trade result/status
        """
        print(f"Attempting to execute {order_type} order for {quantity} of {symbol} in {self.mode} mode...")
        if self.mode == 'paper':
            mock_price: float = price if price is not None else (65000.0 if order_type == 'buy' else 64950.0)
            return self._simulate_trade(symbol, order_type, quantity, mock_price)
        elif self.mode == 'live':
            if not self.broker_client:
                print("ERROR: Live trading client not initialized. Falling back to paper mode.")
                return self._simulate_trade(symbol, order_type, quantity, price or 65000.0)
            try:
                order_params: Dict[str, Any] = {
                    'symbol': symbol,
                    'side': SIDE_BUY if order_type == 'buy' else SIDE_SELL,  # type: ignore[name-defined]
                    'quantity': quantity
                }
                if price is not None:
                    order_params['type'] = ORDER_TYPE_LIMIT  # type: ignore[name-defined]
                    order_params['price'] = f"{price:.2f}"
                    order_params['timeInForce'] = TIME_IN_FORCE_GTC  # type: ignore[name-defined]
                    print(f"Placing LIVE LIMIT {order_type.upper()} order for {quantity} {symbol}...")
                    order = self.broker_client.create_order(**order_params)
                else:
                    order_params['type'] = ORDER_TYPE_MARKET  # type: ignore[name-defined]
                    print(f"Placing LIVE MARKET {order_type.upper()} order for {quantity} {symbol}...")
                    order = self.broker_client.create_order(**order_params)
                print(f"LIVE TRADE: Order {order['orderId']} placed. Status: {order['status']}")
                if order['type'] == 'MARKET' and order['status'] == 'NEW':
                    time.sleep(2)
                    filled_order = self.broker_client.get_order(symbol=symbol, orderId=order['orderId'])
                    filled_price: float = float(filled_order['fills'][0]['price']) if filled_order['fills'] else 0.0
                    print(f"LIVE TRADE: Market order {order['orderId']} filled at approx. {filled_price:.2f}")
                    return {
                        'status': 'success',
                        'order_id': order['orderId'],
                        'symbol': order['symbol'],
                        'type': order_type,
                        'quantity': float(order['executedQty']),
                        'price': filled_price,
                        'timestamp': pd.to_datetime(order['updateTime'], unit='ms').isoformat(),  # type: ignore[attr-defined]
                        'raw_response': filled_order
                    }
                else:
                    return {
                        'status': 'success',
                        'order_id': order['orderId'],
                        'symbol': order['symbol'],
                        'type': order_type,
                        'quantity': float(order['origQty']),
                        'price': float(order.get('price', '0.0')),
                        'timestamp': pd.to_datetime(order['transactTime'], unit='ms').isoformat(),  # type: ignore[attr-defined]
                        'raw_response': order
                    }
            except Exception as e:
                print(f"Error executing live trade: {e}")
                return {'status': 'failed', 'error': str(e)}
        else:
            print(f"Invalid execution mode: {self.mode}")
            return {'status': 'failed', 'error': 'Invalid execution mode'}

    def get_account_balance(self) -> Dict[str, Any]:
        """
        Returns the current account balance (mocked for paper mode).
        :return: dict with account balance info
        """
        if self.mode == 'paper':
            return {'cash': self.paper_cash, 'asset_holdings': self.paper_holdings}
        elif self.mode == 'live':
            if not self.broker_client:
                print("ERROR: Live trading client not initialized for balance check.")
                return {'cash': 0.0, 'asset_holdings': {}, 'error': 'Client not initialized'}
            try:
                account_info: Dict[str, Any] = self.broker_client.get_account()
                balances: Dict[str, float] = {}
                cash_balance: float = 0.0
                for asset in account_info['balances']:
                    free: float = float(str(asset['free']))
                    locked: float = float(str(asset['locked']))
                    total: float = free + locked
                    if total > 0:
                        balances[asset['asset']] = total
                    if asset['asset'] == 'USDT':
                        cash_balance = free
                print(f"LIVE BALANCE: Cash (USDT): {cash_balance:.2f}, Holdings: {balances}")
                return {'cash': cash_balance, 'asset_holdings': balances, 'raw_response': account_info}
            except Exception as e:
                print(f"LIVE BALANCE ERROR: {e}")
                return {'cash': 0.0, 'asset_holdings': {}, 'error': str(e)}
        else:
            return {'cash': 0.0, 'asset_holdings': {}, 'error': 'Invalid execution mode'}