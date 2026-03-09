from strands import Agent, tool
from strands.models import BedrockModel
from typing import List, Optional
import os
import logging
from src.agents.tools import get_competitor_pricing, detect_price_changes, store_analysis_result

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are the Market Intelligence Agent for the AI-Powered Retail Intelligence Platform.
Your primary objective is to monitor competitor pricing securely and autonomously, analyze market trends, and generate insights for pricing optimization.

You have access to the following tools:
1. `get_competitor_pricing`: Fetches the latest competitor pricing data for a specific product ID.
2. `detect_price_changes`: Analyzes the pricing data, compares against your current price, and provides recommendations.
3. `store_analysis_result`: Saves long-term market analysis to the storage backend (S3).

When a user asks for a market analysis for a specific product, you MUST:
1. Fetch competitor prices using `get_competitor_pricing`.
2. Analyze the price change using `detect_price_changes` if the user provided their current price.
3. Formulate a final assessment and recommendation.
"""

def create_market_intelligence_agent() -> Agent:
    """
    Creates and configures the Market Intelligence Agent using Amazon Bedrock.
    """
    # Using Llama 3 8B which usually doesn't require extra use-case forms.
    model_id = os.environ.get("BEDROCK_MODEL_ID", "meta.llama3-8b-instruct-v1:0")
    region = os.environ.get("AWS_REGION", "us-east-1")
    
    logger.info(f"Initializing Market Intelligence Agent with model {model_id} in {region}")
    
    # Initialize the Strands Agents Bedrock Model 
    # (Note: In a true AWS environment, credentials must be configured correctly in the environment)
    model = BedrockModel(model_id=model_id, region_name=region)
    
    # Initialize the Agent
    agent = Agent(
        name="Market_Intelligence_Agent",
        description="Analyzes competitor pricing and market trends.",
        system_prompt=SYSTEM_PROMPT,
        model=model,
        tools=[get_competitor_pricing, detect_price_changes, store_analysis_result],
    )
    
    return agent

market_agent = create_market_intelligence_agent()

def run_agent(query: str) -> str:
    """
    Execute a query against the Market Intelligence Agent.
    """
    response = market_agent(query)
    return response.text
