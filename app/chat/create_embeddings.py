from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.chat.vector_stores.pinecone import vector_store

#Creates embeddings for each of the splits of the pdf, with an ID to label the chunks of text
#Adds documents to the pinecone vectordatabase with a pdf_id
#Updates the metadata of the document/ text chunks
def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    
    loader = PyPDFLoader(pdf_path)
    docs = loader.load_and_split(text_splitter)
    print(docs)
    
    for doc in docs:
        doc.metadata = {
            "page":doc.metadata["page"],
            "text":doc.page_content,
            "pdf_id": pdf_id
        }
    
    vector_store.add_documents(docs)
