import logging
from typing import List, Dict, Any, Optional
from strands import tool
from src.models.core import Customer, Transaction

logger = logging.getLogger(__name__)

# Mock data for Phase 2 implementation using Transaction model
MOCK_TRANSACTIONS = [
    Transaction(transaction_id="t1", customer_id="c1", product_id="p1", amount=150.0, quantity=1),
    Transaction(transaction_id="t2", customer_id="c1", product_id="p2", amount=20.0, quantity=2),
    Transaction(transaction_id="t3", customer_id="c2", product_id="p1", amount=10.0, quantity=1),
]

@tool
def get_customer_transactions(customer_id: str) -> List[Transaction]:
    """
    Fetches the historical transaction data for a given customer and returns a list of Transaction objects.
    """
    logger.info(f"Fetching transactions for customer: {customer_id}")
    return [t for t in MOCK_TRANSACTIONS if t.customer_id == customer_id]

@tool
def update_customer_segment(customer_id: str) -> str:
    """
    Analyzes historical transactions for a customer and updates their market segment.
    """
    transactions = get_customer_transactions(customer_id)
    total_spent = sum(t.amount for t in transactions)
    
    if total_spent > 100:
        segment = "VIP"
    elif total_spent > 0:
        segment = "Regular"
    else:
        segment = "Inactive"
        
    logger.info(f"Updating customer {customer_id} to segment: {segment}")
    return segment
