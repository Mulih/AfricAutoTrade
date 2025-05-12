from fastapi import APIRouter, HTTPException
from src.langchain_tools.retrieval_chain import get_qa_chain
from src.langchain_tools.new_fetcher import fetch_latest_news
from src.langchain_tools.vector_store import load_vector_store, create_vector_store
from src.services.trade_service import TradeService
from src.settings.config import settings

router = APIRouter(prefix="/auto_trade")

@router.post("/{symbol}")
def auto_trade(symbol: str):
    # Refresh RAG store with latest news
    docs = fetch_latest_news(query=symbol)
    try:
        vs = load_vector_store()
        vs.add_documents(docs)
    except FileNotFoundError:
        vs = create_vector_store(docs)
    vs.save_local(settings.faiss_store_path)

    # Generate insight
    qa = get_qa_chain(vs)
    insight = qa(f"What is the market sentiment and recommendation for {symbol} today?")
    decision = TradeService.parse_and_execute(symbol, insight['result'])
    if not decision:
        raise HTTPException(500, "Trade execution failed")
    return {"symbol": symbol, "decision": decision, "insight": insight['result']}