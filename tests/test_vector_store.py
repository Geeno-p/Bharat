import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from src.db.vector_store import VectorStore
import os
import shutil
import numpy as np

@pytest.fixture
def temp_store():
    test_dir = "data/test_lancedb"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    store = VectorStore(test_dir)
    store.init_tables()
    yield store
    shutil.rmtree(test_dir)

@settings(deadline=None, suppress_health_check=list(HealthCheck))
@given(
    st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    st.lists(st.floats(min_value=-1.0, max_value=1.0), min_size=384, max_size=384)
)
def test_vector_search_reliability(item_id, vector):
    # Use a unique directory for each example to ensure isolation
    import uuid
    test_dir = f"data/test_lancedb_{uuid.uuid4()}"
    store = VectorStore(test_dir)
    store.init_tables()
    
    try:
        # Prepare data
        data = [{
            "id": item_id,
            "name": "Test Item",
            "category": "Test",
            "price": 10.0,
            "vector": vector,
            "metadata": "{}"
        }]
        
        # Add data
        store.add_products(data)
        
        # Search for the same vector
        results = store.search_products(vector, limit=1)
        
        assert len(results) > 0
        assert results[0]["id"] == item_id
    finally:
        # Clean up
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)

def test_vector_store_initialization():
    test_dir = "data/test_init_lancedb"
    if os.path.exists(test_dir):
        import shutil
        shutil.rmtree(test_dir)
    store = VectorStore(test_dir)
    store.init_tables()
    assert "products" in store.db.table_names()
    assert "customers" in store.db.table_names()
    if os.path.exists(test_dir):
        import shutil
        shutil.rmtree(test_dir)
