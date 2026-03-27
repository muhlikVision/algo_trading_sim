from src.rag.retriever import TimeAwareRetriever

print("Starting Database X-Ray...")
retriever = TimeAwareRetriever()

# .get() pulls everything currently saved in the database
all_docs = retriever.vectorstore.get()

total_saved = len(all_docs['ids'])
print(f"Total articles physically saved in Chroma: {total_saved}")

if total_saved > 0:
    print("\n--- Metadata for Article 1 ---")
    print(all_docs['metadatas'][0])