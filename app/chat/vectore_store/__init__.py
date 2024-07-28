from .pinecone import build_retriever
#creates a brand new function, using a current function that will recieve any **kwargs that it is next to
#loading up the kwargs ahead so we don't have to specify them later
from functools import partial

#Dictionary that holds keys for retrievers
retriever_map = {
    "pinecone_1": partial(build_retriever, k=1),
    "pinecone_2": partial(build_retriever, k=2),
    "pinecone_3": partial(build_retriever, k=3)
}