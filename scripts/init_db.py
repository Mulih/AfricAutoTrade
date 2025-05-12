from src.models.db import engine, Base
from src.data.models import StockData, CryptoData
from src.data.alphavantage_fetcher import AlphaVantageFetcher
from src.data.binance_fetcher import BinanceFetcher
import os

# Create tables
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully")

def main():
    av = AlphaVantageFetcher(os.getenv('Alpha-vantage-key'))
    stock_records = av.fetchdata('AAPL')
    av.store_data(stock_records, StockData)

    # Fecth sample crypto data
    bn = BinanceFetcher(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'))
    crypto_records = bn.fetch_historical_data('BTCUSDT')
    bn.store_data(crypto_records, CryptoData)


if __name__ == "__main__":
    main()