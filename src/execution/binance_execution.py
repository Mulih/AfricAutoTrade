import os, asyncio
from binance import AsyncClient
from binance.exceptions import BinanceAPIException, BinanceOrderException
from tenacity import retry, stop_after_attempt, wait_exponential
from limits import RateLimitDecorator, parse_many, strategies
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

# Rate limiting for orders
order_limits    = parse_many("10 orders/second, 100 orders/minute")
order_strategy  = strategies.MovingWindow
order_limiter     = RateLimitDecorator(order_limits, strategy=order_strategy)

class OrderParams(BaseModel):
    symbol:         str
    side:           str
    quantity:       float
    order_type:     str = "MARKET"
    price:          float | None = None
    stop_price:     float | None = None
    time_in_force:  str | None = "GTC"

class BinanceExecutionClient:
    def __init__(self, api_key: str, secret: str):
        self.api_key    = api_key
        self.secret     = secret
        self.client: AsyncClient | None = None

    async def __aexit__(self, exec_type, exec_val, exc_tb):
        if self.client:
            await self.client.close_connection()

    @order_limiter
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=60))
    async def execute_order(self, params: OrderParams):
        if not self.client:
            raise RuntimeError("client not initialized")
        try:
            if params.order_type == "MARKET":
                return await self.client.create_order(
                    symbol=params.symbol,
                    side=params.side,
                    type="MARKET",
                    quantity=params.quantity
                )
            # add LIMIT, STOP logic similarly
        except BinanceAPIException as e:
            logger.error("Binance API error: %s", e)
        except BinanceOrderException as e:
            logger.error("Binance order error: %s", e)
        return None

# Example use:
# async with BinanceExecutionClient(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_SECRET_KEY")) as exec:
#     resp = await exec.execute_order(OrderParams(symbol="BTCUSDT", side="BUY", quantity=0.01))
#     logger.info(resp)