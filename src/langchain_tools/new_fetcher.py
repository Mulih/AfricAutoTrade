from newsapi import NewsApiClient
from datetime import datetime, timedelta
from langchain.docstore.document import Document
from src.settings.config import settings

newsapi = NewsApiClient(api_key=settings.newsapi_key)

def fetch_latest_news(query: str = "financial markets") -> list[Document]:
    """
    Fetch articles from the last 24h and convert to LangChain Documents.
    """
    since = (datetime.utcnow() - timedelta(days=1)).isoformat()
    resp = newsapi.get_everything(
        q=query,
        from_param=since,
        sort_by="publishedAt",
        language="en",
    )
    docs = []
    for art in resp.get("articles", []):
        content = f"{art['title']} \
{art.get('description','')}"
        metadata = {
            "source": art['source']['name'],
            "publishedAt": art['publishedAt'],
            "url": art['url'],
        }
        docs.append(Document(page_content=content, metadata=metadata))

    return docs