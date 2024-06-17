import os
import pinecone
from langchain.vectorstores import Pinecone
from app.chat.embeddings.openai import embeddings

#creates the embeddings into a pinecone vectordatabase to extract from later
pinecone.Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME")
)

vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)

#Is a retriver and does a simliarity search in order to find the correct embeddings
def build_retriever(chat_args, k):
    search_kwargs={"filter": {"pdf_id": chat_args.pdf_id}, "k":k}
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )