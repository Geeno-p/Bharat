import lancedb
import pyarrow as pa
import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, uri: str = "data/lancedb"):
        self.uri = uri
        os.makedirs(os.path.dirname(uri), exist_ok=True)
        self.db = lancedb.connect(uri)
        self.product_table_name = "products"
        self.customer_table_name = "customers"

    def _get_or_create_table(self, name: str, schema: pa.Schema):
        if name in self.db.table_names():
            return self.db.open_table(name)
        return self.db.create_table(name, schema=schema)

    def init_tables(self):
        """Initializes the schemas for products and customers."""
        
        # Product Schema: id, name, category, price, vector (384 dimensions for small models)
        product_schema = pa.schema([
            pa.field("id", pa.string()),
            pa.field("name", pa.string()),
            pa.field("category", pa.string()),
            pa.field("price", pa.float32()),
            pa.field("vector", pa.list_(pa.float32(), 384)),
            pa.field("metadata", pa.string())  # JSON string for extra info
        ])
        self._get_or_create_table(self.product_table_name, product_schema)

        # Customer Schema: id, name, segment, vector
        customer_schema = pa.schema([
            pa.field("id", pa.string()),
            pa.field("name", pa.string()),
            pa.field("segment", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), 384)),
            pa.field("metadata", pa.string())
        ])
        self._get_or_create_table(self.customer_table_name, customer_schema)
        logger.info("LanceDB tables initialized.")

    def add_products(self, data: List[Dict[str, Any]]):
        table = self.db.open_table(self.product_table_name)
        table.add(data)

    def add_customers(self, data: List[Dict[str, Any]]):
        table = self.db.open_table(self.customer_table_name)
        table.add(data)

    def search_products(self, vector: List[float], limit: int = 5):
        table = self.db.open_table(self.product_table_name)
        return table.search(vector).limit(limit).to_list()

    def search_customers(self, vector: List[float], limit: int = 5):
        table = self.db.open_table(self.customer_table_name)
        return table.search(vector).limit(limit).to_list()

# Global instance for the app
vector_store = VectorStore()
