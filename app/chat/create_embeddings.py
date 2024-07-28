from vectore_store.pinecone import vector_store
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_embeddings_for_md(raw_data, md_id: str, md_path: str):
    markdown_document = raw_data
    
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, strip_headers=False
    )
    
    md_header_splits = markdown_splitter.split_text(markdown_document)
    
    chunk_size = 250
    chunk_overlap = 30
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_documents(md_header_splits)

    for split in splits:
        split.metadata = {
            "page":split.metadata["page"],
            "text":split.page_content,
            "md_id": md_id
        }
    
    vector_store.add_documents(splits)
