from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from .vector_store import load_vector_store
from src.settings.config import settings

llm = OpenAI(openai_api_key=settings.openai_api_key)

def get_qa_chain(vector_store):
    retriever = vector_store.as_receiver()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain