import os
from binance import Client
from datetime import datetime
from typing import List, Dict, Any
from .fetchers_base import DataFetcher, rate_limiter, binance_limiter
from .models import CryptoData
from .fetchers_base import binance_limiter, binance_rate

class BinanceFetcher(DataFetcher):
    def __init__(self, api_key: str, api_secret: str):
        super().__init__()
        self.client = Client(api_key, api_secret)

    @rate_limiter(binance_limiter, binance_rate)
    def fetch_historical_data(self, symbol: str, interval: str = '1m', start_str: str = '1 Jan. 2017') -> List[Dict[str, Any]]:
        klines = self.client.get_historical_klines(symbol, interval, start_str)
        data = []
        for k in klines:
            dt = datetime.fromtimestamp(k[0]/1000)
            data.append({
                'symbol': symbol,
                'timestamp': dt,
                'open': float(k[1]),
                'high': float(k[2]),
                'low': float(k[3]),
                'close': float(k[4]),
                'volume': float(k[5]),
                'source': 'Binance'
            })
        return data