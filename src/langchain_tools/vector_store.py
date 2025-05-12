from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from src.settings.config import settings

embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

def create_vector_store(documents, store_path="faiss_store"):
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(store_path)
    return vector_store

def load_vector_store(store_path="faiss_store"):
    return FAISS.load_local(store_path, embeddings)