import pytest
from src.rag.retriever import TimeAwareRetriever

@pytest.fixture
def retriever():
    # Initialize your retriever (pointing to a test database in a real scenario)
    return TimeAwareRetriever(persist_directory="./chroma_db")

def test_no_look_ahead_bias(retriever):
    """
    CRITICAL TEST: Ensures the RAG system cannot retrieve news from the future.
    """
    sim_date = "2022-03-12"
    ticker = "AAPL"
    
    # Attempt to fetch news for the simulation day
    retrieved_docs = retriever.get_news_for_date(ticker=ticker, current_sim_date=sim_date, k=5)
    
    for doc in retrieved_docs:
        # Extract the date from the retrieved document's metadata
        # (You'll need to modify your retriever slightly to return the full Document, 
        # not just the page_content string, for this test to work)
        doc_date = doc.metadata.get("date")
        
        # Assert that the document's date is LESS THAN OR EQUAL TO the simulation date
        assert doc_date <= sim_date, f"Data Leakage Detected! Retrieved future article from {doc_date}"