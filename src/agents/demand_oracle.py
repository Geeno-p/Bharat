import os
import logging
from typing import Optional
from strands import Agent
from strands.models import Message
from src.agents.demand_tools import get_inventory_status, get_historical_demand, save_demand_forecast

logger = logging.getLogger(__name__)

def create_demand_oracle_agent() -> Agent:
    """
    Creates and configures the DemandOracle agent.
    """
    model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")
    
    agent = Agent(
        name="DemandOracle",
        role="You are an expert inventory analyst and demand forecaster for a retail platform.",
        objective="Analyze inventory levels and historical sales to provide accurate demand forecasts and restock recommendations.",
        model_id=model_id,
        tools=[get_inventory_status, get_historical_demand, save_demand_forecast]
    )
    
    return agent

# Singleton instance
demand_oracle_agent = create_demand_oracle_agent()

def run_demand_forecast(product_id: str) -> str:
    """
    Execute a demand forecast query for a specific product.
    """
    query = f"Provide a demand forecast and restock recommendation for product {product_id}. Check current inventory first."
    response = demand_oracle_agent(query)
    # Extract text from the message content blocks (using the fix from previous step)
    text_blocks = [block['text'] for block in response.message['content'] if 'text' in block]
    return "".join(text_blocks).strip()
