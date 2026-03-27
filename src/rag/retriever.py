from langchain_community.vectorstores import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

class TimeAwareRetriever:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.embeddings = NVIDIAEmbeddings(model="NV-Embed-QA")
        self.vectorstore = Chroma(
            persist_directory=persist_directory, 
            embedding_function=self.embeddings
        )

    def get_news_for_date(self, ticker: str, current_sim_date: str, k: int = 3):
        metadata_filter = {
            "$and": [
                {"ticker": {"$eq": ticker}},
                {"date": {"$lte": current_sim_date}}
            ]
        }

        query = f"Financial news and sentiment for {ticker}"

        # Return the actual Document objects, not just strings
        return self.vectorstore.similarity_search(
            query=query,
            k=k,
            filter=metadata_filter
        )