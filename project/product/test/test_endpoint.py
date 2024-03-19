import json
import pytest


pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    """
    Test return category name
    """
    endpoint = "/api/product/categories/"

    def test_return_all_category(self, category_factory, api_client):
        category_factory.create_batch(3)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3


class TestProductEndpoints:
    """
    Test returns all products.
    """
    endpoint = "/api/product/products/"

    def test_return_all_products(self, product_factory, api_client):
        product_factory.create_batch(3)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_return_only_produt_per_slug(self, product_factory, api_client):
        product = product_factory(slug="test_slug_product")
        response = api_client().get(f"{self.endpoint}{product.slug}/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_product_list_by_category_slug(self, category_factory, product_factory, api_client):
        """
        Test returns products for a specific category
        """

        category1 = category_factory(slug="slug_category_1", is_active=True)
        category2 = category_factory(slug="slug_category_2", is_active=False)

        product_factory(category=category1)
        product_factory(category=category1)
        product_factory(category=category2)

        response = api_client().get(f"{self.endpoint}category/{category1.slug}/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2
