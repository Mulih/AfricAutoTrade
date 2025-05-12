from tenacity import retry, stop_after_attempt, wait_fixed
from src.models.db import SessionLocal
import logging

logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self):
        self.session = SessionLocal()

    def __del__(self):
        self.session.close()

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
    def fetch_data(self, *args, **kwargs):
        raise NotImplementedError

    def store_data(self, data_list, model):
        try:
            for record in data_list:
                exists = (
                    self.session.query(model)
                    .filter_by(symbol=record['symbol'], timestamp=record['timestamp'])
                    .first()
                )
                if not exists:
                    self.session.add(model(**record))
            self.session.commit()
            logger.info(f"Stored {len(data_list)} records to {model.__tablename__}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error storing data: {e}")
            raise


from limits import RateLimitItemPerMinute, RateLimitItemPerSecond
from limits.strategies import MovingWindowRateLimiter
from limits.storage import MemoryStorage


# DEfine rate limits
alpha_vantage_rate = RateLimitItemPerMinute(5)
binance_rate       = RateLimitItemPerSecond(10)

# Rate limiters
alpha_vantage_limiter = MovingWindowRateLimiter(alpha_vantage_rate, torage=MemoryStorage())
binance_limiter       = MovingWindowRateLimiter(binance_rate, storage=MemoryStorage())
