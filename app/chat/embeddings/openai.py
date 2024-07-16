from langchain_community.embeddings import OpenAIEmbeddings

#Creates the embeddings using a seperate AI
embeddings = OpenAIEmbeddings(model="gpt-4o")