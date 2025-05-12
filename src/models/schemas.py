from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class StockDataSchema(BaseModel):
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

class CryptoDataSchema(StockDataSchema):
    pass

class QARequest(BaseModel):
    question: str

class QAResponse(BaseModel):
    answer: str
    source_documents: List[Dict]