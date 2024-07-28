from langchain_community.vectorstores import Pinecone
import pinecone
import os
from app.chat.embeddings.openai import embeddings
# Initialize Pinecone
pinecone.Pinecone(api_key= os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV_NAME"))

# Use Pinecone index
vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)
def build_retriever(chat_args, k):
    search_kwargs={"filter": {"md_id": chat_args.md_id}, "k":k}
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )