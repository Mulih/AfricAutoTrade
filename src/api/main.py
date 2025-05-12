from fastapi import FastAPI, HTTPException
from src.data.alphavantage_fetcher import AlphaVantageFetcher
from src.data.binance_fetcher import BinanceFetcher
from src.data.models import StockData, CryptoData
from src.models.schemas import StockDataSchema, CryptoDataSchema, QARequest, QAResponse
from src.models.db import SessionLocal, engine, Base
from src.langchain_tools.vector_store import load_vector_store, create_vector_store
from src.langchain_tools.retrieval_chain import get_qa_chain
from src.settings.config import settings

app = FastAPI()

# Initialize DB
Base.metadata.create_all(bind=engine)

@app.post("/fetch/stock/{symbol}", response_model=StockDataSchema)
def fetch_stock(symbol: str):
    fetcher = AlphaVantageFetcher(settings.alpha_vantage_key)
    records = fetcher.fetch_data(symbol)
    if not records:
        raise HTTPException(status_code=404, detail="No stock data found")
    fetcher.store_data(records, StockData)
    return records[-1]

@app.post("/fetch/crypto/{symbol}", response_model=CryptoDataSchema)
def fetch_crypto(symbol: str):
    fetcher = BinanceFetcher(settings.binance_api_key, settings.binance_api_secret)
    records = fetcher.fetch_historical_data(symbol)
    if not records:
        raise HTTPException(status_code=404, detail="No crypto data found")
    fetcher.store_data(records, CryptoData)
    return records[-1]

@app.post("/qa", response_model=QAResponse)
def answer_question(req: QARequest):
    try:
        # Load or build vector store
        try:
            vs = load_vector_store()
        except:
            from src.langchain_tools.document_loader import load_documents_from_folder
            docs = load_documents_from_folder(settings.knowledge_base_path)
            vs = create_vector_store(docs)
        qa_chain = get_qa_chain(vs)
        result = qa_chain(req.question)
        return QAResponse(answer=result["result"], source_documents=[doc.page_content for doc in result["source_documents"]])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)