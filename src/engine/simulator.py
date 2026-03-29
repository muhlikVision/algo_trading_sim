import time
import pandas as pd
from src.engine.portfolio import Portfolio
from src.agent.quant_agent import QuantAgent
from src.rag.retriever import TimeAwareRetriever
from src.market_data import MarketDataFetcher

class BacktestEngine:
    def __init__(self):
        self.portfolio = Portfolio(initial_cash=100000.0)
        self.agent = QuantAgent()
        self.retriever = TimeAwareRetriever()
        
        #for custom csv market data
        #self.price_data = pd.read_csv(prices_csv_path)
        #self.price_data = self.price_data.sort_values(by="Date")

        #data from yahoo finance
        self.market_data = MarketDataFetcher()

    def run_simulation(self, ticker: str, days_back: int = 30):
        print(f"--- Starting LIVE Backtest for {ticker} ---")
        
        self.price_data = self.market_data.get_historical_prices(ticker, days_back)

        # 1. Create a list to store our daily data for the UI
        history = []
        
        for index, row in self.price_data.iterrows():
            current_date = row['Date']
            current_price = row['Close']
            
            # ... (keep your existing retriever and agent logic here) ...
            news_docs = self.retriever.get_news_for_date(ticker, current_date)
            llm_response = self.agent.analyze_and_decide(ticker, current_date, news_docs)
            
            action = self.portfolio.execute_trade(
                decision=llm_response.decision,
                current_price=current_price,
                date=current_date,
                confidence=llm_response.confidence
            )
            
            # 2. Add this day's data to our history list
            history.append({
                "date": current_date,
                "price": current_price,
                "action": action,
                "reasoning": llm_response.reasoning
            })
            
            time.sleep(3) # Your API rate limit delay

        # 3. Calculate final metrics and RETURN them instead of just printing
        final_value = self.portfolio.cash + (self.portfolio.shares * current_price)
        roi = ((final_value - 100000) / 100000) * 100
        
        print(f"--- Backtest Complete ---\nFinal ROI: {roi:.2f}%")
        
        # This is what Streamlit is waiting for!
        return {
        "final_value": final_value,
        "roi": roi,
        "history": history
        }