from fastapi import FastAPI, HTTPException, BackgroundTasks
import logging
from src.data.alphavantage_fetcher import AlphaVantageFetcher
from src.data.binance_fetcher import BinanceFetcher
from src.data.models import StockData, CryptoData
from src.models.schemas import StockDataSchema, CryptoDataSchema, QARequest, QAResponse
from src.models.db import SessionLocal, engine, Base
from src.langchain_tools.vector_store import load_or_rebuild_vector_store, create_vector_store
from src.langchain_tools.retrieval_chain import get_qa_chain
from dotenv import load_dotenv
from src.settings.config import settings


load_dotenv()

logger = logging.getLogger(__name__)
app = FastAPI()

# Initialize DB
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to AfricAutoTrade API!"}

@app.post("/fetch/stock/{symbol}", response_model=StockDataSchema)
def fetch_stock(symbol: str):
    fetcher = AlphaVantageFetcher(settings.alpha_vantage_key)
    records = fetcher.fetch_data(symbol)
    if not records:
        raise HTTPException(status_code=404, detail="No stock data found")
    fetcher.store_data(records, StockData)

    session = SessionLocal()
    try:
        # Fetch the most recent record from DB
        latest = session.query(StockData).filter_by(symbol=symbol).order_by(StockData.timestamp.desc()).first()
        if not latest:
            raise HTTPException(status_code=404, detail="Stored data not found in DB")
        return latest
    finally:
        session.close()

@app.post("/fetch/crypto/{symbol}")
def fetch_crypto(symbol: str, background_tasks: BackgroundTasks):
    """Enqueue crypto ingestion and return the latest record"""
    fetcher = BinanceFetcher(settings.binance_api_key, settings.binance_api_secret)
    background_tasks.add_task(__ingest_crypto, fetcher, symbol)

    # Fetch the most recent record from the database
    session = SessionLocal()
    try:
        latest = session.query(CryptoData).filter_by(symbol=symbol).order_by(CryptoData.timestamp.desc()).first()
        if not latest:
            raise HTTPException(status_code=404, detail="Stored crypto data not found in DB")
        return latest
    finally:
        session.close()


def __ingest_crypto(fetcher: BinanceFetcher, symbol: str):
    records = fetcher.fetch_historical_data(symbol)
    if not records:
        logger.warning(f"No crypto data found during background ingest for {symbol}")
        return
    fetcher.store_data(records, CryptoData)

@app.post("/qa", response_model=QAResponse)
def answer_question(req: QARequest):
    try:
        # Load or build vector store
        vs = load_or_rebuild_vector_store()

        # Get QA chain and processes the question.
        qa_chain = get_qa_chain(vs)
        result = qa_chain(req.question)
        return QAResponse(answer=result["result"], source_documents=[doc.page_content for doc in result["source_documents"]])
    except Exception as e:
        logging.error(f"Error in answer_question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)