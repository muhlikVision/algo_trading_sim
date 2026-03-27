from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

class TimeAwareRetriever:
    def __init__(self, persist_directory: str = "./chroma_db"):

        self.embeddings = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5")
        self.vectorstore = Chroma(
            persist_directory=persist_directory, 
            embedding_function=self.embeddings
        )

    def get_news_for_date(self, ticker: str, current_sim_date: str, k: int = 3):
        query_date_int = int(current_sim_date.replace("-", "")) #for freakin chroma db restrictions
        
        metadata_filter = {
            "$and": [
                {"ticker": {"$eq": ticker}},
                {"date_int": {"$lte": query_date_int}} # Query the integer field!
            ]
        }

        query = f"Financial news and sentiment for {ticker}"
        
        return self.vectorstore.similarity_search(
            query=query,
            k=k,
            filter=metadata_filter
        )