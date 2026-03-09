import json
import pytest
from hypothesis import given, strategies as st
from datetime import datetime, timezone
from src.models.core import Product, MarketData, ProductAttributes, PromotionDetails

# Custom strategies for datetime to handle timezone awareness
datetime_strategy = st.datetimes(timezones=st.just(timezone.utc))

@st.composite
def product_strategy(draw):
    attributes = draw(st.one_of(
        st.none(),
        st.builds(ProductAttributes,
                  color=st.one_of(st.none(), st.text()),
                  size=st.one_of(st.none(), st.text()),
                  weight=st.one_of(st.none(), st.floats(min_value=0, allow_nan=False, allow_infinity=False))
                  )
    ))
    return Product(
        product_id=draw(st.text(min_size=1)),
        name=draw(st.text(min_size=1)),
        category=draw(st.text(min_size=1)),
        brand=draw(st.text(min_size=1)),
        attributes=attributes,
        created_at=draw(datetime_strategy),
        updated_at=draw(datetime_strategy)
    )

@st.composite
def market_data_strategy(draw):
    promotion_details = draw(st.one_of(
        st.none(),
        st.builds(PromotionDetails,
                  discount_percentage=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
                  promotion_type=st.text(min_size=1),
                  start_date=datetime_strategy,
                  end_date=datetime_strategy
                  )
    ))
    return MarketData(
        data_id=draw(st.text(min_size=1)),
        source=draw(st.text(min_size=1)),
        product_id=draw(st.text(min_size=1)),
        competitor_id=draw(st.text(min_size=1)),
        price=draw(st.floats(min_value=0, allow_nan=False, allow_infinity=False)),
        availability=draw(st.booleans()),
        promotion_details=promotion_details,
        collected_at=draw(datetime_strategy)
    )

@given(product_strategy())
def test_product_serialization_roundtrip(product):
    json_data = product.model_dump_json()
    product_dict = json.loads(json_data)
    loaded_product = Product(**product_dict)
    
    assert product.product_id == loaded_product.product_id
    assert product.name == loaded_product.name

@given(market_data_strategy())
def test_market_data_serialization_roundtrip(market_data):
    json_data = market_data.model_dump_json()
    market_data_dict = json.loads(json_data)
    loaded_market_data = MarketData(**market_data_dict)
    
    assert market_data.data_id == loaded_market_data.data_id
    assert market_data.price == loaded_market_data.price

def test_market_data_negative_price():
    with pytest.raises(ValueError):
        MarketData(
            data_id="1",
            source="test",
            product_id="p1",
            competitor_id="c1",
            price=-10.0,
            availability=True
        )
