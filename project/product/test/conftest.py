from pytest_factoryboy import register
import pytest
from rest_framework.test import APIClient

from .factories import (
    CategoryFactory,
    ProductFactory,
    ProductlineFactory,
    ProductImageFactory,
    AttributeFactory,
    ProductTypeFactory,
    ProductlineAttributeValueFactory
)

register(CategoryFactory)
register(ProductFactory)
register(ProductlineFactory)
register(ProductImageFactory)
register(AttributeFactory)
register(ProductTypeFactory)
register(ProductlineAttributeValueFactory)

@pytest.fixture
def api_client():
    return APIClient
