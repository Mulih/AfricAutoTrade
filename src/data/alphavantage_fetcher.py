from limits import RateLimitItemPerMinute, RateLimitItemPerSecond
from limits.strategies import MovingWindow
from limits.storage import MemoryStorage
from limits.decorators import RateLimitDecorator

# DEfine rate limits
alpha_vantage_rate = RateLimitItemPerMinute(5)
binance_rate       = RateLimitItemPerSecond(10)

# Rate limiters
alpha_vantage_limiter = RateLimitDecorator(alpha_vantage_rate, strategy=MovingWindow, storage=MemoryStorage())
binance_limiter       = RateLimitDecorator(binance_rate, strategy=MovingWindow, storage=MemoryStorage())