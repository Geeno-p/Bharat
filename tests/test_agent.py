import pytest
from hypothesis import given, strategies as st
from src.agents.tools import detect_price_changes, get_competitor_pricing, MOCK_MARKET_DATA

@given(st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False))
def test_detect_price_changes_behavior(current_price):
    """
    Property: detect_price_changes should always return a valid analysis string
    based on the relationship between current_price and competitor prices.
    """
    product_id = "p1" # Using product in mock data
    analysis = detect_price_changes(product_id, current_price)
    
    # MOCK_MARKET_DATA is still a list of dicts in the file, but get_competitor_pricing returns objects
    competitor_data = [d for d in MOCK_MARKET_DATA if d["product_id"] == product_id]
    min_comp_price = min(d["price"] for d in competitor_data)
    
    if current_price > min_comp_price:
        assert "ALERT" in analysis
    elif current_price < min_comp_price:
        assert "highly competitive" in analysis
    else:
        assert "matched" in analysis

def test_get_competitor_pricing_valid_product():
    """Verify that mock data is returned correctly for existing products."""
    results = get_competitor_pricing("p1")
    assert len(results) > 0
    assert all(d.product_id == "p1" for d in results)

def test_get_competitor_pricing_invalid_product():
    """Verify that empty list is returned for non-existent products."""
    results = get_competitor_pricing("non_existent")
    assert len(results) == 0

@given(st.text())
def test_detect_price_changes_no_data(product_id):
    """Property: If no competitor data exists, detect_price_changes returns a specific message."""
    # Ensure product_id is not in mock data
    if any(d["product_id"] == product_id for d in MOCK_MARKET_DATA):
        return
        
    analysis = detect_price_changes(product_id, 100.0)
    assert "No competitor data found" in analysis
