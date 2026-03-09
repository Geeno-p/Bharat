import logging
from typing import List, Dict, Any, Optional
from strands import tool
from src.models.core import Customer, Transaction

logger = logging.getLogger(__name__)

# Mock data for Phase 2 implementation
MOCK_TRANSACTIONS = [
    {"transaction_id": "t1", "customer_id": "c1", "product_id": "p1", "amount": 150.0, "quantity": 1},
    {"transaction_id": "t2", "customer_id": "c1", "product_id": "p2", "amount": 20.0, "quantity": 2},
    {"transaction_id": "t3", "customer_id": "c2", "product_id": "p1", "amount": 10.0, "quantity": 1},
]

@tool
def get_customer_transactions(customer_id: str) -> List[Dict[str, Any]]:
    """
    Fetches the historical transaction data for a given customer.
    """
    logger.info(f"Fetching transactions for customer: {customer_id}")
    return [t for t in MOCK_TRANSACTIONS if t["customer_id"] == customer_id]

@tool
def update_customer_segment(customer_id: str, transactions: List[Dict[str, Any]]) -> str:
    """
    Analyzes transaction history and updates the customer's market segment.
    """
    total_spent = sum(t["amount"] for t in transactions)
    
    if total_spent > 100:
        segment = "VIP"
    elif total_spent > 0:
        segment = "Regular"
    else:
        segment = "Inactive"
        
    logger.info(f"Updating customer {customer_id} to segment: {segment}")
    return segment
