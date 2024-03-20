from pytest_factoryboy import register
import pytest
from rest_framework.test import APIClient

from .factories import (
    CategoryFactory,
    ProductFactory,
    ProductlineFactory,
    ProductImageFactory
)

register(CategoryFactory)
register(ProductFactory)
register(ProductlineFactory)
register(ProductImageFactory)


@pytest.fixture
def api_client():
    return APIClient
