from typing import Tuple
import logging
from src.models.db import SessionLocal

logger = logging.getLogger(__name__)

class TradeService:
    """
    Parses LangChain QA insight into BUY/SELL/HOLD and logs the decision.
    """

    def __init__(self):
        self.db = SessionLocal()

    def parse_and_execute(self, symbol: str, insight: str) -> Tuple[str, dict]:
        # Determine action from insight
        text = insight.lower()
        if "buy" in text:
            decision = "BUY"
        elif "sell" in text:
            decision = "SELL"
        else:
            decision = "HOLD"

        # Log execution
        logger.info(f"Executing {decision} for {symbol}: {insight}")

        # (Placeholder) Save trade record or call external API here
        details = {
            "insight": insight,
            "executed_at": str(__import__("datetime").datetime.utcnow())
        }
        return decision, details

    def __del__(self):
        self.db.close()
