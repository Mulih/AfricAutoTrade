import asyncio
import os
from enum import BaseModel, Field
from binance import AsyncClient
import logging

logger = logging.getLogger(__name__)

MAX_POS_PCT         = 0.02
MAX_DAILY_LOSS_PCT  = 0.05
MAX_OPEN_POS        = 5

class RiskParams(BaseModel):
    max_position_size_percent:  float = Field(MAX_POS_PCT)
    max_daily_loss_percent:     float = Field(MAX_DAILY_LOSS_PCT)
    max_open_positions:         int   = Field(MAX_OPEN_POS)

class RiskManager:
    def __init__(self, capital: float, params: RiskParams = RiskParams()):
        self.initial        = capital
        self.current        = capital
        self.daily_loss     = 0.0
        self.open_positions: dict[str, float] = {}
        self.params = params
        self.client: AsyncClient | None = None

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.close_connection()

    async def check_position_size(self, symbol: str, qty: float) -> bool:
        # fetch price & compare against capital*max_position_size_percent
        pass