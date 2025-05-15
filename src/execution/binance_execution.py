import logging

logger = logging.getLogger(__name__)

class ExecutionError(Exception):
    """Custom exception for execution errors"""
    pass

class CircuitBreaker:
    """
    Circuit breaker to halt trading after repeated failures.
    """
    def __init__(self, max_failures: int = 3):
        self.max_failures = max_failures
        self.failure_count = 0
        self.tripped = False

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.max_failures:
            self.tripped = True
            logger.error("Circuit breaker tripped! Trading halted.")

    def reset(self):
        self.failure_count = 0
        self.tripped = False

    def is_tripped(self) -> bool:
        return self.tripped


class BinanceExecutionClient:
    """
    Binance execution client with error handling and circuit breaker
    """
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.circuit_breaker = CircuitBreaker()