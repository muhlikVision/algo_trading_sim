import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class MarketDataFetcher:
    def get_historical_prices(self, ticker: str, days_back: int = 30) -> pd.DataFrame:
        """
        Fetches live historical daily prices from Yahoo Finance.
        """
        print(f"📡 Fetching live market data for {ticker}...")
        
        # Calculate our date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Download the data
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        
        
        df = df.reset_index()
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        print(f"✅ Successfully downloaded {len(df)} days of data for {ticker}.")
        return df