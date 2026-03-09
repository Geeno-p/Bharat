from strands import Agent, tool
from strands.models import BedrockModel
from typing import List, Optional
import os
import logging
from .consumer_tools import get_customer_transactions, update_customer_segment

logger = logging.getLogger(__name__)

def create_consumer_profiler_agent() -> Agent:
    """
    Creates and configures the ConsumerProfiler Agent.
    """
    model_id = os.environ.get("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")
    region = os.environ.get("AWS_REGION", "us-east-1")
    
    logger.info(f"Initializing ConsumerProfiler Agent with model {model_id}")
    
    model = BedrockModel(model_id=model_id, region_name=region)
    
    system_prompt = """
    You are an expert Consumer Behavior Analyst. Your goal is to analyze customer transaction history
    and provide deep insights into their purchasing patterns and segment them into meaningful categories.
    
    You have access to the following tools:
    - get_customer_transactions: Fetches historical transactions.
    - update_customer_segment: Categorizes the customer based on spending.
    
    Provide a concise summary of the customer's profile and recommend actions to improve engagement.
    """
    
    return Agent(
        model=model,
        tools=[get_customer_transactions, update_customer_segment],
        description=system_prompt
    )

consumer_agent = create_consumer_profiler_agent()

def run_consumer_analysis(customer_id: str) -> str:
    """
    Execute a customer analysis query.
    """
    query = f"Analyze customer {customer_id} and update their segment."
    response = consumer_agent(query)
    # Extract text from the message content blocks
    text_blocks = [block['text'] for block in response.message['content'] if 'text' in block]
    return "".join(text_blocks).strip()
