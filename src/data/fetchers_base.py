from functools import wraps
from limits import RateLimitItemPerMinute, RateLimitItemPerSecond
from limits.strategies import MovingWindowRateLimiter
from limits.storage import MemoryStorage
from tenacity import retry, stop_after_attempt, wait_fixed
from src.models.db import SessionLocal
import logging

logger = logging.getLogger(__name__)

# Define rate limits
alpha_vantage_rate = RateLimitItemPerMinute(5)
binance_rate       = RateLimitItemPerSecond(10)

# Initialize storage
storage = MemoryStorage()

# Rate limiters
alpha_vantage_limiter = MovingWindowRateLimiter(storage)
binance_limiter = MovingWindowRateLimiter(storage)

# Use the rate limiters wiith defined rates
alpha_vantage_limiter.hit(alpha_vantage_rate)
binance_limiter.hit(binance_rate)

# Custom rate-limiting decorator
def rate_limiter(limiter, rate):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not limiter.hit(rate):
                raise Exception("Rate limit exceeded")
            return func(*args, **kwargs)
        return wrapper
    return decorator

class DataFetcher:
    def __init__(self):
        self.session = SessionLocal()

    def __del__(self):
        self.session.close()

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
    def fetch_data(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement fetch_data()")

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
