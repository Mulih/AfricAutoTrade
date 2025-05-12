from src.langchain_tools.document_loader import load_documents_from_folder
from src.langchain_tools.vector_store import create_vector_store, load_vector_store
from src.langchain_tools.retrieval_chain import get_qa_chain

# Load docs from local path
docs = load_documents_from_folder("data/docs")

# Create or load FAISS index
try:
    vs = load_vector_store()
except Exception:
    vs = create_vector_store(docs)

# Get chain and ask a question
qa = get_qa_chain(vs)
question = "What is the current trend-following strategy?"
result = qa(question)
print(result)