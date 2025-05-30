import pandas as pd
import requests
from typing import Dict, Any

def get_market_data(symbol: str = 'BTCUSD', limit: int = 100) -> pd.DataFrame:
    """Fetches historical market data from Binance API (production-ready)."""
    api_url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit={limit}"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Binance returns: [open_time, open, high, low, close, volume, ...]
        df = pd.DataFrame(data, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.set_index('open_time')
        print(f"Fetched {len(df)} data points for {symbol}")
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching market data: {e}")
        return pd.DataFrame()

def get_realtime_data(symbol: str = 'BTCUSD') -> Dict[str, Any]:
    """Fetches current real-time market data from Binance API (production-ready)."""
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
        return {'price': None, 'volume': None, 'timestamp': pd.Timestamp.now()}

if __name__ == "__main__":
    # Example usage
    historical_df = get_market_data(symbol='ETHUSDT', limit=5)
    print("\nHistorical Data Sample:")
    print(historical_df.head())

    realtime_price = get_realtime_data(symbol='BTCUSDT')
    print("\nReal-time Data Sample:")
    print(realtime_price)