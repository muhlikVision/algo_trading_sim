import json
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def build_production_index(json_path: str, persist_directory: str = "./chroma_db"):
    """Loads, chunks, and embeds financial news with strict temporal metadata."""
    
    with open(json_path, 'r') as f:
        news_data = json.load(f)

    raw_documents = []
    for item in news_data:
        # We combine headline and content for context
        full_text = f"HEADLINE: {item['headline']}\n\nCONTENT: {item['content']}"
        metadata = {
            "date": item["date"],
            "ticker": item["ticker"]
        }
        raw_documents.append(Document(page_content=full_text, metadata=metadata))

    # ENTERPRISE UPGRADE: Chunking the text
    # This prevents blowing up the LLM context window
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunked_docs = text_splitter.split_documents(raw_documents)
    print(f"Split {len(raw_documents)} articles into {len(chunked_docs)} chunks.")

    embeddings = NVIDIAEmbeddings(model="NV-Embed-QA") 
    
    vectorstore = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print("Indexing complete. Database saved to disk.")
    return vectorstore