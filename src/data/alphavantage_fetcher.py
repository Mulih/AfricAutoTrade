import os
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from typing import List, Dict, Any
from .fetchers_base import DataFetcher, rate_limiter, alpha_vantage_limiter, alpha_vantage_rate
from .models import StockData


class AlphaVantageFetcher(DataFetcher):
    def __init__(self, api_key: str):
        super().__init__()
        self.ts = TimeSeries(key=api_key, output_format='json')

    @rate_limiter(alpha_vantage_limiter, alpha_vantage_rate)
    def fetch_data(self, symbol: str, interval: str = 'daily') -> List[Dict[str, Any]]:
        raw, _ = self.ts.get_daily(symbol=symbol, outputsize='full')
        processed = []
        for ts, vals in raw.items():
            dt = datetime.strptime(ts, '%Y-%m-%d')
            processed.append({
                'symbol': symbol,
                'timestamp': dt,
                'open': float(vals['1. open']),
                'high': float(vals['2. high']),
                'low': float(vals['3. low']),
                'close': float(vals['4. close']),
                'volume': float(vals['5. volume']),
                'source': 'Alpha Vantage'
            })
        return processed