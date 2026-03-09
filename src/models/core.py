from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


class ProductAttributes(BaseModel):
    color: Optional[str] = None
    size: Optional[str] = None
    weight: Optional[float] = None

class Product(BaseModel):
    product_id: str
    name: str
    category: str
    brand: str
    attributes: Optional[ProductAttributes] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PromotionDetails(BaseModel):
    discount_percentage: float
    promotion_type: str
    start_date: datetime
    end_date: datetime

class MarketData(BaseModel):
    data_id: str
    source: str
    product_id: str
    competitor_id: str
    price: float
    availability: bool
    promotion_details: Optional[PromotionDetails] = None
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode='after')
    def check_price_plausibility(self) -> 'MarketData':
        if self.price < 0:
            raise ValueError('Price cannot be negative')
        return self

class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    product_id: str
    amount: float
    quantity: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    segment: Optional[str] = "General"
    last_analysis_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
