from langchain_openai import OpenAIEmbeddings

#Creates the embeddings using a seperate AI
embeddings = OpenAIEmbeddings(model="text-embedding-3-large",dimensions=1536)