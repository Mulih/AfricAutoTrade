import logging
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from src.settings.config import settings
from src.langchain_tools.document_loader import load_documents_from_folder

logger = logging.getLogger(__name__)

embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

def create_vector_store(documents, store_path="faiss_store"):
    """Create a new FAISS vector store from documents and save it locally"""
    logger.info(f"Creating vector store at {store_path}")
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(store_path)
    logger.info(f"Vector store created and saved at {store_path}")
    return vector_store

def load_vector_store(store_path="faiss_store"):
    logger.info(f"Loading vector store from {store_path}")
    return FAISS.load_local(store_path, embeddings)

def load_or_rebuild_vector_store(store_path="faiss_store"):
    """Load the vector store if it exists, otherwise rebuild it"""
    try:
        return load_vector_store(store_path)
    except Exception as e:
        logger.warning(f"Vector store not found or failed to load. Rebuilding: {e}")
        # Load documents from the knowledge base path
        docs = load_documents_from_folder(settings.knowledge_base_path)
        return create_vector_store(docs, store_path)