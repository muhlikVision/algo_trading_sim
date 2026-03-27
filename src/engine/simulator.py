import time
import pandas as pd
from src.engine.portfolio import Portfolio
from src.agent.quant_agent import QuantAgent
from src.rag.retriever import TimeAwareRetriever

class BacktestEngine:
    def __init__(self, prices_csv_path: str):
        self.portfolio = Portfolio(initial_cash=100000.0)
        self.agent = QuantAgent()
        self.retriever = TimeAwareRetriever()
        
        # Load historical price data
        self.prices_df = pd.read_csv(prices_csv_path)
        # Ensure it's sorted by date so we step through time correctly
        self.prices_df = self.prices_df.sort_values(by="Date")

    def run_simulation(self, ticker: str):
        print(f"--- Starting Backtest for {ticker} ---")
        
        # Loop through time, day by day
        for index, row in self.prices_df.iterrows():
            current_date = row['Date']
            current_price = row['Close']
            
            print(f"\n[Date: {current_date} | Price: ${current_price:.2f}]")
            
            # 1. Retrieve context (Strictly <= current_date)
            news_docs = self.retriever.get_news_for_date(ticker, current_date)
            
            print(f"DEBUG: Database found {len(news_docs)} articles for {current_date}")

            # 2. Get LLM Decision
            llm_response = self.agent.analyze_and_decide(ticker, current_date, news_docs)
            
            # 3. Execute Trade based on LLM's strict JSON output
            action = self.portfolio.execute_trade(
                decision=llm_response.decision,
                current_price=current_price,
                date=current_date,
                confidence=llm_response.confidence
            )
            
            print(f"Agent Reasoning: {llm_response.reasoning}")
            print(f"Engine Action: {action}")
            print(f"Current Portfolio Value: ${self.portfolio.cash + (self.portfolio.shares * current_price):.2f}")
            
            time.sleep(3)

        # Final Report
        final_price = self.prices_df.iloc[-1]['Close']
        roi = self.portfolio.get_roi(final_price)
        print(f"\n--- Backtest Complete ---")
        print(f"Final ROI: {roi:.2f}%")