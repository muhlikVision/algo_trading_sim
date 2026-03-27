class Portfolio:
    def __init__(self, initial_cash: float = 100000.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.shares = 0
        self.portfolio_history = []

    def execute_trade(self, decision: str, current_price: float, date: str, confidence: int):
        """Executes the trade based on the LLM's decision and updates the balance."""
        action_taken = "HELD"
        
        # We only trade if the LLM is reasonably confident
        if decision == "BUY" and confidence > 50 and self.cash >= current_price:
            # Buy as many shares as we can afford (simplified)
            shares_to_buy = self.cash // current_price
            self.shares += shares_to_buy
            self.cash -= shares_to_buy * current_price
            action_taken = f"BOUGHT {shares_to_buy} shares"

        elif decision == "SELL" and confidence > 50 and self.shares > 0:
            # Liquidate all shares
            self.cash += self.shares * current_price
            action_taken = f"SOLD {self.shares} shares"
            self.shares = 0

        # Calculate current total value (Cash + Asset Value)
        total_value = self.cash + (self.shares * current_price)
        
        # Log the day's state
        self.portfolio_history.append({
            "date": date,
            "action": action_taken,
            "price": current_price,
            "total_value": total_value
        })
        
        return action_taken

    def get_roi(self, current_price: float) -> float:
        """Calculates the Return on Investment."""
        current_value = self.cash + (self.shares * current_price)
        return ((current_value - self.initial_cash) / self.initial_cash) * 100