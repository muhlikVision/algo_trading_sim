from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.engine.simulator import BacktestEngine

# Create a router to organize our endpoints
router = APIRouter()

# Define what the user needs to send us
class SimulationRequest(BaseModel):
    #ticker: str
    ticker: str = "AAPL"
    prices_csv_path: str = "data/historical_prices.csv"

@router.post("/api/v1/simulate")
async def run_trading_simulation(request: SimulationRequest):
    """
    Triggers a backtest simulation for a given stock ticker.
    """
    try:
        # Initialize the engine with the provided CSV
        engine = BacktestEngine(prices_csv_path=request.prices_csv_path)
        
        # Run the simulation
        results = engine.run_simulation(ticker=request.ticker)
        
        # Return the JSON results
        return {
            "status": "success",
            "message": "Simulation completed successfully.",
            "data": results
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Price data CSV not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")