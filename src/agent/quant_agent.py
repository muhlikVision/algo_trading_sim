import os
from pydantic import BaseModel, Field
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from src.agent.prompts import quant_prompt_template

# 1. Define the strict output schema (The Recruiter Hook)
class TradingDecision(BaseModel):
    decision: str = Field(description="Must be exactly 'BUY', 'SELL', or 'HOLD'")
    confidence: int = Field(description="An integer from 0 to 100 indicating confidence in the decision")
    reasoning: str = Field(description="A concise, one-sentence justification based ONLY on the provided news")

class QuantAgent:
    def __init__(self):
        # Initialize Nemotron. 
        # We set temperature=0.1 because we want highly deterministic, logical outputs, not creative storytelling.
        # Ensure you use the exact model ID for Nemotron 3 from your NVIDIA NIM dashboard.
        self.llm = ChatNVIDIA(model="nvidia/nemotron-4-340b-instruct", temperature=0.1) 
        
        # 2. Bind the Pydantic schema to the LLM
        self.structured_llm = self.llm.with_structured_output(TradingDecision)
        
        # 3. Create the LangChain pipeline
        self.chain = quant_prompt_template | self.structured_llm

    def analyze_and_decide(self, ticker: str, current_date: str, news_docs: list) -> TradingDecision:
        """Passes the context to Nemotron and returns a validated Pydantic object."""
        
        # Extract the text from the retrieved LangChain Document objects
        news_texts = [doc.page_content for doc in news_docs]
        
        # Combine the chunks into a single string for the prompt
        if news_texts:
            news_context = "\n---\n".join(news_texts)
        else:
            news_context = "No significant news found for this period."
        
        print(f"[{current_date}] Asking Nemotron for a decision on {ticker}...")
        
        # Execute the chain
        result = self.chain.invoke({
            "ticker": ticker,
            "current_date": current_date,
            "news_context": news_context
        })
        
        return result

# Quick test if you run this file directly
if __name__ == "__main__":
    # Make sure you've exported your NVIDIA_API_KEY in your terminal!
    if not os.environ.get("NVIDIA_API_KEY"):
        print("Warning: Please set your NVIDIA_API_KEY environment variable.")
    else:
        agent = QuantAgent()
        
        # Mocking a retrieved LangChain document to test the system
        class MockDoc:
            def __init__(self, text):
                self.page_content = text
                
        mock_news = [MockDoc("Apple announces record-breaking iPhone sales in Q1, exceeding all analyst expectations.")]
        
        decision = agent.analyze_and_decide("AAPL", "2022-03-12", mock_news)
        
        # Because we used Pydantic, 'decision' is a Python object, not a raw string.
        print("\n--- LLM Output ---")
        print(f"Action: {decision.decision}")
        print(f"Confidence: {decision.confidence}%")
        print(f"Reasoning: {decision.reasoning}")