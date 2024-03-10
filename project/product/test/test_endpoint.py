import json
import pytest


pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    endpoint = "/api/product/categories/"

    def test_return_all_category(self, category_factory, api_client):
        category_factory.create_batch(3)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3


class TestProductEndpoints:
    endpoint = "/api/product/products/"

    def test_return_all_products(self, product_factory, api_client):
        product_factory.create_batch(3)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3
