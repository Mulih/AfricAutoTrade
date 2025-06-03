import pandas as pd
from src.data_ingestion import (
    get_market_data, get_realtime_data, get_order_book,
    get_order_book_metrics, get_crypto_news, get_onchain_data
)


def test_get_market_data():
    df = get_market_data(symbol='BTCUSD', limit=5)
    assert isinstance(df, pd.DataFrame)
    assert 'close' in df.columns


def test_get_realtime_data():
    data = get_realtime_data(symbol='BTCUSD')
    assert isinstance(data, dict)
    assert 'price' in data
    assert 'volume' in data


def test_get_order_book():
    ob = get_order_book(symbol='BTCUSDT', limit=5)
    assert 'bids' in ob and 'asks' in ob
    assert isinstance(ob['bids'], list)


def test_get_order_book_metrics():
    metrics = get_order_book_metrics(symbol='BTCUSDT', limit=5)
    assert 'spread' in metrics
    assert 'imbalance' in metrics


def test_get_crypto_news():
    news = get_crypto_news()
    assert isinstance(news, list)
    assert 'headline' in news[0]


def test_get_onchain_data():
    data = get_onchain_data(asset='BTC')
    assert isinstance(data, dict)
    assert 'whale_alerts' in data
