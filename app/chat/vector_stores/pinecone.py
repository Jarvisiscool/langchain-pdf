import os
import pinecone
from langchain.vectorstores import Pincecone
from app.chat.embeddings.openai import embeddings

pinecone.Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME")
)

vector_store = Pincecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)