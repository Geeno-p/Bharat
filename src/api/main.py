from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional
from src.api.auth import get_api_key
from src.models.core import Product, MarketData, Customer
from src.agents.market_intelligence import run_agent
from src.agents.consumer_profiler import run_consumer_analysis
from src.agents.demand_oracle import run_demand_forecast
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Retail Intelligence Platform MVP",
    description="Autonomous market intelligence and pricing optimization.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the AI-Powered Retail Intelligence Platform - VERSION V2-DEBUG",
        "docs": "/docs",
        "status": "online",
        "timestamp": "2026-03-15"
    }

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "retail-intelligence-mvp"}

@app.post("/analyze/market", tags=["Market Intelligence"])
async def analyze_market(
    product_id: str, 
    current_price: Optional[float] = None,
    api_key: str = Depends(get_api_key)
):
    """
    Triggers the Market Intelligence Agent to analyze a product's market position.
    """
    logger.info(f"Market analysis requested for product: {product_id}")
    try:
        query = f"Provide a market analysis for product ID {product_id}."
        if current_price:
            query += f" My current price is {current_price}."
            
        result = run_agent(query)
        return {
            "product_id": product_id,
            "analysis": result
        }
    except Exception as e:
        logger.error(f"Error during agent execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/customer", tags=["Customer Intelligence"])
async def analyze_customer(customer_id: str, api_key: str = Depends(get_api_key)):
    """
    Triggers consumer behavior analysis for a specific customer.
    """
    logger.info(f"Customer analysis requested for customer: {customer_id}")
    try:
        result = run_consumer_analysis(customer_id)
        return {"customer_id": customer_id, "analysis": result}
    except Exception as e:
        logger.error(f"Error during customer analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/demand", tags=["Inventory Intelligence"])
async def analyze_demand(product_id: str, api_key: str = Depends(get_api_key)):
    """
    Triggers demand forecasting and restocking analysis for a product.
    """
    logger.info(f"Demand analysis requested for product: {product_id}")
    try:
        result = run_demand_forecast(product_id)
        return {"product_id": product_id, "forecast": result}
    except Exception as e:
        logger.error(f"Error during demand analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/summary", tags=["Dashboard"])
async def get_dashboard_summary(api_key: str = Depends(get_api_key)):
    """
    Returns a summary of market intelligence for the dashboard (MVP version).
    """
    # In a full version, this would query a database
    # For MVP, we provide a placeholder response showing the structure
    return {
        "status": "success",
        "data": {
            "total_products_monitored": 10,
            "alerts_active": 2,
            "market_trends": "Stable",
            "last_updated": "2026-03-09T00:00:00Z"
        }
    }
