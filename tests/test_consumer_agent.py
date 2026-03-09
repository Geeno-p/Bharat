import pytest
from hypothesis import given, strategies as st
from src.agents.consumer_tools import update_customer_segment

@given(st.lists(st.fixed_dictionaries({
    "amount": st.floats(min_value=0, max_value=1000)
})))
def test_update_customer_segment_logic(transactions):
    segment = update_customer_segment("test_user", transactions)
    
    total = sum(t["amount"] for t in transactions)
    if total > 100:
        assert segment == "VIP"
    elif total > 0:
        assert segment == "Regular"
    else:
        assert segment == "Inactive"
