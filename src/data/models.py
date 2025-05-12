from sqlalchemy import Column, Integer, String, Float, DateTime
from src.models.db import Base

class StockData(Base):
    __tablename__ = "stock_data"
    id        = Column(Integer, primary_key=True)
    symbol    = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    open      = Column(Float)
    high      = Column(Float)
    low       = Column(Float)
    close     = Column(Float)
    volume    = Column(Float)
    source    = Column(String)

class CryptoData(Base):
    __tablename__ = "crypto_data"
    id            = Column(Integer, primary_key=True)
    symbol        = Column(String, index=True)
    timestamp     = Column(DateTime, index=True)
    open          = Column(Float)
    high          = Column(Float)
    low           = Column(Float)
    close         = Column(Float)
    volume        = Column(Float)
    source        = Column(String)