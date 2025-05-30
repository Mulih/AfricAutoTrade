import pandas as pd
import requests
from typing import Dict, Any, List

# --- Advanced Data Sources and Features Scaffold ---

# 1. Order Book Data


def get_order_book(symbol: str = 'BTCUSDT',
                   limit: int = 100) -> Dict[str, Any]:
    """Fetches order book (depth) data from Binance REST API."""
    api_url = \
        f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            'bids': data.get('bids', []),
            'asks': data.get('asks', []),
            'lastUpdateId': data.get('lastUpdateId')
        }
    except Exception as e:
        print(f"Error fetching order book: {e}")
        return {'bids': [], 'asks': [], 'lastUpdateId': None}


def get_order_book_spread(symbol: str = 'BTCUSDT',
                          limit: int = 10) -> Dict[str, Any]:
    """Fetches order book and computes spread and top-of-book liquidity."""
    order_book = get_order_book(symbol, limit)
    try:
        best_bid = float(order_book['bids'][0][0]) \
                            if order_book['bids'] else None
        best_ask = float(order_book['asks'][0][0]) \
                            if order_book['asks'] else None
        spread = (best_ask - best_bid) if (
            best_bid is not None and best_ask is not None
        ) else None
        bid_qty = float(order_book['bids'][0][1]) \
                            if order_book['bids'] else None
        ask_qty = float(order_book['asks'][0][1]) \
                            if order_book['asks'] else None
        return {
            'best_bid': best_bid,
            'best_ask': best_ask,
            'spread': spread,
            'bid_qty': bid_qty,
            'ask_qty': ask_qty,
            'bids': order_book['bids'],
            'asks': order_book['asks'],
            'lastUpdateId': order_book['lastUpdateId']
        }
    except Exception as e:
        print(f"Error computing order book spread: {e}")
        return {
            'best_bid': None, 'best_ask': None,
            'spread': None, 'bid_qty': None,
            'ask_qty': None, 'bids': [],
            'asks': [], 'lastUpdateId': None
        }


def get_order_book_metrics(symbol: str = 'BTCUSDT',
                           limit: int = 10) -> Dict[str, Any]:
    """
    Compute advanced order book metrics:
        spread, imbalance,
        depth-weighted price, liquidity.
    """
    ob = get_order_book(symbol, limit)
    try:
        best_bid = float(ob['bids'][0][0]) if ob['bids'] else None
        best_ask = float(ob['asks'][0][0]) if ob['asks'] else None
        spread = (best_ask - best_bid) \
                    if (best_bid is not None and best_ask is not None) \
                    else None
        bid_qty = float(ob['bids'][0][1]) if ob['bids'] else None
        ask_qty = float(ob['asks'][0][1]) if ob['asks'] else None
        total_bid_qty = sum(float(bid[1]) for bid in ob['bids']) \
                            if ob['bids'] else 0.0
        total_ask_qty = sum(float(ask[1]) for ask in ob['asks']) \
                            if ob['asks'] else 0.0
        imbalance = (
            (total_bid_qty - total_ask_qty) /
            (total_bid_qty + total_ask_qty)
        ) if (total_bid_qty + total_ask_qty) > 0 else None

        def vwap(levels: List[Any]) -> float | None:
            total_qty = sum(float(level[1]) for level in levels)
            if total_qty == 0:
                return None
            return sum(
                float(level[0]) * float(level[1]) for level in levels
            ) / total_qty

        vwap_bid = vwap(ob['bids']) if ob['bids'] else None
        vwap_ask = vwap(ob['asks']) if ob['asks'] else None
        return {
            'best_bid': best_bid,
            'best_ask': best_ask,
            'spread': spread,
            'bid_qty': bid_qty,
            'ask_qty': ask_qty,
            'imbalance': imbalance,
            'vwap_bid': vwap_bid,
            'vwap_ask': vwap_ask,
            'bids': ob['bids'],
            'asks': ob['asks'],
            'lastUpdateId': ob['lastUpdateId']
        }
    except Exception as e:
        print(f"Error computing order book metrics: {e}")
        return {
            'best_bid': None, 'best_ask': None,
            'spread': None, 'bid_qty': None,
            'ask_qty': None, 'imbalance': None,
            'vwap_bid': None, 'vwap_ask': None,
            'bids': [], 'asks': [], 'lastUpdateId': None
        }


async def binance_ws_ticker(symbol: str = 'btcusdt',
                            on_message=None): # type: ignore
    """Connects to Binance WebSocket for real-time ticker updates."""
    import websockets
    url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@ticker"
    async with websockets.connect(url) as ws:
        async for message in ws:
            if on_message:
                on_message(message)
            else:
                print(message)


def get_crypto_news() -> List[Dict[str, Any]]:
    """
    Stub for fetching crypto news headlines
    (integrate with CryptoPanic, etc.).
    """
    return [
        {
            "headline": "Bitcoin hits new high!",
            "source": "CryptoPanic",
            "timestamp": pd.Timestamp.now()
        }
    ]


def get_onchain_data(asset: str = 'BTC') -> Dict[str, Any]:
    """
    Stub for fetching on-chain analytics
    (integrate with Glassnode, etc.).
    """
    return {
        "whale_alerts": 0,
        "large_transfers": 0,
        "timestamp": pd.Timestamp.now()
    }


try:
    import pandas_ta as ta  # type: ignore
    has_ta = True
except ImportError:
    has_ta = False


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds common technical indicators to a DataFrame:
                                    (SMA, RSI, MACD, etc.).
    """
    if not has_ta:
        print("pandas-ta not installed. Skipping technical indicators.")
        return df
    df = df.copy()
    df['sma_20'] = ta.sma(df['close'], length=20)  # type: ignore
    df['rsi_14'] = ta.rsi(df['close'], length=14)  # type: ignore
    macd = ta.macd(df['close'])  # type: ignore
    if macd is not None:
        df['macd'] = macd['MACD_12_26_9']
        df['macd_signal'] = macd['MACDs_12_26_9']
    return df


def get_macro_data() -> Dict[str, Any]:
    """
    Stub for macroeconomic indicators
    (integrate with FRED, etc.).
    """
    return {
        "vix": None,
        "sp500": None,
        "timestamp": pd.Timestamp.now()
    }


def get_market_data(symbol: str = 'BTCUSD',
                    limit: int = 100) -> pd.DataFrame:
    """
    Fetches historical market data from Binance API.
    """
    api_url = f"https://api.binance.com/api/v3/klines? \
                symbol={symbol}&interval=1h&limit={limit}"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
            'ignore'
        ])
        df['open_time'] = pd.to_datetime(df['open_time'],  # type: ignore
                                         unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'],  # type: ignore
                                          unit='ms')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # type: ignore
        df = df.set_index('open_time')  # type: ignore
        print(f"Fetched {len(df)} data points for {symbol}")
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching market data: {e}")
        return pd.DataFrame()


def get_realtime_data(symbol: str = 'BTCUSD') -> Dict[str, Any]:
    """
    Fetches current real-time market data from Binance API.
    """
    api_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            'price': float(data['lastPrice']),
            'volume': float(data['volume']),
            'timestamp': pd.Timestamp.now()
        }
    except Exception as e:
        print(f"Error fetching real-time data: {e}")
        return {'price': None, 'volume': None,
                'timestamp': pd.Timestamp.now()
               }


if __name__ == "__main__":
    # Example usage
    historical_df = get_market_data(symbol='ETHUSDT', limit=5)
    print("\nHistorical Data Sample:")
    print(historical_df.head())

    realtime_price = get_realtime_data(symbol='BTCUSDT')
    print("\nReal-time Data Sample:")
    print(realtime_price)

    # Advanced features (scaffolded)
    order_book = get_order_book(symbol='BTCUSDT', limit=5)
    print("\nOrder Book Sample:")
    print(order_book)

    order_book_spread = get_order_book_spread(symbol='BTCUSDT', limit=5)
    print("\nOrder Book Spread Sample:")
    print(order_book_spread)

    # Note: WebSocket example is not run here as it requires an async env
    # import asyncio
    # asyncio.run(binance_ws_ticker(symbol='btcusdt'))

    news = get_crypto_news()
    print("\nCrypto News Sample:")
    print(news)

    onchain_data = get_onchain_data(asset='BTC')
    print("\nOn-Chain Data Sample:")
    print(onchain_data)

    macro_data = get_macro_data()
    print("\nMacroeconomic Data Sample:")
    print(macro_data)